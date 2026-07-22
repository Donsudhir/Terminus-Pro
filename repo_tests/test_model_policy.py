"""Regression coverage for current, legacy, and unknown model identities."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import agent_test
import model_policy
from ci_checks import rubric_review


class ModelPolicyRegressionTest(unittest.TestCase):
    def test_current_pair_and_effective_date_are_pinned(self) -> None:
        self.assertEqual(model_policy.CURRENT_MODEL_EFFECTIVE_DATE, "2026-06-12")
        self.assertEqual(model_policy.CURRENT_MODEL_IDS, ("gpt-5.5", "claude-opus-4.8"))
        self.assertEqual(tuple(agent_test.MODELS), model_policy.CURRENT_MODEL_IDS)
        args = agent_test._parse_args(["run", "tasks/example", "--dry-run"])
        self.assertEqual(tuple(args.models), model_policy.CURRENT_MODEL_IDS)

    def test_current_run_flags_match_platform_contract(self) -> None:
        self.assertEqual(
            model_policy.CURRENT_OPENAI_MODEL.harbor_flag,
            "@openai/gpt-5.5",
        )
        self.assertEqual(
            model_policy.CURRENT_ANTHROPIC_MODEL.harbor_flag,
            "@anthropic/claude-opus-4-8",
        )
        self.assertEqual(
            model_policy.QUALITY_CHECK_MODEL,
            "openai/@openai/gpt-5.5",
        )
        self.assertEqual(model_policy.RUBRIC_REVIEW_MODEL, "claude-opus-4-8")
        self.assertEqual(rubric_review.DEFAULT_MODEL, model_policy.RUBRIC_REVIEW_MODEL)

    def test_current_and_legacy_identifiers_remain_parseable(self) -> None:
        cases = {
            "terminus-2__@openai/gpt-5.5__adhoc": "gpt-5.5",
            "@anthropic/claude-opus-4-8": "claude-opus-4.8",
            "terminus-2__@openai/gpt-5.2__adhoc": "gpt-5.2",
            "claude-opus-4.6": "claude-opus-4.6",
        }
        for raw, expected in cases.items():
            with self.subTest(raw=raw):
                self.assertEqual(model_policy.identify_model(raw), expected)

    def test_unknown_future_model_is_visible_but_oracle_is_not_a_model(self) -> None:
        raw = "terminus-2__@openai/gpt-6.0__adhoc"
        self.assertEqual(model_policy.identify_model(raw), "unknown:" + raw)
        self.assertIsNone(model_policy.identify_model("oracle__adhoc"))
        self.assertIsNone(model_policy.identify_model("nop__adhoc"))

    def test_unknown_future_model_survives_job_report(self) -> None:
        eval_key = "terminus-2__@openai/gpt-6.0__adhoc"
        with tempfile.TemporaryDirectory() as tmp:
            job = Path(tmp)
            (job / "result.json").write_text(
                json.dumps(
                    {
                        "stats": {
                            "evals": {
                                eval_key: {
                                    "n_trials": 2,
                                    "n_errors": 0,
                                    "reward_stats": {
                                        "reward": {"1.0": ["t1"], "0.0": ["t2"]}
                                    },
                                }
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )
            report = agent_test.build_report(task_dir=None, job_dirs=[job])
        model_id = "unknown:" + eval_key
        self.assertIn(model_id, report["models"])
        self.assertEqual(report["models"][model_id]["passes"], 1)
        self.assertEqual(report["models"][model_id]["trials"], 2)

    def test_model_generation_does_not_change_difficulty_math(self) -> None:
        legacy = {
            "gpt-5.2": agent_test.ModelRunStats("gpt-5.2", "GPT-5.2", 2, 5, 0, 0.4),
            "claude-opus-4.6": agent_test.ModelRunStats(
                "claude-opus-4.6", "Claude Opus 4.6", 0, 5, 0, 0.0
            ),
        }
        current = {
            "gpt-5.5": agent_test.ModelRunStats("gpt-5.5", "GPT-5.5", 2, 5, 0, 0.4),
            "claude-opus-4.8": agent_test.ModelRunStats(
                "claude-opus-4.8", "Claude Opus 4.8", 0, 5, 0, 0.0
            ),
        }
        legacy_verdict = agent_test.classify_difficulty(legacy)
        current_verdict = agent_test.classify_difficulty(current)
        self.assertEqual(current_verdict, legacy_verdict)

    def test_current_operational_guidance_has_no_legacy_default(self) -> None:
        repo = Path(__file__).resolve().parents[1]
        operational_files = (
            "agent_test.py",
            "requirements_check.py",
            "commands.md",
            "workflow.md",
            ".cursor/rules/review-and-submit.mdc",
            "ci_checks.mdc",
            "ci_checks/rubric_review.py",
            "quality_check_adjudicate.py",
            "terminus_unified_ground_truth_specification_updated.md",
            "REPO_CONVENTIONS.md",
        )
        legacy_tokens = ("gpt-5.2", "GPT-5.2", "claude-opus-4-6", "Opus 4.6")
        for relative in operational_files:
            text = (repo / relative).read_text(encoding="utf-8")
            with self.subTest(path=relative):
                for token in legacy_tokens:
                    self.assertNotIn(token, text)


if __name__ == "__main__":
    unittest.main()
