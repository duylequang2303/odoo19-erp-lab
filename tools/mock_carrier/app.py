"""Mock server cho carrier Lab Mock (thay thế dịch vụ giao vận thật khi test).

Chạy nhanh:
    pip install flask
    python tools/mock_carrier/app.py
Rồi gọi thử:
    curl -s localhost:5000/v1/shipping/fee -d '{"weight":2}'
    curl -s localhost:5000/v2/shipping/fee -d '{"weight":2}'
"""
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/v1/shipping/fee", methods=["POST"])
def fee_v1():
    weight = request.json.get("weight", 1)
    return jsonify({"code": 0, "data": {"fee": 20000 + weight * 11000, "currency": "VND", "service": "V1-standard"}})


@app.route("/v2/shipping/fee", methods=["POST"])
def fee_v2():
    weight = request.json.get("weight", 1)
    return jsonify({"result": {"price": {"total": 22000 + weight * 11500, "currency": "VND"}, "version": "v2", "eta": "2-3 ngay"}})


@app.route("/v1/orders", methods=["POST"])
def create_v1():
    return jsonify({"code": 0, "data": {"tracking": "MOCKV1-%06d" % 774120}})


@app.route("/v2/orders", methods=["POST"])
def create_v2():
    return jsonify({"result": {"tracking_ref": "MOCKV2-%06d" % 881230, "status": "created"}})


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
