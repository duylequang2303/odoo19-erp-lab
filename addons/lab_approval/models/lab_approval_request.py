from odoo import api, fields, models
from odoo.exceptions import UserError

APPROVAL_THRESHOLD = 5_000_000


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
    amount = fields.Float(string="Số tiền (VND)", digits=(14, 2), tracking=True)
    description = fields.Text(string="Mô tả")
    date_request = fields.Date(
        string="Ngày tạo", default=fields.Date.context_today, tracking=True
    )
    state = fields.Selection(
        [
            ("draft", "Nháp"),
            ("submitted", "Chờ duyệt TP"),
            ("manager_approved", "Chờ duyệt GĐ"),
            ("approved", "Đã duyệt"),
            ("rejected", "Từ chối"),
        ],
        string="Trạng thái",
        default="draft",
        tracking=True,
        copy=False,
    )
    need_director = fields.Boolean(
        string="Cần Giám đốc duyệt",
        compute="_compute_need_director",
        store=True,
        tracking=True,
    )

    _sql_constraints = [
        (
            "name_unique",
            "unique(name)",
            "Tên phiếu đề xuất đã tồn tại, vui lòng đặt tên khác.",
        )
    ]

    @api.depends("amount")
    def _compute_need_director(self):
        for rec in self:
            rec.need_director = rec.amount >= APPROVAL_THRESHOLD

    @api.constrains("amount")
    def _check_amount_positive(self):
        for rec in self:
            if rec.amount <= 0:
                raise UserError(
                    "Số tiền đề xuất phải lớn hơn 0 (VND). Vui lòng kiểm tra lại."
                )

    def _new_approver_activity(self, summary):
        approver_group = (
            self.env.ref("lab_base.group_lab_director")
            if self.need_director
            else self.env.ref("lab_base.group_lab_manager")
        )
        for rec in self:
            for user in approver_group.users:
                self.env["mail.activity"].create(
                    {
                        "res_model_id": self.env["ir.model"]._get_id(
                            "lab.approval.request"
                        ),
                        "res_id": rec.id,
                        "user_id": user.id,
                        "activity_type_id": self.env.ref(
                            "mail.mail_activity_data_todo"
                        ).id,
                        "summary": summary,
                        "note": rec.name,
                    }
                )

    def _done_activities(self):
        activities = self.env["mail.activity"].search(
            [("res_id", "in", self.ids), ("res_model", "=", self._name)]
        )
        activities.action_done()

    def action_submit(self):
        self.write({"state": "submitted"})
        self._new_approver_activity("Cần duyệt phiếu đề xuất")

    def action_manager_approve(self):
        for rec in self:
            if rec.need_director:
                rec.write({"state": "manager_approved"})
            else:
                rec.write({"state": "approved"})
                rec._done_activities()

    def action_director_approve(self):
        self.write({"state": "approved"})
        self._done_activities()

    def action_reject(self):
        self.write({"state": "rejected"})
        self._done_activities()

    def action_reset_to_draft(self):
        self.write({"state": "draft"})
