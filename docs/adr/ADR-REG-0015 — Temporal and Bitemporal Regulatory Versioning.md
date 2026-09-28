# ADR-REG-0015 — Temporal and Bitemporal Regulatory Versioning

**Status:** Proposed — Foundational Temporal Architecture  
**Decision ID:** `ADR-REG-0015`  
**Engine:** Baobab Regulations  
**Target Repository:** `baobab-platform/baobab-regulations`  
**Date:** 2026-09-28  
**Decision Type:** Temporal Semantics / Bitemporal Persistence / Regulatory Versioning / Historical Replay / Future Simulation  
**Strategic Classification:** Core Regulatory Truth Infrastructure

---

## 1. Depends On

This ADR SHALL be interpreted consistently with:

- `ADR-REG-0001 — Mission, Authority, Regulatory Execution and System Boundary`
- `ADR-REG-0003 — Regulatory Authority, Source Authenticity, Interpretation and Derived Rule Boundary`
- `ADR-REG-0006 — Canonical Regulatory Domain Model`
- `ADR-REG-0007 — Jurisdiction, Regulatory Authority and Legal Hierarchy Model`
- `ADR-REG-0008 — Regulatory Instrument, Provision, Rule, Obligation and Requirement Model`
- `ADR-REG-0009 — Normative Semantics and Defeasibility Model`
- `ADR-REG-0010 — Regulatory Knowledge Graph and Relationship Model`
- `ADR-REG-0011 — Authoritative Source Registry and Multidimensional Source Trust Model`
- `ADR-REG-0013 — Source Ingestion, Normalisation and Adapter Architecture`
- `ADR-REG-0014 — Provenance, Citation and Evidentiary Chain`

Relevant platform architecture includes:

- Control Plane temporal context and trade-lane models
- Pulse evidence/versioning principles
- Shared canonical identifiers and mapping contracts

---

# 2. Executive Decision

Baobab Regulations SHALL implement a **bitemporal canonical regulatory model** capable of answering two independent questions:

```text id="w7ujhd"
VALID TIME

"When was this legally true
or legally applicable?"
```

and:

```text id="7yw2nd"
KNOWLEDGE / RECORDED TIME

"When did Baobab know,
record, verify or publish
this state?"
```

The canonical query model SHALL therefore support:

```text id="eu0thr"
regulatory state
AS OF legal_time
AS KNOWN AT knowledge_time
```

These two axes SHALL remain independent.

---

# 3. Foundational Principle

> **What the law was and what Baobab knew the law to be are different historical questions.**

Example:

```text id="0xnagp"
Regulation becomes effective:
1 September

Baobab discovers it:
15 September
```

Then:

```text id="28gdhd"
LEGAL VALID TIME
starts 1 September

KNOWLEDGE TIME
starts 15 September.
```

Baobab SHALL preserve both.

---

# 4. Why This Matters

Without bitemporal semantics, a database updated on 15 September may make it appear that:

```text id="llbwct"
Baobab knew the regulation
on 1 September.
```

That would falsify historical decision reconstruction.

---

# 5. Four Different Questions

The system must be able to answer:

```text id="wefb7t"
Q1
What law legally applied
on 10 September?

Q2
What did Baobab believe applied
on 10 September,
based on knowledge available then?

Q3
Knowing what we know today,
what law actually applied
on 10 September?

Q4
What rules will apply
on 1 January next year?
```

These queries can return different answers.

---

# 6. Bitemporal Coordinates

Every material temporally versioned regulatory assertion SHOULD conceptually occupy a rectangle:

```text id="6t6squ"
                   KNOWLEDGE TIME
                         ───────────────►

              ┌──────────────────────────┐
              │                          │
LEGAL         │       Assertion A        │
VALID         │                          │
TIME          └──────────────────────────┘
  │
  │
  ▼
```

One axis says:

```text id="ke0pvy"
when it was legally true.
```

The other says:

```text id="53y10o"
when Baobab held that assertion.
```

---

# 7. Bitemporal Is Not the Whole Legal Time Model

Legal systems contain additional time semantics.

Baobab SHALL distinguish:

```text id="pzqy2w"
publication time

promulgation time

assent / enactment time

commencement / entry-into-force time

efficacy time

applicability time

expiry time

suspension time

repeal time

annulment time

retroactive effect time

transition period

grandfathering period

regulated-event time.
```

These events inform legal-valid semantics but SHALL not be collapsed into one timestamp.

---

# 8. LegalRuleML Alignment

LegalRuleML explicitly recognises that legal norms vary over time and distinguishes temporal concepts including when norms enter into force, when they have efficacy, and when they apply. It notes that rules may vary temporally in status, validity and jurisdiction.

Baobab SHALL preserve this richer distinction.

---

# 9. Akoma Ntoso Alignment

Akoma Ntoso models legal-document lifecycle events and temporal information explicitly, including amendment, repeal and intervals relating to force and efficacy. It distinguishes original, consolidated/single-version and multiple-version representations of legal documents.

Baobab SHALL remain compatible with these concepts without adopting Akoma Ntoso as its canonical persistence model.

---

# 10. ELI Alignment

The ELI ontology includes metadata such as:

```text id="s6l3f9"
version date

first date of entry into force

date no longer in force

date of applicability
```

and lifecycle relationships such as amendment, repeal, correction and consolidation.

These concepts reinforce Baobab's temporal separation.

---

# 11. Core Temporal Dimensions

The Regulations domain SHALL support at least:

```text id="uwjaj0"
LEGAL_VALID_TIME

KNOWLEDGE_TIME

PUBLICATION_TIME

EFFECTIVE / FORCE TIME

APPLICABILITY_TIME

EVALUATION_TIME

REGULATED_EVENT_TIME
```

Not every object requires every dimension.

---

# 12. Legal Valid Time

`legal_valid_time` means:

> The period during which a regulatory assertion is legally relevant according to Baobab's verified interpretation.

It does not necessarily mean:

```text id="xg6c6x"
the document exists.
```

---

# 13. Knowledge Time

`knowledge_time` means:

> The period during which Baobab's canonical system held this version/assertion as recorded knowledge.

It begins when the canonical assertion is recorded/promoted, not when the underlying law necessarily became effective.

---

# 14. Knowledge Time versus Acquisition Time

These SHALL differ.

Example:

```text id="uvx18f"
source acquired:
12:04

review completed:
16:45

rule promoted:
17:20
```

Possible:

```text id="8hnzai"
acquired_at = 12:04

verified_at = 16:45

knowledge_valid_from = 17:20.
```

---

# 15. Knowledge Time versus Discovery Time

Baobab may first discover a possible change on:

```text id="uk1b3s"
10 September
```

but verify it on:

```text id="2z7wya"
12 September.
```

The system MAY preserve both:

```text id="ahhfbc"
discovered_at
verified_at
recorded_at.
```

---

# 16. Recorded Time

Physical implementation MAY use:

```text id="7ii1ri"
recorded_from

recorded_to
```

as the canonical database representation of knowledge time.

---

# 17. Transaction/System Time Terminology

Database literature often calls the second axis:

```text id="5e8bap"
transaction time
```

or:

```text id="7r2tzj"
system time.
```

For Baobab domain language, **knowledge time** is clearer because it represents when Baobab's canonical knowledge held the assertion.

Technical schemas MAY still use:

```text id="mn8j5k"
system_period
```

where appropriate.

---

# 18. Publication Time

`published_at` describes when a source was officially published.

This is not automatically:

```text id="wv46rw"
entry into force.
```

---

# 19. Enactment Time

An instrument may be:

```text id="q17xju"
passed

signed

assented to

promulgated
```

before its provisions become legally operative.

---

# 20. Commencement / Entry Into Force

A rule may begin legal force:

```text id="9vazga"
on publication

on specified future date

on proclamation

on occurrence of event

in stages.
```

---

# 21. Provision-Level Commencement

Different provisions in the same instrument MAY commence on different dates.

Therefore:

```text id="vuxgp1"
Instrument effective date
```

SHALL NOT universally override:

```text id="qq8ugf"
ProvisionVersion effective date.
```

---

# 22. Partial Commencement

Example:

```text id="m52bt9"
Act A

Sections 1–10:
1 January

Sections 11–20:
1 April

Section 21:
date to be proclaimed.
```

Baobab SHALL model this at provision/rule granularity.

---

# 23. Applicability Time

A provision may be legally in force while applying only to:

```text id="52cdau"
transactions after date X

contracts entered after date Y

goods imported after date Z.
```

Therefore:

```text id="15wwph"
IN_FORCE
≠
APPLIES_TO_TRANSACTION.
```

---

# 24. Efficacy

Where legal semantics distinguish legal force from efficacy, Baobab SHALL preserve that distinction rather than compressing it.

Akoma Ntoso explicitly models efficacy periods separately in temporal metadata.

---

# 25. Regulated Event Time

The relevant date for rule application might be:

```text id="9i2s9q"
contract_date

invoice_date

shipment_date

export_date

import_entry_date

customs_clearance_date

payment_date

filing_date

manufacture_date

employment_start_date.
```

The rule itself SHALL specify which temporal anchor matters.

---

# 26. Evaluation Time

`evaluation_time` is when Baobab evaluates the regulatory question.

Example:

```text id="a4g1ha"
today:
28 September

regulated shipment event:
20 September

rule effective:
1 September.
```

The system cannot simply use:

```text id="x6v63a"
NOW()
```

to determine applicability.

---

# 27. Decision Time

`decided_at` records when the regulatory decision was made.

It does not determine the legal period unless the relevant rule uses that date.

---

# 28. Basic Bitemporal Example

Suppose:

```text id="6dhjdx"
Rule R became effective:
2026-09-01

Baobab discovered it:
2026-09-15

Baobab verifies/publishes:
2026-09-16
```

The RuleVersion may conceptually hold:

```text id="zcmq0y"
legal_valid_period =
[2026-09-01, ∞)

knowledge_period =
[2026-09-16, ∞)
```

---

# 29. Historical Query Before Discovery

Query:

```text id="h84a1u"
legal_time = 2026-09-10
knowledge_time = 2026-09-10
```

Result:

```text id="votaw3"
Baobab did not yet know Rule R.
```

---

# 30. Corrected Historical Query

Query today:

```text id="nhq8v0"
legal_time = 2026-09-10
knowledge_time = NOW
```

Result:

```text id="f4av2f"
Rule R legally applied.
```

This is why both axes are essential.

---

# 31. Historical Replay

Historical replay from ADR-REG-0014 SHALL ordinarily query:

```text id="r8fwmn"
legal time = original regulated-event time

knowledge time = original decision time.
```

---

# 32. Restated Historical Truth

A different analytical mode MAY query:

```text id="6o19u5"
legal time = original regulated-event time

knowledge time = current knowledge.
```

This answers:

> Knowing everything we now know, what should the legal result have been then?

---

# 33. These Modes Must Be Named

Never expose an ambiguous:

```text id="oypqu4"
GET /rules?date=...
```

without defining whether the query means:

```text id="wc0rc3"
historically known

currently reconstructed

future projected.
```

---

# 34. Canonical Query Modes

Baobab SHOULD eventually expose semantics equivalent to:

```text id="rk5i3v"
CURRENT_STATE

HISTORICAL_AS_KNOWN

HISTORICAL_RESTATED

FUTURE_EFFECTIVE

CUSTOM_BITEMPORAL.
```

---

# 35. Current State

`CURRENT_STATE` means:

```text id="1aez8p"
legal time = now

knowledge time = now.
```

---

# 36. Historical As Known

`HISTORICAL_AS_KNOWN` means:

```text id="bp8y1g"
legal time = T

knowledge time = K
```

where `K` usually equals the historical decision time.

---

# 37. Historical Restated

`HISTORICAL_RESTATED` means:

```text id="9xip89"
legal time = T

knowledge time = now.
```

---

# 38. Future Effective

`FUTURE_EFFECTIVE` means:

```text id="blnwpr"
legal time = future T

knowledge time = now.
```

using only currently known future-effective law.

---

# 39. Future Simulation Is Not Prediction

If an enacted law is scheduled for future commencement:

```text id="miti9p"
future simulation
```

is deterministic legal-state projection.

If commencement depends on an uncertain future proclamation:

```text id="o1c4xx"
future applicability remains conditional/unknown.
```

---

# 40. Future Proposed Law

Draft or proposed regulations SHALL not enter the canonical future-effective rule set as binding law.

They MAY enter:

```text id="sqyrtf"
candidate / scenario
```

state.

---

# 41. Scenario Simulation

Baobab MAY later support:

```text id="oo16sk"
IF Draft Regulation D becomes effective
on proposed date T,
what changes?
```

This is scenario analysis.

It SHALL remain distinct from verified future law.

---

# 42. Temporal Event Model

Baobab SHALL model legal lifecycle events explicitly.

Conceptually:

```text id="6gfgqp"
RegulatoryTemporalEvent
├── event_id
├── event_type
├── subject_ref
├── legal_date_or_period
├── source_refs[]
├── causing_instrument_ref?
├── jurisdiction_ref
├── recorded_at
├── verification_state
└── provenance
```

---

# 43. Temporal Event Types

At minimum:

```text id="0vg6bq"
PUBLISHED

ENACTED

ASSENTED

PROMULGATED

COMMENCED

PARTIALLY_COMMENCED

BECAME_APPLICABLE

SUSPENDED

RESUMED

AMENDED

CORRECTED

REPEALED

EXPIRED

REVOKED

ANNULLED

SUPERSEDED

RETROACTIVELY_EFFECTIVE

TRANSITION_STARTED

TRANSITION_ENDED.
```

---

# 44. Event Type Is Not Status

Example:

```text id="sx85o2"
REPEALED
```

is an event.

```text id="30zvwu"
NOT_IN_FORCE
```

is a derived status for a particular time.

---

# 45. Status Is Time-Dependent

Baobab SHALL avoid storing only:

```text id="a3u8wx"
status = ACTIVE.
```

Instead it SHOULD be able to answer:

```text id="zf97lm"
status at time T.
```

---

# 46. RegulatoryTemporalStatus

Potential derived values include:

```text id="yum3vp"
NOT_YET_PUBLISHED

PUBLISHED_NOT_IN_FORCE

IN_FORCE_NOT_YET_APPLICABLE

IN_FORCE_AND_APPLICABLE

PARTIALLY_APPLICABLE

SUSPENDED

REPEALED

EXPIRED

ANNULLED

TRANSITIONAL

UNKNOWN.
```

---

# 47. Version versus Temporal Status

A `RuleVersion` identity SHALL remain distinct from:

```text id="a8lrx7"
whether the rule is active at time T.
```

---

# 48. Stable Identity / Version Pattern

Preferred:

```text id="lzl2u1"
RegulatoryRule
    stable canonical identity

RegulatoryRuleVersion
    immutable versioned semantics.
```

---

# 49. Provision Pattern

Similarly:

```text id="5fjg8r"
Provision
    stable structural identity

ProvisionVersion
    immutable text/legal version.
```

---

# 50. Interpretation Pattern

Interpretations SHALL also be versionable.

Example:

```text id="atcj15"
Interpretation I
├── Version 1
└── Version 2
```

where V2 may:

```text id="7f66bi"
correct
supersede
refine
```

V1 without rewriting history.

---

# 51. Source Edition Pattern

A source publication SHALL be versioned through:

```text id="cnc09j"
Source

SourceEdition

SourceArtefact.
```

---

# 52. No Destructive Current Record

Rejected:

```text id="zimpip"
regulatory_rule.current_text
```

continually overwritten in place.

---

# 53. Append-Oriented Versioning

Material temporal changes SHALL generally create:

```text id="re5ehe"
new immutable version
+
relationship to previous version.
```

---

# 54. Version Relationships

At minimum:

```text id="3qbpzg"
SUPERSEDES

AMENDS

CORRECTS

REPLACES

RESTATES.
```

These semantics SHALL remain distinct.

---

# 55. Amendment

An amendment modifies legal content.

It is not necessarily a correction.

---

# 56. Correction

A correction may fix:

```text id="xacj4z"
publication error

clerical error

Baobab extraction error

Baobab interpretation error.
```

Those categories SHALL remain distinguishable.

---

# 57. Official Correction versus Baobab Correction

Example:

```text id="5zgisb"
OFFICIAL_CORRECTION
```

changes the legal-source history.

```text id="whjy4j"
BAOBAB_PARSER_CORRECTION
```

changes only Baobab's recorded representation.

---

# 58. Knowledge-Time Correction

Suppose Baobab discovers on 20 September that its prior representation was wrong.

Do not rewrite:

```text id="yfjb7y"
knowledge history
```

as though the correct version had always been stored.

Instead:

```text id="xh8htk"
Old assertion knowledge period:
[10 Sep, 20 Sep)

Corrected assertion knowledge period:
[20 Sep, ∞)
```

while both may refer to the same historical legal-valid period.

---

# 59. Classic Bitemporal Correction

Conceptually:

```text id="btjzva"
Row A:
legal_valid = [1 Sep, ∞)
knowledge   = [10 Sep, 20 Sep)
value       = incorrect interpretation

Row B:
legal_valid = [1 Sep, ∞)
knowledge   = [20 Sep, ∞)
value       = corrected interpretation
```

This preserves what Baobab believed between 10 and 20 September.

---

# 60. Retroactive Legal Change

Law can sometimes have effect from a date earlier than:

```text id="3oi4p4"
publication

promulgation

Baobab discovery.
```

Baobab SHALL support:

```text id="5wws1c"
legal_valid_from < publication_at
```

when verified.

---

# 61. Retroactivity Is High-Risk

Retroactive effect SHALL require explicit legal basis/provenance.

It SHALL never be inferred simply because:

```text id="zidzyj"
a regulator now says a rule existed earlier.
```

---

# 62. Retroactive Impact

A verified retroactive change SHOULD trigger:

```text id="6q1od6"
historical impact analysis.
```

Potential targets:

```text id="se55rk"
prior assessments

prior decisions

open transactions

completed transactions

customer reports.
```

---

# 63. Retroactive Change Does Not Automatically Reopen Everything

Impact analysis identifies candidate historical decisions.

Separate policy determines:

```text id="1ezz2q"
whether reassessment

notification

remediation
```

is required.

---

# 64. Repeal

Repeal SHALL terminate legal validity according to verified semantics.

Example:

```text id="4etg1c"
legal_valid_period =
[2024-01-01, 2026-09-30)
```

---

# 65. Half-Open Interval Convention

Where appropriate, canonical temporal intervals SHOULD use:

```text id="5ppwo9"
[start, end)
```

meaning:

```text id="yxwtiv"
start inclusive
end exclusive.
```

PostgreSQL range types natively support inclusive/exclusive bounds and date ranges use a canonical lower-inclusive, upper-exclusive form.

---

# 66. Why Half-Open Intervals

They avoid ambiguity at consecutive boundaries:

```text id="0mb5hq"
V1 [1 Jan, 1 Apr)

V2 [1 Apr, ∞)
```

There is neither:

```text id="cbzd1a"
overlap
```

nor:

```text id="jm2jo2"
gap.
```

---

# 67. Date versus Timestamp

Many laws operate at:

```text id="wsk8oj"
day precision.
```

Others may take effect at:

```text id="oyeqih"
specific timestamp.
```

The model SHALL preserve declared temporal precision.

---

# 68. Do Not Invent Midnight

If a source only states:

```text id="z6isq3"
effective 1 January
```

Baobab SHOULD represent legal-date semantics rather than falsely claiming:

```text id="37oam1"
00:00:00.000000 UTC
```

unless jurisdictional interpretation establishes that convention.

---

# 69. Time Zone

Where timestamp precision is legally relevant:

```text id="yi4ijy"
jurisdictional timezone
```

SHALL be known.

PostgreSQL `timestamptz` stores timezone-aware timestamps internally in UTC while supporting timezone-aware interpretation/display.

---

# 70. Calendar Date as Legal Value

Legal instruments frequently specify a civil date independent of system timezone.

Therefore:

```text id="h67aqk"
DATE
```

may be superior to:

```text id="atyp38"
TIMESTAMPTZ
```

for legal commencement.

---

# 71. Temporal Precision

Potential precision values:

```text id="1g5nge"
YEAR

MONTH

DATE

MINUTE

SECOND

UNKNOWN.
```

---

# 72. Approximate Time

If the exact date is uncertain:

```text id="psl20u"
do not invent precision.
```

Use:

```text id="p67nxi"
UNKNOWN

ESTIMATED

DATE_RANGE

REVIEW_REQUIRED.
```

---

# 73. Open-Ended Period

Rules may remain effective with no known end:

```text id="f2kh4j"
[start, ∞)
```

PostgreSQL range types support unbounded ranges directly.

---

# 74. Suspension

A rule may be:

```text id="fwam1r"
effective

suspended

resumed.
```

Therefore one continuous interval may be insufficient.

---

# 75. Multirange

Conceptually:

```text id="clbrun"
legal_effective_periods =
{
  [1 Jan, 1 Mar),
  [1 Apr, ∞)
}
```

PostgreSQL 17 supports corresponding multirange types for its built-in range types.

---

# 76. Multirange Is a Storage Option

The canonical domain SHALL support discontinuous temporal validity.

It need not expose PostgreSQL multirange types directly in public contracts.

---

# 77. Suspension versus Repeal

These SHALL differ.

```text id="kh4qtr"
SUSPENSION
may permit later resumption.

REPEAL
normally terminates the provision/rule
subject to legal transition/savings.
```

---

# 78. Expiry

Some provisions terminate automatically:

```text id="p7ttph"
sunset clause

fixed licence period

temporary emergency regulation.
```

Expiry SHALL be modelled explicitly.

---

# 79. Sunset

A sunset clause may terminate:

```text id="u3lgu6"
whole instrument

specific provision

specific power.
```

The temporal model SHALL permit that granularity.

---

# 80. Annulment / Invalidity

Court or competent-authority decisions may affect legal validity.

Possible effect:

```text id="7l9udw"
prospective only

retroactive

suspended declaration of invalidity

partial

limited to specific scope.
```

The engine SHALL not treat:

```text id="fwu2tz"
INVALIDATED
```

as universally:

```text id="7v2jcf"
erase rule from all history.
```

---

# 81. Grandfathering

A new rule may not apply to:

```text id="znqxpd"
existing contracts

existing permits

transactions initiated before cut-off date.
```

This is not simply a rule-validity range.

---

# 82. Grandfathering Is Applicability Logic

Example:

```text id="c0u8e1"
RuleVersion R2
effective from 1 Jan

BUT

contracts signed before 1 Jan
remain governed by R1.
```

Both R1 and R2 may need evaluation depending on transaction facts.

---

# 83. Transitional Rule

Transitional rules SHALL be modelled as explicit rules/conditions rather than hidden temporal hacks.

---

# 84. Savings Provision

Repeal may preserve prior rights, obligations or proceedings.

Therefore:

```text id="7r9lo3"
repealed
```

does not automatically imply:

```text id="v7rm79"
irrelevant to all post-repeal decisions.
```

---

# 85. Example — Historical Liability

A repealed customs rule may remain relevant when assessing:

```text id="inwxi4"
shipment that occurred before repeal.
```

---

# 86. Example — Ongoing Licence

A licence issued under old legislation may remain valid under a savings provision.

The old rule may remain relevant to:

```text id="9olpeh"
licence origin/history
```

while new renewal requirements come from newer law.

---

# 87. Temporal Rule Conditions

Rules MAY contain predicates like:

```text id="gb2k4s"
transaction_date >= T

permit_issued_before T

contract_existed_on T

activity_continues_after T.
```

These are rule semantics.

They SHALL not be substituted for database version periods.

---

# 88. Legal Valid Period versus Trigger Time

Example:

```text id="a8ia6d"
Rule active:
2026–2030

Obligation triggered:
on import event.
```

The two times are independent.

---

# 89. Obligation Temporal Model

A contextual obligation MAY have:

```text id="fnyfxg"
arose_at

due_at

satisfied_at

violated_at

ceased_at

superseded_at.
```

---

# 90. Obligation Exists beyond Rule Change

A rule's repeal does not necessarily extinguish:

```text id="34syf2"
obligation already incurred.
```

---

# 91. Requirement Temporal Model

A requirement may have:

```text id="no0pbe"
required_from

required_by

valid_until

satisfaction_period.
```

---

# 92. Evidence Temporal Model

Evidence may have:

```text id="b33358"
issued_at

valid_from

valid_to

revoked_at

observed_at

recorded_at.
```

---

# 93. Evidence Knowledge Time

If Baobab learns on 10 October that a permit was revoked effective 1 October:

```text id="lwe75h"
legal/factual validity changed:
1 Oct

Baobab knowledge changed:
10 Oct.
```

The same bitemporal principle applies.

---

# 94. Context Facts Can Be Bitemporal

Relevant external facts may themselves be corrected later.

Example:

```text id="6js4pt"
Product classification originally recorded:
0901

later corrected:
0902

correction effective for original transaction.
```

Historical decisions need both fact history and knowledge history.

---

# 95. Canonical Master Data Remains External

Regulations SHALL not become the source of truth for:

```text id="v6prze"
product

shipment

organisation.
```

But its decision snapshot SHALL preserve the temporal fact it used.

---

# 96. Trade Event Time

Cross-border trade can involve:

```text id="h6yw0v"
contract time

dispatch time

export declaration time

border-crossing time

import declaration time

customs clearance time

delivery time.
```

Different regulatory rules may anchor to different events.

---

# 97. Trade Lane Time

Jurisdiction/regime membership may itself be temporal.

Example:

```text id="z6a6x5"
Country enters regime at T1

preferential arrangement changes at T2.
```

Regulatory applicability SHALL query the membership state for the relevant legal time.

---

# 98. Authority Competence Time

An authority's competence may change.

Therefore:

```text id="nh5qqp"
AuthorityRelationship

RegulatoryCompetence
```

SHALL carry effective temporal state.

---

# 99. Authority Succession

When Authority B succeeds Authority A:

```text id="9hxuj3"
historical documents
remain associated with A.
```

Future authority actions associate with B.

History SHALL not be rewritten.

---

# 100. Regime Membership Time

`RegimeMembership` SHALL be effective-dated.

Example:

```text id="fpxz4v"
member_from

member_to

ratification_date

entry_into_force_date
```

may all be relevant.

---

# 101. Treaty Signature ≠ Treaty Effect

These SHALL remain distinguishable:

```text id="kx814e"
signature

ratification

entry into force

domestic implementation

private-party applicability.
```

---

# 102. Source Temporal Model

`SourceEdition` MAY have:

```text id="67qt29"
published_at

official_version_date

retrieved_at

superseded_at.
```

---

# 103. Consolidation Time

A consolidated document represents:

```text id="q8r6t1"
state of source text as of a date.
```

It SHALL identify its consolidation/version date.

---

# 104. Consolidation Is a View

Conceptually:

```text id="bfrmir"
Base Instrument
+
Amendments effective by T
=
Consolidated representation as of T.
```

---

# 105. Consolidated Text Does Not Replace Event History

Baobab SHALL preserve:

```text id="4vz8en"
amendment lifecycle
```

rather than storing only the latest consolidation.

Akoma Ntoso similarly treats the lifecycle events generating document versions as explicit data.

---

# 106. Version Materialisation

Baobab MAY materialise:

```text id="mz0zyc"
Instrument as of T
```

for performance.

That view SHALL be derivable from canonical temporal history.

---

# 107. Materialised Version Is Rebuildable

A current-law view SHALL be:

```text id="brwmpi"
projection
```

not the only surviving copy.

---

# 108. "Current" Is a Query

The architecture SHALL treat:

```text id="vjam3c"
CURRENT LAW
```

as:

```text id="ldxeqp"
query over temporal history.
```

Not as a special mutable table containing only current records.

---

# 109. Current Rule Projection

For high-performance evaluation, Baobab MAY maintain:

```text id="2djlzu"
current_effective_rules
```

projection/cache.

It SHALL be rebuildable.

---

# 110. Future Rule Projection

Similarly:

```text id="ylrvr2"
future_effective_rules
```

MAY support market-entry simulation.

---

# 111. Historical Projection

Historical queries SHALL access temporal canonical history rather than attempting to reverse-engineer earlier state from current data.

---

# 112. PostgreSQL 17 Strategy

The initial authoritative implementation SHOULD use PostgreSQL 17 temporal primitives such as:

```text id="m9tvzi"
daterange

tstzrange

datemultirange

tstzmultirange

GiST indexes

exclusion constraints.
```

PostgreSQL 17 supports range/multirange types, overlap/containment operators and GiST-based exclusion constraints suitable for preventing inappropriate overlapping intervals.

---

# 113. Important PostgreSQL 17 Limitation

PostgreSQL 17 SHALL NOT be assumed to provide native SQL temporal primary/foreign keys using:

```text id="sdip5l"
WITHOUT OVERLAPS

PERIOD
```

Those temporal-constraint features were introduced in PostgreSQL 18 after the earlier PostgreSQL 17 implementation was reverted before release.

Therefore the PostgreSQL 17 implementation SHALL use:

```text id="vbbz0c"
range columns

exclusion constraints

application/domain validation

carefully designed temporal references.
```

---

# 114. No Fake PostgreSQL Feature Dependency

`ADR-REG-0015` SHALL NOT require PostgreSQL 18 temporal-key syntax while the platform standard remains PostgreSQL 17.

---

# 115. Future PostgreSQL Upgrade

A later platform upgrade MAY adopt PostgreSQL 18 temporal constraints after separate compatibility/performance review.

Canonical temporal semantics SHALL not depend upon that upgrade.

---

# 116. Temporal Range Storage

Illustrative only:

```text id="brr00n"
legal_valid_period daterange

knowledge_period tstzrange
```

or timestamp ranges where legal precision requires.

---

# 117. Date Legal Time / Timestamp Knowledge Time

A common pattern MAY be:

```text id="x5ozhp"
legal valid time:
DATE / daterange

knowledge time:
TIMESTAMPTZ / tstzrange
```

because:

```text id="lv27a6"
law often changes by civil date

Baobab records changes at exact system times.
```

---

# 118. Precision Override

Objects requiring precise legal timestamp semantics MAY use timestamp-based valid periods.

---

# 119. Exclusion Constraint

For versions where only one canonical assertion may occupy a legal interval for a given knowledge slice, Baobab MAY enforce non-overlap using GiST exclusion constraints.

PostgreSQL 17 explicitly supports range overlap constraints via `EXCLUDE USING GIST`.

---

# 120. Do Not Over-Constrain Legal Alternatives

Some legal objects legitimately contain:

```text id="y40mo1"
competing interpretations

coexisting rules

overlapping obligations.
```

Database exclusion constraints SHALL not mistakenly prohibit semantic coexistence.

---

# 121. Version-Stream Key

A non-overlap constraint should apply only within a clearly defined version stream such as:

```text id="uxpg8l"
same RuleVersion lineage

same source-expression identity

same canonical assertion dimension.
```

---

# 122. Bitemporal Table Pattern

Illustrative:

```text id="eqdn1y"
RuleVersionTemporalRecord
├── rule_version_id
├── semantic_version_id
├── legal_valid_period
├── knowledge_period
├── recorded_at
├── superseded_at?
├── source_event_ref
└── provenance
```

---

# 123. Version Identity versus Bitemporal Assertion

Baobab MAY distinguish:

```text id="b6t45e"
immutable semantic RuleVersion
```

from:

```text id="92qop3"
bitemporal assertion about its validity.
```

This can reduce duplication where the same semantics are later reclassified temporally.

---

# 124. Temporal Assertion

Conceptually:

```text id="b7iyhc"
TemporalAssertion
├── assertion_id
├── subject_ref
├── temporal_dimension
├── valid_period
├── knowledge_period
├── assertion_type
├── basis_refs[]
└── provenance
```

---

# 125. Avoid Generic Everything-Temporal Table

Not every temporal concept SHOULD be forced through one opaque:

```text id="ss9okg"
TemporalThing
```

table.

Domain-specific temporal fields remain preferable where semantics differ.

---

# 126. Knowledge Interval Mutation

When canonical knowledge changes at `K2`, the prior knowledge period SHALL close:

```text id="dufu7b"
[K1, K2)
```

and new assertion begins:

```text id="xcqq8m"
[K2, ∞)
```

---

# 127. No Backdating Knowledge Time

Baobab SHALL NOT backdate:

```text id="2h3d94"
knowledge_valid_from
```

to make historical records look cleaner.

---

# 128. Backdated Legal Time Is Allowed

Legal-valid time MAY precede knowledge time if the authoritative source establishes that fact.

That is precisely the purpose of bitemporal storage.

---

# 129. Legal Date Correction

Suppose Baobab initially records:

```text id="zooyat"
effective 1 October.
```

Later discovers:

```text id="0xlf4h"
effective 15 September.
```

Do not overwrite.

Create a new knowledge version:

```text id="l074d5"
Old belief:
legal valid from 1 Oct
knowledge [K1,K2)

New belief:
legal valid from 15 Sep
knowledge [K2,∞)
```

---

# 130. Multiple Late Discoveries

The architecture SHALL support repeated corrections:

```text id="cdfb0r"
K1 → K2 → K3 → K4.
```

No arbitrary fixed number of revisions.

---

# 131. Temporal Provenance

Every temporal boundary SHOULD answer:

```text id="m20c8e"
Why does this period begin here?

Why does it end here?

Which source/event established it?

When did Baobab record it?
```

---

# 132. Temporal Boundary Basis

Potential:

```text id="zualu8"
publication provision

commencement clause

proclamation

amending instrument

repeal provision

court order

regulator determination

verified interpretation.
```

---

# 133. Unknown End Date

Do not infer repeal/expiry merely because no recent source exists.

Use:

```text id="45d56q"
open-ended validity
```

until evidence establishes an end.

---

# 134. Unknown Start Date

If commencement cannot be determined:

```text id="hllcqv"
valid_from = UNKNOWN
```

or equivalent unresolved temporal state.

Do not guess from publication date.

---

# 135. Publication Default

A jurisdiction-specific interpretation MAY establish:

```text id="i7a99s"
effective on publication
```

for certain instrument classes.

That rule SHALL itself be explicit and source-backed.

---

# 136. Temporal Defaults Are Jurisdiction-Specific

Baobab SHALL NOT implement a global:

```text id="n0d3zj"
if no effective date:
    effective = publication_date
```

rule.

---

# 137. Date Interpretation Policy

Where local law defines how commencement dates work:

```text id="bck9zv"
JurisdictionTemporalPolicy
```

MAY encode those legal conventions.

---

# 138. Temporal Policy Is Regulatory Knowledge

It SHALL be versioned/provenanced like other regulatory rules.

---

# 139. Temporal Resolution Outcome

Potential outcomes:

```text id="esufgy"
DEFINITELY_ACTIVE

DEFINITELY_INACTIVE

FUTURE_EFFECTIVE

SUSPENDED

TRANSITIONALLY_APPLICABLE

CONDITIONAL

INDETERMINATE.
```

---

# 140. Indeterminate Is Valid

If commencement cannot be determined safely:

```text id="396kqi"
INDETERMINATE
```

is preferable to invented certainty.

---

# 141. Application Interval

A `RuleVersion` SHOULD be able to express a legal applicability period distinct from its force period.

Example:

```text id="lvg73f"
force:
[1 Jan, ∞)

applicability:
transactions occurring
from 1 Mar onward.
```

---

# 142. Efficacy / Applicability Representation

Potential:

```text id="1lvjfb"
in_force_period

efficacy_period

applicability_period
```

where the legal source meaningfully distinguishes them.

---

# 143. Do Not Populate Empty Dimensions Artificially

If a jurisdiction does not distinguish:

```text id="f3ifhq"
efficacy
```

for the relevant rule:

```text id="gk4ph6"
do not invent a separate period.
```

---

# 144. Rule Evaluation Temporal Inputs

A rule evaluation MAY require:

```text id="nxa71g"
legal_reference_time

regulated_event_time

knowledge_cutoff_time

decision_time.
```

---

# 145. Evaluation Contract

Conceptually:

```text id="7ymch7"
evaluate(
    regulatory_context,
    legal_time,
    knowledge_time,
    ruleset_snapshot
)
```

---

# 146. Default Knowledge Time

Ordinary live evaluation:

```text id="cnhrci"
knowledge_time = current canonical knowledge.
```

---

# 147. Default Legal Time

Ordinary live evaluation SHALL use:

```text id="dq021t"
rule-specific relevant regulated-event time
```

where available.

Not blindly:

```text id="ehdjtq"
current timestamp.
```

---

# 148. Current Transaction Example

A shipment planned tomorrow may need:

```text id="htfhvo"
future legal time
```

even though evaluation occurs today.

---

# 149. Planning Query

Example:

```text id="o9ut4b"
Can we ship on 10 January 2027?
```

Evaluation:

```text id="rswuje"
legal_time = 10 Jan 2027

knowledge_time = now.
```

This applies currently known future law.

---

# 150. Planned Event Date Changes

If shipment date changes from:

```text id="scg2c0"
30 Dec
```

to:

```text id="gt0iei"
2 Jan
```

a future-effective regulation may suddenly apply.

Regulations SHALL support automatic reassessment.

---

# 151. Decision Validity Window

Some decisions MAY have:

```text id="9ftqh9"
valid_for_period.
```

Example:

```text id="ghp7q6"
regulatory pre-clearance
valid until legal change
or transaction-date change.
```

---

# 152. Decision Is Not Eternally Valid

A regulatory decision SHOULD NOT imply:

```text id="4fqg91"
safe forever.
```

It is tied to:

```text id="0l0fvt"
ruleset

context

legal time

knowledge state.
```

---

# 153. Decision Staleness

Decision may become stale because:

```text id="guap4c"
rule changed

source corrected

context changed

evidence expired

future effective date crossed.
```

---

# 154. Temporal Revalidation Trigger

Potential events:

```text id="eh4t00"
RULE_BECAME_EFFECTIVE

RULE_EXPIRED

RULE_SUSPENDED

RULE_REPEALED

TRANSITION_ENDED

EVIDENCE_EXPIRED

DECISION_VALIDITY_ENDED.
```

---

# 155. Future Activation Scheduler

Baobab SHOULD NOT depend on a cron job being the legal authority.

A scheduler may trigger:

```text id="my15zt"
recalculation

notification

projection refresh.
```

The canonical temporal query itself determines state.

---

# 156. Missed Scheduler Safety

If a scheduled activation job fails at midnight:

```text id="11sm1p"
querying effective law
```

must still return the correct state from temporal data.

---

# 157. Projection Refresh

Current-rule caches MAY require refresh when:

```text id="k509ik"
legal time crosses boundary.
```

---

# 158. Cache Key

Temporal cache keys SHOULD include material components such as:

```text id="3c2s5m"
legal_time bucket

knowledge_version

ruleset fingerprint

jurisdiction

context.
```

---

# 159. No Eternal `ALLOW` Cache

A prior allow result SHALL not survive beyond:

```text id="2k4bm4"
its legal/context/evidence validity.
```

---

# 160. Publication Time Drift

Providers may correct publication metadata.

The correction SHALL alter:

```text id="c23tq0"
knowledge history
```

without falsely changing original publication history unless the official source itself was corrected.

---

# 161. Ingestion Backfill

Historical sources may be loaded years later.

Example:

```text id="t74m48"
law valid in 2015

Baobab imports source in 2027.
```

Then:

```text id="io1ys3"
legal_valid_time = 2015…

knowledge_time = 2027…
```

---

# 162. Historical Corpus Import

Backfilling historical regulation SHALL NOT make Baobab appear to have held that knowledge in earlier years.

---

# 163. Data Migration

If Regulations migrates databases:

```text id="rblf77"
migration time
```

SHALL not reset:

```text id="piif0z"
knowledge time.
```

---

# 164. System Migration Event

Infrastructure migration MAY create separate:

```text id="nuxiys"
custody/provenance event
```

without altering regulatory history.

---

# 165. Bulk Correction

If a parser bug affected 10,000 provisions:

```text id="rfp20w"
new knowledge versions
```

SHALL be created where material rather than rewriting old canonical history invisibly.

---

# 166. Materiality

Pure technical metadata corrections that do not alter regulatory meaning MAY be handled differently.

A technical specification SHALL define:

```text id="qjqu7r"
semantic versus non-semantic correction.
```

---

# 167. Semantic Correction

Examples:

```text id="cu1p4z"
effective date

threshold

bearer

exception

rate

prohibition scope.
```

These require versioned semantic correction.

---

# 168. Non-Semantic Correction

Examples might include:

```text id="0dsoav"
display label typo

whitespace

non-material formatting.
```

These MAY avoid new regulatory semantic versions while remaining audited.

---

# 169. Retroactive Judicial Effect

A court decision may establish that a rule:

```text id="1vkkud"
was invalid from earlier date

or

is invalid prospectively

or

remains temporarily effective.
```

Temporal outcome SHALL be encoded according to the actual ruling.

---

# 170. No Universal Court-Decision Temporal Algorithm

Rejected:

```text id="aoivtk"
court invalidates rule
⇒
delete entire historical validity.
```

---

# 171. Administrative Guidance Change

New guidance may change:

```text id="js64uo"
Baobab interpretation
```

without changing:

```text id="q6i1wb"
underlying instrument.
```

Knowledge/version history SHALL show this.

---

# 172. Interpretation Time

An interpretation MAY have:

```text id="wo3r26"
interpretation_valid_period

knowledge_period.
```

---

# 173. Counsel Opinion

A tenant counsel interpretation may apply from:

```text id="hwnwrm"
approval date

specified legal period

historical period under review.
```

Tenant scope and temporal scope SHALL both be explicit.

---

# 174. Tenant Overlay Time

A tenant-specific interpretation overlay may be active:

```text id="ja619t"
[T1,T2)
```

without altering platform-shared interpretation history.

---

# 175. Override Time

A human override from ADR-REG-0004 SHALL carry:

```text id="4sw3fd"
effective period

expires_at

decision/reference scope.
```

No indefinite override by omission.

---

# 176. Override Expiry

At expiry:

```text id="t2ksb9"
canonical underlying rule
```

resumes unless a new approved state exists.

---

# 177. Waiver / Exemption Time

Legal exemptions or waivers SHALL carry:

```text id="r4chah"
valid_from

valid_to

revoked_at?

conditions.
```

---

# 178. Exemption Historical Replay

If exemption revoked today but was valid when shipment occurred:

```text id="32lv8v"
historical replay
```

must recognise the old exemption.

---

# 179. Licence / Permit Time

Regulatory evidence such as licences SHALL represent:

```text id="jvdhzz"
issue time

effective period

expiry

suspension

revocation.
```

---

# 180. Permit Renewal

Renewal SHOULD ordinarily create:

```text id="xjjuso"
new evidence/version
```

rather than extend old evidence silently.

---

# 181. Classification Scheme Time

HS and similar classification schemes change by edition/version.

A product classification SHALL include:

```text id="1fo8t0"
scheme

scheme version

classification period.
```

---

# 182. Tariff Time

Tariff rates may change independently from:

```text id="44ig87"
classification identity.
```

The tariff rule SHALL therefore be separately effective-dated.

---

# 183. Rate at Transaction Time

A tariff calculation SHALL use:

```text id="vqf4w9"
rate legally applicable
at the rule-defined customs event time.
```

---

# 184. FX and External Reference Time

If calculations use:

```text id="1ro9p1"
FX

reference prices

indices
```

their observation/effective times SHALL be preserved separately from regulatory-rule validity.

---

# 185. Time Zone at Borders

Cross-border events may occur across time zones.

Canonical event timestamps SHOULD use:

```text id="932btv"
timezone-aware timestamps
```

while preserving relevant local civil date where legal thresholds depend on local date.

---

# 186. Daylight-Saving Changes

Where a jurisdiction observes daylight-saving time, legal deadline calculation SHALL use:

```text id="9d5u3v"
appropriate named timezone / calendar rules
```

not fixed offsets if DST matters.

PostgreSQL uses the IANA timezone database for named time zones.

---

# 187. Business-Day Calendar Versioning

If deadline rules use business days:

```text id="m794nf"
holiday calendar
```

must be versioned/effective-dated.

A later-added public holiday may affect calculation.

---

# 188. Calendar Provenance

Deadline calculation SHALL identify:

```text id="pvlhzn"
calendar version

timezone

adjustment convention.
```

---

# 189. Temporal Dependency Graph

The Regulatory Knowledge Graph SHALL support:

```text id="l98hyv"
Rule R2
SUPERSEDES
Rule R1

Amendment A
CHANGES
Provision P

Proclamation C
COMMENCES
Provision P.
```

---

# 190. Temporal Graph Queries

Examples:

```text id="8as10o"
What rules were active on date T?

What changed between T1 and T2?

Which future changes are already known?

What did Baobab know as of K?

Which decisions used superseded rule versions?
```

---

# 191. Temporal Diff

Baobab SHOULD support a temporal difference capability:

```text id="1ap5je"
RegulatoryState(T1)
   vs
RegulatoryState(T2).
```

---

# 192. Semantic Diff

The useful output should identify:

```text id="08x4gp"
rule added

rule removed

threshold changed

requirement added

exception narrowed

rate changed

effective date changed.
```

Not merely:

```text id="m5kcha"
text changed.
```

---

# 193. Change Detection versus Temporal Truth

ADR-REG-0023 will detect changes.

This ADR determines:

```text id="thg9jj"
how their temporal effects are represented.
```

---

# 194. Out-of-Order Events

Source events may arrive out of order.

Example:

```text id="prfc4h"
repeal source ingested

later original amendment discovered.
```

The temporal model SHALL permit insertion of historical events without rewriting knowledge time.

---

# 195. Event Ordering

Baobab SHALL distinguish:

```text id="3yvldo"
legal chronological order
```

from:

```text id="cqvwbv"
ingestion/knowledge order.
```

---

# 196. Same-Day Multiple Changes

Multiple instruments may affect one provision on the same date.

Akoma Ntoso explicitly treats different modifying documents on the same date as distinct lifecycle events.

Baobab SHALL preserve event identity and precedence rather than assuming date alone establishes ordering.

---

# 197. Intra-Day Ordering

Where order within the same day matters:

```text id="zukqm3"
publication number

specified commencement time

legal precedence

source sequence
```

may need interpretation.

If unresolved:

```text id="s66tyr"
REVIEW_REQUIRED.
```

---

# 198. Temporal Conflict

Potential conflict types include:

```text id="84yt9c"
OVERLAPPING_VERSIONS

UNKNOWN_COMMENCEMENT

CONFLICTING_EFFECTIVE_DATES

GAP_IN_VERSION_CHAIN

RETROACTIVE_CORRECTION

CONFLICTING_REPEAL_DATE

UNKNOWN_SUSPENSION_END.
```

---

# 199. Temporal Conflict Is First-Class

It SHALL not be auto-fixed with:

```text id="p35mg4"
MAX(date)
```

or:

```text id="ij47zs"
latest record wins.
```

---

# 200. Temporal Integrity Checks

The domain SHOULD validate:

```text id="9w9a7a"
start < end

no impossible period

no forbidden overlap

known causal source

consistent supersession

valid precision

knowledge interval monotonicity.
```

---

# 201. Knowledge Period Monotonicity

A later knowledge version cannot begin before:

```text id="6rt5f3"
its predecessor was recorded
```

without an explicit data-repair process preserving audit history.

---

# 202. Legal Period Need Not Be Monotonic

A newly discovered historical rule can have:

```text id="w0ugjc"
legal_valid_from
```

far earlier than previous records.

That is expected.

---

# 203. Temporal Referential Integrity

Where object B depends on version A for a period:

```text id="mtn08g"
B's period
```

SHOULD be validated against the relevant periods of A where semantics require.

---

# 204. PostgreSQL 17 Referential Limitation

Because PostgreSQL 17 does not provide the PostgreSQL 18 `PERIOD` temporal foreign-key feature, some temporal referential integrity SHALL be enforced through application/domain constraints and tests.

---

# 205. Temporal Service Boundary

Baobab SHOULD centralise domain-level temporal resolution logic rather than allowing every repository query to reinvent:

```text id="48bwod"
current valid version.
```

---

# 206. Example Resolver

Conceptually:

```text id="n8m8bn"
TemporalResolver.resolve(
    subject,
    legal_time,
    knowledge_time,
    context
)
```

---

# 207. Resolver Shall Be Deterministic

For a fixed:

```text id="onxi0n"
database snapshot

legal time

knowledge time

context
```

temporal resolution SHALL be deterministic.

---

# 208. Resolver Shall Not Use Wall Clock Invisibly

Functions SHALL avoid hidden:

```text id="vwbdmt"
NOW()
```

for consequential historical queries.

Current time SHOULD be supplied explicitly or through well-defined query context.

---

# 209. Testability

Tests SHALL use fixed clocks.

---

# 210. Temporal Clock Service

Application runtime MAY use:

```text id="hryhe3"
ClockPort
```

or equivalent to avoid uncontrolled system-clock dependencies.

---

# 211. Clock Skew

Distributed processing timestamps MAY differ slightly.

Knowledge-time assignment for canonical promotion SHOULD come from:

```text id="hxp9q7"
authoritative database/service transaction boundary
```

rather than arbitrary worker clocks.

---

# 212. Database Time

Canonical `recorded_at` MAY use PostgreSQL transaction time/current timestamp semantics at the commit boundary.

Implementation details SHALL be documented.

---

# 213. Event Time versus Processing Time

Domain events SHALL support both where relevant:

```text id="ekr4ng"
occurred_at

recorded_at

published_at.
```

---

# 214. Event Replay

Replaying a domain event SHALL NOT change its original:

```text id="jibpsg"
occurred_at.
```

New processing time may be separately recorded.

---

# 215. Outbox Event

Transactional outbox events SHOULD carry:

```text id="9g3upw"
canonical version

legal-effective period

recorded_at

event type.
```

---

# 216. Pulse Temporal Boundary

Pulse may ask Regulations:

```text id="02odrj"
What regulatory changes became legally effective between T1 and T2?
```

or:

```text id="4el9iy"
What changes did Baobab first learn between K1 and K2?
```

These are different analytics.

---

# 217. Pulse Signal Discovery Time

Pulse's discovery timestamp SHALL not overwrite Regulations':

```text id="q1yp92"
legal event time.
```

---

# 218. Regulations → Pulse Change Event

A verified change projection SHOULD expose:

```text id="li00rf"
legal_effective_from

published_at

verified_at

recorded_at
```

where available.

This allows Pulse to analyse:

```text id="dw5v9n"
legal impact

information lag

commercial reaction lag.
```

---

# 219. CMS Temporal Boundary

CMS may need:

```text id="upkb8l"
current publishable explanation
```

and:

```text id="81tguy"
future-effective notice.
```

Regulations SHALL expose temporal status explicitly.

---

# 220. CMS Article Staleness

A CMS article referencing:

```text id="19z1zf"
RuleVersion R1
```

can be flagged when:

```text id="nu73yg"
R2 supersedes R1
```

or when a known future-effective version approaches.

---

# 221. Scheduled Publishing Opportunity

CMS MAY schedule explanatory content for:

```text id="sihz8e"
future effective date.
```

But Regulations remains the temporal authority.

---

# 222. Known Future Change Event

Potential event:

```text id="74xyn3"
regulation.rule.future_effective_registered
```

could allow:

```text id="h58lev"
Pulse preparation

CMS editorial planning

Trade readiness.
```

---

# 223. Future Effective Activation Event

When legal time crosses the effective boundary, the system MAY emit:

```text id="2wkqfp"
regulation.rule.became_effective
```

for downstream convenience.

The canonical state remains query-driven.

---

# 224. Historical Decision API

Potential:

```text id="yfrn5o"
GET /decisions/{id}/replay
```

with modes:

```text id="00qbkk"
as-known

restated-current-knowledge.
```

---

# 225. Time-Travel Rule API

Potential:

```text id="6ghm1p"
GET /rules/{id}
    ?legal_at=T
    &known_at=K
```

---

# 226. Regulatory State API

Potential:

```text id="2ncmc9"
POST /regulatory-state/resolve
```

with:

```text id="be3yjw"
jurisdiction

context

legal_at

known_at.
```

---

# 227. Temporal Explainability

Every temporal result SHOULD answer:

```text id="5ijle1"
Why is this version active?

Which event started it?

Which event ended the prior version?

When did Baobab learn that?
```

---

# 228. Human-Readable Temporal Explanation

Example:

> Rule R17 became legally effective on 1 September 2026 under Gazette Notice N. Baobab first acquired the notice on 14 September and published the verified RuleVersion on 15 September. This decision, made on 10 September, therefore did not use R17 in its historical-as-known ruleset; a current restatement indicates R17 was legally applicable.

This is exactly the distinction the bitemporal architecture must preserve.

---

# 229. Decision Impact Classification

Late-discovered law MAY create:

```text id="rm6hoe"
HISTORICAL_KNOWLEDGE_GAP.
```

---

# 230. Knowledge Gap Does Not Automatically Mean System Fault

Possible causes:

```text id="fa4ycr"
late official publication access

source outage

provider delay

Baobab ingestion failure

verification backlog.
```

The provenance chain determines cause.

---

# 231. Knowledge Lag Metric

Baobab SHOULD measure:

```text id="zbp0ay"
knowledge_lag =
canonical_verified_at
-
official_publication_or_availability_time
```

where meaningful.

---

# 232. Legal Effect Lag

Separate:

```text id="zjkujb"
effective_at
-
published_at.
```

A future-effective law may have positive preparation lead time.

---

# 233. Negative Knowledge Lag Is Impossible

Baobab cannot verify an authoritative publication before it exists unless using:

```text id="a70z0o"
draft/scenario information.
```

Those states SHALL remain non-binding.

---

# 234. Change Preparedness

Known future-effective law enables:

```text id="hwb98n"
precompile rules

notify tenants

update CMS content

simulate commercial impact

test operational readiness.
```

---

# 235. Precompiled Future Rule

Baobab MAY compile a verified future rule before it becomes active.

The compiled artefact SHALL carry:

```text id="v8gkh8"
future legal-valid period.
```

---

# 236. OPA Bundle Timing

Future OPA bundles MAY include future-effective policy if the decision input includes legal time and the rules correctly test effective periods.

Alternatively, active/future bundles may be separated.

The exact strategy belongs to ADR-REG-0016/0019.

---

# 237. No Bundle Activation as Legal Authority

OPA bundle deployment time SHALL NOT define legal commencement.

---

# 238. Example Error to Avoid

Wrong:

```text id="pzqhzu"
rule became law
when OPA bundle deployed.
```

Correct:

```text id="jh7xje"
rule became legally effective
according to source-backed temporal semantics.

OPA bundle deployment
is operational state.
```

---

# 239. Deployment Time

Track separately:

```text id="azw9d8"
compiled_at

deployed_at

loaded_at.
```

---

# 240. Temporal Readiness

If legal rule becomes effective before operational deployment:

```text id="1k6gtn"
READINESS_FAILURE
```

SHALL be observable.

---

# 241. Enforcement Lag

Potential metric:

```text id="n68k8g"
enforcement_readiness_lag =
runtime_ready_at
-
legal_effective_at.
```

This is operational risk.

---

# 242. Future Readiness SLO

Commercial jurisdiction packs MAY later guarantee:

```text id="m2q7hc"
verified machine rule available
within X time of authoritative publication.
```

That is distinct from legal effective time.

---

# 243. Regulatory Change SLA

ADR-REG-0030 may commercialise:

```text id="9w7o4u"
source monitoring latency

verification latency

rule-publication latency.
```

The temporal model enables measurement.

---

# 244. Temporal Audit

The system SHALL be able to answer:

```text id="1besje"
When was this source published?

When did it take effect?

When did Baobab acquire it?

When was it interpreted?

When was the rule promoted?

When was it deployed?

When did the decision occur?
```

---

# 245. Temporal Chain

```text id="qzvwxi"
PUBLISHED
    │
    ▼
LEGAL EFFECT
    │
    ▼
ACQUIRED
    │
    ▼
VERIFIED
    │
    ▼
PROMOTED
    │
    ▼
COMPILED
    │
    ▼
DEPLOYED
    │
    ▼
DECIDED
```

This ordering is NOT guaranteed.

For future-effective law:

```text id="y6weuq"
PUBLISHED
→ ACQUIRED
→ VERIFIED
→ PROMOTED
→ COMPILED
→ DEPLOYED
→ LEGAL EFFECT
```

may be correct.

---

# 246. Temporal State Must Allow Both Orders

The schema SHALL not assume:

```text id="zmf91a"
effective_at <= acquired_at.
```

---

# 247. Temporal Data Quality

Potential quality issues:

```text id="3u9tky"
MISSING_START

MISSING_END

CONFLICTING_START

CONFLICTING_END

AMBIGUOUS_TIMEZONE

UNKNOWN_PRECISION

UNRESOLVED_RETROACTIVITY

INCONSISTENT_EVENT_CHAIN.
```

---

# 248. Temporal Verification

Consequential temporal boundaries SHOULD carry:

```text id="5qe7br"
verification_state

basis_refs

reviewer

verified_at.
```

---

# 249. AI Temporal Extraction

AI MAY propose:

```text id="d6apyw"
effective date

repeal date

transition clause

retroactive effect.
```

These remain candidate temporal assertions until verified.

---

# 250. AI SHALL Not Infer Missing Dates as Fact

Example:

```text id="4xibak"
"comes into force as prescribed"
```

cannot be converted automatically into:

```text id="pnnxcb"
publication date.
```

---

# 251. Temporal Language Parsing

The knowledge-processing layer SHOULD eventually recognise patterns such as:

```text id="vdm4rv"
"with effect from"

"commences on"

"shall come into operation"

"applies to transactions entered into after"

"deemed to have come into effect"

"expires on"

"subject to transitional provisions."
```

But extraction remains candidate semantics.

---

# 252. Golden Temporal Cases

Implementation SHOULD include cases covering:

```text id="zhmpf3"
future effective law

late discovery

retroactive law

partial commencement

suspension/resumption

repeal

sunset

grandfathering

transitional provision

late parser correction

future proclamation unknown

historical backfill

same-day amendments

tenant counsel reinterpretation

evidence revocation.
```

---

# 253. Golden Case — Future Effective

```text id="u3vrmx"
Published:
1 September

Effective:
1 January

Known:
1 September

Query 1 October:
not currently applicable

Planning query 10 January:
applicable.
```

---

# 254. Golden Case — Late Discovery

```text id="ogbm77"
Effective:
1 September

Baobab knows:
15 September

Decision:
10 September
```

Historical-as-known:

```text id="n6zqma"
old rule set.
```

Historical-restated:

```text id="ne6oyt"
newly discovered rule applies.
```

---

# 255. Golden Case — Retroactivity

```text id="0g2czv"
Published:
15 September

Expressly effective:
1 September.
```

Baobab records:

```text id="xmla59"
legal_valid_from = 1 Sep

knowledge_from = 15 Sep.
```

---

# 256. Golden Case — Partial Commencement

```text id="je3aj4"
Sections 1–5:
1 Jan

Sections 6–10:
1 Mar.
```

Provision-specific RuleVersions activate separately.

---

# 257. Golden Case — Suspension

```text id="q1cxoi"
Rule valid:
1 Jan–1 Jun

suspended:
1 Mar–1 Apr

resumed:
1 Apr.
```

Temporal query on 15 March returns:

```text id="a7oshg"
SUSPENDED.
```

---

# 258. Golden Case — Grandfathering

```text id="hj6z3l"
New rule:
effective 1 July.

Contract:
signed 15 June.

Transition:
existing contracts governed by old rule.
```

Evaluation after 1 July may still apply the old rule to that contract.

---

# 259. Golden Case — Correction

Baobab records wrong commencement date, later corrects it.

Historical knowledge query before correction returns old belief.

Current restatement returns corrected legal history.

---

# 260. Golden Case — Parser Change

Parser V1 misreads date.

Parser V2 corrects it.

This creates:

```text id="njl3t8"
knowledge correction
```

not:

```text id="am7x1u"
legal amendment.
```

---

# 261. Golden Case — Repeal with Savings

Rule repealed on 1 October.

Savings clause preserves obligations arising before 1 October.

Post-repeal assessment of September transaction continues using old rule where applicable.

---

# 262. Golden Case — Future Unknown Commencement

Act says:

```text id="j94z6v"
effective on date appointed by Minister.
```

No appointment published.

Result:

```text id="2yogns"
PUBLISHED_NOT_IN_FORCE
```

not:

```text id="snsepi"
effective immediately.
```

---

# 263. Golden Case — Same-Day Amendments

Two notices affect the same provision on the same date.

The system retains separate temporal events and resolves legal order from sources/interpretation rather than date sorting alone.

---

# 264. Temporal Architecture Invariants

| ID | Invariant |
|---|---|
| `REG-TIME-I01` | Legal valid time SHALL remain distinct from knowledge time |
| `REG-TIME-I02` | Publication time SHALL not automatically equal commencement time |
| `REG-TIME-I03` | Entry into force SHALL not automatically equal applicability |
| `REG-TIME-I04` | Evaluation time SHALL remain distinct from regulated-event time |
| `REG-TIME-I05` | Current law SHALL be a temporal query, not a destructively maintained record |
| `REG-TIME-I06` | Historical legal versions SHALL not be overwritten |
| `REG-TIME-I07` | Knowledge corrections SHALL preserve prior Baobab knowledge state |
| `REG-TIME-I08` | Late discovery SHALL not be backdated in knowledge time |
| `REG-TIME-I09` | Retroactive legal effect SHALL be explicitly sourced |
| `REG-TIME-I10` | Provision-level commencement SHALL be supported |
| `REG-TIME-I11` | Suspension and repeal SHALL remain distinct |
| `REG-TIME-I12` | Discontinuous validity SHALL be representable |
| `REG-TIME-I13` | Transitional and grandfathering rules SHALL be explicit regulatory semantics |
| `REG-TIME-I14` | Repeal SHALL not automatically erase incurred obligations |
| `REG-TIME-I15` | Historical replay SHALL use historical knowledge state |
| `REG-TIME-I16` | Historical restatement SHALL be distinguishable from historical replay |
| `REG-TIME-I17` | Future-effective verified law SHALL be queryable before commencement |
| `REG-TIME-I18` | Draft law SHALL not enter binding future-effective state |
| `REG-TIME-I19` | Unknown commencement SHALL remain unknown |
| `REG-TIME-I20` | Temporal precision SHALL not be invented |
| `REG-TIME-I21` | Legal civil dates SHALL not be arbitrarily converted to UTC timestamps |
| `REG-TIME-I22` | Temporal boundaries SHALL retain provenance |
| `REG-TIME-I23` | Parser/source corrections SHALL remain distinguishable from legal amendments |
| `REG-TIME-I24` | Authority/regime relationships SHALL be effective-dated |
| `REG-TIME-I25` | OPA deployment time SHALL not define legal effective time |
| `REG-TIME-I26` | Temporal state SHALL survive framework/provider replacement |
| `REG-TIME-I27` | Downstream projections SHALL be rebuildable from temporal canonical state |
| `REG-TIME-I28` | Cached decisions SHALL respect legal/evidence validity windows |
| `REG-TIME-I29` | PostgreSQL-version-specific temporal features SHALL not leak into canonical contracts |
| `REG-TIME-I30` | Every consequential temporal query SHALL make its temporal perspective unambiguous |

---

# 265. Rejected Alternative — One `effective_date`

Rejected.

It cannot represent:

```text id="m37lyf"
publication

force

applicability

knowledge

suspension

repeal

retroactivity.
```

---

# 266. Rejected Alternative — `is_active`

Rejected as canonical truth.

```text id="q8ji9n"
active
```

is a time-dependent conclusion.

---

# 267. Rejected Alternative — Latest Row Wins

Rejected.

Latest recording time does not necessarily determine legal state.

---

# 268. Rejected Alternative — Rewrite Old Record

Rejected.

It destroys knowledge history.

---

# 269. Rejected Alternative — Discovery Date = Effective Date

Rejected.

Late discovery is normal in fragmented regulatory environments.

---

# 270. Rejected Alternative — Publication Date = Commencement Date

Rejected as a universal rule.

---

# 271. Rejected Alternative — Repeal Deletes Rule

Rejected.

Historical decisions and savings provisions require old rules.

---

# 272. Rejected Alternative — Repealed Means Irrelevant

Rejected.

Historical and continuing obligations may survive.

---

# 273. Rejected Alternative — Future Draft = Future Law

Rejected.

Drafts remain scenarios until legally enacted/effective.

---

# 274. Rejected Alternative — Current Law Only

Rejected.

It prevents historical replay and audit.

---

# 275. Rejected Alternative — Current Knowledge Rewrites Historical Decisions

Rejected.

Historical-as-known and current-restated analyses answer different questions.

---

# 276. Rejected Alternative — OPA Activation Controls Legal Time

Rejected.

OPA is execution infrastructure.

---

# 277. Rejected Alternative — Scheduler Controls Legal Time

Rejected.

A missed job must not alter what law applies.

---

# 278. Rejected Alternative — One Global Timezone

Rejected for civil-date-sensitive legal events.

---

# 279. Rejected Alternative — PostgreSQL `NOW()` Everywhere

Rejected.

Historical and planning queries require explicit temporal inputs.

---

# 280. Rejected Alternative — PostgreSQL 18 Temporal Syntax on PostgreSQL 17

Rejected.

PostgreSQL 18 introduced native `WITHOUT OVERLAPS` and `PERIOD` temporal constraints; those are not PostgreSQL 17 features.

---

# 281. Minimum Implementation Proof

Before this ADR is considered implemented, Baobab SHOULD demonstrate:

```text id="ky6azf"
1. Legal valid-time range.

2. Knowledge-time range.

3. Current-state query.

4. Historical-as-known query.

5. Historical-restated query.

6. Future-effective query.

7. Late-discovered regulation.

8. Future commencement.

9. Retroactive effect.

10. Repeal.

11. Suspension.

12. Resumption.

13. Sunset/expiry.

14. Partial commencement.

15. Provision-specific commencement.

16. Unknown commencement.

17. Grandfathered transaction.

18. Transitional provision.

19. Savings provision.

20. Historical obligation surviving repeal.

21. Official legal correction.

22. Baobab parser correction.

23. Baobab interpretation correction.

24. Source metadata correction.

25. Multiple knowledge revisions.

26. Same-day multiple amendments.

27. Temporal conflict requiring review.

28. Date-precision state.

29. Timestamp-precision state.

30. Unbounded future validity.

31. Discontinuous validity.

32. Authority succession over time.

33. Regime membership over time.

34. Tenant overlay effective period.

35. Temporary override expiry.

36. Evidence validity and revocation.

37. Classification scheme versioning.

38. Tariff rate effective dates.

39. Deadline/calendar versioning.

40. PostgreSQL range indexing.

41. PostgreSQL exclusion constraint.

42. No dependence on PostgreSQL 18 temporal syntax.

43. Stable RuleSetSnapshot for historical decision.

44. OPA bundle deployment distinct from legal validity.

45. Future rule compiled before commencement.

46. Missed scheduler does not produce wrong temporal query.

47. CMS future-effective projection.

48. Pulse verified-change temporal projection.

49. Knowledge-lag metric.

50. Full bitemporal decision replay.
```

---

# 282. Initial Uganda → South Africa Proof

The first corridor implementation SHOULD prove temporal handling for:

```text id="t7twsq"
HS classification edition changes

customs tariff amendments

permit expiry

SPS certificate validity

rules-of-origin changes

Gazette amendments

future-effective notices

tax-rate changes.
```

Actual rules/dates SHALL come from verified official sources at implementation time.

---

# 283. Initial Scenario

Synthetic architectural example:

```text id="q3ab8p"
South African tariff amendment
published 1 September

effective 1 October

Baobab verifies 3 September

ZuriBeans quotation:
20 September

planned customs entry:
5 October.
```

The assessment on 20 September SHOULD recognise:

```text id="hnnkwk"
current tariff:
old rate

planned 5 October tariff:
new rate.
```

This enables prospective landed-cost assessment without pretending the new rate is already current.

---

# 284. Pulse Opportunity

Pulse may then ask:

```text id="5n2oqd"
What commercial exposure exists
before the 1 October tariff change?
```

Regulations supplies deterministic future-effective legal state.

Pulse supplies commercial analysis.

---

# 285. CMS Opportunity

CMS may publish:

```text id="e40x6r"
"New tariff takes effect 1 October"
```

before commencement, based on the verified future-effective projection.

---

# 286. Trade Opportunity

Trade may reassess:

```text id="vh2w3k"
open quotations

orders

shipments
```

whose expected regulated-event date crosses the new legal boundary.

---

# 287. Strategic Capability — Regulatory Time Machine

The bitemporal model enables a serious enterprise capability:

```text id="d4iwst"
What law applied?

What did we know then?

What do we know now?

What will apply next?
```

These are four different regulatory questions.

Baobab should answer all four.

---

# 288. Strategic Capability — Change Preparedness

Because future-effective law is stored before commencement:

```text id="3go2s8"
Regulations
    ↓
future legal change
    ↓
Trade readiness
CMS preparation
Pulse impact analysis
Customer notification.
```

---

# 289. Strategic Capability — Historical Defence

Years later Baobab can reconstruct:

```text id="61kl8t"
Decision D
was made on K

using legal state T

as known at K.
```

That is much stronger than presenting today's law and pretending it was always known.

---

# 290. Strategic Capability — Corrected Historical Truth

Baobab can also separately report:

```text id="j9xrdj"
With current verified knowledge,
the historical legal result differs.
```

That supports:

```text id="m9ec43"
audit

remediation

legal review

impact analysis.
```

---

# 291. Strategic Capability — Information-Lag Risk

Baobab can measure:

```text id="gt5lns"
publication
→ discovery
→ verification
→ rule publication
→ operational readiness.
```

That creates a measurable regulatory-operations capability.

---

# 292. Commercial Product Implication

Possible commercial features include:

```text id="0fiq57"
Historical Regulatory State API

Future Regulatory State API

Regulatory Change Calendar

Future-Effective Impact Analysis

Regulatory Decision Replay

Historical Restatement

Regulatory Knowledge-Lag Analytics.
```

---

# 293. Research Foundation Summary

LegalRuleML explicitly recognises multiple temporal dimensions of legal norms, including entry into force, efficacy and applicability, and supports time-dependent rule status and validity. This confirms that a regulatory system needs more than a single effective-date field.

Akoma Ntoso models the lifecycle and evolution of legal documents through dated events and temporal data, supports original and consolidated/multiple versions, and links modifying acts to the events they cause.

ELI similarly models legislation with metadata for version dates, entry into force, no-longer-in-force and applicability, as well as amendment, repeal, correction and consolidation relationships.

PostgreSQL 17 provides native date/timestamp range and multirange types, overlap/containment operators, GiST indexing and exclusion constraints, giving Baobab strong primitives for implementing legal-valid intervals and knowledge intervals.

PostgreSQL 18 subsequently introduced native temporal `WITHOUT OVERLAPS` primary/unique constraints and `PERIOD` foreign keys. PostgreSQL's own development history confirms the equivalent feature set was reverted before PostgreSQL 17, so Baobab's PostgreSQL 17 design shall implement temporal referential rules through range/exclusion/domain logic rather than depending on PostgreSQL 18 syntax.

---

# 294. Final Decision

Baobab Regulations SHALL implement a **bitemporal, event-rich regulatory versioning architecture**.

The canonical mental model is:

```text id="gl8adk"
                 LEGAL WORLD
                     │
                     ▼
             publication event
                     │
                     ▼
             commencement event
                     │
                     ▼
             applicability period
                     │
                     ▼
          amendment / suspension /
          repeal / transition events
                     │
                     ▼
              LEGAL VALID TIME


                 BAOBAB WORLD
                     │
                     ▼
                 discovery
                     │
                     ▼
                acquisition
                     │
                     ▼
                verification
                     │
                     ▼
                promotion
                     │
                     ▼
              KNOWLEDGE TIME
```

The bitemporal record answers:

```text id="u4vju1"
LEGAL TIME:
When was this true in law?

KNOWLEDGE TIME:
When did Baobab know it?
```

while the richer temporal domain answers:

```text id="f52z7e"
When was it published?

When did it enter into force?

When did it become applicable?

Was it suspended?

Was it retroactive?

Was it repealed?

Did transitional rules preserve it?

Which event date controls this transaction?
```

The governing rule is:

> **Baobab SHALL never rewrite history merely because its knowledge of history improved.**

The regulatory rule is:

> **The newest database record is not necessarily the law that applies.**

The operational rule is:

> **A regulatory assessment must evaluate the version legally applicable to the relevant event, using an explicit knowledge perspective.**

The audit rule is:

> **Historical replay must reproduce what Baobab knew then; historical restatement must separately show what Baobab now knows was legally true then.**

And the strategic consequence is:

> **Baobab Regulations becomes capable of reasoning across the past, present and already-known regulatory future without confusing any of them.**

That is the architecture established by `ADR-REG-0015`.

---

## Decision Summary

```text id="k96if3"
ADR-REG-0015
────────────────────────────────────────

TWO PRIMARY AXES

LEGAL VALID TIME

"When was this legally true?"

KNOWLEDGE TIME

"When did Baobab know it?"


ADDITIONAL LEGAL TIMES

Publication
Enactment
Commencement
Force
Efficacy
Applicability
Suspension
Repeal
Expiry
Retroactivity
Transition


CORE RULE

Legal time
≠
Knowledge time.


EXAMPLE

Law effective:
1 September

Baobab learns:
15 September

legal_valid_from:
1 September

knowledge_from:
15 September


HISTORICAL AS-KNOWN

What did Baobab know then?


HISTORICAL RESTATED

What do we now know
was legally true then?


FUTURE EFFECTIVE

What currently verified law
will apply in the future?


VERSIONING

Never overwrite
material historical semantics.

Create immutable versions
and temporal assertions.


TRANSITION

Grandfathering and savings
are explicit rule semantics,
not date hacks.


POSTGRESQL 17

daterange
tstzrange
multirange
GiST
exclusion constraints

YES.

PostgreSQL 18
WITHOUT OVERLAPS / PERIOD

NO dependency while
the platform uses PG17.


OPA

Bundle deployment time
≠
legal effective time.


PULSE

Consumes verified temporal
regulatory changes for
commercial impact.


CMS

Consumes current/future
publishable temporal views.


STRATEGIC RESULT

PAST:
What applied?

HISTORY:
What did we know?

PRESENT:
What applies now?

FUTURE:
What will apply?
```