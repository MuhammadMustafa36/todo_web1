import traceback
from flask import Flask
from config import Config
from models import db
from auth import auth_bp
from routes import routes_bp


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # -------------------------------
    # DEBUG: Check database URL
    # -------------------------------
    db_uri = app.config.get("SQLALCHEMY_DATABASE_URI", "")

    print("=" * 60, flush=True)
    print("Application Starting...", flush=True)
    print("Database URL Found:", bool(db_uri), flush=True)

    if db_uri:
        # Only print the first part of the URL (safe)
        print("Database URL Prefix:", db_uri[:40], flush=True)

    print("=" * 60, flush=True)

    # -------------------------------
    # Initialize Database
    # -------------------------------
    db.init_app(app)

    # -------------------------------
    # Register Blueprints
    # -------------------------------
    app.register_blueprint(auth_bp)
    app.register_blueprint(routes_bp)

    # -------------------------------
    # Database Initialization
    # -------------------------------
    with app.app_context():
        try:
            print("Creating database tables...", flush=True)
            db.create_all()
            print("Database initialized successfully.", flush=True)

        except Exception as e:
            print("=" * 60, flush=True)
            print("DATABASE INITIALIZATION FAILED", flush=True)
            print("=" * 60, flush=True)

            traceback.print_exc()

            print("Exception:", str(e), flush=True)

            # Re-raise so Vercel logs show the full error
            raise

    return app


# Create Flask App
app = create_app()


if __name__ == "__main__":
    print("Starting Student Management System...", flush=True)

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
