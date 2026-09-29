{
    'name': 'Auto-Archive Rules | No-Code Cleanup for Inactive Records',
    'version': '17.0.1.0.0',
    'category': 'Productivity',
    'author': 'Meisanqo',
    'support': 'meisanqo@outlook.com',
    'summary': 'Auto-archive inactive records on any model — no code, from Settings.',
    'description': """
Auto-Archive Rules
=====================

Old leads, stale draft quotations, ancient log-like records piling up in
every list view — this module archives them for you, automatically.

Getting started
----------------

Settings > Technical > Auto-Archive Rules: create a rule — pick a model
and how many days of inactivity should trigger archiving. Save. A daily
scheduled action does the rest.

Options per rule
------------------

- **Based on date field**: which date/datetime field counts as "last
  activity". Leave empty to use the record's own last-modified date.
- **Extra filter**: an optional additional domain, e.g. only archive
  records matching `[('stage_id.is_won', '=', False)]`.
- **Run Now**: trigger a rule immediately instead of waiting for the
  daily cron, useful to test a rule before trusting it.
- Each rule remembers when it last ran and how many records it archived.

Safety
-------

- Only models with an "Active" field can be targeted (that's what makes a
  record disappear from normal views without being deleted) — Odoo
  itself stops you from picking a model without one.
- Archiving, not deleting: every affected record is one click away from
  being restored (its Active field is simply set to False).
- Zero rules configured = zero behavior change.
""",
    'depends': ['base'],
    'images': ['static/description/banner.png'],
    'data': [
        'security/ir.model.access.csv',
        'views/auto_archive_rule_views.xml',
        'data/auto_archive_cron.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
