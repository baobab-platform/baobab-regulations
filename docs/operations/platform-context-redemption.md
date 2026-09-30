# Platform context redemption (REG-1)

**ADRs:** ADR-REG-0026, ADR-REG-0028, ADR-BCP-004  
**Status:** Scaffold contract (no live Control Plane call yet)

## Problem

Regulations must evaluate under a verified platform context (tenant, organisation,
legal entity, market, trade lane) without becoming the system of record for those
entities.

## Two accepted input shapes

### A. Inline `PlatformContextRef` (scaffold default)

Callers supply opaque IDs already resolved by Control Plane:

```json
{
  "tenant_id": "tenant-zuribeans",
  "organisation_id": "org-…",
  "legal_entity_id": "le-…",
  "market_id": "market-…",
  "trade_lane_id": "lane-…",
  "capability_grant_ids": ["grant-…"],
  "context_id": null
}
```

`tenant_id` is mandatory. Empty / missing → `TenantContextError` (fail closed).

### B. Opaque `context_id` (production target)

Callers supply only a Control Plane `context_id`. Regulations redeems it via
Control Plane `platform-context` resolution (capability `context:resolve` /
successor). Until that client is wired:

- API accepts header `X-Baobab-Context-Id` **or** body field `platform.context_id`
- Redemption returns a structured error `CONTEXT_REDEMPTION_NOT_IMPLEMENTED`
  rather than inventing platform state

Regulations **never**:

- creates tenants, organisations, legal entities, markets, or trade lanes
- treats `tenant_id` alone as full isolation (ADR-REG-0028 defence-in-depth)
- stores platform entities as regulatory aggregates

## HTTP conventions (scaffold)

| Header | Purpose |
|--------|---------|
| `X-Baobab-Tenant-Id` | Required for evaluation routes when body omits platform.tenant_id |
| `X-Baobab-Context-Id` | Optional; opaque CP context for future redemption |
| `X-Baobab-Correlation-Id` | Propagated into audit events |

Health endpoints (`/healthz`, `/readyz`) do not require tenant context.

## Audit

Every evaluation attempt SHOULD emit `regulations.evaluation.requested` /
`regulations.evaluation.completed` draft shapes under `contracts/events/` once
the evaluate route lands. REG-1 defines the schema only.
