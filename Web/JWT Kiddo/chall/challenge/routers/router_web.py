from flask import Blueprint, render_template, jsonify, request

web = Blueprint("web", __name__)


@web.route("/", methods=["GET"])
def index():
	return render_template("index.html")
