import requests
import base64

from app import app
CLIENT_ID = ""
APP_SECRET  = app.secret_key
base = "https://api-m.sandbox.paypal.com"

# create an order
async def create_order():
  purchase_amount = "100.00" # TODO: pull amount from a database or session
  access_token = await generate_access_token()
  url = f"{base}/v2/checkout/orders"
  response = requests.post(url, json={
    "intent": "CAPTURE",
    "purchase_units": [
      {
        "amount": {
          "currency_code": "USD",
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
async def capture_payment(order_id):
  access_token = await generate_access_token()
  url = f"{base}/v2/checkout/orders/{order_id}/capture"
  response = requests.post(url, headers={
    "Content-Type": "application/json",
    "Authorization": f"Bearer {access_token}"
  })
  data = response.json()
  return data

# generate an access token
async def generate_access_token():
  auth = base64.b64encode(f"{CLIENT_ID}:{APP_SECRET}".encode("utf-8")).decode("utf-8")
  response = requests.post(f"{base}/v1/oauth2/token",
                           data="grant_type=client_credentials",
                           headers={"Authorization": f"Basic {auth}"})
  json_data = handle_response(response)
  return json_data["access_token"]

# generate a client token
async def generate_client_token():
  access_token = await generate_access_token()
  response = requests.post(f"{base}/v1/identity/generate-token",
                           headers={
                             "Authorization": f"Bearer {access_token}",
                             "Accept-Language": "en_US",
                             "Content-Type": "application/json"
                           })
  print("response", response.status_code)
  json_data = handle_response(response)
  return json_data["client_token"]

async def handle_response(response):
  if response.status in (200, 201):
    return response.json()

  error_message = await response.text()
  raise Exception(error_message)