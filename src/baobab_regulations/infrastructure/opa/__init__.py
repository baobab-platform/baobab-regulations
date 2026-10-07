"""OPA HTTP / Rego adapter package.

Production R-CAP-09 evaluation uses OPA behind the provider-neutral
RegulatoryPolicyEvaluatorPort. Canonical contracts never expose OPA topology or
Rego package paths.
"""

from baobab_regulations.infrastructure.opa.client import OpaRegulatoryPolicyEvaluator

__all__ = ["OpaRegulatoryPolicyEvaluator"]
