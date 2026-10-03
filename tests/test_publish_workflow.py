from __future__ import annotations

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "publish-pypi.yml"


class PublishWorkflowTests(unittest.TestCase):
    def test_publish_happens_before_sigstore_bundle_creation(self):
        text = WORKFLOW.read_text(encoding="utf-8")
        publish = text.index("- name: Publish with Trusted Publishing")
        sign = text.index("- name: Sign wheel after publication")
        self.assertLess(publish, sign)

    def test_pypi_upload_reads_only_pre_signature_dist_directory(self):
        text = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("packages-dir: dist/", text)
        self.assertIn("inputs: dist/*.whl", text)

    def test_release_checkout_does_not_persist_git_credentials(self):
        text = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("persist-credentials: false", text)


if __name__ == "__main__":
    unittest.main()
