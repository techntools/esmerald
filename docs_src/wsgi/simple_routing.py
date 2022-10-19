from flask import Flask, request

from esmerald import Esmerald, Gateway, Include, Request, get
from esmerald.middleware import WSGIMiddleware

flask_app = Flask(__name__)


@flask_app.route("/")
def flask_main():
    name = request.args.get("name", "Esmerald")
    return f"Hello, {name} from your Flask integrated!"


@get("/home/{name:str}")
async def home(request: Request) -> dict:
    name = request.path_params["name"]
    return {"name": name}


app = Esmerald(
    routes=[
        Gateway(handler=home),
        Include("/flask", WSGIMiddleware(flask_app)),
    ]
)
