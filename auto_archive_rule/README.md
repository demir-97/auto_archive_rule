# Auto-Archive Rules

**No-code cleanup for inactive records, on any model.**

Old leads, stale draft quotations, ancient log-like records piling up in
every list view — this module archives them for you, automatically.

## Getting started

Settings > Technical > Auto-Archive Rules: create a rule — pick a model
and how many days of inactivity should trigger archiving. Save. A daily
scheduled action does the rest.

## Options per rule

- **Based on date field**: which date/datetime field counts as "last
  activity". Leave empty to use the record's own last-modified date.
- **Extra filter**: an optional additional domain, e.g. only archive
  records matching `[('stage_id.is_won', '=', False)]`.
- **Run Now**: trigger a rule immediately instead of waiting for the
  daily cron, useful to test a rule before trusting it.
- Each rule remembers when it last ran and how many records it archived.

## Safety

- Only models with an "Active" field can be targeted — Odoo itself stops
  you from picking a model without one.
- Archiving, not deleting: every affected record is one click away from
  being restored.
- Zero rules configured = zero behavior change.

---
Author: Meisanqo — meisanqo@outlook.com
