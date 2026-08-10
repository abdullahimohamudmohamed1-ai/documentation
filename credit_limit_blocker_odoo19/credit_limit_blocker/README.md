# Credit Limit Blocker — Odoo 19 Enterprise

Features:
- Credit Limit per customer
- Current Credit
- Available Credit
- Hard block on Sales Order confirmation
- Hard block on customer Invoice posting
- Manager override permission

Rules:
- Credit Limit = 0 means blocking is disabled.
- Current Credit uses Odoo's standard posted receivable (`res.partner.credit`).
- Sales Order check: Current Credit + Sales Order total.
- Invoice check: Current Credit + Invoice total.
- Customer refunds are not blocked.
- Users assigned to `Credit Limit Manager (Override)` bypass both blocks.

Installation:
1. Upload/extract the module into your custom addons path, or use Odoo's module ZIP import if enabled.
2. Enable Developer Mode.
3. Apps > Update Apps List.
4. Search `Credit Limit Blocker`.
5. Install.
6. Open a customer and enter Credit Limit.
7. Give the override group only to authorized managers.

Test on a staging/duplicate database before production.
