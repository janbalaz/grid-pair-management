from functools import wraps
import time
from flask import Flask, abort
import backend.utils as utils
from backend.grid_manager import GridManager

app = Flask(__name__)
TOKEN = "abc"
GMS = dict(mgm=None, hgm=None)


def owns_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if TOKEN != kwargs['token']:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


@app.route("/<token>")
@owns_token
def hello(token):
    return "Hello World!"


@app.route("/init-grid/<int:obj_count>/<int:x_size>/<int:y_size>/<token>")
@owns_token
def initialize_grid(obj_count, x_size, y_size, token):
    # for example http://localhost:5000/init-grid/10/600/600/abc
    GMS['mgm'] = GridManager(utils.StoreType.matrix, obj_count, x_size, y_size, 40)
    GMS['hgm'] = GridManager(utils.StoreType.hashed, obj_count, x_size, y_size, 40)

    boxes = utils.generate_objects(obj_count, x_size, y_size, 256, 256, 40)

    for box in boxes:
        GMS['mgm'].add_box(box)
        GMS['hgm'].add_box(box)

    return utils.get_grids_json(GMS)


@app.route("/move-objects/<token>")
def move_objects(token):
    times = []
    try:
        for _, gm in GMS.items():
            start = time.time()
            gm.update_boxes()
            times.append(time.time() - start)

        return utils.get_grids_json(GMS, times)
    except (ValueError, TypeError):
        return "{}"


if __name__ == "__main__":
    app.debug = True
    app.run()
