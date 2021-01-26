import string
import random
from flask import Flask, jsonify, request, abort, redirect
from faunadb import query as q
from faunadb.objects import Ref
from faunadb.client import FaunaClient

app = Flask(__name__)
client = FaunaClient(secret="fnAEAcAKliACCJH00BfVSH2dPZ0EIMPWHlMCTbEX")


def generate_id(n=8):
    identifier = ""
    for i in range(n):
        identifier += random.choice(string.ascii_letters)
    return identifier


@app.route("/")
def home():
    return "Welcome to @beducode shortlink server dicebot"


@app.route("/generate/<path:address>/")
def generate(address, params):
    id = generate_id()
    if not (address.startswith("http://") or address.startswith("https://")):
        address = "http://" + address

    client.query(q.create(q.collection("shortlink"), {
        "data": {
            "id": id,
            "url": address,
            "param": params
        }
    }))

    shortlink = request.host_url + id
    return jsonify({"url_id": id, "url": shortlink, "param": params})


@app.route("/<string:url_id>/")
def fetch_original(url_id):
    try:
        url = client.query(
            q.get(q.match(q.index("url_by_id"), url_id)))
    except:
        abort(404)
    return redirect(url["data"]["url"])


if __name__ == "__main__":
    app.run(debug=True)
