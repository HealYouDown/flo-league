from flask import request, current_app


def get_locale():
    if "language" in request.cookies:
        cookie_lang = request.cookies["language"]
        if cookie_lang in current_app.config["LANGUAGES"]:
            return cookie_lang

    return request.accept_languages.best_match(
        current_app.config["LANGUAGES"])
