from flask import Flask, render_template, request, jsonify
from . import utils


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/graph")
def graph():
    return render_template("graph.html")


@app.route("/process", methods=["POST"])
def process():
    data = request.json

    if not (_expr := data.get("expr")):
        return jsonify({
            "success": False,
            "message": "Missing expr",
            "data": {}
        })

    try:
        parsed_expr = utils.convert_expr(_expr)
        graphed_expr = utils.graph_expr(parsed_expr)

        return jsonify({
            "success": True,
            "message": None,
            "data": {
                "graph": graphed_expr
            }
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e),
            "data": {}
        })
