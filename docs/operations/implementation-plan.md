# Gate REG — Implementation Plan (summary)

**Branch / PR:** `feat/regulations-scaffold` → [PR #4](https://github.com/baobab-platform/baobab-regulations/pull/4)

```text
REG-0  Scaffold + invariants          DONE
REG-1  Platform contracts + tenancy   DONE
REG-2  Canonical aggregates + schema  DONE
REG-3  Source registry + provenance   DONE
REG-4  BRIR v0 + applicability        NEXT
REG-5  Evaluation + UG→ZA coffee golden
REG-6–12  Persistence hardening, OPA, ingestion, AI, packs, commercial
```

## REG-3 (done)

- `AuthoritativeSource`, `SourceArtefact`, `ProvenanceLink`, `DerivedRuleRegistration`
- `RightsClass`: allow_store_text | hash_only | citation_only | no_ai_train
- `InMemorySourceRegistry` refuses derived rules without source+artefact+rights
- Migration `000002_source_registry.sql`
- Architecture test forbids vendor SDKs in domain

## Next: REG-4

BRIR fragment schema v0; extract UG→ZA coffee checks from ReferenceEvaluator; VERIFIED-only load into active rule set.
