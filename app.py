from io import BytesIO
from utils import get_image, mask
from PIL import Image, ImageSequence
from flask import Flask, Response, request, send_file


app = Flask(__name__)

@app.route("/")
def index():
    return {"message": "Please use a valid endpoint"}, 400


@app.route("/jail")
def jail():
    avatar = request.args.get("avatar")

    if avatar.startswith("https://cdn.discordapp.com/avatars/") == False:
        return {"message": "The avatar must start with https://cdn.discordapp.com/avatars/"}, 400

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

    if avatar.startswith("https://cdn.discordapp.com/avatars/") == False:
        return {"message": "The avatar must start with https://cdn.discordapp.com/avatars/"}, 400
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
