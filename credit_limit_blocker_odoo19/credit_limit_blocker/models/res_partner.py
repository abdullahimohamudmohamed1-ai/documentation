from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    credit_limit = fields.Monetary(
        string="Credit Limit",
        currency_field="credit_limit_currency_id",
        company_dependent=True,
        help="Maximum customer credit/exposure. Set to 0 to disable blocking."
    )

    credit_limit_currency_id = fields.Many2one(
        "res.currency",
        string="Credit Limit Currency",
        related="company_id.currency_id",
        readonly=True,
    )

    current_credit = fields.Monetary(
        string="Current Credit",
        currency_field="credit_limit_currency_id",
        compute="_compute_credit_values",
        help="Current posted receivable balance."
    )

    available_credit = fields.Monetary(
        string="Available Credit",
        currency_field="credit_limit_currency_id",
        compute="_compute_credit_values",
        help="Credit limit minus current credit."
    )

    @api.depends("credit", "credit_limit")
    def _compute_credit_values(self):
        for partner in self:
            current = max(partner.commercial_partner_id.credit, 0.0)
            partner.current_credit = current
            partner.available_credit = (
                max(partner.credit_limit - current, 0.0)
                if partner.credit_limit
                else 0.0
            )
