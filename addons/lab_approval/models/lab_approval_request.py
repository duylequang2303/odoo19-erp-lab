from odoo import api, fields, models
from odoo.exceptions import UserError


class LabApprovalRequest(models.Model):
    _name = "lab.approval.request"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Phiếu đề xuất mua sắm"
    _order = "create_date desc"

    name = fields.Char(string="Tên phiếu đề xuất", required=True, tracking=True)
    requester_id = fields.Many2one(
        "res.users",
        string="Người đề xuất",
        default=lambda self: self.env.user,
        tracking=True,
    )
    department = fields.Char(string="Phòng ban", tracking=True)
    amount = fields.Float(string="Số tiền (VND)", digits=(12, 2), tracking=True)
    description = fields.Text(string="Mô tả")
    date_request = fields.Date(
        string="Ngày tạo", default=fields.Date.context_today, tracking=True
    )
    state = fields.Selection(
        [
            ("draft", "Nháp"),
            ("submitted", "Chờ duyệt"),
            ("approved", "Đã duyệt"),
            ("rejected", "Từ chối"),
        ],
        string="Trạng thái",
        default="draft",
        tracking=True,
        copy=False,
    )

    _sql_constraints = [
        (
            "name_unique",
            "unique(name)",
            "Tên phiếu đề xuất đã tồn tại, vui lòng đặt tên khác.",
        )
    ]

    @api.constrains("amount")
    def _check_amount_positive(self):
        for rec in self:
            if rec.amount <= 0:
                raise UserError(
                    "Số tiền đề xuất phải lớn hơn 0 (VND). Vui lòng kiểm tra lại."
                )

    def action_submit(self):
        """Gửi phiếu đi duyệt."""
        self.write({"state": "submitted"})

    def action_approve(self):
        """Duyệt phiếu."""
        self.write({"state": "approved"})

    def action_reject(self):
        """Từ chối phiếu."""
        self.write({"state": "rejected"})

    def action_reset_to_draft(self):
        """Trả về nháp để chỉnh sửa."""
        self.write({"state": "draft"})
