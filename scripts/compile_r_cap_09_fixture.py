#!/usr/bin/env python3
"""Compile the governed R-CAP-09 BRIR fixture into deterministic Rego v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from baobab_regulations.brir.compiler import RegoV1Compiler
from baobab_regulations.brir.models import BrirRuleSet


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--metadata", type=Path)
    args = parser.parse_args()

    document = json.loads(args.input.read_text(encoding="utf-8"))
    rule_set = BrirRuleSet.model_validate(document)
    artifact = RegoV1Compiler().compile(rule_set)

    args.output.write_text(artifact.source, encoding="utf-8")
    if args.metadata is not None:
        args.metadata.write_text(
            json.dumps(
                {
                    "rule_set_id": artifact.rule_set_id,
                    "rule_set_fingerprint": artifact.rule_set_fingerprint,
                    "compiler_id": artifact.compiler_id,
                    "compiler_version": artifact.compiler_version,
                    "target": artifact.target,
                    "entrypoint": artifact.entrypoint,
                    "artifact_fingerprint": artifact.artifact_fingerprint,
                },
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )

    print(
        f"{artifact.rule_set_id} "
        f"{artifact.rule_set_fingerprint} "
        f"{artifact.artifact_fingerprint}"
    )


if __name__ == "__main__":
    main()
