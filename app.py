import traceback
from flask import Flask
from config import Config
from models import db
from auth import auth_bp
from routes import routes_bp


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # TEMPORARY DEBUG: confirms whether the env var is actually reaching
    # the app, without leaking the password. Remove once connection is
    # confirmed working.
    db_uri = app.config.get("SQLALCHEMY_DATABASE_URI", "")
    print("Database URL found:", bool(db_uri))
    if db_uri:
        print("Database URL prefix:", db_uri[:40])

    # Initialize extensions
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(routes_bp)

    # Create tables if they don't exist.
    # Wrapped in try/except so a transient DB issue doesn't crash
    # the whole serverless function on import (which caused every
    # route, including /favicon.ico, to 500). Full traceback is printed
    # so Vercel logs show the real underlying exception instead of a
    # truncated message.
    with app.app_context():
        try:
            db.create_all()
        except Exception:
            traceback.print_exc()

    return app


# Instantiate the application at the module level for WSGI / Vercel
app = create_app()

if __name__ == '__main__':
    print("Starting Student Management System server...")
    app.run(host='127.0.0.1', port=5000, debug=True)
