# REV-1 reviewer feedback — sparse-jacobian-color-contract

Source: Snorkel d9082cd8 (2026-07-19)

I'd mark this as Needs Revision for Instruction Styling, Test Alignment/Coverage Issues, and Rubric. Please clarify the public contract for per-batch gauge isolation, required output run ordering, the exact meanings of 'span_info.ref' and 'span_info.step', and the 'ledger.active == len(values)' relationship. Also add coverage for the explicit malformed-input requirement, and strengthen assertions for 'ids' content preservation and absolute 'span_info' correctness. Finally, replace the rubric: it is process-heavy and includes unrelated SQLite/repository criteria that do not apply to this sparse Jacobian task.
