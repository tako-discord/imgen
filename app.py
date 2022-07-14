from PIL import Image
from io import BytesIO
from utils import get_image, mask
from flask import Flask, Response, request, send_file


app = Flask(__name__)

@app.route("/")
def index():
    return Response({"message": "Please use a valid endpoint"}, 400, mimetype="text/json")

@app.route("/pride")
def pride():
    type = request.args.get("type", "lgbtq")
    avatar = request.args.get("avatar")
    
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
