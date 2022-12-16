import os
import requests
import flask
from flask import render_template, request, redirect, url_for, jsonify

from app import app
from app import paypalapis as paypal

app.config["DEBUG"] = True


@app.route("/",methods=['GET'])
def render_checkout_page():
  client_id = "AQgM3qUsIoidiTXAnKizmCwNvuzwn9Nwhf0vvEza9A8gpVPW_qhpsk2wzAo7h8pckJE_bSmoQLGoHI0y"
  client_token = paypal.generate_client_token()
  return render_template("checkout.html", client_id = client_id, client_token= client_token)


@app.route("/api/orders", methods=["POST"])
def create_order():
  order = paypal.create_order()
  return jsonify(order)

@app.route("/api/orders/<order_id>/capture", methods=["POST"])
def capture_payment(order_id):
  capture_data = paypal.capture_payment(order_id)
  return jsonify(capture_data)


