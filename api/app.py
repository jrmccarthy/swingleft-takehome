from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS, cross_origin
from models import db, VoterRegDeadline
from engine import get_row, get_rows, CONNECTION_STRING

app = Flask("swingleft")
app.config["SQLALCHEMY_DATABASE_URI"] = CONNECTION_STRING
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
db.init_app(app)

@app.route("/")
def home():
    return "<p>Homepage</p>"

@app.route("/api")
def api_home():
    return "<p>API Home</p>"

@app.route("/api/voter_reg_deadline", methods=['GET'])
def voter_reg_deadline_list():
    filter_by = request.args.get("filter_by")
    filter_op = request.args.get("filter_op")
    filter_value = request.args.get("filter_value")
    order_by = request.args.get("order_by")
    sort_order = request.args.get("sort_order")
    order_attr = getattr(VoterRegDeadline, order_by or "", None)

    if filter_by and filter_op and filter_value:
        rows = get_rows(db.engine, filter_by=filter_by, filter_op=filter_op, filter_value=filter_value, order_by=order_attr, sort_order=sort_order)
    else:
        rows = get_rows(db.engine, order_by=order_attr, sort_order=sort_order)
    if rows:
        return jsonify([row.serialize() for row in rows])
    else:
        return jsonify({})
        

@app.route("/api/voter_reg_deadline/<id>", methods=['GET'])
def voter_reg_deadline_get(id):
    row = get_row(db.engine, id)
    if row:
        return jsonify(row.serialize())
    else:
        return jsonify({})