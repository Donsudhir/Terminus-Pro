# Report Format

The report is a compact JSON object with `schema_version`, ordered `batches`, and `digest`. Each batch has an `identity` object containing `family`, `variant`, and `point_ids`; `cells`; `adjacency`; `orientation`; `validity`; and `topology`.

Each cell is an oriented quadruple of point identities. Rows are sorted in their stable canonical order. An adjacency row has four integers. Entry `k` identifies the cell across the face opposite cell vertex `k`, or `-1` when that face is on the boundary.

`orientation` contains `positive`, `negative`, and `zero`. `validity` contains `checks` and `violations`. `topology` contains `vertices`, `edges`, `faces`, `cells`, `boundary_faces`, and `euler`.

The digest is sixteen lowercase hexadecimal characters. It is computed over the compact top-level object before the digest member is appended. Batch ordering is lexical by family and then variant, making the report independent of source-block order.
