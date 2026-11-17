from flask import Blueprint, jsonify
from services import reports as report_service

reports_bp = Blueprint("reports", __name__)


@reports_bp.route("/reports/overdue", methods=["GET"])
def report_overdue():
    return jsonify(report_service.get_overdue_report())


@reports_bp.route("/reports/summary", methods=["GET"])
def report_summary():
    return jsonify(report_service.get_summary_report())
