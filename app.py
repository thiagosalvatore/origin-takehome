# import sentry_sdk
import os

from flask import Flask, jsonify
from flask_cors import CORS
from werkzeug.exceptions import InternalServerError, NotFound

from origin_takehome.apis.api import origin_test_bp


# from sentry_sdk.integrations.flask import FlaskIntegration
# from werkzeug.exceptions import HTTPException


def make_app():
    environment = os.environ.get("APPLICATION_ENV", "development")

    application = Flask(__name__)
    application.config.from_object("config.default")
    application.config.from_object(f"config.{environment}")

    # TODO: CORS on production only from origin on AWS
    CORS(application)

    # I usually use sentry to capture any kind of exceptions on my code, we could enabled it in here
    # if environment not in ["development", "testing"]:
    #
    #     def before_send(event, hint):
    #         if 'exc_info' in hint:
    #             exc_type, exc_value, tb = hint['exc_info']
    #             if isinstance(exc_value, (HTTPException,)):
    #                 return None
    #         return event
    #
    #     sentry_sdk.init(
    #         dsn=application.config["SENTRY_DSN"],
    #         integrations=[FlaskIntegration()],
    #         environment=environment,
    #         before_send=before_send
    #     )

    application.register_blueprint(origin_test_bp)

    @application.errorhandler(NotFound)
    def handle_404(_):
        return jsonify({"message": "The URL requested doesn't exist"}), 404

    @application.errorhandler(InternalServerError)
    def handle_500(_):
        return jsonify({"message": "Internal Server Error"}), 500

    return application


if __name__ == "__main__":
    app = make_app()
    app.run(host="0.0.0.0")
