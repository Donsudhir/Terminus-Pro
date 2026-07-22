# VERIFICATION — envelope-rotation-shear REV-2

Checks exercise vaultctl recover/maintain/get/audit from clean resets and generated namespaces. They assert recovered values, exact recovery.json identity inventory, recovery of identities with prior history, healthy-byte preservation, maintain re-encryption of older records with second-run stability, isolation, strict get failure on substituted records without invoking recover, and rejection of tampered or substituted records under audit. NOP remains 0.0; oracle remains 1.0 across ten Harbor trials.
