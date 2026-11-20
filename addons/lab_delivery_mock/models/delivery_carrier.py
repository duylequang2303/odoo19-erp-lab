import requests
from odoo import fields, models
from odoo.exceptions import UserError


class DeliveryCarrier(models.Model):
    _inherit = "delivery.carrier"

    delivery_type = fields.Selection(
        selection_add=[("lab_mock", "Lab Mock API")],
        ondelete={"lab_mock": "cascade"},
    )
    lab_api_version = fields.Selection(
        [("v1", "V1"), ("v2", "V2")],
        string="Phiên bản API",
        default="v1",
    )
    lab_base_url = fields.Char(string="Base URL", default="http://mock:5000")
    lab_token = fields.Char(string="Token")

    def _get_lab_endpoint(self, route=""):
        self.ensure_one()
        base = (self.lab_base_url or "").rstrip("/")
        version = self.lab_api_version or "v1"
        return f"{base}/{version}/{route}".rstrip("/")

    def _lab_request(self, route, payload=None, method="post"):
        url = self._get_lab_endpoint(route)
        headers = {"Authorization": f"Bearer {self.lab_token or ''}"}
        try:
            response = requests.request(
                method, url, json=payload or {}, headers=headers, timeout=5
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            raise UserError(
                "Không kết nối được mock server (timeout sau 5 giây). "
                "Kiểm tra dịch vụ lab_mock_carrier trước khi tạo vận đơn."
            )
        except requests.exceptions.HTTPError as exc:
            raise UserError(f"Dịch vụ trả lỗi {exc.response.status_code}: {exc}")
        except requests.exceptions.RequestException as exc:
            raise UserError(f"Lỗi gọi dịch vụ giao vận mô phỏng: {exc}")

    def lab_mock_rate(self, order):
        data = self._lab_request("shipping/fee", {"weight": order.weight or 0})
        if self.lab_api_version == "v1":
            return {"price": data.get("data", {}).get("fee", 0.0)}
        return {"price": data.get("result", {}).get("price", {}).get("total", 0.0)}

    def lab_mock_send_shipping(self, pickings):
        results = []
        for picking in pickings:
            data = self._lab_request(
                "orders", {"order": picking.name, "partner": picking.partner_id.name}
            )
            tracking = (
                data.get("data", {}).get("tracking")
                or data.get("result", {}).get("tracking_ref")
                or ""
            )
            picking.write({"carrier_tracking_ref": tracking})
            results.append({"exact_price": 0.0, "tracking_number": tracking})
        return results
