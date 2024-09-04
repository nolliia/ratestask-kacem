from flask import Blueprint, request, jsonify, Response
from app.services import get_price_averages

bp = Blueprint("main", __name__)


@bp.route("/rates", methods=["GET"])
def rates():
    date_from = request.args.get("date_from")
    date_to = request.args.get("date_to")
    origin = request.args.get("origin")
    destination = request.args.get("destination")

    result = get_price_averages(date_from, date_to, origin, destination)

    if isinstance(result, tuple):
        return jsonify({"Error": result[0]}), result[1]

    return Response(result, content_type="application/json; charset=utf-8")
