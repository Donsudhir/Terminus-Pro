# REV-2 reviewer feedback — sparse-jacobian-color-contract

I'd mark this as Needs Revision for Instruction Styling, Test Alignment/Coverage Issues, and Rubric. Please clarify the public contract for per-batch gauge isolation, required output run ordering, the exact meanings of 'span_info.ref' and 'span_info.step', and the 'ledger.active == len(values)' relationship. Also add coverage for the explicit malformed-input requirement, and strengthen assertions for 'ids' content preservation and absolute 'span_info' correctness. Finally, replace the rubric: it is process-heavy and includes unrelated SQLite/repository criteria that do not apply to this sparse Jacobian task.

Platform difficulty (post-upload): HARD, solvable. Agents often stall on k05/k10/k11 (shared gauge / ordering / scale summary) — instruction must state those contracts without turning into a fix recipe.
