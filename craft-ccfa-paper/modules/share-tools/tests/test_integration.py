"""Regression tests for the unified skill's handoff and export contracts."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from check_section import check as section_check
from check_terms import check as terms_check, parse_facts
from figkit import Figure
from pypdf import PdfReader

FACTS = ROOT / 'tests/fictional/facts.md'
TERMS = ['Frequency-routed Motion Prior', 'Band-wise Test-time Adaptation', 'Spectral Alignment Loss']


class HandoffTests(unittest.TestCase):
    def test_style_is_nonblocking_for_legal_short_titles(self):
        report = section_check('title', 'On Models')
        self.assertTrue(any(level == 'WARN' for level, _ in report))
        self.assertFalse(any(level == 'FAIL' for level, _ in report))
        run = subprocess.run([sys.executable, str(ROOT / 'scripts/check_section.py'),
                              'title', str(ROOT / 'tests/bad/title.txt'), '--json'],
                             text=True, capture_output=True)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertTrue(any(level == 'WARN' for level, _ in json.loads(run.stdout)))

    def test_evidenced_numbers_are_not_style_errors(self):
        body = 'We present a model. Experiments show a 10% increase in accuracy.'
        for section in ('abstract', 'conclusion'):
            self.assertFalse(any('specific numbers' in msg for _, msg in section_check(section, body)))

    def test_local_figure_and_short_abstract_may_omit_modules(self):
        report = terms_check(FACTS, {'abstract': 'We present TideMotion.'}, [TERMS[0]])
        self.assertFalse(any(level == 'FAIL' for level, _ in report), report)
        self.assertFalse(any(msg.startswith('abstract:') for _, msg in report), report)
        required = terms_check(FACTS, {}, [TERMS[0]], require_in=['figure'])
        self.assertEqual(sum(level == 'FAIL' for level, _ in required), 2, required)

    def test_complete_method_and_figure_with_alias_pass(self):
        report = terms_check(FACTS, {'method': 'We use ' + ', '.join(TERMS)},
                             [TERMS[0], 'BTA', TERMS[2]], require_in=['method', 'figure'])
        self.assertEqual(report, [])

    def test_alias_does_not_hide_misspelled_full_name(self):
        body = 'Frequency routed Motion Prior, BTA, Spectral Alignment Loss. Motion Prior.'
        report = terms_check(FACTS, {'method': body}, None)
        self.assertTrue(any(level == 'FAIL' and 'differs' in msg for level, msg in report), report)

    def test_require_scope_without_input_is_error(self):
        with self.assertRaisesRegex(ValueError, 'no input'):
            terms_check(FACTS, {}, None, require_in=['figure'])

    def test_malformed_facts_report_input_error(self):
        samples = ['', '## Modules\n',
                   '## Modules\n| Name | Aliases |\n|---|---|\n| Missing alias |\n']
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / 'facts.md'
            for table in samples:
                f.write_text('# Facts\n- Name: Example\n' + table)
                with self.assertRaises(ValueError):
                    parse_facts(f)

    def test_cli_checks_input_and_strict_scope(self):
        script = str(ROOT / 'scripts/check_terms.py')
        missing = subprocess.run([sys.executable, script, str(FACTS)], capture_output=True, text=True)
        self.assertEqual(missing.returncode, 2)
        self.assertIn('supply at least', missing.stderr)
        with tempfile.TemporaryDirectory() as d:
            labels = Path(d) / 'labels.json'
            labels.write_text(json.dumps({'labels': [TERMS[0]]}))
            cmd = [sys.executable, script, str(FACTS), '--figure', str(labels)]
            local = subprocess.run(cmd, capture_output=True, text=True)
            complete = subprocess.run(cmd + ['--require-in', 'figure'], capture_output=True, text=True)
            self.assertEqual(local.returncode, 0, local.stderr)
            self.assertEqual(complete.returncode, 1, complete.stderr)
            self.assertIn('FAIL', complete.stdout)


class FigureTests(unittest.TestCase):
    def test_example_cli_writes_to_requested_directory(self):
        with tempfile.TemporaryDirectory() as d:
            run = subprocess.run([sys.executable, str(ROOT / 'examples/minimal/build.py'),
                                  '--output', d], text=True, capture_output=True)
            self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
            self.assertTrue((Path(d) / 'framework.pdf').is_file())
            labels = json.loads((Path(d) / 'labels.json').read_text())
            self.assertTrue(any('placeholders' in note for _, note in labels['schematic']))

    def test_exports_have_requested_print_size_and_restore_environment(self):
        with tempfile.TemporaryDirectory() as d:
            f = Figure(900, 300, 'Export contract', print_width_in=3.5, base=30)
            f.block(100, 80, 600, 100, 'Example Module')
            f.schematic('Module', 'conceptual diagram')
            before = os.environ.get('FONTCONFIG_FILE')
            f.save(d)
            self.assertEqual(os.environ.get('FONTCONFIG_FILE'), before)
            for name in ('index.html', 'framework.svg', 'framework-outlined.svg', 'framework.pdf', 'preview.png', 'labels.json'):
                self.assertTrue((Path(d) / name).stat().st_size > 0, name)
            self.assertIn('<text ', (Path(d) / 'framework.svg').read_text())
            self.assertNotIn('<text ', (Path(d) / 'framework-outlined.svg').read_text())
            pdf = PdfReader(Path(d) / 'framework.pdf')
            self.assertAlmostEqual(float(pdf.pages[0].mediabox.width) / 72, 3.5, places=5)
            self.assertAlmostEqual(float(pdf.pages[0].mediabox.height) / 72, 3.5 / 3, places=5)
            labels = json.loads((Path(d) / 'labels.json').read_text())
            self.assertIn('Example Module', labels['labels'])
            self.assertEqual(labels['schematic'], [['Module', 'conceptual diagram']])

    def test_export_failure_restores_env_and_preserves_error(self):
        import cairosvg
        def fail_export(**kwargs):
            self.assertEqual(os.environ['FONTCONFIG_FILE'], '/original/config')
            raise RuntimeError('export failed')

        with tempfile.TemporaryDirectory() as d, patch.dict(os.environ, {'FONTCONFIG_FILE': '/original/config'}):
            with patch.object(cairosvg, 'svg2png', side_effect=fail_export):
                with self.assertRaisesRegex(RuntimeError, 'export failed'):
                    Figure(600, 200, 'Failure').save(d)
            self.assertEqual(os.environ['FONTCONFIG_FILE'], '/original/config')

    def test_lint_detects_overlaps_and_lines_crossing_text(self):
        f = Figure(1000, 300, 'Layout')
        f.label(300, 100, 'Alpha')
        f.label(300, 100, 'Beta')
        f.arrow((100, 100), (500, 100))
        report = f.lint()
        self.assertTrue(any('text overlap' in msg for msg in report), report)
        self.assertTrue(any('line crosses text' in msg for msg in report), report)


if __name__ == '__main__':
    unittest.main()
