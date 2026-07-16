import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "translate-hea-manuscript"
sys.path.insert(0, str(SKILL / "scripts"))

import literature_pipeline as literature
import local_corpus


class SkillStructureTests(unittest.TestCase):
    def test_required_skill_files_exist(self):
        self.assertTrue((SKILL / "SKILL.md").is_file())
        self.assertTrue((SKILL / "agents" / "openai.yaml").is_file())
        self.assertTrue((SKILL / "references" / "local-corpus.md").is_file())

    def test_skill_frontmatter(self):
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\nname: translate-hea-manuscript\n"))
        frontmatter = text.split("---", 2)[1]
        keys = [line.split(":", 1)[0] for line in frontmatter.splitlines() if ":" in line]
        self.assertEqual(keys, ["name", "description"])


class LiteraturePipelineTests(unittest.TestCase):
    def test_cc_location_and_learning_use(self):
        work = {
            "id": "https://openalex.org/W1",
            "doi": "https://doi.org/10.1234/example",
            "display_name": "Electronic structure of NbTaMoW refractory high-entropy alloys",
            "publication_year": 2024,
            "type": "article",
            "language": "en",
            "is_retracted": False,
            "is_paratext": False,
            "open_access": {"is_oa": True, "oa_status": "gold"},
            "primary_location": {
                "is_oa": True,
                "pdf_url": "https://example.org/paper.pdf",
                "landing_page_url": "https://example.org/paper",
                "license": "cc-by",
                "version": "publishedVersion",
                "source": {"display_name": "Acta Materialia"},
            },
            "best_oa_location": None,
            "locations": [],
            "authorships": [{"author": {"display_name": "A. Author"}}],
            "abstract_inverted_index": {
                "density": [0], "of": [1], "states": [2], "and": [3], "DFT": [4]
            },
        }
        record = literature.record_from_work(work, "NbTaMoW DFT", "cc-only")
        self.assertIsNotNone(record)
        self.assertEqual(record["doi"], "10.1234/example")
        self.assertEqual(record["license"], "cc-by")
        self.assertIn("Electronic Structure", record["main_translation_use"])

    def test_private_download_url_is_blocked(self):
        with self.assertRaises(ValueError):
            literature.validate_remote_url("http://127.0.0.1/paper.pdf")


class LocalCorpusTests(unittest.TestCase):
    def test_markdown_import_is_read_only_and_deduplicated(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            papers = root / "papers"
            output = root / "project"
            papers.mkdir()
            content = (
                "---\ntitle: XPS study of an HEA\ndoi: 10.1234/local\nyear: 2024\n---\n"
                "# Electronic structure\n\nThe density of states was calculated.\n"
            )
            first = papers / "first.md"
            second = papers / "second.md"
            first.write_text(content, encoding="utf-8")
            second.write_text(content, encoding="utf-8")
            before = hashlib.sha256(first.read_bytes()).hexdigest()

            files = local_corpus.discover_files([papers], False, output)
            markdown_dir = output / "02_reference_papers" / "markdown"
            originals_dir = output / "02_reference_papers" / "local_originals"
            records = [
                local_corpus.import_record(
                    path, index, markdown_dir, originals_dir, False, False
                )
                for index, path in enumerate(files, 1)
            ]
            local_corpus.mark_duplicates(records)
            local_corpus.write_indexes(output, records, [papers])

            self.assertEqual(before, hashlib.sha256(first.read_bytes()).hexdigest())
            self.assertEqual(sum(bool(item["duplicate_of"]) for item in records), 1)
            manifest = json.loads(
                (output / "02_reference_papers" / "local_corpus_manifest.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(len(manifest["papers"]), 2)


if __name__ == "__main__":
    unittest.main()
