import os
import requests
import flask
from flask import render_template, request, redirect, url_for, jsonify

from app import app
from app import paypalapis as paypal

app.config["DEBUG"] = True


@app.route("/",methods=['GET'])
async def render_checkout_page():
  client_id = os.environ["CLIENT_ID"]
  client_token = await paypal.generate_client_token()
  return render_template("checkout.html", {"client_id": client_id, "client_token": client_token})


@app.route("/api/orders", methods=["POST"])
async def create_order():
  order = await paypal.create_order()
  return jsonify(order)

@app.route("/api/orders/<order_id>/capture", methods=["POST"])
async def capture_payment(order_id):
  capture_data = await paypal.capture_payment(order_id)
  return jsonify(capture_data)


