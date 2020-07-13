import os

from flask import (Blueprint, current_app, render_template, request,
                   send_from_directory)

main_bp = Blueprint(__name__, "main")


@main_bp.route('/', defaults={'path': ''})
@main_bp.route('/<path:path>')
def index(path: str):
    return render_template("index.html")


@main_bp.route(r"/static/js/<regex('main\.\w{8}.chunk\.js'):fname>")
@main_bp.route(r"/static/js/<regex('\d\.\w{8}.chunk.js'):fname>")
def gzipped_bundle(fname):
    """Returns gzipped version of requested js, if allowed."""
    accept_encoding = request.headers.get('Accept-Encoding', '')
    gzip_supported = "gzip" in accept_encoding

    if gzip_supported:
        fname += ".gz"

    js_directory = os.path.join(current_app.static_folder,
                                "js")

    # Response object
    rv = send_from_directory(js_directory,
                             fname,
                             mimetype="text/javascript")

    # Increase cache timeout (365 days)
    rv.cache_control.max_age = 31536000

    if gzip_supported:
        rv.headers.set("Content-Encoding", "gzip")

    return rv
