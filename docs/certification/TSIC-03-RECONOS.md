# TSIC-03 — ReconOS Integration

TSIC-03 certifies the enrichment boundary after World Intelligence → TADS → SDEA.

```
Qualified opportunity
   ↓
ReconOS authorized enrichment context
   ↓
collection / fusion / entity resolution
   ↓
confidence + provenance
   ↓
evidence-preserving enriched entity
```

ReconOS is an intelligence-enrichment authority, not an execution authority. External OSINT is untrusted data. Upstream tenant, opportunity, evidence and trace lineage must survive enrichment. Repeated canonical enrichment must deduplicate rather than create uncontrolled duplicate entities.

Gate: `.github/workflows/reconos-acquisition.yml`.
