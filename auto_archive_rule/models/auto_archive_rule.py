import logging
from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.tools.safe_eval import safe_eval

_logger = logging.getLogger(__name__)


class AutoArchiveRule(models.Model):
    _name = 'auto_archive.rule'
    _description = 'Auto-Archive Rule'
    _order = 'model_name'

    name = fields.Char(compute='_compute_name', store=True)
    model_id = fields.Many2one(
        'ir.model', string='Model', required=True, ondelete='cascade',
        domain=[('transient', '=', False)],
    )
    model_name = fields.Char(string='Model (technical name)', related='model_id.model', store=True, readonly=True)
    days = fields.Integer(
        string='Inactive for (days)', required=True, default=90,
        help="Records whose reference date is older than this many days are archived.",
    )
    date_field_id = fields.Many2one(
        'ir.model.fields', string='Based on date field', ondelete='cascade',
        domain="[('model_id', '=', model_id), ('ttype', 'in', ['date', 'datetime']), ('store', '=', True)]",
        help="Leave empty to use the record's last update date (write_date).",
    )
    date_field_name = fields.Char(related='date_field_id.name', store=True, readonly=True)
    extra_domain = fields.Char(
        string='Extra filter (domain)',
        help="Optional additional Odoo domain, e.g. [('stage_id.is_won', '=', False)]. "
             "Only matching records are considered.",
    )
    active = fields.Boolean(default=True)
    last_run = fields.Datetime(readonly=True, copy=False)
    last_run_count = fields.Integer(readonly=True, copy=False, string='Archived Last Run')

    @api.depends('model_id.name', 'days')
    def _compute_name(self):
        for rule in self:
            if rule.model_id:
                rule.name = _("%(model)s: inactive %(days)s+ days", model=rule.model_id.name, days=rule.days)
            else:
                rule.name = _("New Rule")

    @api.constrains('model_id')
    def _check_model_has_active_field(self):
        for rule in self:
            if rule.model_id and 'active' not in self.env[rule.model_id.model]._fields:
                raise ValidationError(_(
                    "The model %(model)s has no 'Active' field, so records of this "
                    "model cannot be archived.", model=rule.model_id.name,
                ))

    def _run_one(self):
        self.ensure_one()
        Model = self.env[self.model_name]
        if 'active' not in Model._fields:
            _logger.warning("auto_archive_rule: model %s has no 'active' field, skipping rule %s", self.model_name, self.id)
            return 0
        date_field = self.date_field_name or 'write_date'
        threshold = fields.Datetime.now() - timedelta(days=self.days)
        domain = [(date_field, '<=', threshold), ('active', '=', True)]
        if self.extra_domain:
            try:
                extra = safe_eval(self.extra_domain)
                if extra:
                    domain += extra
            except Exception:
                _logger.warning("auto_archive_rule: invalid extra_domain on rule %s: %r", self.id, self.extra_domain)
        records = Model.sudo().search(domain)
        count = len(records)
        if count:
            records.write({'active': False})
        self.write({'last_run': fields.Datetime.now(), 'last_run_count': count})
        return count

    @api.model
    def _run_all(self):
        for rule in self.search([('active', '=', True)]):
            try:
                rule._run_one()
            except Exception:
                _logger.exception("auto_archive_rule: failed to run rule %s", rule.id)

    def action_run_now(self):
        for rule in self:
            rule._run_one()
        return True
