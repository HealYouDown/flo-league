from flask import make_response, request, url_for


def set_language_endpoint(lang: str):
    resp = make_response()
    resp.set_cookie("language", value=lang, max_age=60 * 60 * 24 * 365 * 5)

    # redirect to page referred from or landing page if unknown
    resp.headers["location"] = request.referrer or url_for("main.index")

    return resp, 302
