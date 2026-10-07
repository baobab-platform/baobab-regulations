"""HTTP capability runtime wiring for the two canonical RTD-06 operations."""

from dataclasses import dataclass

from baobab_regulations.application.ports.authentication import WorkloadAuthenticatorPort
from baobab_regulations.application.services.evidence_assessment import EvidenceAssessmentService
from baobab_regulations.application.services.requirement_resolution import (
    RequirementResolutionService,
)


@dataclass(frozen=True, slots=True)
class CapabilityApiRuntime:
    """Dependencies required before canonical Regulations routes can serve traffic."""

    authenticator: WorkloadAuthenticatorPort
    requirement_resolution: RequirementResolutionService
    evidence_assessment: EvidenceAssessmentService


__all__ = ["CapabilityApiRuntime"]
