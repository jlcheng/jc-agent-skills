"""Public CLI tests: uv run --with pyyaml python -m unittest discover -s tests."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/validate_repo.py"


class ValidatorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        manifest = {
            "name": "jc-code",
            "version": "1.2.3",
            "description": "Skills: example (demo).",
            "author": {"name": "John"},
        }
        self.write_json("plugins/jc-code/.claude-plugin/plugin.json", manifest)
        self.write_json(
            "plugins/jc-code/.codex-plugin/plugin.json",
            {
                **manifest,
                "skills": "./skills/",
                "interface": {"longDescription": manifest["description"]},
            },
        )
        self.write_json(
            ".claude-plugin/marketplace.json",
            {
                "plugins": [
                    {
                        "name": "jc-code",
                        "source": "./plugins/jc-code",
                        "description": "Example skill",
                    }
                ]
            },
        )
        self.write_json(
            ".agents/plugins/marketplace.json",
            {
                "plugins": [
                    {
                        "name": "jc-code",
                        "source": {"source": "local", "path": "./plugins/jc-code"},
                        "policy": {
                            "installation": "AVAILABLE",
                            "authentication": "ON_INSTALL",
                        },
                        "category": "Productivity",
                    }
                ]
            },
        )
        self.write(
            "plugins/jc-code/skills/example/SKILL.md",
            "---\nname: example\ndescription: Demo\nversion: 9.0\nother-agent-setting: yes\n---\nDemo\n",
        )
        self.write(
            "README.md",
            "## Plugins\n\n| `jc-code` | `example` |\n\n## Layout\n\n.claude-plugin/plugin.json # version 1.2.3\n.codex-plugin/plugin.json # version 1.2.3\n\n## Change Log\n\n### 1.2.3 — today\n",
        )
        self.write("VETTING.md", "## jc-code:example\nReviewed.\n")

    def write(self, path, value):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(value)

    def write_json(self, path, value):
        self.write(path, json.dumps(value))

    def run_cli(self):
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--root", str(self.root)],
            capture_output=True,
            check=False,
            text=True,
        )

    def test_valid_repo_accepts_extensions_and_upstream_version(self):
        result = self.run_cli()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_manifest_errors_are_aggregated_with_paths(self):
        self.write_json(
            "plugins/jc-code/.codex-plugin/plugin.json",
            {
                "name": "wrong",
                "version": "2.0.0",
                "description": "wrong",
                "author": "wrong",
                "interface": [],
                "skills": "elsewhere",
            },
        )
        self.write("plugins/jc-code/skills/example/broken.json", "{")
        result = self.run_cli()
        self.assertEqual(result.returncode, 1)
        for expected in [
            "plugin.json",
            "version",
            "description",
            "author",
            "interface",
            "skills",
            "broken.json",
        ]:
            self.assertIn(expected, result.stdout)
        self.assertNotIn("Traceback", result.stderr)

    def test_each_shared_manifest_field_is_checked_independently(self):
        path = "plugins/jc-code/.codex-plugin/plugin.json"
        original = (self.root / path).read_text()
        for field, value in [
            ("version", "8.0.0"),
            ("description", "Changed"),
            ("author", {"name": "Another person"}),
            ("longDescription", "Changed"),
        ]:
            with self.subTest(field=field):
                manifest = json.loads(original)
                if field == "longDescription":
                    manifest["interface"][field] = value
                else:
                    manifest[field] = value
                if field == "description":
                    manifest["interface"]["longDescription"] = value
                self.write_json(path, manifest)
                result = self.run_cli()
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertIn(field, result.stdout)
                self.assertIn(path, result.stdout)

    def test_marketplace_paths_and_catalog_metadata(self):
        self.write_json(
            ".claude-plugin/marketplace.json",
            {"plugins": [{"name": "jc-code", "source": "elsewhere"}]},
        )
        self.write_json(
            ".agents/plugins/marketplace.json",
            {"plugins": [{"name": "jc-code", "source": [], "policy": None}]},
        )
        result = self.run_cli()
        self.assertEqual(result.returncode, 1)
        for expected in [
            ".claude-plugin/marketplace.json",
            ".agents/plugins/marketplace.json",
            "source",
            "policy",
            "category",
        ]:
            self.assertIn(expected, result.stdout)

    def test_explicit_only_policy_parity_and_boolean_types(self):
        skill = "plugins/jc-code/skills/example/"
        for claude, codex, valid in [
            ("true", None, False),
            (None, "false", False),
            ("true", "false", True),
            ("false", "true", True),
            ("true", "true", False),
            ("false", "false", False),
            ('"false"', "true", False),
            ("false", '"true"', False),
        ]:
            with self.subTest(claude=claude, codex=codex):
                field = (
                    f"disable-model-invocation: {claude}\n"
                    if claude is not None
                    else ""
                )
                self.write(
                    skill + "SKILL.md",
                    f"---\nname: example\ndescription: Demo\n{field}---\nBody\n",
                )
                policy_path = self.root / (skill + "agents/openai.yaml")
                policy_path.unlink(missing_ok=True)
                if codex is not None:
                    self.write(
                        skill + "agents/openai.yaml",
                        f"policy:\n  allow_implicit_invocation: {codex}\nother-agent: custom\n",
                    )
                result = self.run_cli()
                self.assertEqual(result.returncode, 0 if valid else 1, result.stdout)
                if not valid:
                    self.assertIn("example/", result.stdout)

    def test_ui_only_agent_config_uses_default_activation(self):
        self.write(
            "plugins/jc-code/skills/example/agents/openai.yaml",
            "interface:\n  display_name: Example\n",
        )
        result = self.run_cli()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_malformed_frontmatter_timestamp_is_a_diagnostic(self):
        self.write(
            "plugins/jc-code/skills/example/SKILL.md",
            "---\nname: example\ndescription: Demo\ndate: 2026-99-99\n---\nBody\n",
        )
        result = self.run_cli()
        self.assertEqual(result.returncode, 1)
        self.assertNotIn("Traceback", result.stderr)
        self.assertIn("example/SKILL.md: invalid frontmatter", result.stdout)

    def test_skill_metadata_and_yaml_errors(self):
        self.write(
            "plugins/jc-code/skills/example/SKILL.md",
            "---\nname: wrong\ndescription: []\n---\nBody\n",
        )
        self.write("plugins/jc-code/skills/example/agents/openai.yaml", "policy: [")
        self.write("plugins/jc-code/skills/missing/README.md", "forgot SKILL.md")
        result = self.run_cli()
        self.assertEqual(result.returncode, 1)
        for expected in ["name", "description", "openai.yaml", "missing/SKILL.md"]:
            self.assertIn(expected, result.stdout)

    def test_documented_inventory_and_release_versions(self):
        self.write(
            "README.md",
            "## Plugins\n| `jc-code` | `removed` |\n## Layout\n.claude-plugin/plugin.json # version 1.0.0\n.codex-plugin/plugin.json # version 1.0.0\n## Change Log\n### 1.0.0 — today\n",
        )
        self.write("VETTING.md", "## jc-code:removed\nHistorical review\n")
        result = self.run_cli()
        self.assertEqual(result.returncode, 1)
        for expected in [
            "README.md",
            "Plugins",
            "Layout",
            "Change Log",
            "VETTING.md",
            "example",
        ]:
            self.assertIn(expected, result.stdout)


if __name__ == "__main__":
    unittest.main()
