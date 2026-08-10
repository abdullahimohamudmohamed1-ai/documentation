from odoo import fields, models, _
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = "account.move"

    def action_post(self):
        for move in self:
            if move.move_type == "out_invoice" and move.state == "draft":
                move._check_credit_limit()
        return super().action_post()

    def _check_credit_limit(self):
        self.ensure_one()

        if self.env.user.has_group(
            "credit_limit_blocker.group_credit_limit_manager"
        ):
            return

        partner = self.partner_id.commercial_partner_id
        limit = partner.credit_limit

        # 0 means credit blocking is disabled.
        if not limit:
            return

        current = max(partner.credit, 0.0)

        invoice_amount = self.currency_id._convert(
            self.amount_total,
            self.company_id.currency_id,
            self.company_id,
            self.invoice_date or fields.Date.context_today(self),
        )

        exposure = current + invoice_amount

        if exposure > limit:
            raise UserError(_(
                "CREDIT LIMIT EXCEEDED\n\n"
                "Customer: %(customer)s\n"
                "Credit Limit: %(limit).2f\n"
                "Current Credit: %(current).2f\n"
                "Invoice: %(invoice).2f\n"
                "Total Exposure: %(exposure).2f\n"
                "Excess: %(excess).2f\n\n"
                "This customer invoice cannot be posted.",
                customer=partner.display_name,
                limit=limit,
                current=current,
                invoice=invoice_amount,
                exposure=exposure,
                excess=exposure - limit,
            ))
