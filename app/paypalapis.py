import requests
import base64
import json
#from app import app
CLIENT_ID = "AQgM3qUsIoidiTXAnKizmCwNvuzwn9Nwhf0vvEza9A8gpVPW_qhpsk2wzAo7h8pckJE_bSmoQLGoHI0y"
APP_SECRET  = "EMApXQUqkmM1vDGhJd4ukYfaxxl1M0-FzdGbWyI5OjRA6e3vmp-9iprnllQhhw2dQMn_9UW55GcdURNa"
base = "https://api-m.sandbox.paypal.com"

# create an order
def create_order(purchase_amount):
  
  access_token = generate_access_token()
  url = f"{base}/v2/checkout/orders"
  response = requests.post(url, json={
    "intent": "CAPTURE",
    "purchase_units": [
      {
        "amount": {
          "currency_code": "GBP",
          "value": purchase_amount
        },
      },
    ],
  }, headers={
    "Content-Type": "application/json",
    "Authorization": f"Bearer {access_token}"
  })
  data = response.json()
  return data

# capture payment for an order
def capture_payment(order_id):
  access_token = generate_access_token()
  url = f"{base}/v2/checkout/orders/{order_id}/capture"
  response = requests.post(url, headers={
    "Content-Type": "application/json",
    "Authorization": f"Bearer {access_token}"
  })
  data = response.json()
  return data

# generate an access token
def generate_access_token():
  auth = base64.b64encode(f"{CLIENT_ID}:{APP_SECRET}".encode("utf-8")).decode("utf-8")
  response = requests.post(f"{base}/v1/oauth2/token",
                           data="grant_type=client_credentials",
                           headers={"Authorization": f"Basic {auth}"})
  json_data = handle_response(response)
  return json_data["access_token"]

# generate a client token
def generate_client_token():
  access_token = generate_access_token()
  response = requests.post(f"{base}/v1/identity/generate-token",
                           headers={
                             "Authorization": f"Bearer {access_token}",
                             "Accept-Language": "en_US",
                             "Content-Type": "application/json"
                           })
  print("response", response.status_code)
  json_data = handle_response(response)
  return json_data

def handle_response(response):
    if response.status_code in (200, 201):
        return response.json()


    error_message = response.text()
    raise Exception(error_message)

