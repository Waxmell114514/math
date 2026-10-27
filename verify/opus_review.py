#!/usr/bin/env python3
"""Referee the ETH-disproof manuscript and its Lean statement with Claude Opus.

Stages (each writes one Markdown report to verify/reports/ and is skipped on re-runs
unless --force is given, so an interrupted run never pays twice for finished work):

  statement   Is the trusted Lean statement (ComparatorChallenges/SubexponentialSAT.lean)
              a faithful formalization that really implies "ETH is false"?
  sec-*       Line-by-line proof check of one section/appendix of the paper.
  synthesis   Overall verdict from all of the reports above.

Every request carries the whole paper (with its \\input files inlined) behind a 1-hour
prompt-cache breakpoint, so the paper is paid for once and read from cache afterwards.

The API key is read from $ANTHROPIC_API_KEY or from --key-file; it is never written anywhere.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import datetime
import json
import os
import pathlib
import re
import sys

import anthropic

MODEL = "claude-opus-5-5"
# USD per million tokens for claude-opus-5-5 (input, output, cache read, 1h cache write).
PRICE = {"input": 4.00, "output": 20.00, "cache_read": 0.20, "cache_write_1h": 8.00}

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAPER_DIR = ROOT / "preprints/The-Exponential-Time-Hypothesis-is-False-October-25-2026/build"
CHALLENGE = ROOT / "lean/ComparatorChallenges/SubexponentialSAT.lean"
SCOPE_DOC = ROOT / "lean/docs/378.md"
REPORTS = ROOT / "verify/reports"

SYSTEM = """\
You are a meticulous referee in theoretical computer science and mathematics (exact and \
fine-grained algorithms, algebraic and polynomial methods, complexity theory, and Lean 4 \
formalization). You are refereeing a manuscript that claims to refute the Exponential Time \
Hypothesis with a deterministic, polynomial-space algorithm that exactly counts the satisfying \
assignments of a k-CNF on n variables and m clauses in time (n+m)^{O_k(1)} 2^{n/(log n)^{1/2+o(1)}}.

Extraordinary claims require extraordinary scrutiny: your job is to find errors, not to be \
persuaded. When asked to check a part of the paper, check it line by line: recompute every \
calculation and parameter choice, check that every cited lemma (internal or external) really \
gives what is used, with the right hypotheses, quantifiers and parameter ranges, and check that \
parameters are chosen consistently across sections. Never accept "it is easy to see", \
"standard", or "similarly" without verifying the claim yourself. When something is correct, say \
so briefly and move on; spend your words on the places that are wrong, unclear, or load-bearing.

Classify every problem you find as exactly one of:
  FATAL  - breaks the claimed result as stated (no evident local repair);
  GAP    - a missing or incorrect argument that you believe can be repaired (say how);
  MINOR  - typo, notation, or presentation issue that does not affect correctness.
Be concrete: cite labels (\\label names), equation numbers, or quote the relevant text. Do not \
speculate about who wrote the paper or how it was produced; judge only the mathematics."""

STATEMENT_TASK = """\
Below is the *trusted statement* file of the paper's Lean 4 formalization (a Comparator \
challenge: the theorem is stated with `sorry`; a separate solution file must prove the identical \
statement, with the same supporting definitions, using only the axioms propext, Quot.sound and \
Classical.choice). Assume the Lean proof has been checked by the kernel and that it matches this \
statement exactly - do NOT review the proof. Review the statement itself:

Is `OAI.Algorithms.SubexponentialSAT.SqrtLogSpace.exact_count_and_sat` a faithful formalization \
that, if true, genuinely implies that the Exponential Time Hypothesis is false?

Examine at least:
1. The machine model `PrimitiveMachine` and its step semantics (`step`, `init`, `locatedStep`, \
`Trace`). Is it a standard deterministic multi-tape Turing machine, or could it be more powerful \
(per-step work, alphabet, number of states/tapes, how input is placed, head moves, halting)? Is \
a time bound for it meaningful in the usual sense?
2. The input encoding `encodeCNF` / `formulaBitLength`: is it a reasonable encoding, of length \
polynomial in n and m? Could it leak information that makes the problem easier? Note that a CNF \
is a `Finset` of clauses and a clause a `Finset` of literals.
3. The output conditions (count tape, answer tape, halting state) and `SAT.count`: do they pin \
down the right answer for every formula? Any vacuity, e.g. an unsatisfiable hypothesis, a \
degenerate `Turing.Tape.mk₁` equality, or a `Trace` that can be satisfied trivially?
4. Quantifier order and uniformity: is there one machine per k, independent of n and F?
5. The time bound `runtimeBound C A d (formulaBitLength F) n`: show explicitly whether it is \
2^{o(n)} for 3-CNF instances, including the polynomial factor in the bit length (bound the \
number of distinct width-3 clauses and the encoding length in terms of n). Check the real-number \
edge cases (logs of small arguments, `Real.sqrt`) and whether they matter.
6. The space condition: what exactly does it say, and is it the claimed polynomial-space bound?
7. Compare with the paper's main theorem (the Introduction states it) and with the scope \
document below: list every discrepancy (e.g. the exponent n (log log n)^2 / sqrt(log n) in Lean \
versus the paper's sharper bound) and whether it matters for refuting ETH.

Then write out the complete chain of implications from the Lean theorem to "3-SAT on n variables \
is decidable by a deterministic algorithm in time 2^{o(n)}", hence "ETH is false", naming every \
standard fact used (e.g. robustness of ETH to input encoding and to TM-vs-RAM models) and \
checking that each one applies.

Format: Markdown with sections "## Findings" (numbered, each with severity FATAL/GAP/MINOR or \
"OK"), "## Implication chain", "## Verdict". The final line must be exactly one of
VERDICT: FAITHFUL
VERDICT: FAITHFUL-WITH-CAVEATS
VERDICT: NOT-FAITHFUL

=== lean/docs/378.md (scope document) ===
{scope}

=== lean/ComparatorChallenges/SubexponentialSAT.lean (trusted statement) ===
{challenge}
"""

SECTION_TASK = """\
Referee the following part of the paper in full detail:

    {title}

(the part begins at the line `{first_line}` and ends where the next \\section or the end of the \
document begins). The rest of the paper is context: you may rely on results proved in other \
parts, but list every such dependency explicitly (label, and the exact statement and parameter \
range used here) so that it can be cross-checked against the review of that part. Also list \
what this part provides to other parts.

Check every lemma, claim and proof in this part line by line, recomputing all bounds.{extra}

Format: Markdown with sections
## What this part proves
## Dependencies on other parts
## Detailed verification   (lemma by lemma)
## Issues                  (numbered; each FATAL / GAP / MINOR, with location and explanation)
## Verdict
The final line must be exactly one of
VERDICT: SOUND
VERDICT: SOUND-WITH-MINOR-ISSUES
VERDICT: GAPS
VERDICT: FATAL
"""

EXTRA = {
    "Introduction": " For this part, focus on the precise statements of the main theorems and "
    "corollaries, and on whether each claimed consequence (refuting ETH, the circuit lower "
    "bounds, any other corollaries) really follows from the main theorem with the stated "
    "parameters; check the comparison with prior work only for factual consistency.",
    "Technique overview": " This part is informal; check that it is consistent with the formal "
    "sections (parameters, exponents, which object is counted), and flag any idea described "
    "here that the formal sections never actually prove.",
}

SYNTHESIS_TASK = """\
Below are independent referee reports, one on the Lean statement and one per part of the paper \
(each written by a referee who had the whole paper available). Produce the final assessment:

1. Cross-check the "Dependencies" each report lists against what the cited part actually proves \
(according to its report and to the paper itself); flag any parameter or statement mismatch \
between parts.
2. Re-examine yourself every issue rated FATAL or GAP in any report: confirm it, refute it, or \
mark it unresolved, with reasons.
3. Give an overall verdict on (a) the paper's proof of its main theorem, (b) whether the Lean \
statement faithfully captures a refutation of ETH, and (c) what remains for human experts to \
check. Keep in mind that a kernel-checked Lean proof of a faithful statement settles the \
claim regardless of gaps in the prose.

Format: Markdown with sections "## Cross-part consistency", "## Re-examined issues", \
"## Overall assessment", "## What humans should check". The final line must be exactly one of
VERDICT: PROOF-APPEARS-CORRECT
VERDICT: PROOF-HAS-REPAIRABLE-GAPS
VERDICT: PROOF-HAS-FATAL-ERRORS
VERDICT: UNDETERMINED

{reports}
"""


def fill(template: str, **values: str) -> str:
    """Substitute {name} placeholders without str.format (the prompts contain TeX braces)."""
    for k, v in values.items():
        template = template.replace("{" + k + "}", v)
    return template


def inline_inputs(tex_path: pathlib.Path) -> str:
    """Return the TeX source with each \\input{name} replaced by that file's contents."""

    def repl(match: re.Match) -> str:
        child = tex_path.parent / (match.group(1).removesuffix(".tex") + ".tex")
        return f"% ---- begin \\input{{{match.group(1)}}} ----\n{child.read_text()}\n" \
               f"% ---- end \\input{{{match.group(1)}}} ----\n"

    return re.sub(r"^\\input\{([^}]+)\}\s*$", repl, tex_path.read_text(), flags=re.M)


def sections(paper: str) -> list[tuple[str, str, str]]:
    """(slug, title, first line) for each \\section of the paper, in order."""
    out = []
    for i, line in enumerate(paper.splitlines()):
        m = re.match(r"\\section\{(.+?)\}(?:\\label|\s*$)", line)
        if not m:
            continue
        title = re.sub(r"\\texorpdfstring\{[^}]*\}\{([^}]*)\}", r"\1", m.group(1))
        slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:40]
        out.append((f"sec-{len(out) + 1:02d}-{slug}", title, line.strip()))
    return out


def ask(client: anthropic.Anthropic, paper: str, task: str, effort: str) -> anthropic.types.beta.BetaMessage:
    with client.beta.messages.stream(
        model=MODEL,
        max_tokens=128000,
        thinking={"type": "adaptive"},
        output_config={"effort": effort},
        # On a policy refusal, let the API route the request to a fallback model; the report
        # header records which model actually answered.
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
        system=SYSTEM,
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": "=== The manuscript (LaTeX source) ===\n" + paper,
                 "cache_control": {"type": "ephemeral", "ttl": "1h"}},
                {"type": "text", "text": task},
            ],
        }],
    ) as stream:
        return stream.get_final_message()


def cost(usage) -> float:
    return (usage.input_tokens * PRICE["input"] + usage.output_tokens * PRICE["output"]
            + (usage.cache_read_input_tokens or 0) * PRICE["cache_read"]
            + (usage.cache_creation_input_tokens or 0) * PRICE["cache_write_1h"]) / 1e6


def run_stage(client, paper, name, task, effort, force) -> str:
    out = REPORTS / f"{name}.md"
    if out.exists() and not force:
        print(f"[skip] {name} (report exists)", flush=True)
        return out.read_text()
    print(f"[start] {name}", flush=True)
    msg = ask(client, paper, task, effort)
    text = "".join(b.text for b in msg.content if b.type == "text")
    served = {it.model or msg.model for it in (msg.usage.iterations or [])} or {msg.model}
    fell_back = any(it.type == "fallback_message" for it in (msg.usage.iterations or []))
    meta = {
        "stage": name,
        "requested_model": MODEL,
        "served_by": sorted(served),
        "fallback_used": fell_back,
        "effort": effort,
        "stop_reason": msg.stop_reason,
        "input_tokens": msg.usage.input_tokens,
        "cache_read_input_tokens": msg.usage.cache_read_input_tokens,
        "cache_creation_input_tokens": msg.usage.cache_creation_input_tokens,
        "output_tokens": msg.usage.output_tokens,
        "estimated_cost_usd": round(cost(msg.usage), 4),
        "request_id": msg._request_id,
        "finished_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
    }
    if msg.stop_reason == "refusal":
        text += f"\n\n**Request refused.** stop_details: {msg.stop_details}\n"
    elif msg.stop_reason == "max_tokens":
        text += "\n\n**Output truncated at max_tokens.**\n"
    out.write_text(f"<!-- {json.dumps(meta)} -->\n\n{text}\n")
    print(f"[done] {name}: stop={msg.stop_reason} out={msg.usage.output_tokens} "
          f"cache_read={msg.usage.cache_read_input_tokens} ~${meta['estimated_cost_usd']}", flush=True)
    return out.read_text()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--key-file", help="file containing the API key (default: $ANTHROPIC_API_KEY)")
    ap.add_argument("--effort", default="max", choices=["low", "medium", "high", "xhigh", "max"])
    ap.add_argument("--only", nargs="*", help="run only these stages (statement, sec-NN-..., synthesis)")
    ap.add_argument("--workers", type=int, default=4, help="parallel section reviews")
    ap.add_argument("--force", action="store_true", help="re-run stages whose report already exists")
    ap.add_argument("--list", action="store_true", help="list the stages and exit")
    args = ap.parse_args()

    paper = inline_inputs(PAPER_DIR / "main_full_version.tex")
    secs = sections(paper)
    stages = ["statement"] + [s[0] for s in secs] + ["synthesis"]
    if args.list:
        print("\n".join(stages))
        return 0
    wanted = set(args.only or stages)

    key = pathlib.Path(args.key_file).read_text().strip() if args.key_file else os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        sys.exit("no API key: set ANTHROPIC_API_KEY or pass --key-file")
    client = anthropic.Anthropic(api_key=key, max_retries=4)
    REPORTS.mkdir(parents=True, exist_ok=True)

    # The statement review runs first and on its own so that it writes the paper into the
    # prompt cache before the parallel section reviews read it.
    if "statement" in wanted:
        task = fill(STATEMENT_TASK, scope=SCOPE_DOC.read_text(), challenge=CHALLENGE.read_text())
        run_stage(client, paper, "statement", task, args.effort, args.force)

    jobs = []
    for slug, title, first in secs:
        if slug in wanted:
            extra = next((v for k, v in EXTRA.items() if title.startswith(k)), "")
            jobs.append((slug, fill(SECTION_TASK, title=title, first_line=first, extra=extra)))
    failed = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(run_stage, client, paper, n, t, args.effort, args.force): n for n, t in jobs}
        for fut in concurrent.futures.as_completed(futures):
            try:
                fut.result()
            except anthropic.APIError as e:
                failed.append(futures[fut])
                print(f"[error] {futures[fut]}: {type(e).__name__}: {e}", flush=True)

    if "synthesis" in wanted:
        missing = [s for s in stages[:-1] if not (REPORTS / f"{s}.md").exists()]
        if missing:
            print(f"[skip] synthesis: missing reports {missing}", flush=True)
        else:
            reports = "\n\n".join(f"=== REPORT: {s} ===\n{(REPORTS / f'{s}.md').read_text()}" for s in stages[:-1])
            run_stage(client, paper, "synthesis", fill(SYNTHESIS_TASK, reports=reports), args.effort, args.force)

    total = 0.0
    for p in sorted(REPORTS.glob("*.md")):
        m = re.match(r"<!-- (\{.*\}) -->", p.read_text())
        if m:
            total += json.loads(m.group(1))["estimated_cost_usd"]
    print(f"estimated total spend across all reports: ${total:.2f}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
