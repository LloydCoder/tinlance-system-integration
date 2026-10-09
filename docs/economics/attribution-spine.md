# Economic Attribution Spine

The same execution identity used for governance and telemetry is used for economics. Cost records attach to execution, agent, workspace, organization, service, cost center, and tenant. Revenue records use the same immutable execution and trace identities but are represented as a distinct `entry_type`; costs and revenue must never be conflated in one ledger entry.

## Canonical record

The normative JSON Schema is [contracts/economics/attribution.json](../../contracts/economics/attribution.json). The field and invariant registry is [policies/economic-attribution-baseline.json](../../policies/economic-attribution-baseline.json).

Every attribution record carries:

- Immutable entry and idempotency identities.
- Tenant, organization, workspace, service, agent, and execution context.
- Typed `entry_type` (`cost` or `revenue`), non-negative amount, and currency code.
- Trace and evidence identifiers, source-event identity when available, and occurrence timestamp.
- Meter type and cost center; optional allocation method/ratio for shared costs.

## Accounting and safety invariants

- **Cost and revenue are separate records.** Each record has one `entry_type`; revenue records cannot include `cost_amount`, and cost records cannot include `revenue_amount`.
- **Currency is explicit.** `currency` is an uppercase three-letter code; runtime accounting integrations must validate it against a maintained ISO 4217 registry. A regex alone is not proof of a valid ISO currency.
- **Amounts are non-negative.** Credits, reversals, and refunds must use explicit typed adjustment/reversal semantics rather than silently writing negative amounts.
- **Evidence is mandatory.** Each record includes `evidence_id` and `trace_id`; attribution without source evidence must not be presented as verified.
- **Idempotency is mandatory.** The idempotency key is stable for a logical attribution event and is enforced by the persistence layer to prevent duplicate charges/revenue.
- **Tenant identity is immutable.** Tenant/workspace context is inherited from verified server-side execution context, never trusted from unvalidated client input.
- **Delivery route is explicit.** Engineering, transformation, and domain delivery economics must remain distinguishable.
- **Derived metrics are not ledger facts.** MRR, ACV, and LTV are derived/reporting fields and must not be confused with the underlying event-level amount.

## Certification

Run:

```bash
python3 scripts/certify_economic_attribution.py
python3 scripts/forensic_audit_phase13.py
```

The dedicated workflow checks schema/registry consistency and representative valid and invalid records. It is a contract and conformance gate, not a substitute for an accounting ledger, tax advice, revenue-recognition policy, or external audit.
