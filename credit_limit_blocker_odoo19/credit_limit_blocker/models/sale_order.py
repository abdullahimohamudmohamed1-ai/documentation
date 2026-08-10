from odoo import fields, models, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        for order in self:
            if order.state in ("draft", "sent"):
                order._check_credit_limit()
        return super().action_confirm()

    def _check_credit_limit(self):
        self.ensure_one()

        if self.env.user.has_group(
            "credit_limit_blocker.group_credit_limit_manager"
        ):
            return

        partner = self.partner_id.commercial_partner_id
        limit = partner.credit_limit

        # 0 means credit blocking is disabled for this customer.
        if not limit:
            return

        current = max(partner.credit, 0.0)

        order_amount = self.currency_id._convert(
            self.amount_total,
            self.company_id.currency_id,
            self.company_id,
            self.date_order.date() if self.date_order else fields.Date.context_today(self),
        )

        exposure = current + order_amount

        if exposure > limit:
            raise UserError(_(
                "CREDIT LIMIT EXCEEDED\n\n"
                "Customer: %(customer)s\n"
                "Credit Limit: %(limit).2f\n"
                "Current Credit: %(current).2f\n"
                "Sales Order: %(order).2f\n"
                "Total Exposure: %(exposure).2f\n"
                "Excess: %(excess).2f\n\n"
                "This Sales Order cannot be confirmed.",
                customer=partner.display_name,
                limit=limit,
                current=current,
                order=order_amount,
                exposure=exposure,
                excess=exposure - limit,
            ))
