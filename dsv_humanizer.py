#!/usr/bin/env python3
"""Strict Humanizer-derived policy for submission explanation fields.

This module validates only Difficulty, Solution, and Verification prose. It is
not a general AI detector and it never rewrites text. Agents perform the
semantic Humanizer pass; this module enforces the mechanical parts and records
a content-addressed audit for the revision dossier.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

POLICY_ID = "terminus-dsv-humanizer-acceptance-safe-2026-07-22"
UPSTREAM_VERSION = "2.9.1"
UPSTREAM_COMMIT = "523374dee72d67c7b2b5f858ea0094ffda49c3ac"
AUDIT_FILENAME = "DSV-HUMANIZER-AUDIT.json"
REQUIRED_MARKER = "DSV_HUMANIZER_REQUIRED: yes"

FIELD_ORDER = ("difficulty", "solution", "verification")
ACCEPTANCE_PRECEDENCE = (
    "current platform field requirements and reviewer feedback",
    "finished task truth from instruction, solution, tests, and evidence",
    "TERMINUS lifecycle, acceptance, and submission rules",
    "Humanizer style preferences",
)
FIELD_LABELS = {
    "difficulty": "Difficulty",
    "solution": "Solution",
    "verification": "Verification",
}
EXACT_OPENERS = {
    "difficulty": "This task is hard because",
    "verification": "The tests checks",
}

# Mechanically detectable members of the upstream 33-pattern Humanizer policy.
# Semantic patterns such as synonym cycling and false significance still require
# the model-side audit described by the workspace skill.
BANNED_PATTERNS: tuple[tuple[str, re.Pattern[str], str], ...] = (
    (
        "H01",
        re.compile(
            r"\b(?:stands? as|serves? as|a testament to|pivotal moment|"
            r"broader (?:trend|context|landscape)|marks? a shift|"
            r"underscores? (?:the )?(?:importance|significance))\b",
            re.IGNORECASE,
        ),
        "inflated significance",
    ),
    (
        "H02",
        re.compile(
            r"\b(?:widely recognized|renowned|notable|media coverage|"
            r"leading expert|active social media presence)\b",
            re.IGNORECASE,
        ),
        "notability or media-padding language",
    ),
    (
        "H03",
        re.compile(
            r",\s*(?:highlighting|underscoring|emphasizing|ensuring|"
            r"reflecting|symbolizing|showcasing|fostering|cultivating)\b",
            re.IGNORECASE,
        ),
        "superficial -ing analysis",
    ),
    (
        "H04",
        re.compile(
            r"\b(?:boasts?|vibrant|groundbreaking|breathtaking|stunning|"
            r"commitment to excellence|best-in-class|world-class)\b",
            re.IGNORECASE,
        ),
        "promotional language",
    ),
    (
        "H05",
        re.compile(
            r"\b(?:experts (?:say|argue|believe)|observers (?:say|note|cite)|"
            r"industry reports|some critics argue|several sources)\b",
            re.IGNORECASE,
        ),
        "vague attribution",
    ),
    (
        "H06",
        re.compile(
            r"\b(?:despite (?:these|the) challenges|future outlook|"
            r"challenges and (?:opportunities|legacy)|continues? to thrive)\b",
            re.IGNORECASE,
        ),
        "formulaic challenges or outlook prose",
    ),
    (
        "H07",
        re.compile(
            r"\b(?:additionally|crucial|delve|enduring|fostering|garner|"
            r"intricate|intricacies|pivotal|showcase|tapestry|testament|"
            r"underscore|vibrant)\b",
            re.IGNORECASE,
        ),
        "overused AI vocabulary",
    ),
    (
        "H08",
        re.compile(r"\b(?:serves? as|stands? as|boasts?)\b", re.IGNORECASE),
        "copula avoidance",
    ),
    (
        "H09",
        re.compile(
            r"\b(?:not only|not just|not merely)\b|,\s*no (?:guessing|waste|confusion)\b",
            re.IGNORECASE,
        ),
        "negative parallelism or tailing negation",
    ),
    (
        "H12",
        re.compile(r"\bfrom\s+[^.!?]{1,80}\s+to\s+[^.!?]{1,80}", re.IGNORECASE),
        "range-shaped rhetoric; state the concrete cases directly",
    ),
    (
        "H20",
        re.compile(
            r"\b(?:I hope this helps|of course|certainly|would you like|"
            r"want me to|let me know|here is an overview)\b",
            re.IGNORECASE,
        ),
        "chatbot communication artifact",
    ),
    (
        "H21",
        re.compile(
            r"\b(?:as of my last|training update|based on available information|"
            r"specific details are (?:limited|scarce)|it is believed that|likely)\b",
            re.IGNORECASE,
        ),
        "speculative gap filling",
    ),
    (
        "H22",
        re.compile(
            r"\b(?:great question|excellent point|you are absolutely right|"
            r"you're absolutely right)\b",
            re.IGNORECASE,
        ),
        "sycophantic language",
    ),
    (
        "H23",
        re.compile(
            r"\b(?:in order to|due to the fact that|at this point in time|"
            r"in the event that|has the ability to|it is important to note that)\b",
            re.IGNORECASE,
        ),
        "filler phrase",
    ),
    (
        "H24",
        re.compile(
            r"\b(?:could potentially|might possibly|potentially possibly|"
            r"it could be argued that)\b",
            re.IGNORECASE,
        ),
        "excessive hedging",
    ),
    (
        "H25",
        re.compile(
            r"\b(?:the future looks bright|exciting times (?:lie|are) ahead|"
            r"a step in the right direction|journey toward excellence)\b",
            re.IGNORECASE,
        ),
        "generic positive conclusion",
    ),
    (
        "H27",
        re.compile(
            r"\b(?:the real question is|at its core|what really matters|"
            r"fundamentally|the deeper issue|the heart of the matter)\b",
            re.IGNORECASE,
        ),
        "persuasive authority trope",
    ),
    (
        "H28",
        re.compile(
            r"\b(?:let's dive in|let us dive in|let's explore|let us explore|"
            r"let's break this down|here's what you need to know|"
            r"without further ado|now let's look at)\b",
            re.IGNORECASE,
        ),
        "signposting announcement",
    ),
    (
        "H30",
        re.compile(
            r"\b(?:was (?:added|changed|updated|replaced)|previously|"
            r"the old approach|the former implementation|this change)\b",
            re.IGNORECASE,
        ),
        "diff-anchored writing",
    ),
    (
        "H32",
        re.compile(
            r"\b(?:the language of|the currency of|the architecture of|"
            r"is not a tool but|becomes a trap)\b",
            re.IGNORECASE,
        ),
        "aphorism formula",
    ),
    (
        "H33",
        re.compile(
            r"^(?:honestly\??|look[,!]?|here's the thing|the thing is|"
            r"let's be honest|real talk)\b",
            re.IGNORECASE,
        ),
        "fake-candid rhetorical opener",
    ),
)

MARKDOWN_PATTERN = re.compile(
    r"(?m)^\s*(?:#{1,6}\s|[-*+]\s|\d+[.)]\s|>\s)|```|`[^`]+`|\*\*|__"
)
EMOJI_PATTERN = re.compile(
    "[\U0001F1E6-\U0001F1FF\U0001F300-\U0001FAFF\U00002700-\U000027BF]"
)
WORD_PATTERN = re.compile(r"[A-Za-z0-9]+(?:'[A-Za-z]+)?")


@dataclass(frozen=True)
class Finding:
    field: str
    code: str
    message: str


@dataclass
class ValidationReport:
    policy_id: str
    ok: bool
    findings: list[Finding]
    metrics: dict[str, dict[str, Any]]
    normalized: dict[str, str]

    def json_dict(self) -> dict[str, Any]:
        return {
            "policy_id": self.policy_id,
            "upstream": {
                "repository": "https://github.com/blader/humanizer",
                "version": UPSTREAM_VERSION,
                "commit": UPSTREAM_COMMIT,
            },
            "scope": list(FIELD_ORDER),
            "transformation_boundary": "wording-and-rhythm-only",
            "acceptance_precedence": list(ACCEPTANCE_PRECEDENCE),
            "ok": self.ok,
            "findings": [asdict(item) for item in self.findings],
            "metrics": self.metrics,
        }


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _strip_capture_heading(field: str, text: str) -> str:
    """Remove the dossier's generated title while retaining raw prose rules."""
    text = text.replace("\r\n", "\n").replace("\r", "\n").strip()
    lines = text.splitlines()
    if lines and lines[0].startswith("#"):
        label = FIELD_LABELS[field].lower()
        if label in lines[0].lower():
            lines = lines[1:]
            while lines and not lines[0].strip():
                lines.pop(0)
    return "\n".join(lines).strip()


def _sentences(body: str) -> list[str]:
    flattened = re.sub(r"\s+", " ", body).strip()
    if not flattened:
        return []
    return [part.strip() for part in re.split(r"(?<=[.!?])\s+", flattened) if part.strip()]


def _words(text: str) -> list[str]:
    return WORD_PATTERN.findall(text)


def _finding(findings: list[Finding], field: str, code: str, message: str) -> None:
    findings.append(Finding(field=field, code=code, message=message))


def _validate_field(field: str, text: str, findings: list[Finding]) -> tuple[str, dict[str, Any]]:
    body = _strip_capture_heading(field, text)
    sentences = _sentences(body)
    word_counts = [len(_words(sentence)) for sentence in sentences]
    words = _words(body)

    if not body:
        _finding(findings, field, "DSV001", "field is empty")
        return body, {"sentences": 0, "words": 0, "sentence_words": []}

    if "\n\n" in body:
        _finding(findings, field, "DSV002", "use one prose paragraph")
    if MARKDOWN_PATTERN.search(body):
        _finding(findings, field, "DSV003", "Markdown, lists, headings, and code formatting are forbidden")
    if not body.endswith((".", "!", "?")):
        _finding(findings, field, "DSV004", "field must end with sentence punctuation")
    if len(sentences) not in (4, 5):
        _finding(
            findings,
            field,
            "DSV005",
            f"expected 4 or 5 sentences, found {len(sentences)}",
        )

    opener = EXACT_OPENERS.get(field)
    if opener and not body.startswith(opener):
        _finding(findings, field, "DSV006", f"must start exactly with {opener!r}")

    if len(words) < 45 or len(words) > 140:
        _finding(
            findings,
            field,
            "DSV007",
            f"expected 45 to 140 words, found {len(words)}",
        )
    for index, count in enumerate(word_counts, start=1):
        if count < 6 or count > 45:
            _finding(
                findings,
                field,
                "DSV008",
                f"sentence {index} has {count} words; expected 6 to 45",
            )
    if len(word_counts) >= 4 and max(word_counts) - min(word_counts) <= 3:
        _finding(findings, field, "H31", "sentence lengths are mechanically uniform")
    if sum(count <= 5 for count in word_counts) >= 3:
        _finding(findings, field, "H31", "contains manufactured staccato fragments")

    forbidden_chars = {
        "—": "em dash",
        "–": "en dash",
        ";": "semicolon",
        "“": "curly opening quote",
        "”": "curly closing quote",
        "‘": "curly opening apostrophe",
        "’": "curly closing apostrophe",
    }
    for char, label in forbidden_chars.items():
        if char in body:
            _finding(findings, field, "DSV009", f"contains forbidden {label}")
    if " -- " in body:
        _finding(findings, field, "DSV009", "contains a double-hyphen dash")
    if EMOJI_PATTERN.search(body):
        _finding(findings, field, "H18", "contains an emoji or decorative symbol")
    if re.search(r"https?://|www\.", body, re.IGNORECASE):
        _finding(findings, field, "DSV010", "URLs and citations do not belong in these fields")
    if re.search(r"\b(?:I found|I thought|I believe|in my view|to me)\b", body, re.IGNORECASE):
        _finding(
            findings,
            field,
            "DSV011",
            "first-person claims are forbidden unless separately evidenced; use neutral builder voice",
        )

    for code, pattern, description in BANNED_PATTERNS:
        match = pattern.search(body)
        if match:
            _finding(
                findings,
                field,
                code,
                f"{description}: {match.group(0)!r}",
            )

    hyphenated = re.findall(r"\b[A-Za-z]+-[A-Za-z]+\b", body)
    if len(hyphenated) > 4:
        _finding(
            findings,
            field,
            "H26",
            f"hyphenated compound overuse: found {len(hyphenated)}",
        )

    starts = [" ".join(word.lower() for word in _words(sentence)[:3]) for sentence in sentences]
    duplicate_starts = sorted({start for start in starts if start and starts.count(start) > 1})
    if duplicate_starts:
        _finding(
            findings,
            field,
            "DSV012",
            "repeated sentence opening: " + ", ".join(repr(item) for item in duplicate_starts),
        )

    return body, {
        "sentences": len(sentences),
        "words": len(words),
        "sentence_words": word_counts,
        "hyphenated_compounds": len(hyphenated),
    }


def _normalized_ngrams(text: str, size: int = 5) -> set[str]:
    tokens = [token.lower() for token in _words(text)]
    return {" ".join(tokens[index : index + size]) for index in range(len(tokens) - size + 1)}


def validate_texts(*, difficulty: str, solution: str, verification: str) -> ValidationReport:
    texts = {
        "difficulty": difficulty,
        "solution": solution,
        "verification": verification,
    }
    findings: list[Finding] = []
    normalized: dict[str, str] = {}
    metrics: dict[str, dict[str, Any]] = {}

    for field in FIELD_ORDER:
        normalized[field], metrics[field] = _validate_field(field, texts[field], findings)

    ngrams = {field: _normalized_ngrams(normalized[field]) for field in FIELD_ORDER}
    for left_index, left in enumerate(FIELD_ORDER):
        for right in FIELD_ORDER[left_index + 1 :]:
            overlap = sorted(ngrams[left] & ngrams[right])
            if overlap:
                sample = ", ".join(repr(item) for item in overlap[:3])
                _finding(
                    findings,
                    "all",
                    "DSV013",
                    f"repeated five-word phrase across {left} and {right}: {sample}",
                )

    list_of_three_count = sum(
        len(re.findall(r",\s+[^,.!?]{1,45},\s+(?:and|or)\s+", normalized[field]))
        for field in FIELD_ORDER
    )
    if list_of_three_count > 1:
        _finding(
            findings,
            "all",
            "H10",
            f"rule-of-three cadence appears {list_of_three_count} times",
        )

    return ValidationReport(
        policy_id=POLICY_ID,
        ok=not findings,
        findings=findings,
        metrics=metrics,
        normalized=normalized,
    )


def validate_files(files: dict[str, Path]) -> ValidationReport:
    missing = [field for field in FIELD_ORDER if field not in files]
    if missing:
        findings = [
            Finding(field=field, code="DSV000", message="required field file is missing")
            for field in missing
        ]
        return ValidationReport(POLICY_ID, False, findings, {}, {})
    return validate_texts(
        difficulty=files["difficulty"].read_text(encoding="utf-8"),
        solution=files["solution"].read_text(encoding="utf-8"),
        verification=files["verification"].read_text(encoding="utf-8"),
    )


def write_audit(path: Path, report: ValidationReport, files: dict[str, Path]) -> None:
    if not report.ok:
        raise ValueError("cannot write a PASS audit for invalid DSV prose")
    payload = report.json_dict()
    payload.update(
        {
            "result": "PASS",
            "generated_at": utc_now(),
            "files": {
                field: {
                    "name": files[field].name,
                    "sha256": sha256_file(files[field]),
                }
                for field in FIELD_ORDER
            },
            "semantic_attestation": (
                "The writing agent must compare every claim and obligation with the completed "
                "task, solution, tests, platform feedback, project rules, and recorded evidence. "
                "Humanizer may change wording and rhythm only. The mechanical validator cannot "
                "prove semantic equivalence or platform acceptance."
            ),
        }
    )
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def verify_audit(path: Path, files: dict[str, Path]) -> tuple[bool, str]:
    if not path.is_file():
        return False, f"missing {path.name}"
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        return False, f"invalid {path.name}: {exc}"
    if payload.get("policy_id") != POLICY_ID or payload.get("result") != "PASS":
        return False, f"{path.name} does not contain a PASS for {POLICY_ID}"
    if payload.get("scope") != list(FIELD_ORDER):
        return False, f"{path.name} has an invalid Humanizer scope"
    if payload.get("transformation_boundary") != "wording-and-rhythm-only":
        return False, f"{path.name} has an invalid Humanizer transformation boundary"
    if payload.get("acceptance_precedence") != list(ACCEPTANCE_PRECEDENCE):
        return False, f"{path.name} does not preserve acceptance precedence"
    for field in FIELD_ORDER:
        file_path = files.get(field)
        if file_path is None or not file_path.is_file():
            return False, f"missing {FIELD_LABELS[field]} form file"
        expected = ((payload.get("files") or {}).get(field) or {}).get("sha256")
        actual = sha256_file(file_path)
        if expected != actual:
            return False, f"{file_path.name} changed after strict Humanizer audit"
    report = validate_files(files)
    if not report.ok:
        first = report.findings[0]
        return False, f"current DSV prose fails {first.code}: {first.message}"
    return True, "acceptance-safe DSV Humanizer audit matches current form files"


def format_findings(report: ValidationReport) -> str:
    if report.ok:
        field_summary = ", ".join(
            f"{FIELD_LABELS[field]}={report.metrics[field]['sentences']} sentences"
            for field in FIELD_ORDER
        )
        return f"PASS {POLICY_ID}: {field_summary}"
    lines = [f"FAIL {POLICY_ID}: {len(report.findings)} finding(s)"]
    lines.extend(
        f"  - {item.field} {item.code}: {item.message}" for item in report.findings
    )
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate strict Humanizer policy for Difficulty/Solution/Verification prose."
    )
    parser.add_argument("--difficulty-file", required=True, type=Path)
    parser.add_argument("--solution-file", required=True, type=Path)
    parser.add_argument("--verification-file", required=True, type=Path)
    parser.add_argument("--json", action="store_true", help="emit machine-readable report")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    report = validate_files(
        {
            "difficulty": args.difficulty_file,
            "solution": args.solution_file,
            "verification": args.verification_file,
        }
    )
    if args.json:
        print(json.dumps(report.json_dict(), indent=2, sort_keys=True))
    else:
        print(format_findings(report))
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
