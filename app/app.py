import os
from datetime import datetime, timezone

from flask import Flask, jsonify


def create_app() -> Flask:
    app = Flask(__name__)

    @app.get("/")
    def index():
        return jsonify(
            {
                "app": "Docker Container Hardening Lab",
                "message": "Container security learning lab is running.",
                "status": "ok",
            }
        )

    @app.get("/health")
    def health():
        return jsonify(
            {
                "status": "healthy",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        )

    @app.get("/config-demo")
    def config_demo():
        return jsonify(
            {
                "environment": os.getenv("APP_ENV", "development"),
                "debug_mode": os.getenv("FLASK_DEBUG", "0") == "1",
                "note": "No secrets are stored in this demo endpoint.",
            }
        )

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
