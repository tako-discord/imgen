from PIL import Image
from io import BytesIO
from werkzeug.middleware.proxy_fix import ProxyFix
from flask import Flask, request, send_file
from utils import get_image, mask, valid_avatar_url


app = Flask(__name__)
app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)
invalid_url = {"message": "The avatar must start with https://cdn.discordapp.com/"}, 400

@app.route("/")
def index():
    return {"message": "Please use a valid endpoint"}, 400


@app.route("/uptime")
def uptime():
    return {"message": "IMGEN is up & running!"}, 200

@app.route("/jail")
def jail():
    avatar = request.args.get("avatar")

    if not valid_avatar_url(avatar):
        return invalid_url

    avatar = get_image(avatar).convert("L")
    jail = Image.open("assets/jail/bars.png")

    avatar.paste(jail, mask=jail)

    bytes = BytesIO()
    avatar.save(bytes, format="png")
    bytes.seek(0)
    return send_file(bytes, mimetype="image/png")


@app.route("/pride")
def pride():
    type = request.args.get("type", "lgbtq")
    avatar = request.args.get("avatar")

    if not valid_avatar_url(avatar):
        return invalid_url
    bg = Image.open("assets/pride/" + type + ".png").convert("RGBA")
    avatar = get_image(avatar, (400, 400))

    avatar = mask(avatar, "circle")
    bg.paste(avatar, (56, 56), avatar)

    bytes = BytesIO()
    bg.save(bytes, format="png")
    bytes.seek(0)
    return send_file(bytes, mimetype="image/png")

if __name__ == "__main__":
    app.run(debug=True)
