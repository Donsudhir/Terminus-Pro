# Dyadic Family Format

A source file contains one or more family blocks. Blank lines and lines beginning with `#` are ignored.

- `family NAME` opens a block.
- `point ID X Y Z` adds one point. Each coordinate uses `MANTISSA@EXPONENT` and represents `MANTISSA * 2^EXPONENT`.
- `variant NAME SCALE TX TY TZ` adds a translated, uniformly scaled view. `SCALE` is a signed power-of-two exponent. Translation components use the same dyadic notation.
- `end` closes the block.

Names use ASCII letters, digits, underscore, or hyphen. Point identities are unique within a family. A family contains between six and twelve points and at least one variant. Coordinate exponent spread and aligned magnitudes are bounded so the integer refinement interface remains finite. Uniform scale is always strictly positive because it is represented as a power of two.
