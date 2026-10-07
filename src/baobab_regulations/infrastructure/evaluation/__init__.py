"""Offline and non-OPA evaluation adapters.

Production OPA/Rego lives under ``infrastructure.opa``. Deterministic
reference evaluators used for scaffold, RTD contract adapters and golden tests
live here so the ``opa`` package is not polluted with non-OPA implementations.
"""

from baobab_regulations.infrastructure.evaluation.documentary import (
    ProjectionDocumentaryEvidenceAssessor,
)
from baobab_regulations.infrastructure.evaluation.reference import ReferenceEvaluator

__all__ = [
    "ProjectionDocumentaryEvidenceAssessor",
    "ReferenceEvaluator",
]
