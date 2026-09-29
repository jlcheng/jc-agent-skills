#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["PyYAML>=6,<7"]
# ///
"""Read-only checks for this repository's shared Claude/Codex packaging."""

import argparse
import json
import re
from pathlib import Path
from typing import Any

import yaml


class Validator:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.errors: list[str] = []
        self.parsed: dict[str, Any] = {}

    def error(self, path: str, message: str) -> None:
        self.errors.append(f"{path}: {message}")

    def read(self, path: str) -> str | None:
        try:
            return (self.root / path).read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            self.error(path, str(exc))
            return None

    def load(self, path: str) -> Any:
        if path in self.parsed:
            return self.parsed[path]
        source = self.read(path)
        value = None
        if source is not None:
            try:
                value = (
                    json.loads(source)
                    if path.endswith(".json")
                    else yaml.safe_load(source)
                )
            except (ValueError, yaml.YAMLError) as exc:
                self.error(path, f"invalid syntax: {exc}")
        self.parsed[path] = value
        return value

    def mapping(self, value: Any, path: str, label: str) -> dict[str, Any]:
        if not isinstance(value, dict):
            self.error(path, f"{label} must be an object/mapping")
            return {}
        return value

    def validate(self) -> None:
        # Scan the plugin tree and the two marketplace configuration roots.
        for directory in ("plugins", ".claude-plugin", ".agents"):
            for data_path in sorted((self.root / directory).rglob("*")):
                if data_path.is_file() and data_path.suffix in {
                    ".json",
                    ".yaml",
                    ".yml",
                }:
                    self.load(data_path.relative_to(self.root).as_posix())
        base = "plugins/jc-code"
        claude_path = f"{base}/.claude-plugin/plugin.json"
        codex_path = f"{base}/.codex-plugin/plugin.json"
        claude = self.mapping(self.load(claude_path), claude_path, "manifest")
        codex = self.mapping(self.load(codex_path), codex_path, "manifest")
        for key in ("name", "version", "description", "author"):
            if (
                key not in claude
                or key not in codex
                or claude.get(key) != codex.get(key)
            ):
                self.error(codex_path, f"{key} must match {claude_path}")
        for path, manifest in ((claude_path, claude), (codex_path, codex)):
            for key in ("name", "version", "description"):
                if not isinstance(manifest.get(key), str) or not manifest[key].strip():
                    self.error(path, f"{key} must be a nonempty string")
            if manifest.get("name") != "jc-code":
                self.error(path, "name must be jc-code")
            self.mapping(manifest.get("author"), path, "author")
        interface = self.mapping(codex.get("interface"), codex_path, "interface")
        if interface.get("longDescription") != codex.get("description"):
            self.error(codex_path, "interface.longDescription must match description")
        for path, manifest in ((claude_path, claude), (codex_path, codex)):
            if manifest.get("skills", "./skills/") not in ("./skills", "./skills/"):
                self.error(path, "skills must use the shared ./skills/ directory")
        self.marketplaces()
        self.skills()
        self.docs(claude.get("version"))

    def docs(self, version: Any) -> None:
        skills = {
            path.name
            for path in (self.root / "plugins/jc-code/skills").glob("*")
            if path.is_dir()
        }
        readme = self.read("README.md")
        if readme is not None:
            sections = dict(
                re.findall(
                    r"^## ([^\n]+)\n(.*?)(?=^## |\Z)", readme, re.MULTILINE | re.DOTALL
                )
            )
            table_skills = set(
                re.findall(
                    r"^\|\s*`jc-code`\s*\|\s*`([^`]+)`",
                    sections.get("Plugins", ""),
                    re.MULTILINE,
                )
            )
            if skills != table_skills:
                self.error(
                    "README.md",
                    f"Plugins table inventory mismatch: missing {sorted(skills - table_skills)}, stale {sorted(table_skills - skills)}",
                )
            layout = sections.get("Layout", "")
            for platform in ("claude", "codex"):
                match = re.search(
                    rf"\.{platform}-plugin/plugin\.json[^\n]*\bversion (\S+)", layout
                )
                if not match or match.group(1) != version:
                    self.error(
                        "README.md",
                        f"Layout {platform} plugin version must be {version}",
                    )
            releases = re.findall(
                r"^### (\d+\.\d+\.\d+)\b", sections.get("Change Log", ""), re.MULTILINE
            )
            if not releases or releases[0] != version:
                self.error("README.md", f"first Change Log release must be {version}")
        vetting = self.read("VETTING.md")
        if vetting is not None:
            documented = set(
                re.findall(r"^## jc-code:([^\s]+)\s*$", vetting, re.MULTILINE)
            )
            for missing in sorted(skills - documented):
                self.error("VETTING.md", f"missing entry for jc-code:{missing}")

    def skills(self) -> None:
        directory = self.root / "plugins/jc-code/skills"
        if not directory.is_dir():
            self.error("plugins/jc-code/skills", "shared skills directory is missing")
            return
        for folder in sorted(directory.iterdir()):
            if not folder.is_dir():
                continue
            path = (folder / "SKILL.md").relative_to(self.root).as_posix()
            source = self.read(path)
            if source is None:
                continue
            lines = source.splitlines()
            if not lines or lines[0] != "---" or "---" not in lines[1:]:
                self.error(
                    path, "must start with YAML frontmatter enclosed by --- lines"
                )
                continue
            try:
                metadata = yaml.safe_load("\n".join(lines[1 : lines.index("---", 1)]))
            except (ValueError, yaml.YAMLError) as exc:
                self.error(path, f"invalid frontmatter: {exc}")
                continue
            metadata = self.mapping(metadata, path, "frontmatter")
            if metadata.get("name") != folder.name:
                self.error(path, f"name must match skill directory {folder.name}")
            if (
                not isinstance(metadata.get("description"), str)
                or not metadata["description"].strip()
            ):
                self.error(path, "description must be a nonempty string")
            disabled = metadata.get("disable-model-invocation", False)
            policy_path = (
                (folder / "agents/openai.yaml").relative_to(self.root).as_posix()
            )
            implicit = True
            if (self.root / policy_path).exists():
                config = self.mapping(
                    self.load(policy_path), policy_path, "agent config"
                )
                policy = self.mapping(config.get("policy", {}), policy_path, "policy")
                implicit = policy.get("allow_implicit_invocation", True)
            if not isinstance(disabled, bool):
                self.error(path, "disable-model-invocation must be a boolean")
            if not isinstance(implicit, bool):
                self.error(
                    policy_path, "policy.allow_implicit_invocation must be a boolean"
                )
            if (
                isinstance(disabled, bool)
                and isinstance(implicit, bool)
                and disabled == implicit
            ):
                self.error(
                    path,
                    f"disable-model-invocation={str(disabled).lower()} requires "
                    f"policy.allow_implicit_invocation={str(not disabled).lower()} "
                    f"in {policy_path}; found {str(implicit).lower()} "
                    "(true is the default when absent)",
                )

    def marketplaces(self) -> None:
        for path in (
            ".claude-plugin/marketplace.json",
            ".agents/plugins/marketplace.json",
        ):
            catalog = self.mapping(self.load(path), path, "marketplace")
            entries = catalog.get("plugins")
            if not isinstance(entries, list):
                self.error(path, "plugins must be a list")
                continue
            matches = [
                entry
                for entry in entries
                if isinstance(entry, dict) and entry.get("name") == "jc-code"
            ]
            if len(matches) != 1:
                self.error(path, "plugins must contain exactly one jc-code entry")
                continue
            entry = matches[0]
            if path.startswith(".claude"):
                if entry.get("source") != "./plugins/jc-code":
                    self.error(path, "jc-code source must be ./plugins/jc-code")
                if (
                    not isinstance(entry.get("description"), str)
                    or not entry["description"].strip()
                ):
                    self.error(path, "jc-code description must be a nonempty string")
            else:
                source = self.mapping(entry.get("source"), path, "jc-code source")
                if (
                    source.get("source") != "local"
                    or source.get("path") != "./plugins/jc-code"
                ):
                    self.error(
                        path, "jc-code source must be local with path ./plugins/jc-code"
                    )
                policy = self.mapping(entry.get("policy"), path, "jc-code policy")
                for key, expected in (
                    ("installation", "AVAILABLE"),
                    ("authentication", "ON_INSTALL"),
                ):
                    if policy.get(key) != expected:
                        self.error(path, f"jc-code policy.{key} must be {expected}")
                if entry.get("category") != "Productivity":
                    self.error(path, "jc-code category must be Productivity")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root", type=Path, default=Path(__file__).resolve().parents[1]
    )
    args = parser.parse_args()
    validator = Validator(args.root)
    validator.validate()
    for error in validator.errors:
        print(error)
    if validator.errors:
        print(f"Validation failed: {len(validator.errors)} error(s).")
        return 1
    print("Repository validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
