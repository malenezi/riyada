"""Tests for the bundled scripts. Run: python -m unittest discover -s tests"""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LINT = ROOT / "shared/scripts/context_lint.py"
MODEL = ROOT / "shared/scripts/build_model.py"
EXAMPLE = ROOT / "examples/mawja"
TODAY = "2026-11-16"


def run(*args):
    return subprocess.run([sys.executable, *map(str, args)], capture_output=True, text=True)


class ContextLint(unittest.TestCase):
    def lint(self, folder, *extra):
        r = run(LINT, folder, "--format", "json", "--today", TODAY, *extra)
        return r.returncode, json.loads(r.stdout)

    def pack(self):
        tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, tmp)
        shutil.copytree(EXAMPLE / "context/en", tmp / "context")
        return tmp / "context"

    def rules(self, report):
        return {f["rule"] for f in report["findings"]}

    def test_examples_are_clean(self):
        for lang in ("en", "ar"):
            code, report = self.lint(EXAMPLE / "context" / lang)
            self.assertEqual((code, report["findings"]), (0, []), lang)

    def test_blank_templates_fail_on_placeholders(self):
        code, report = self.lint(ROOT / "context")
        self.assertEqual(code, 1)
        self.assertIn("CTX002", self.rules(report))
        self.assertNotIn("CTX013", self.rules(report))  # en and ar are separate packs

    def test_missing_layer(self):
        pack = self.pack()
        (pack / "06-authority-governance.md").unlink()
        code, report = self.lint(pack)
        self.assertEqual(code, 1)
        self.assertIn("CTX001", self.rules(report))

    def test_conflicting_fact(self):
        pack = self.pack()
        f = pack / "05-knowledge-data.md"
        f.write_text(f.read_text(encoding="utf-8") +
                     "\n- **Pricing:** SAR 399 per branch per month\n", encoding="utf-8")
        _, report = self.lint(pack)
        self.assertIn("CTX009", self.rules(report))

    def test_secret_is_reported_but_not_echoed(self):
        pack = self.pack()
        f = pack / "04-operations.md"
        secret = "sk-" + "a1B2c3D4e5F6g7H8i9J0"
        f.write_text(f.read_text(encoding="utf-8") + f"\nCRM key: {secret}\n", encoding="utf-8")
        r = run(LINT, pack, "--today", TODAY)
        self.assertEqual(r.returncode, 1)
        self.assertIn("CTX011", r.stdout)
        self.assertNotIn(secret, r.stdout)

    def test_governance_needs_matrix_and_never(self):
        pack = self.pack()
        (pack / "06-authority-governance.md").write_text(
            "# Layer 6\n\n- **Owner:** A\n- **Last reviewed:** 2026-11-10\n\n"
            "## Rules\n\nAgents should be careful.\n", encoding="utf-8")
        _, report = self.lint(pack)
        self.assertLessEqual({"CTX007", "CTX008"}, self.rules(report))

    def test_stale_review_is_a_warning(self):
        pack = self.pack()
        code, report = self.lint(pack, "--max-age-days", "3")
        self.assertEqual(code, 0)
        self.assertIn("CTX005", self.rules(report))
        code, _ = self.lint(pack, "--max-age-days", "3", "--strict")
        self.assertEqual(code, 1)

    def test_empty_section(self):
        pack = self.pack()
        f = pack / "02-strategy.md"
        f.write_text(f.read_text(encoding="utf-8") + "\n## Open questions\n", encoding="utf-8")
        _, report = self.lint(pack)
        self.assertIn("CTX003", self.rules(report))


class BuildModel(unittest.TestCase):
    def build(self, assumptions, lang="en"):
        tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, tmp)
        src = tmp / "a.json"
        src.write_text(json.dumps(assumptions), encoding="utf-8")
        r = run(MODEL, src, "--out", tmp / "model", "--lang", lang, "--no-xlsx")
        md = (tmp / "model.md").read_text(encoding="utf-8") if (tmp / "model.md").exists() else ""
        return r, md, tmp

    def example(self):
        return json.loads((EXAMPLE / "assumptions.json").read_text(encoding="utf-8"))

    def test_example_figures(self):
        r, md, tmp = self.build(self.example())
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        for expected in ("338,119", "14,040", "| 7.8 |", "| 5.1 |", "| 27 |", "1,746,527"):
            self.assertIn(expected, md)
        rows = (tmp / "model.csv").read_text(encoding="utf-8-sig").splitlines()
        self.assertEqual(len(rows), 37)

    def test_arabic_labels(self):
        r, md, _ = self.build(self.example(), lang="ar")
        self.assertEqual(r.returncode, 0)
        self.assertIn("ملخص النموذج المالي", md)
        self.assertIn("338,119", md)

    def test_unfunded_plan_blocks(self):
        a = self.example()
        a["funding"] = []
        r, md, _ = self.build(a)
        self.assertEqual(r.returncode, 1)
        self.assertIn("BLOCKING", r.stdout)

    def test_warnings(self):
        a = self.example()
        a.update(monthly_churn=0.08, gross_margin=0.95, acquisition_cost_per_customer=9000)
        r, md, _ = self.build(a)
        for phrase in ("Monthly churn of 8.0%", "above 90%", "below 3"):
            self.assertIn(phrase, md)

    def test_rejects_percent_written_as_whole_number(self):
        a = self.example()
        a["monthly_churn"] = 3
        r, _, _ = self.build(a)
        self.assertEqual(r.returncode, 2)
        self.assertIn("monthly_churn", r.stderr)

    def test_workbook_is_written_when_openpyxl_is_available(self):
        try:
            import openpyxl
        except ImportError:
            self.skipTest("openpyxl not installed")
        tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, tmp)
        r = run(MODEL, EXAMPLE / "assumptions.json", "--out", tmp / "m", "--lang", "ar")
        self.assertEqual(r.returncode, 0, r.stderr)
        wb = openpyxl.load_workbook(tmp / "m.xlsx")
        self.assertEqual(len(wb.sheetnames), 5)
        self.assertTrue(wb.worksheets[0].sheet_view.rightToLeft)
        monthly = wb.worksheets[4]
        self.assertTrue(str(monthly["F2"].value).startswith("="))


if __name__ == "__main__":
    unittest.main()
