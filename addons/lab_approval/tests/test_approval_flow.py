from odoo.tests.common import TransactionCase


class TestApprovalFlow(TransactionCase):
    def setUp(self):
        super().setUp()
        self.Request = self.env["lab.approval.request"]
        self.manager = self.env.ref("lab_base.group_lab_manager").users[:1]
        self.director = self.env.ref("lab_base.group_lab_director").users[:1]

    def _make(self, name, amount):
        return self.Request.create(
            {"name": name, "amount": amount, "department": "Phát triển"}
        )

    def test_below_threshold_manager_only(self):
        rec = self._make("Phiếu dưới 5 triệu", 3_000_000)
        self.assertEqual(rec.state, "draft")
        self.assertFalse(rec.need_director)
        rec.action_submit()
        self.assertEqual(rec.state, "submitted")
        rec.with_user(self.manager).action_manager_approve()
        self.assertEqual(rec.state, "approved")

    def test_above_threshold_needs_director(self):
        rec = self._make("Phiếu trên 5 triệu", 8_000_000)
        self.assertTrue(rec.need_director)
        rec.action_submit()
        rec.with_user(self.manager).action_manager_approve()
        self.assertEqual(rec.state, "manager_approved")
        rec.with_user(self.director).action_director_approve()
        self.assertEqual(rec.state, "approved")

    def test_reject_flow(self):
        rec = self._make("Phiếu bị từ chối", 1_500_000)
        rec.action_submit()
        rec.action_reject()
        self.assertEqual(rec.state, "rejected")
        rec.action_reset_to_draft()
        self.assertEqual(rec.state, "draft")
