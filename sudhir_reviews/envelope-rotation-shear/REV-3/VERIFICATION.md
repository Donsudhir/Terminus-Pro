# VERIFICATION — envelope-rotation-shear REV-3

The tests checks recovery, maintenance, reads, and audit from clean resets and verifier-generated namespaces. They require valid live records in newly introduced namespaces to read without recovery, while intact substitutions fail through both read and audit paths. Other cases assert exact recovered identity inventory, prior-history recovery, healthy byte preservation, older-record re-encryption, and second-run stability. Tampered records must still reject, NOP stays at zero reward, and the oracle passes the complete suite.
