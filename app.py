import string
import random
from flask import Flask, jsonify, request, abort, redirect
from faunadb import query as q
from faunadb.objects import Ref
from faunadb.client import FaunaClient

app = Flask(__name__)
client = FaunaClient(secret="fnAEAcAKliACCJH00BfVSH2dPZ0EIMPWHlMCTbEX")


def generate_id(n=8):
    id = ""
    for i in range(n):
        id += random.choice(string.ascii_letters)
    return id


@app.route("/")
def home():
    return "Welcome to @beducode shortlink server dicebot"


@app.route("/generate/<path:address>/")
def generate(address):
    id = generate_id()
    if not (address.startswith("http://") or address.startswith("https://")):
        address = "http://" + address
        
    shorturl = "https://semawur.com/st/?api=3c4a1e5bff36089e900d4784f7b124b2fc074466&url=" + address

    client.query(q.create(q.collection("shortlink"), {
        "data": {
            "id": id,
            "url": shorturl
        }
        
    }))

    shortlink = request.host_url + id
    return jsonify({"url_id": id, "url": shortlink})


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
