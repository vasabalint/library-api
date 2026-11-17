from flask import Blueprint, jsonify, request
from error_handling import AppError, error_response
from services import members as member_service

members_bp = Blueprint("members", __name__)


@members_bp.route("/members", methods=["GET"])
def list_members():
    return jsonify(member_service.list_members())


@members_bp.route("/members/<int:member_id>", methods=["GET"])
def get_member(member_id):
    try:
        member = member_service.get_member(member_id)
        return jsonify(member)
    except AppError as e:
        return error_response(e.message, e.status_code)


@members_bp.route("/members", methods=["POST"])
def create_member():
    data = request.get_json(silent=True) or {}
    try:
        member = member_service.create_member(data)
        return jsonify(member), 201
    except AppError as e:
        return error_response(e.message, e.status_code)


@members_bp.route("/members/<int:member_id>/loans", methods=["GET"])
def member_loans(member_id):
    try:
        summary = member_service.get_member_loans(member_id)
        return jsonify(summary)
    except AppError as e:
        return error_response(e.message, e.status_code)
