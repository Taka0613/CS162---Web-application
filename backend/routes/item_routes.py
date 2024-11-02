from flask import Blueprint, request, jsonify, session
from app import db
from models import List, Item
from utils.auth_util import login_required

item_bp = Blueprint("items", __name__)


@item_bp.route("/", methods=["POST"])
@login_required
def create_item():
    data = request.json
    list_id = data.get("list_id")
    parent_item_id = data.get("parent_item_id")
    title = data.get("title")
    lst = List.query.filter_by(list_id=list_id, user_id=session["user_id"]).first()
    if not lst:
        return jsonify({"message": "List not found"}), 404
    if parent_item_id:
        parent_item = Item.query.filter_by(
            item_id=parent_item_id, list_id=list_id
        ).first()
        if not parent_item:
            return jsonify({"message": "Parent item not found"}), 404
    else:
        parent_item = None
    new_item = Item(list_id=list_id, parent_item_id=parent_item_id, title=title)
    db.session.add(new_item)
    db.session.commit()
    return jsonify({"message": "Item created", "item_id": new_item.item_id}), 201


@item_bp.route("/<int:list_id>", methods=["GET"])
@login_required
def get_items(list_id):
    lst = List.query.filter_by(list_id=list_id, user_id=session["user_id"]).first()
    if not lst:
        return jsonify({"message": "List not found"}), 404
    items = Item.query.filter_by(list_id=list_id).all()
    items_data = []
    for item in items:
        items_data.append(
            {
                "item_id": item.item_id,
                "parent_item_id": item.parent_item_id,
                "title": item.title,
                "is_completed": item.is_completed,
            }
        )
    return jsonify({"items": items_data}), 200


@item_bp.route("/<int:item_id>", methods=["PUT"])
@login_required
def update_item(item_id):
    data = request.json
    title = data.get("title")
    is_completed = data.get("is_completed")
    item = Item.query.get(item_id)
    if not item or item.list.user_id != session["user_id"]:
        return jsonify({"message": "Item not found"}), 404
    if title:
        item.title = title
    if is_completed is not None:
        item.is_completed = is_completed
    db.session.commit()
    return jsonify({"message": "Item updated"}), 200


@item_bp.route("/<int:item_id>", methods=["DELETE"])
@login_required
def delete_item(item_id):
    item = Item.query.get(item_id)
    if not item or item.list.user_id != session["user_id"]:
        return jsonify({"message": "Item not found"}), 404
    delete_sub_items(item)
    db.session.commit()
    return jsonify({"message": "Item and sub-items deleted"}), 200


def delete_sub_items(item):
    for sub_item in item.sub_items:
        delete_sub_items(sub_item)
        db.session.delete(sub_item)
    db.session.delete(item)


@item_bp.route("/<int:item_id>/move", methods=["PUT"])
@login_required
def move_item(item_id):
    data = request.json
    new_list_id = data.get("new_list_id")
    item = Item.query.get(item_id)
    new_list = List.query.filter_by(
        list_id=new_list_id, user_id=session["user_id"]
    ).first()
    if not item or not new_list or item.list.user_id != session["user_id"]:
        return jsonify({"message": "Item or list not found"}), 404
    if item.parent_item_id is not None:
        return jsonify({"message": "Only top-level items can be moved"}), 400
    item.list_id = new_list_id
    db.session.commit()
    return jsonify({"message": "Item moved"}), 200


@item_bp.route("/<int:item_id>/complete", methods=["PUT"])
@login_required
def complete_item(item_id):
    item = Item.query.get(item_id)
    if not item or item.list.user_id != session["user_id"]:
        return jsonify({"message": "Item not found"}), 404
    item.is_completed = True
    db.session.commit()
    return jsonify({"message": "Item marked as complete"}), 200
