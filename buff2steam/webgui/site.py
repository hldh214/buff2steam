from flask import Flask, render_template, Blueprint, request
from buff2steam.webgui.db import items
import threading

main = Blueprint("main", __name__)

def start_app():
    app = Flask(__name__)
    app.register_blueprint(main)
    app.run(host="0.0.0.0",port=1821)

@main.route("/")
def index():
    return render_template("index.html")

#sorting

@main.route("/sort_buff_up")
def sort_buff_up():
    return render_template("add_items.html", results=items.get_buff_increasing())

@main.route("/sort_buff_down")
def sort_buff_down():
    return render_template("add_items.html", results=items.get_buff_decreasing())

@main.route("/sort_steam_up")
def sort_steam_up():
    return render_template("add_items.html", results=items.get_steam_increasing())

@main.route("/sort_steam_down")
def sort_steam_down():
    return render_template("add_items.html", results=items.get_steam_decreasing())

@main.route("/sort_volume_up")
def sort_volume_up():
    return render_template("add_items.html", results=items.get_volume_increasing())

@main.route("/sort_volume_down")
def sort_volume_down():
    return render_template("add_items.html", results=items.get_volume_decreasing())

@main.route("/sort_ratio_up")
def sort_ratio_up():
    return render_template("add_items.html", results=items.get_ratio_increasing())

@main.route("/sort_ratio_down")
def sort_ratio_down():
    return render_template("add_items.html", results=items.get_ratio_decreasing())

@main.route("/delete_item")
def delete_item():
    item_name = request.args.get("market_hash_name")
    items.delete_item(item_name)
    return render_template("add_items.html", results=items.latest_list())

@main.route("/refresh")
def events():
    return render_template("add_items.html", results=items.latest_list())

flask_thread = threading.Thread(target=start_app)
flask_thread.start()
