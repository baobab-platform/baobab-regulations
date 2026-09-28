# ADR-REG-0007 — Jurisdiction, Regulatory Authority and Legal Hierarchy Model

**Status:** Proposed — Normative Foundational Architecture  
**Decision ID:** `ADR-REG-0007`  
**Engine:** Baobab Regulations  
**Target Repository:** `baobab-platform/baobab-regulations`  
**Date:** 2026-09-28  
**Decision Type:** Jurisdiction, Competence, Authority, Legal Hierarchy, Regime Interaction and Conflict Resolution Architecture  
**Strategic Classification:** Core Regulatory IP / Applicability Foundation

**Parent Decisions**

- `ADR-REG-0001 — Baobab Regulations Mission, Authority, Regulatory Execution and System Boundary`
- `ADR-REG-0002 — Baobab Regulations as a Headless Platform Engine and Capability Provider`
- `ADR-REG-0003 — Regulatory Authority, Source Authenticity, Interpretation and Derived Rule Boundary`
- `ADR-REG-0004 — Advisory, Review and Enforcement Decision Classes`
- `ADR-REG-0005 — Provider-Neutral Regulatory Intelligence, Source Acquisition and Anti-Corruption Architecture`
- `ADR-REG-0006 — Canonical Regulatory Domain Model, Legal Resource Identity and Aggregate Boundaries`

**Relevant Existing Baobab Architecture**

- `ADR-BCP-004 — Context, Market, Geography, Legal-Entity and Digital Estate Resolution Model`
- `ADR-BCP-011 — Market Participation, Trade Lanes and Cross-Market Trading Model`
- `ADR-BCP-018 — Canonical Organisation, Corporate Group, Platform Account and Tenant Relationship Model`
- `ADR-BCP-020 — Administrative Authority, Delegated Administration, Privileged Access and Separation-of-Duties Model`
- applicable Shared canonical identifier, external-reference and context contracts

**Primary Principle**

> **There is no universal legal precedence ladder. Regulatory authority is resolved within a defined jurisdiction, regime, subject matter, time, legal relationship and factual context.**

---

# 1. Executive Decision

Baobab Regulations SHALL implement a **Jurisdiction and Legal Authority Topology** capable of representing:

```text
territorial jurisdiction
        +
personal / entity jurisdiction
        +
subject-matter competence
        +
regulatory regime
        +
issuing authority
        +
delegated authority
        +
instrument hierarchy
        +
judicial hierarchy
        +
treaty / regional relationships
        +
temporal validity
        +
explicit precedence rules
        +
implementation / domestic-effect status
        +
exceptions
        +
conflict relationships
```

before determining which regulatory rule controls a particular assessment.

Baobab SHALL explicitly reject this architecture:

```text
Constitution            rank 1
Treaty                  rank 2
Act                     rank 3
Regulation              rank 4
Notice                  rank 5
Guidance                rank 6
```

as a universal platform rule.

Instead:

```text
                        REGULATORY CONTEXT
                               │
              ┌────────────────┼─────────────────┐
              ▼                ▼                 ▼
         Jurisdictions     Regimes          Subject Matter
              │                │                 │
              └────────────────┼─────────────────┘
                               ▼
                    Candidate Authorities
                               │
                               ▼
                  Competence Resolution
                               │
                               ▼
                    Candidate Instruments
                               │
                               ▼
                     Legal Relationships
                               │
                ┌──────────────┼──────────────┐
                ▼              ▼              ▼
            hierarchy       temporal       explicit
            relations       relations      precedence
                │              │              │
                └──────────────┼──────────────┘
                               ▼
                       Conflict Analysis
                               │
                 ┌─────────────┼─────────────┐
                 ▼             ▼             ▼
             resolved       coexisting    unresolved
                 │             │             │
                 ▼             ▼             ▼
            controlling    cumulative      REVIEW
               rule         obligations    REQUIRED
```

No source SHALL control merely because it was:

```text
newer
more specific
regional
national
from a regulator
from a court
from a treaty
```

unless the relevant legal topology supports that consequence.

---

# 2. Why This ADR Exists

`ADR-REG-0006` defines:

```text
Jurisdiction
RegulatoryRegime
RegulatoryAuthority
RegulatoryInstrument
RegulatoryRule
```

but does not yet answer:

> Which jurisdiction is legally relevant?

> Which authority had competence to issue this instrument?

> Does a regional regime apply directly?

> Does a treaty require domestic implementation?

> Does national legislation implement or modify the regime?

> Does another instrument override this one?

> Does a court decision change the interpretation?

> What happens when two apparently applicable rules conflict?

Without this ADR, an applicability engine could find many relevant rules but have no defensible mechanism for determining their relationship.

---

# 3. Research Finding: Legal Topology Is Jurisdiction-Specific

South Africa illustrates the problem.

Section 231 of the Constitution distinguishes between an international agreement **binding the Republic internationally** and the conditions under which it **becomes law in the Republic**. Parliamentary approval is generally required for specified agreements, and domestic legal effect ordinarily requires enactment, subject to the constitutional provision for qualifying self-executing treaty provisions. Sections 232 and 233 separately address customary international law and interpretation consistent with international law.

Therefore:

```text
Treaty binds State internationally
            ≠
Treaty automatically operates
as domestic transactional rule
```

as a universal proposition.

---

# 4. Uganda Demonstrates a Different Constitutional Path

Uganda's Constitution provides that the President or an authorised person may make treaties and agreements, while Parliament is to make laws governing ratification. It also preserves qualifying pre-existing treaty obligations through Article 287.

Baobab therefore SHALL NOT infer:

```text
Treaty signed
   =
directly executable domestic rule
```

without jurisdiction-specific implementation state.

---

# 5. EAC Demonstrates Express Regional Precedence

The EAC Treaty goes materially further.

Article 8 requires Partner States to give Community legislation, regulations and directives the force of law required by the Treaty, and provides that Community organs, institutions and laws take precedence over similar national ones on matters relating to Treaty implementation.

The Treaty also provides that decisions of the East African Court of Justice concerning interpretation and application of the Treaty take precedence over national court decisions on similar matters.

This cannot safely be represented by a generic:

```text
regional = stronger than national
```

rule.

It is a **Treaty-specific, subject-specific precedence relationship**.

---

# 6. AfCFTA Demonstrates Conditional Conflict Rules

AfCFTA supplies another important pattern.

Article 19 provides that AfCFTA prevails to the extent of a specific inconsistency with another regional agreement, **but** State Parties belonging to RECs, regional trading arrangements or customs unions that have attained higher levels of regional integration retain those higher levels among themselves.

Therefore:

```text
AfCFTA
   >
all REC arrangements
```

would be wrong.

The actual topology is closer to:

```text
AfCFTA
   │
   ├── prevailing relationship
   │   for specific inconsistency
   │
   └── exception
       for higher regional integration
       among relevant members
```

That is exactly the kind of relationship Baobab must model explicitly.

---

# 7. SACU Demonstrates Layered Regulatory Authority

The modern SACU Agreement establishes a common customs architecture among Botswana, Eswatini, Lesotho, Namibia and South Africa and provides for common customs duties and related institutional mechanisms.

Yet national law continues to matter.

The SACU framework itself preserves specified national import/export restrictions, while South Africa's International Trade Administration Act implements aspects of SACU domestically.

Accordingly:

```text
SACU rule
+
national implementing legislation
+
national regulatory control
```

may all be relevant to the same transaction.

---

# 8. Treaty Obligations and Domestic Law Must Remain Distinct

The Vienna Convention on the Law of Treaties states that treaties in force bind their parties and must be performed in good faith, and that a party generally may not invoke its internal law as justification for treaty non-performance. It separately addresses non-retroactivity and territorial scope.

Baobab SHALL distinguish:

```text
INTERNATIONAL OBLIGATION OF STATE
```

from:

```text
DIRECTLY APPLICABLE BUSINESS OBLIGATION
```

from:

```text
DOMESTIC IMPLEMENTING RULE.
```

Those layers may be related but are not interchangeable.

---

# 9. Core Separation

The following SHALL be architectural invariants:

```text
Country
    ≠
Jurisdiction

Jurisdiction
    ≠
Territory

Jurisdiction
    ≠
Regulatory Regime

Regulatory Regime
    ≠
Legal Hierarchy

Authority
    ≠
Competence

Authority Type
    ≠
Legal Rank

Treaty Membership
    ≠
Domestic Effect

Legal Hierarchy
    ≠
Source Preference

Court Hierarchy
    ≠
Instrument Hierarchy

Later Rule
    ≠
Automatically Superior Rule

More Specific Rule
    ≠
Automatically Superior Rule
```

---

# 10. Control Plane Jurisdiction Remains Canonical

Baobab Control Plane SHALL remain authoritative for canonical platform jurisdiction identity.

Regulations SHALL consume:

```text
jurisdiction_id
```

and attach regulatory semantics through:

```text
RegulatoryJurisdictionProfile.
```

Regulations SHALL NOT create a second canonical country/jurisdiction registry.

---

# 11. RegulatoryJurisdictionProfile

Conceptually:

```text
RegulatoryJurisdictionProfile
├── jurisdiction_ref
├── jurisdiction_kind
├── legal_system_metadata
├── territorial_scope
├── parent_jurisdiction_refs[]
├── child_jurisdiction_refs[]
├── applicable_regime_refs[]
├── authority_refs[]
├── hierarchy_policy_refs[]
├── judicial_structure_refs[]
├── treaty_implementation_profiles[]
├── regulatory_domains[]
├── valid_from
├── valid_to?
└── provenance
```

This is Regulations-owned enrichment.

---

# 12. Jurisdiction Kinds

Regulations SHOULD be capable of reasoning over jurisdictions such as:

```text
SOVEREIGN_STATE

PROVINCE / STATE

MUNICIPAL / LOCAL

CUSTOMS_TERRITORY

SPECIAL_ECONOMIC_ZONE

SUPRANATIONAL

OTHER LEGALLY RELEVANT TERRITORY
```

Actual canonical taxonomy SHALL remain governed with Control Plane.

---

# 13. Territory and Jurisdiction

A geographical territory does not necessarily correspond one-to-one with one regulatory jurisdiction.

Example:

```text
Durban
  │
  ├── municipal rules
  ├── KwaZulu-Natal context
  ├── South African national law
  ├── SACU customs environment
  ├── SADC trade arrangements
  └── AfCFTA where applicable
```

The location participates in several legal layers simultaneously.

---

# 14. Jurisdiction Roles

A regulatory context SHALL support **role-qualified jurisdictions**.

Conceptually:

```text
JurisdictionRole
├── jurisdiction_ref
├── role
└── provenance
```

Candidate roles include:

```text
INCORPORATION

ESTABLISHMENT

ORIGIN

EXPORT

IMPORT

DESTINATION

TRANSIT

PLACE_OF_SUPPLY

PLACE_OF_PROCESSING

DATA_SUBJECT_LOCATION

EMPLOYEE_LOCATION

ASSET_LOCATION

CONTRACT_PERFORMANCE

REGULATORY_AUTHORITY

DISPUTE_FORUM
```

The vocabulary SHALL be extensible.

---

# 15. Why Jurisdiction Roles Matter

For a shipment:

```text
Uganda
   ↓
Kenya transit
   ↓
South Africa
```

Baobab may need:

```text
UG  role=EXPORT

KE  role=TRANSIT

ZA  role=IMPORT + DESTINATION
```

Those roles may activate different rules.

---

# 16. No Single `jurisdiction_id` for Complex Assessments

A single:

```text
assessment.jurisdiction_id
```

SHALL NOT be sufficient for multi-jurisdiction regulatory evaluation.

Assessments MUST support several jurisdiction roles where the domain requires.

---

# 17. RegulatoryRegime

A `RegulatoryRegime` may span one or several jurisdictions.

Examples:

```text
AfCFTA

EAC

SACU

SADC trade regime

national customs regime

national food-safety regime.
```

A regime SHALL contain or reference its own applicability semantics.

---

# 18. Regime Membership

Baobab SHALL model membership as effective-dated relationship state.

Conceptually:

```text
RegimeMembership
├── regime_ref
├── jurisdiction_ref
├── member_state_ref?
├── membership_type
├── signed_at?
├── ratified_at?
├── entered_into_force_at?
├── provisional_application_from?
├── withdrawn_at?
├── suspended_at?
├── status
└── provenance
```

---

# 19. Membership Is Temporally Sensitive

An assessment on:

```text
2025-01-01
```

and:

```text
2028-01-01
```

may produce different regime applicability even for identical commercial facts.

Membership SHALL therefore never be timeless metadata.

---

# 20. TreatyLifecycle

The model SHALL be capable of representing:

```text
ADOPTED

SIGNED

RATIFIED

ACCEDED

PROVISIONALLY_APPLIED

ENTERED_INTO_FORCE

SUSPENDED

WITHDRAWAL_PENDING

WITHDRAWN

TERMINATED
```

where appropriate.

These states SHALL not all imply the same legal effect.

---

# 21. DomesticEffectProfile

For a treaty/regional instrument, Baobab SHALL support a jurisdiction-specific domestic-effect profile.

Conceptually:

```text
DomesticEffectProfile
├── regime_ref
├── jurisdiction_ref
├── constitutional_basis_refs[]
├── implementation_instrument_refs[]
├── effect_type
├── effective_from
├── effective_to?
├── subject_scope
├── limitations[]
├── verification_state
└── provenance
```

---

# 22. Domestic Effect Types

Possible conceptual states:

```text
INTERNATIONAL_ONLY

REQUIRES_IMPLEMENTATION

IMPLEMENTED_DOMESTICALLY

DIRECT_EFFECT_RECOGNISED

SELF_EXECUTING_WITH_CONDITIONS

PARTIALLY_IMPLEMENTED

UNCERTAIN

NOT_IN_FORCE
```

These SHALL be treated as jurisdiction-specific legal facts.

---

# 23. South African Example

The South African Constitution demonstrates why this object is necessary: parliamentary approval and domestic enactment are distinct matters, with a constitutional exception for qualifying self-executing provisions.

Baobab therefore needs to ask:

```text
Is the treaty binding internationally?

Has the necessary approval occurred?

Has domestic implementation occurred?

Is the relevant provision self-executing?

Is another constitutional/statutory limitation relevant?
```

rather than simply:

```text
Is South Africa a party?
```

---

# 24. Competence

`RegulatoryAuthority` identity alone SHALL NOT establish authority over every subject.

Baobab SHALL model **RegulatoryCompetence**.

Conceptually:

```text
RegulatoryCompetence
├── id
├── authority_ref
├── jurisdiction_scope[]
├── regime_scope[]
├── regulatory_domains[]
├── subject_scope[]
├── activity_scope[]
├── instrument_types_authorised[]
├── delegated_from?
├── legal_basis_refs[]
├── valid_from
├── valid_to?
├── limitations[]
└── provenance
```

---

# 25. Authority Is Not Competence

Example:

```text
SARS
```

may be a valid South African authority.

That does not mean it has authority to regulate:

```text
every food-safety standard
every employment rule
every data-protection issue.
```

Applicability must resolve competence.

---

# 26. Competence Is Contextual

An authority may have competence:

```text
nationally
```

for one domain and:

```text
only within a delegated function
```

for another.

Baobab SHALL therefore avoid:

```text
authority.rank = NATIONAL
```

as a proxy for legal competence.

---

# 27. Delegated Authority

Regulatory authority may be delegated.

The model SHALL support:

```text
DELEGATES_TO

DERIVES_AUTHORITY_FROM

EXERCISES_ON_BEHALF_OF

SUBDELEGATES_TO
```

with:

```text
legal basis

scope

validity

conditions.
```

---

# 28. Delegation Must Be Source-Backed

An authority relationship SHALL NOT be inferred because:

```text
Agency B usually handles this matter.
```

High-assurance competence should link to the enabling instrument or recognised authority source.

---

# 29. SACU Example of Institutional Allocation

The SACU architecture illustrates institutional allocation: its Tariff Board is provided for under the Agreement, while SACU currently states that ITAC handles tariff applications on an interim basis because the Tariff Board is not yet operational.

This is exactly why:

```text
formal institution
```

and:

```text
current exercising authority
```

must be separately representable.

---

# 30. AuthorityRelationship

Conceptually:

```text
AuthorityRelationship
├── source_authority_ref
├── target_authority_ref
├── relationship_type
├── legal_basis_refs[]
├── regulatory_domain_scope[]
├── jurisdiction_scope[]
├── valid_from
├── valid_to?
└── provenance
```

---

# 31. Authority Relationship Types

Potential types:

```text
DELEGATES_TO

SUPERVISES

APPEAL_FROM

APPEAL_TO

REVIEWS

IMPLEMENTS_DECISIONS_OF

REPORTS_TO

DESIGNATES

RECOGNISES

SUCCESSOR_TO

PREDECESSOR_OF
```

---

# 32. Institutional Hierarchy Is Not Instrument Hierarchy

A ministry supervising an agency does not automatically mean:

```text
all ministry publications override all agency decisions.
```

The source and legal basis must control.

---

# 33. LegalHierarchyPolicy

Baobab SHALL model legal hierarchy through governed, scope-specific policies.

Conceptually:

```text
LegalHierarchyPolicy
├── id
├── jurisdiction_ref?
├── regime_ref?
├── regulatory_domain?
├── subject_scope?
├── valid_from
├── valid_to?
├── precedence_rules[]
├── conflict_rules[]
├── source_refs[]
├── assurance_state
└── version
```

---

# 34. No Universal Global Policy

There SHALL NOT be one global:

```text
GLOBAL_LEGAL_HIERARCHY
```

controlling every jurisdiction.

Policies may share reusable concepts.

Their actual legal effect remains jurisdiction-specific.

---

# 35. PrecedenceRelationship

The domain SHALL support explicit rule/instrument relationships such as:

```text
HAS_PRECEDENCE_OVER

SUBORDINATE_TO

OVERRIDES

DISPLACES

PREVAILS_TO_EXTENT_OF_CONFLICT

PRESERVES_HIGHER_INTEGRATION

IMPLEMENTS

INCORPORATES

DERIVES_AUTHORITY_FROM

REQUIRES_DOMESTIC_IMPLEMENTATION
```

---

# 36. Precedence Can Be Partial

A higher rule may prevail only:

```text
for a particular subject matter

for a defined inconsistency

within a certain territory

for a defined class of persons

during a defined period.
```

Therefore:

```text
A > B
```

as an unconditional edge may be too crude.

---

# 37. Scoped Precedence

Conceptually:

```text
PrecedenceRelationship
├── higher_ref
├── lower_ref
├── relationship_type
├── jurisdiction_scope[]
├── regulatory_domain_scope[]
├── subject_scope[]
├── conflict_scope?
├── condition_expression?
├── valid_from
├── valid_to?
├── legal_basis_refs[]
└── provenance
```

---

# 38. AfCFTA as Model Example

AfCFTA Article 19 can be represented conceptually:

```text
AfCFTA Agreement
    PREVAILS_TO_EXTENT_OF_CONFLICT
Regional Agreement

EXCEPT WHEN

State Parties belong to
higher-integration REC / customs union
for relations among those members
```

That is substantially richer than:

```text
AfCFTA rank = 2.
```


---

# 39. EAC as Model Example

The EAC Treaty may be represented conceptually:

```text
EAC Community Law
    HAS_PRECEDENCE_OVER
similar national law

scope:
matters pertaining to implementation
of the EAC Treaty.
```


Likewise:

```text
EACJ interpretation/application decision
    HAS_PRECEDENCE_OVER
national court decision on similar matter
```

within the Treaty architecture.

---

# 40. Coexistence Is Not Conflict

Several applicable rules MAY coexist.

Example:

```text
AfCFTA:
rules of origin

South Africa:
import documentation

SPS regime:
phytosanitary certificate

SACU:
customs tariff architecture
```

Baobab SHALL NOT search for a "winner" unless there is actual inconsistency.

---

# 41. Cumulative Obligations

Where rules are compatible:

```text
Rule A requires document X

Rule B requires document Y
```

the result may simply be:

```text
require X + Y.
```

No hierarchy resolution is necessary.

---

# 42. Conflict

A legal conflict SHALL be identified only where complying with one relevant norm:

```text
prevents
contradicts
or legally displaces
```

another, or where the legal framework defines them as conflicting.

Similarity is not conflict.

---

# 43. Conflict Types

The model SHOULD distinguish:

```text
DIRECT_CONTRADICTION

INCONSISTENT_PERMISSION_PROHIBITION

DUPLICATIVE_REQUIREMENT

OVERLAPPING_SCOPE

TEMPORAL_CONFLICT

JURISDICTIONAL_CONFLICT

AUTHORITY_CONFLICT

INTERPRETATION_CONFLICT

IMPLEMENTATION_CONFLICT

APPARENT_CONFLICT
```

---

# 44. Apparent Conflict

Two rules may initially appear inconsistent but become compatible after resolving:

```text
scope

definitions

exceptions

time

regulated actor

territory.
```

The engine SHOULD resolve these dimensions before invoking hierarchy.

---

# 45. Conflict Resolution Pipeline

The canonical pipeline SHALL be:

```text
Candidate Rules
      │
      ▼
Temporal Validity
      │
      ▼
Jurisdiction Scope
      │
      ▼
Regime Applicability
      │
      ▼
Authority Competence
      │
      ▼
Subject / Activity Scope
      │
      ▼
Definitions
      │
      ▼
Conditions & Exceptions
      │
      ▼
Actual Conflict?
      │
   ┌──┴────────────┐
   │               │
   NO              YES
   │               │
   ▼               ▼
Cumulative     Explicit precedence?
application         │
                 ┌──┴─────┐
                 │        │
                YES       NO
                 │        │
                 ▼        ▼
              resolve   interpretive/
                         hierarchy rules
                            │
                     ┌──────┴──────┐
                     │             │
                  resolved      unresolved
                     │             │
                     ▼             ▼
                  apply       REVIEW_REQUIRED
```

---

# 46. Explicit Legal Text Beats Generic Heuristics

Where a treaty or statute expressly says:

```text
this provision prevails over...
```

that explicit relationship SHOULD ordinarily control before applying generic interpretive heuristics, subject to constitutional and jurisdiction-specific rules.

---

# 47. Interpretive Canons Are Not Universal Algorithms

Concepts often expressed as:

```text
lex superior

lex specialis

lex posterior
```

may be useful legal interpretive principles.

Baobab SHALL NOT hard-code them globally as:

```python
if conflict:
    choose higher_rank
    else choose more_specific
    else choose newer
```

Their applicability and ordering SHALL be jurisdiction-profile decisions.

---

# 48. Specificity

A more specific rule MAY prevail over a general rule in some legal contexts.

That SHALL be modelled as a policy/interpretive relationship where legally supported.

It SHALL not be assumed universally.

---

# 49. Later-in-Time Rules

A later instrument MAY amend, repeal or displace an earlier rule.

But:

```text
newer publication date
```

alone SHALL not prove:

```text
older rule repealed.
```

Baobab SHALL require:

```text
explicit amendment/repeal

recognised hierarchy rule

or verified interpretation.
```

---

# 50. Amendment Is Stronger Than Timestamp Guessing

If:

```text
Instrument B
    AMENDS
Instrument A
```

Baobab should use the amendment relationship.

It should not infer succession merely because B is newer.

---

# 51. Repeal

Explicit:

```text
REPEALS
```

relationships SHALL remove future applicability according to effective-date semantics.

Historical validity remains.

---

# 52. Implied Repeal

Where a jurisdiction recognises implied repeal or equivalent doctrine, Baobab SHALL treat it as an interpretation requiring legal support.

It SHALL NOT be automatic platform behaviour.

---

# 53. Constitutional Review

Where a competent court declares a law invalid, Baobab SHALL represent:

```text
court decision

affected rule/instrument

scope of invalidity

effective date

retrospective limitation, if any

suspension of invalidity, if any.
```

South Africa's Constitution, for example, authorises courts in constitutional matters to declare inconsistent law invalid and permits orders limiting retrospectivity or suspending invalidity.

This means:

```text
court says invalid
```

does not always imply:

```text
rule never existed at any historical moment.
```

---

# 54. JudicialAuthority

Regulations SHALL model courts and tribunals as regulatory/legal authorities where their decisions affect interpretation or validity.

---

# 55. Court Hierarchy

Court hierarchy SHALL be jurisdiction-specific.

South Africa's Constitution establishes its court structure and identifies the Constitutional Court as the highest court of the Republic.

Uganda's Judiciary identifies the Supreme Court as the highest court and final appellate court, followed by the Court of Appeal/Constitutional Court, High Court and subordinate courts.

These structures SHALL be modelled per jurisdiction rather than inferred from generic names such as:

```text
Supreme Court.
```

---

# 56. JudicialHierarchyProfile

Conceptually:

```text
JudicialHierarchyProfile
├── jurisdiction_ref
├── court_refs[]
├── appellate_relationships[]
├── precedent_rules[]
├── decision_scope_rules[]
├── constitutional_review_rules[]
├── valid_from
├── valid_to?
└── source_refs[]
```

---

# 57. Court Rank Does Not Fully Define Precedent

Baobab SHALL NOT assume:

```text
higher court
=
every statement binds all lower courts
```

without jurisdiction-specific precedent semantics.

The model must support:

```text
binding

persuasive

case-specific

overruled

distinguished

superseded
```

where required.

---

# 58. JudicialDecision

A judicial decision relevant to regulation SHOULD carry:

```text
court_ref

case_identifier

decision_date

jurisdiction

subject matter

affected instrument/provision refs

legal effect

precedential status

appeal status

effective implications

provenance.
```

---

# 59. Appeal Status

A lower-court decision subject to appeal MAY still have legal effect.

Baobab SHALL not automatically suppress it.

Its authority state should reflect:

```text
appeal pending

affirmed

reversed

varied

set aside.
```

---

# 60. Regulatory Authority versus Judicial Authority

A regulator interpretation and court interpretation may conflict.

Baobab SHALL NOT decide:

```text
regulator always wins
```

or:

```text
court always wins
```

through source type alone.

The jurisdiction's legal hierarchy and the decision's scope determine effect.

---

# 61. Competent Authority

Many regulatory instruments identify a:

```text
competent authority

designated authority

administering authority.
```

The AfCFTA Rules of Origin, for example, define designated competent authorities for Certificates of Origin and customs authorities responsible for customs law.

Baobab SHOULD preserve these legal roles explicitly.

---

# 62. AuthorityRole

An authority may participate as:

```text
ISSUER

ADMINISTRATOR

ENFORCER

INTERPRETER

APPELLATE_BODY

DESIGNATED_COMPETENT_AUTHORITY

LICENSING_AUTHORITY

CERTIFICATION_AUTHORITY

INSPECTION_AUTHORITY
```

for different regulatory objects.

---

# 63. Role Is Contextual

The same authority may be:

```text
ISSUER
```

for one instrument and:

```text
ADMINISTRATOR
```

for another.

The role SHALL therefore be relational.

---

# 64. Regime Interaction

Baobab SHALL support several regimes simultaneously.

For a UG → ZA commodity trade, potential regime context may include:

```text
Ugandan national export law

EAC-related origin/export context where applicable

AfCFTA

South African national customs/import law

SACU

SADC arrangements where applicable

WTO-derived domestic obligations/rules where relevant.
```

The applicability engine determines which actually matter.

---

# 65. Regime Membership Does Not Mean Transaction Qualification

Even if both jurisdictions participate in a regime:

```text
membership
```

does not necessarily mean:

```text
transaction qualifies for preference.
```

Product origin, tariff schedule, rules of origin, proof and other conditions may still have to be satisfied.

---

# 66. AfCFTA Example

AfCFTA's Rules of Origin determine when products qualify as originating and require prescribed proof for preferential treatment.

Therefore:

```text
UG is AfCFTA State Party
+
ZA is AfCFTA State Party
```

does not alone establish:

```text
preferential tariff applies.
```

Baobab must evaluate the actual originating criteria and evidence.

---

# 67. Higher Integration Relationship

A regime SHALL support:

```text
HIGHER_INTEGRATION_THAN
```

or equivalent scoped relationship.

This is necessary to model AfCFTA Article 19 correctly.

---

# 68. Customs Union Is Not Ordinary FTA

Baobab SHALL model:

```text
CUSTOMS_UNION
```

distinctly from:

```text
FREE_TRADE_AREA.
```

A customs union may involve common external tariff architecture and deeper integration.

SACU, for example, operates a common customs area with a common external tariff framework.

---

# 69. RegimeRelationship

Conceptually:

```text
RegimeRelationship
├── source_regime_ref
├── target_regime_ref
├── relationship_type
├── member_scope[]
├── regulatory_domain_scope[]
├── subject_scope[]
├── valid_from
├── valid_to?
├── legal_basis_refs[]
└── provenance
```

---

# 70. Regime Relationship Types

Potential:

```text
SUPERSEDES

COMPLEMENTS

IMPLEMENTS

HIGHER_INTEGRATION_THAN

PREVAILS_OVER_TO_EXTENT_OF_CONFLICT

COEXISTS_WITH

INCORPORATES

DEPENDS_ON

CARVES_OUT
```

---

# 71. Conflict of Laws Is Broader Than Legal Hierarchy

Some matters involve choosing between laws from different jurisdictions rather than ranking instruments within one hierarchy.

Examples:

```text
cross-border contracts

data transfers

employment

consumer transactions

corporate matters.
```

This ADR SHALL provide the structural model.

Detailed private-international-law choice-of-law engines are out of scope initially.

---

# 72. GoverningLawFact

Where contractually relevant, RegulatoryContext MAY carry:

```text
governing_law_ref

forum_ref

choice_of_law_clause_ref
```

as facts.

These do not automatically determine all mandatory regulatory obligations.

---

# 73. Mandatory Law May Still Apply

The presence of:

```text
contract governing law = X
```

SHALL NOT cause Baobab to discard:

```text
mandatory law of jurisdiction Y
```

where legally applicable.

---

# 74. ConflictOfLawsPolicy

Future regulatory domains MAY define:

```text
ConflictOfLawsPolicy
```

for legally recognised choice-of-law analysis.

It SHALL be separate from ordinary instrument hierarchy.

---

# 75. Jurisdiction Applicability Graph

An assessment SHOULD conceptually build:

```text
                   TRANSACTION
                        │
         ┌──────────────┼───────────────┐
         ▼              ▼               ▼
      origin         transit        destination
         │              │               │
         ▼              ▼               ▼
    jurisdiction    jurisdiction     jurisdiction
         │              │               │
         └──────────────┼───────────────┘
                        ▼
                 applicable regimes
                        │
                        ▼
               competent authorities
                        │
                        ▼
              candidate instruments
                        │
                        ▼
                 candidate rules
```

---

# 76. Jurisdiction Resolution Is Evidence-Backed

Baobab SHALL preserve why a jurisdiction entered an assessment.

Example:

```text
ZA included because:
destination = ZA

UG included because:
exporting legal entity + origin = UG

KE included because:
transit route includes KE
```

---

# 77. No Jurisdiction by IP Address Alone

A user's network location SHALL NOT automatically determine legal jurisdiction.

IP-derived geography may be one contextual signal for appropriate domains.

It is not universal legal truth.

---

# 78. No Jurisdiction by Currency

Transaction currency does not establish jurisdiction.

```text
USD
```

does not imply:

```text
United States law applies.
```

---

# 79. No Jurisdiction by Digital Estate

A ZuriBeans South Africa storefront does not, by itself, establish every applicable legal rule.

---

# 80. No Jurisdiction by Incorporation Alone

A Ugandan-incorporated company trading into South Africa may become subject to South African import/product rules despite Ugandan incorporation.

---

# 81. No Jurisdiction by Market Alone

This preserves BCP-004:

```text
Market
≠
Jurisdiction.
```

---

# 82. LegalHierarchyRule

A precedence policy SHALL be composed of explicit `LegalHierarchyRule` objects or equivalent.

Conceptually:

```text
LegalHierarchyRule
├── id
├── jurisdiction/regime_scope
├── regulatory_domain_scope
├── candidate_type_a
├── candidate_type_b
├── relationship
├── conditions
├── exception_conditions[]
├── legal_basis_refs[]
├── interpretation_ref?
├── assurance_state
├── effective_from
├── effective_to?
└── version
```

---

# 83. Hierarchy Rule Example

Conceptually:

```text
IF
    regime = EAC
AND
    matter pertains to implementation of Treaty
AND
    candidate A = applicable Community law
AND
    candidate B = similar national measure
THEN
    A has precedence
```

with the Treaty provision as legal basis.

---

# 84. AfCFTA Hierarchy Rule Example

```text
IF
    AfCFTA conflicts with regional agreement
THEN
    AfCFTA prevails to extent of inconsistency

EXCEPT
    qualifying higher-integration arrangements
    among their members.
```


---

# 85. No Plain Numeric Rank as Canonical Model

A numeric rank MAY be used internally as an optimisation **after** legal relationships are resolved.

It SHALL NOT become the canonical legal-semantic representation.

---

# 86. ConflictResolutionResult

Conceptually:

```text
ConflictResolutionResult
├── conflict_refs[]
├── candidate_rule_refs[]
├── controlling_rule_refs[]
├── displaced_rule_refs[]
├── cumulative_rule_refs[]
├── resolution_basis
├── hierarchy_policy_version
├── interpretation_refs[]
├── unresolved_questions[]
├── outcome
└── provenance
```

---

# 87. Resolution Outcomes

Canonical outcomes SHOULD support:

```text
NO_CONFLICT

CUMULATIVE_APPLICATION

RULE_A_CONTROLS

RULE_B_CONTROLS

PARTIAL_DISPLACEMENT

TEMPORAL_DISPLACEMENT

CONTEXT_SPECIFIC_EXCEPTION

UNRESOLVED
```

---

# 88. Unresolved Is Valid

Where legal hierarchy cannot be determined reliably:

```text
UNRESOLVED
```

SHALL propagate toward:

```text
REVIEW_REQUIRED
```

under ADR-REG-0004.

The engine SHALL NOT fabricate precedence.

---

# 89. Hierarchy Assurance

Hierarchy relationships SHALL themselves carry assurance.

A hierarchy rule based on:

```text
explicit constitutional provision
```

may have stronger assurance than one based upon:

```text
Baobab legal interpretation.
```

---

# 90. Hierarchy Provenance

Every consequential precedence determination SHOULD answer:

> Why did Rule A prevail over Rule B?

with:

```text
legal basis

jurisdiction profile

regime relationship

instrument relationship

judicial interpretation

effective date.
```

---

# 91. Judicial Interpretation Can Alter Hierarchy Behaviour

A competent court may determine how two instruments interact.

Such interpretation SHALL be capable of modifying:

```text
LegalHierarchyPolicy
```

through governed versioning.

---

# 92. Hierarchy Policy Must Be Temporal

The legal structure itself may change.

Examples:

```text
constitutional amendment

court reorganisation

treaty accession

withdrawal

new regional protocol

agency restructuring.
```

Therefore hierarchy policy SHALL be effective-dated.

---

# 93. Historical Reconstruction

A 2032 assessment of a 2027 transaction must use:

```text
2027 jurisdiction topology

2027 regime memberships

2027 authority competence

2027 legal hierarchy

2027 applicable case law
```

not current 2032 structure.

---

# 94. Knowledge Time

Baobab also needs to distinguish:

```text
what hierarchy legally existed
```

from:

```text
what Baobab knew about it at the time.
```

Detailed bitemporal semantics remain under ADR-REG-0015.

---

# 95. Authority Reorganisation

If:

```text
Authority A
     ↓
abolished
     ↓
Authority B succeeds it
```

historical instruments remain attributed to A.

B may become the administering authority prospectively.

---

# 96. Successor Authority Does Not Rewrite History

Rejected:

```text
UPDATE all old instruments
SET authority = B.
```

Use explicit succession relationships.

---

# 97. Competence Transfer

A transfer of regulatory competence SHALL create effective-dated relationships.

Example:

```text
A competent until 2027-06-30

B competent from 2027-07-01.
```

---

# 98. Legal Personality and Institutional Identity

A regional body may have its own legal personality and institutions.

SACU's 2002 Agreement, for example, established a modern institutional architecture and legal personality for the organisation.

Baobab SHALL therefore be able to represent:

```text
regional organisation
    as authority/institution
```

separately from its Member States.

---

# 99. State Party

The model SHOULD distinguish:

```text
RegulatoryAuthority

StateParty

Jurisdiction.
```

A State may be party to a treaty without being the authority issuing every implementing instrument.

---

# 100. RegimePartyRelationship

Conceptually:

```text
RegimePartyRelationship
├── regime_ref
├── organisation/jurisdiction_ref
├── party_role
├── treaty_status
├── effective_dates
└── provenance
```

---

# 101. International Obligation Effects

A treaty provision may impose an obligation primarily upon:

```text
State Party
```

rather than directly upon:

```text
private company.
```

Baobab SHALL represent the bearer accurately.

---

# 102. No Automatic Private-Sector Obligation

The engine SHALL NOT transform:

> "State Parties shall establish..."

into:

> "ZuriBeans must..."

without identifying the domestic rule or other mechanism creating the company-level obligation.

---

# 103. Implementation Chain

Preferred model:

```text
Treaty Obligation
      │
      ▼
State Party
      │
      ▼
Domestic Implementing Instrument
      │
      ▼
Regulatory Provision
      │
      ▼
Rule affecting private actor.
```

---

# 104. Direct Effect Exception

Where the legal framework genuinely grants direct effect:

```text
Treaty / regional provision
      │
      ▼
private actor
```

Baobab may model that explicitly.

It SHALL not infer it globally.

---

# 105. Regime Instrument Structure

A regime MAY contain:

```text
founding treaty

protocols

annexes

appendices

decisions

regulations

directives

manuals

guidelines

tariff schedules

member-state implementing law.
```

These are not necessarily equal in legal force.

---

# 106. AfCFTA Structure

The AfCFTA Agreement states that its Protocols, Annexes and Appendices form integral parts of the Agreement subject to the applicable entry-into-force framework.

Baobab SHOULD model:

```text
Agreement
   │
   ├── Protocol
   │     └── Annex
   │          └── Appendix
```

with explicit legal relationships rather than treating each PDF as unrelated regulation.

---

# 107. Guidance versus Binding Instrument

A rules manual explaining an annex MAY be important operationally without necessarily having exactly the same normative force as the underlying treaty provision.

The AfCFTA Rules of Origin Manual describes itself as providing guidance for operationalisation and uniform understanding of the Rules of Origin regime.

Therefore source type and legal force SHALL remain explicit.

---

# 108. Implementing Decisions

Regional councils, committees or authorities may issue:

```text
decisions

directives

implementing regulations

guidelines.
```

Their binding status SHALL be derived from the relevant constitutive legal framework.

---

# 109. Decision-Making Authority

AfCFTA's current institutional description notes, for example, that decisions of the Council of Ministers are binding on State Parties, subject to specified treatment where decisions have legal, structural or financial implications.

This reinforces the need for:

```text
AuthorityCompetence
+
InstrumentLegalForce
```

rather than generic document classes.

---

# 110. LegalForceProfile

Each material instrument/expression SHOULD be capable of carrying a `LegalForceProfile`.

Conceptually:

```text
LegalForceProfile
├── instrument_ref
├── jurisdiction/regime_scope
├── force_type
├── binding_on[]
├── direct_effect_state
├── implementation_state
├── commencement_state
├── limitations[]
├── effective_dates
├── legal_basis_refs[]
└── verification_state
```

---

# 111. Force Types

Potential categories:

```text
CONSTITUTIONAL

PRIMARY_LEGISLATION

DELEGATED_LEGISLATION

REGULATION

BINDING_DECISION

JUDICIAL_DECISION

TREATY_OBLIGATION

REGIONAL_RULE

GUIDANCE

INTERPRETIVE

PROCEDURAL

NON_BINDING

UNKNOWN
```

These are descriptive categories.

They SHALL NOT themselves define universal rank.

---

# 112. `UNKNOWN` Is Necessary

Where Baobab does not yet know the legal force of a source:

```text
UNKNOWN
```

is correct.

Guessing from document title is not.

---

# 113. Competence Validation Before Rule Promotion

No rule should become high-assurance merely because the text is authentic.

Baobab SHOULD establish:

```text
issuer authentic

issuer competent

instrument legally valid

instrument in force

rule within competence.
```

---

# 114. Ultra Vires / Validity Questions

Where a source's validity is disputed:

```text
VALIDITY_DISPUTED
```

SHOULD be representable.

Baobab SHALL not independently adjudicate complex validity questions beyond supported authority.

---

# 115. Constitutional Supremacy

Where a jurisdiction's constitutional structure establishes constitutional supremacy, this SHALL be encoded in that jurisdiction's hierarchy policy.

It SHALL not be assumed for every legal system.

---

# 116. Subnational Law

A national rule and provincial/local rule may coexist.

Baobab must represent:

```text
territorial scope

delegated competence

subject matter

pre-emption/override relationship
```

where applicable.

---

# 117. Municipal Rules

A municipal requirement SHALL not automatically apply to an entire national market.

Context must resolve the relevant locality.

---

# 118. Special Zones

Special Economic Zones may introduce distinct fiscal/customs/regulatory treatment within national territory.

AfCFTA's Rules of Origin framework itself recognises special economic arrangements/zones as geographically demarcated areas where legal, fiscal and customs regimes may differ from the rest of the State Party's territory.

Baobab therefore SHALL support zone-specific regulatory context.

---

# 119. RegulatoryZone

Conceptually:

```text
RegulatoryZone
├── zone_id
├── jurisdiction_ref
├── geography_ref
├── regime_refs[]
├── special_rule_refs[]
├── valid_from
├── valid_to?
└── provenance
```

This need not be a separate aggregate if Control Plane already provides an adequate canonical geography object.

---

# 120. Trade Lane Does Not Determine Regime Automatically

BCP-011 provides the canonical Trade Lane.

Regulations SHALL consume:

```text
origin

destination

transit

market participation.
```

It SHALL then determine applicable regimes.

The Trade Lane SHALL NOT hard-code:

```text
regime = AfCFTA.
```

---

# 121. Preferred Regime Is Not Applicable Regime

A commercial actor may wish to claim AfCFTA preference.

That is a:

```text
requested treatment
```

not proof of eligibility.

---

# 122. Requested Regulatory Treatment

RegulatoryContext MAY include:

```text
requested_trade_regime = AfCFTA
```

or equivalent.

The engine then determines whether that treatment is available.

---

# 123. Alternative Regimes

A transaction may potentially qualify under:

```text
Regime A

Regime B

MFN/default treatment.
```

Regulations MAY evaluate alternatives.

It SHALL not automatically select the economically cheapest regime unless the business workflow explicitly requests optimisation and legal qualification is established.

---

# 124. Regulatory Applicability versus Commercial Optimisation

Baobab Regulations determines:

```text
legally available treatments.
```

Pulse/Trade may later determine:

```text
commercially preferred treatment.
```

---

# 125. Rules of Origin Interaction

Preferential treatment may depend on:

```text
origin criteria

certificate

exporter status

product classification

shipment conditions.
```

The AfCFTA Rules of Origin contain detailed originating criteria and proof requirements.

These belong to applicability/evaluation, not regime membership alone.

---

# 126. Conflict Graph

The logical knowledge graph SHALL support:

```text
Rule A
   │
   ├── conflicts_with → Rule B
   ├── displaced_by → Rule C
   ├── excepted_by → Rule D
   └── interpreted_by → Decision E
```

with scope and provenance on the edges.

---

# 127. Conflict Edge Is Not Permanent Truth

A conflict may exist only:

```text
during a certain period

for one product class

for one jurisdiction

for one interpretation.
```

Edges SHALL therefore be effective-dated where needed.

---

# 128. ConflictDetectionResult

Automated conflict detection MAY produce:

```text
POTENTIAL_CONFLICT
```

from semantic or rule comparison.

Only governed verification may promote:

```text
VERIFIED_LEGAL_CONFLICT
```

where legal interpretation is involved.

---

# 129. AI Role

AI MAY:

```text
detect possible conflicts

identify competing provisions

extract authority relationships

suggest hierarchy mappings

compare amendments.
```

It SHALL NOT unilaterally determine:

```text
Rule A legally overrides Rule B
```

for consequential enforcement unless the relationship is otherwise verified.

---

# 130. Human Review

Complex hierarchy questions may require:

```text
regulatory analyst

local counsel

customs expert

tax specialist

authority ruling.
```

The review should create a versioned interpretation/hierarchy decision, not a one-off comment buried in a ticket.

---

# 131. Hierarchy Interpretation

Where precedence is not explicit, Baobab SHOULD create:

```text
RegulatoryInterpretation
```

covering the hierarchy question.

That interpretation becomes provenance for `LegalHierarchyRule`.

---

# 132. Tenant Counsel

A tenant may hold a counsel opinion on hierarchy/applicability.

It SHALL remain tenant-scoped unless independently promoted.

---

# 133. Platform Default

Baobab MAY maintain a platform-default hierarchy interpretation.

It SHALL be labelled as Baobab interpretation rather than authority-issued law.

---

# 134. Court Decision as Stronger Authority

Where an applicable competent court has resolved the same legal question, the hierarchy profile SHALL be capable of incorporating that decision according to jurisdiction-specific precedent rules.

---

# 135. No AI Reversal of Court Authority

A model's alternative interpretation SHALL not override a verified controlling judicial determination.

---

# 136. LegalHierarchyDecision

For difficult cases, Baobab MAY persist a:

```text
LegalHierarchyDecision
```

conceptually:

```text
LegalHierarchyDecision
├── id
├── candidate_refs[]
├── context_scope
├── resolved_controlling_refs[]
├── displaced_refs[]
├── cumulative_refs[]
├── basis_refs[]
├── interpretation_refs[]
├── reviewer_refs[]
├── effective_from
├── effective_to?
├── assurance
└── provenance
```

Whether this becomes its own aggregate root is deferred.

---

# 137. Hierarchy Decision Is Reusable Only Within Scope

A hierarchy decision for:

```text
ZA customs classification context
```

SHALL not automatically resolve:

```text
ZA employment law.
```

---

# 138. Cache Key Implications

Hierarchy/applicability caching MUST include material dimensions such as:

```text
jurisdictions

regimes

effective time

regulatory domain

rule-set version

hierarchy-policy version.
```

---

# 139. Regulatory Decision Replay

Historical replay MUST preserve:

```text
jurisdiction profile version

regime membership state

authority competence version

hierarchy-policy version

judicial authority state.
```

Otherwise the decision cannot be reproduced faithfully.

---

# 140. Change Detection

Changes to any of these SHALL potentially trigger regulatory impact analysis:

```text
regime membership

treaty entry into force

domestic implementation

authority competence

delegation

court ruling

instrument hierarchy

conflict relationship

jurisdiction boundary.
```

---

# 141. Hierarchy Change Event

Potential event:

```text
regulation.hierarchy.changed
```

may identify:

```text
affected jurisdictions

affected regimes

affected domains

affected rules

effective time.
```

Final event vocabulary belongs in Shared.

---

# 142. Authority Competence Event

Potential:

```text
regulation.authority.competence.changed
```

could trigger reassessment of source/rule authority.

---

# 143. Regime Membership Event

Potential:

```text
regulation.regime.membership.changed
```

could affect:

```text
trade preferences

rules of origin

applicable protocols.
```

---

# 144. Domestic Effect Event

Potential:

```text
regulation.regime.domestic-effect.changed
```

may occur when implementing legislation enters into force.

---

# 145. Regulatory Readiness

A jurisdiction pack SHALL NOT be considered fully ready merely because sources are ingested.

It also requires adequate:

```text
authority mappings

competence mappings

regime memberships

domestic-effect mappings

hierarchy rules

conflict policy

temporal state.
```

---

# 146. Coverage Dimension — Legal Topology

Coverage SHALL therefore include a dimension such as:

```text
LEGAL_TOPOLOGY_COMPLETE

LEGAL_TOPOLOGY_PARTIAL

LEGAL_TOPOLOGY_UNKNOWN.
```

---

# 147. Partial Topology Caps Enforcement

A rule may be well parsed and individually verified, but if its relationship to another applicable rule is unresolved:

```text
E4
```

may be unsafe.

Effect authority SHALL be downgradable under ADR-REG-0004.

---

# 148. Hierarchy Failure Is Not No Rule

If Baobab cannot resolve which of two rules controls:

```text
INDETERMINATE / REVIEW_REQUIRED
```

is appropriate.

Not:

```text
use first result.
```

---

# 149. Source Priority Is Operational Only

Example source preference:

```text
Official Gazette
    preferred over
Commercial mirror
```

means:

```text
preferred acquisition/evidence source.
```

It does not automatically mean the Gazette's every document has higher legal force than every court ruling or treaty.

---

# 150. Search Rank Is Irrelevant to Hierarchy

Google result #1 has no legal precedence.

Vector similarity has no legal precedence.

Provider confidence has no legal precedence.

---

# 151. Instrument Title Is Not Hierarchy

A document called:

```text
Regulation
```

is not automatically lower/higher than another source based solely on the English noun.

The enabling legal framework determines its status.

---

# 152. Authority Name Is Not Hierarchy

A source issued by:

```text
Minister
```

does not automatically outrank:

```text
Commission
```

or vice versa.

Competence and legal basis control.

---

# 153. Practical Initial Scope

The first implemented hierarchy profiles SHOULD focus narrowly on what the ZuriBeans UG → ZA trade corridor actually requires.

Initial domains:

```text
customs

tariffs

trade controls

rules of origin

SPS

food/agricultural controls

import/export documentation.
```

---

# 154. Initial Uganda Profile

The Uganda profile SHOULD establish at minimum:

```text
national jurisdiction

constitutional/treaty implementation context

relevant export/customs authorities

commodity regulatory authorities

EAC relationships

AfCFTA relationships

relevant national implementing instruments.
```

---

# 155. Initial South Africa Profile

The South African profile SHOULD establish at minimum:

```text
national legal hierarchy

constitutional treaty-effect rules

SARS customs authority

ITAC trade-control authority

relevant agricultural/SPS authorities

SACU

SADC

AfCFTA

relevant implementing instruments.
```

---

# 156. Initial Regional Profiles

At minimum:

```text
EAC

SACU

SADC Trade

AfCFTA
```

should have explicit regime identities and relationships where relevant to the corridor.

---

# 157. Initial AfCFTA Relationship

The implementation SHALL model Article 19 rather than merely storing it as text.

This should become a golden legal-topology case.

---

# 158. Initial EAC Relationship

Article 8(4)/(5) and Article 33 should similarly become golden topology cases for Uganda/EAC architecture.

---

# 159. Initial South African Treaty Case

Section 231 of the Constitution SHALL become a golden case proving:

```text
international obligation
≠
domestic enforceability
```

as a simplistic universal equivalence.

---

# 160. Initial SACU Case

The implementation SHOULD demonstrate:

```text
SACU common customs framework
+
South African national implementation/control
```

coexisting within one assessment rather than being treated as competing duplicate law.

---

# 161. Minimum Domain Proof

Implementation of this ADR SHOULD demonstrate all of the following:

```text
1. One transaction resolves multiple jurisdiction roles.

2. One jurisdiction participates in several regulatory regimes.

3. Regime membership is effective-dated.

4. Treaty signature and domestic effect are represented separately.

5. One authority has domain-scoped competence.

6. Delegated competence is source-backed.

7. One formal authority differs from current exercising authority.

8. Explicit precedence edge resolves a rule conflict.

9. Two compatible rules apply cumulatively.

10. An apparent conflict disappears after scope resolution.

11. AfCFTA Article 19 higher-integration exception is represented.

12. EAC regional precedence is represented.

13. South African treaty domestic-effect state is represented.

14. Court hierarchy is jurisdiction-specific.

15. A judicial decision changes an interpretation without rewriting source law.

16. An unresolved hierarchy dispute produces REVIEW_REQUIRED.

17. Historical assessment replays using historical hierarchy state.

18. Source preference does not alter legal hierarchy.

19. A tenant counsel interpretation remains tenant-scoped.

20. No numeric universal hierarchy is needed to evaluate the cases.
```

---

# 162. Golden Topology Test — AfCFTA / REC

```text
GIVEN

Regime A:
AfCFTA

Regime B:
qualifying REC/customs union

State Parties:
members of both

Relationship:
Regime B has higher integration
among those members

WHEN

a specific inconsistency is evaluated

THEN

engine must evaluate
AfCFTA Article 19 exception semantics

NOT

blindly select AfCFTA because:
"continental > regional".
```

---

# 163. Golden Topology Test — EAC

```text
GIVEN

EAC Community rule

National rule

Matter:
Treaty implementation

WHEN

verified conflict exists

THEN

EAC precedence relationship
is considered

BECAUSE

the Treaty explicitly establishes it.
```

---

# 164. Golden Topology Test — South African Treaty

```text
GIVEN

international agreement provision

South African transaction

WHEN

domestic effect is assessed

THEN

engine must consider
constitutional approval /
enactment / qualifying
self-executing status

NOT

party-to-treaty = direct business rule.
```

---

# 165. Golden Topology Test — Cumulative Regulation

```text
UG export certificate
+
ZA import permit
+
AfCFTA origin proof

DO NOT conflict.

Result:
all applicable obligations accumulate.
```

---

# 166. Golden Topology Test — Unresolved Conflict

```text
Authority interpretation A

Court decision B

precedential status unresolved

Result:
REVIEW_REQUIRED

NOT:
take newer document.
```

---

# 167. Architecture Invariants

| ID | Invariant |
|---|---|
| `REG-H-I01` | No universal global legal-precedence ladder SHALL exist |
| `REG-H-I02` | Jurisdiction SHALL remain distinct from RegulatoryRegime |
| `REG-H-I03` | Market SHALL remain distinct from Jurisdiction |
| `REG-H-I04` | Assessments SHALL support multiple jurisdiction roles |
| `REG-H-I05` | Regulatory authority SHALL remain distinct from regulatory competence |
| `REG-H-I06` | Authority type SHALL not imply universal legal rank |
| `REG-H-I07` | Regime membership SHALL be effective-dated |
| `REG-H-I08` | Treaty membership SHALL remain distinct from domestic legal effect |
| `REG-H-I09` | International State obligations SHALL not automatically become private-actor obligations |
| `REG-H-I10` | Delegated authority SHALL be scope- and source-backed |
| `REG-H-I11` | Legal hierarchy SHALL remain distinct from source preference |
| `REG-H-I12` | Court hierarchy SHALL be jurisdiction-specific |
| `REG-H-I13` | Judicial precedence semantics SHALL be jurisdiction-specific |
| `REG-H-I14` | Explicit legal precedence relationships SHALL be preferred over generic heuristics |
| `REG-H-I15` | Lex superior/specialis/posterior concepts SHALL not be globally hard-coded |
| `REG-H-I16` | Newer publication SHALL not automatically repeal older law |
| `REG-H-I17` | Several applicable rules MAY operate cumulatively |
| `REG-H-I18` | Conflict resolution SHALL occur only after scope/applicability analysis |
| `REG-H-I19` | An unresolved conflict SHALL remain explicit |
| `REG-H-I20` | Unresolved hierarchy SHALL not produce E4 automated enforcement |
| `REG-H-I21` | Precedence relationships SHALL support limited/scoped effect |
| `REG-H-I22` | Regime interactions SHALL be represented explicitly |
| `REG-H-I23` | Higher regional integration SHALL be modelable |
| `REG-H-I24` | Domestic implementing legislation SHALL remain linked to its international/regional source |
| `REG-H-I25` | Legal topology SHALL be temporally reconstructable |
| `REG-H-I26` | Authority succession SHALL not rewrite historical attribution |
| `REG-H-I27` | Competence transfers SHALL be effective-dated |
| `REG-H-I28` | A court ruling SHALL not overwrite historical legislation |
| `REG-H-I29` | Source/provider ranking SHALL never substitute for legal hierarchy |
| `REG-H-I30` | AI SHALL not unilaterally establish consequential hierarchy relationships |

---

# 168. Rejected Alternative — One Global Hierarchy Table

Rejected:

```text
constitution = 100
treaty = 90
statute = 80
regulation = 70
guidance = 20
```

because actual legal relationships are jurisdiction-specific and sometimes conditional.

---

# 169. Rejected Alternative — Continental Always Beats Regional

Rejected by the actual AfCFTA conflict architecture, which preserves qualifying higher levels of regional integration.

---

# 170. Rejected Alternative — Regional Always Beats National

Rejected.

EAC provides explicit precedence for defined Treaty matters, but that cannot be generalised to every regional institution.

---

# 171. Rejected Alternative — Treaty Party Means Direct Domestic Rule

Rejected.

South African constitutional architecture alone demonstrates why this is unsafe.

---

# 172. Rejected Alternative — Newer Rule Wins

Rejected.

Recency without legal amendment/repeal/precedence semantics is insufficient.

---

# 173. Rejected Alternative — Specific Rule Always Wins

Rejected.

Specificity may matter under relevant legal doctrine but is not a universal machine rule.

---

# 174. Rejected Alternative — Higher Court Name Means Binding

Rejected.

Precedential effect must come from the jurisdiction's judicial model.

---

# 175. Rejected Alternative — One Country per Assessment

Rejected.

Cross-border trade inherently involves several jurisdiction roles.

---

# 176. Rejected Alternative — Trade Lane Determines Regulation

Rejected.

Trade Lane is commercial/platform context.

Regulations resolves the legal topology.

---

# 177. Rejected Alternative — Regime Membership Determines Preference

Rejected.

Rules of origin and evidence still need evaluation.

---

# 178. Rejected Alternative — Search/AI Determines Controlling Law

Rejected.

Retrieval identifies candidates.

Verified legal topology determines authority.

---

# 179. Consequences — Positive

This architecture enables:

```text
credible multi-jurisdiction assessments

treaty-aware reasoning

regional integration modelling

historical legal reconstruction

court/regulator interaction

source-backed precedence

explicit unresolved conflicts

safe applicability evaluation

reliable African corridor expansion.
```

---

# 180. Consequences — Strategic

This is a particularly important differentiator for Baobab.

A regulatory chatbot can retrieve:

```text
10 apparently relevant rules.
```

Baobab's intended capability is stronger:

```text
10 candidate rules
       │
       ▼
3 not temporally valid
       │
       ▼
2 outside competence
       │
       ▼
1 not applicable to this actor
       │
       ▼
4 remain
       │
       ├── 3 cumulative
       └── 1 displaced by explicit precedence
       │
       ▼
Operational regulatory position.
```

That is much closer to true regulatory infrastructure.

---

# 181. Consequences — Commercial

The model enables trustworthy:

```text
Jurisdiction Packs

Regional Regime Packs

Trade Corridor Packs

Treaty Qualification Services

Cross-Border Assessments

Regulatory Change Impact
```

without encoding regional relationships manually into every customer workflow.

---

# 182. Consequences — Cost

Legal-topology curation is expensive.

Baobab will need:

```text
local legal research

authority mapping

treaty mapping

case-law monitoring

temporal maintenance

specialist review.
```

That cost is accepted.

A cheap but legally naïve hierarchy engine would undermine the entire product.

---

# 183. Consequences — Coverage Honesty

Baobab may know the substantive rule but lack adequate hierarchy coverage.

In such a case the system must say:

```text
PARTIAL / REVIEW_REQUIRED
```

rather than pretending the model is complete.

---

# 184. Relationship to ADR-REG-0008

`ADR-REG-0008` SHALL now deepen:

```text
Instrument

Provision

Rule

Obligation
```

using the authority and hierarchy model established here.

It will determine exactly how:

```text
one or more provisions
       ↓
produce
       ↓
machine rules
       ↓
which create
       ↓
contextual obligations.
```

---

# 185. Relationship to ADR-REG-0009

`ADR-REG-0009` SHALL define the detailed semantics of:

```text
obligation

permission

prohibition

exemption

exception

discretion

defeasibility.
```

The hierarchy graph created here will provide the rule-priority mechanism those semantics require.

---

# 186. Relationship to ADR-REG-0010

`ADR-REG-0010` SHALL formalise the Regulatory Knowledge Graph.

Among its most important edge types will be those introduced here:

```text
MEMBER_OF_REGIME

DELEGATES_TO

DERIVES_AUTHORITY_FROM

HAS_PRECEDENCE_OVER

PREVAILS_TO_EXTENT_OF_CONFLICT

HIGHER_INTEGRATION_THAN

IMPLEMENTS

AMENDS

REPEALS

INTERPRETS

OVERRULES

SUPERSEDES.
```

---

# 187. Research Foundation

This ADR is grounded in actual differences among the legal environments Baobab initially expects to serve.

South Africa's Constitution expressly distinguishes the international binding status and domestic legal effect of international agreements and requires courts to prefer reasonable legislation interpretations consistent with international law where possible.

Uganda's Constitution provides a distinct constitutional framework for treaty-making and parliamentary governance of ratification.

The EAC Treaty expressly grants Community organs, institutions and laws precedence over similar national ones for Treaty implementation and provides precedence for EACJ Treaty interpretation over national decisions on similar matters.

The AfCFTA Agreement contains its own explicit conflict rule while preserving higher integration achieved among members of qualifying RECs, trading arrangements and customs unions.

SACU demonstrates the interaction between regional customs-union rules and national implementation, including common external tariff architecture and continuing national regulatory roles.

SADC's Trade Protocol provides yet another layer of regional trade rules covering liberalisation, customs cooperation, rules of origin, documentation, transit and related matters.

The Vienna Convention supplies foundational treaty-law principles concerning treaty observance, internal law, non-retroactivity and territorial scope, but Baobab SHALL still evaluate their relevance according to the States and legal regimes involved rather than turning them into a simplistic business-rule hierarchy.

---

# 188. Final Decision

Baobab Regulations SHALL implement legal authority as a **temporal, scoped and provenance-backed topology**, not a flat ranking.

The target architecture is:

```text
                     BUSINESS CONTEXT
                           │
                           ▼
                  Jurisdiction Roles
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
       Origin           Transit        Destination
          │                │                │
          └────────────────┼────────────────┘
                           ▼
                  Applicable Regimes
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
       National         Regional       Continental /
                                          Treaty
          │                │                │
          └────────────────┼────────────────┘
                           ▼
                   Competent Authorities
                           │
                           ▼
                    Legal Instruments
                           │
                           ▼
                    Candidate Rules
                           │
                     Scope Analysis
                           │
                ┌──────────┴───────────┐
                ▼                      ▼
            Compatible              Conflict
                │                      │
                ▼                      ▼
          Cumulative Rules      Hierarchy Policy
                                       │
                          ┌────────────┴────────────┐
                          ▼                         ▼
                       Resolved                 Unresolved
                          │                         │
                          ▼                         ▼
                    Applicable Rules         REVIEW_REQUIRED
                          │
                          ▼
                      Assessment
```

The engine SHALL understand that:

```text
AfCFTA
EAC
SACU
SADC
national legislation
delegated regulations
regulator decisions
court decisions
local rules
```

may simultaneously participate in the legal environment without belonging to one simple ordinal hierarchy.

The architecture SHALL therefore answer:

> **Which legal authority had competence over this issue, in this jurisdiction or regime, at this point in time?**

Then:

> **Which rules were actually applicable?**

Then:

> **Were those rules cumulative, conflicting, subordinate, superseded, excepted or controlling?**

And only then:

> **What regulatory effect follows for this business context?**

This ADR establishes a major principle for Baobab Regulations:

> **Finding a regulation is easy compared with determining whether it controls.**

The latter is where serious regulatory technology begins.

---

## Decision Summary

```text
ADR-REG-0007
──────────────────────────────────────────────

CORE DECISION

No universal legal hierarchy.

Baobab uses a scoped,
effective-dated Legal Authority Topology.

RESOLUTION DIMENSIONS

Jurisdiction
Regime
Competence
Subject matter
Actor
Activity
Territory
Time
Instrument
Domestic effect
Judicial authority
Explicit precedence

CORE SEPARATIONS

Country ≠ Jurisdiction
Jurisdiction ≠ Regime
Authority ≠ Competence
Treaty membership ≠ Domestic effect
Source preference ≠ Legal hierarchy
Court hierarchy ≠ Instrument hierarchy
Newer ≠ Automatically superior
More specific ≠ Automatically superior

REGIONAL MODELLING

EAC:
explicit Treaty precedence

AfCFTA:
specific conflict rule
+
higher-integration exception

SACU:
customs union architecture
+
national implementation

SADC:
additional regional trade layer

ASSESSMENT FLOW

Context
→ Jurisdictions
→ Regimes
→ Competent Authorities
→ Candidate Rules
→ Scope
→ Conflict
→ Precedence
→ Applicable Rule Set

FAILURE PRINCIPLE

Unresolved hierarchy
→ REVIEW_REQUIRED

Never:
"pick the newest rule."

STRATEGIC RESULT

Baobab moves beyond
regulatory search into
defensible determination
of controlling law.
```