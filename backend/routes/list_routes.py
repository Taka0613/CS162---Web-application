from flask import Blueprint, request, jsonify, session
from app import db
from models import List
from utils.auth_util import login_required

list_bp = Blueprint("lists", __name__)


@list_bp.route("/", methods=["POST"])
@login_required
def create_list():
    data = request.json
    title = data.get("title")
    if not title:
        return jsonify({"message": "Title is required"}), 400
    new_list = List(user_id=session["user_id"], title=title)
    db.session.add(new_list)
    db.session.commit()
    return jsonify({"message": "List created", "list_id": new_list.list_id}), 201


@list_bp.route("/", methods=["GET"])
@login_required
def get_lists():
    user_lists = List.query.filter_by(user_id=session["user_id"]).all()
    lists = [{"list_id": lst.list_id, "title": lst.title} for lst in user_lists]
    return jsonify({"lists": lists}), 200


@list_bp.route("/<int:list_id>", methods=["PUT"])
@login_required
def update_list(list_id):
    data = request.json
    title = data.get("title")
    if not title:
        return jsonify({"message": "Title is required"}), 400
    lst = List.query.filter_by(list_id=list_id, user_id=session["user_id"]).first()
    if not lst:
        return jsonify({"message": "List not found"}), 404
    lst.title = title
    db.session.commit()
    return jsonify({"message": "List updated"}), 200


@list_bp.route("/<int:list_id>", methods=["DELETE"])
@login_required
def delete_list(list_id):
    lst = List.query.filter_by(list_id=list_id, user_id=session["user_id"]).first()
    if not lst:
        return jsonify({"message": "List not found"}), 404
    db.session.delete(lst)
    db.session.commit()
    return jsonify({"message": "List deleted"}), 200
