import os


class Config:
    # Secret key for signing cookies/sessions
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-12345-student-mgmt'

    # Database configuration
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # Prefer the POOLED connection (PgBouncer, port 6543) first since this
    # app runs on serverless - direct connections (POSTGRES_URL_NON_POOLING)
    # can exhaust Supabase's connection limit under serverless load.
    database_url = (
        os.environ.get('DATABASE_URL') or
        os.environ.get('POSTGRES_URL') or
        os.environ.get('POSTGRES_URL_NON_POOLING')
    )

    if database_url:
        # Flask-SQLAlchemy expects postgresql:// instead of postgres://
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql://", 1)
        SQLALCHEMY_DATABASE_URI = database_url

        # Serverless-friendly pool settings. pool_pre_ping avoids using a
        # stale connection; small pool size since PgBouncer/Supabase already
        # pools connections on its end.
        SQLALCHEMY_ENGINE_OPTIONS = {
            "pool_pre_ping": True,
            "pool_size": 1,
            "max_overflow": 0,
        }
    # Fallback to SQLite
    elif os.environ.get('VERCEL') == '1' or os.environ.get('VERCEL'):
        SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/database.db'
    else:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'database.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
