# Store layout

Live bundles are JSON arrays of protected frames despite their `.bin` suffix.
The suffix distinguishes operational bundles from configuration and reports;
it does not imply a raw binary encoding. `catalog.json` maps each public item
identity to a bundle name and zero-based slot.

Each frame header carries an item pair, an axis label, a key epoch, and a
monotonic sequence. The protected fields are a nonce, body, wrapped data key,
and authentication tag. All protected fields use unpadded base64 text. Header
fields participate in protected-frame validation and are not presentation
metadata.

Segment bundles use the same frame encoding. They are immutable inputs to
ordinary compaction accounting and retention audits. Compaction indexes count
versions per item and reject duplicate sequence numbers. Segment bundles never
contain decoded payloads, expected reports, or repaired live bundles.
