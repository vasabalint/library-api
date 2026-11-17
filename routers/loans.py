from flask import Blueprint, jsonify, request
from error_handling import AppError, error_response
from services import loans as loan_service

loans_bp = Blueprint("loans", __name__)


@loans_bp.route("/loans", methods=["GET"])
def list_loans():
    overdue_filter = request.args.get("overdue") == "true"
    result = loan_service.list_loans(overdue_filter=overdue_filter)
    return jsonify(result)


@loans_bp.route("/loans/<int:loan_id>", methods=["GET"])
def get_loan(loan_id):
    try:
        loan = loan_service.get_loan(loan_id)
        return jsonify(loan)
    except AppError as e:
        return error_response(e.message, e.status_code)


@loans_bp.route("/loans", methods=["POST"])
def create_loan():
    data = request.get_json(silent=True) or {}
    try:
        loan = loan_service.create_loan(data)
        return jsonify(loan), 201
    except AppError as e:
        return error_response(e.message, e.status_code)


@loans_bp.route("/loans/<int:loan_id>/return", methods=["POST"])
def return_book(loan_id):
    try:
        updated = loan_service.return_book(loan_id)
        return jsonify(updated)
    except AppError as e:
        return error_response(e.message, e.status_code)


@loans_bp.route("/loans/<int:loan_id>/renew", methods=["POST"])
def renew_loan(loan_id):
    try:
        updated = loan_service.renew_loan(loan_id)
        return jsonify(updated)
    except AppError as e:
        return error_response(e.message, e.status_code)


@loans_bp.route("/loans/<int:loan_id>/pay-fine", methods=["POST"])
def pay_fine(loan_id):
    try:
        updated = loan_service.pay_fine(loan_id)
        return jsonify(updated)
    except AppError as e:
        return error_response(e.message, e.status_code)
