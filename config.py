import os
from urllib.parse import urlparse
from sqlalchemy.engine.url import make_url

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    UPLOAD_FOLDER = os.path.abspath(os.path.join(os.getcwd(), "app/static/storage/app"))
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    # Email (Flask-Mail) Config
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'true').lower() == 'true'
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL', 'false').lower() == 'true'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', '')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', '')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', MAIL_USERNAME)

    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_recycle': 280,
        'pool_timeout': 10,
        'pool_pre_ping': True,
    }

    # Decide database type: 'sqlite', 'mysql', or 'postgresql'
    DB_TYPE = os.getenv("DB_TYPE", "postgresql").lower()

    if DB_TYPE == "mysql":
        MYSQL_DATABASE_URL = os.getenv("MYSQL_DATABASE_URL", "mysql+pymysql://root:@localhost/mces_inventory")
        parsed_url = urlparse(MYSQL_DATABASE_URL)
        SQLALCHEMY_DATABASE_URI = MYSQL_DATABASE_URL
        MYSQL_USER = parsed_url.username
        MYSQL_PASSWORD = parsed_url.password
        MYSQL_HOST = parsed_url.hostname
        MYSQL_PORT = parsed_url.port or 3306
        MYSQL_DB_NAME = parsed_url.path.lstrip("/")

    elif DB_TYPE == "postgresql":
        POSTGRES_DATABASE_URL = os.getenv("POSTGRES_DATABASE_URL", "postgresql+psycopg2://postgres:@localhost/mces_inventory")
        parsed_url = urlparse(POSTGRES_DATABASE_URL)
        SQLALCHEMY_DATABASE_URI = POSTGRES_DATABASE_URL
        POSTGRES_USER = parsed_url.username
        POSTGRES_PASSWORD = parsed_url.password
        POSTGRES_HOST = parsed_url.hostname
        POSTGRES_PORT = parsed_url.port or 5432
        POSTGRES_DB_NAME = parsed_url.path.lstrip("/")

    else:
        SQLITE_DB_PATH = os.getenv("SQLITE_DB_PATH", os.path.join(BASE_DIR, "app.db"))
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{SQLITE_DB_PATH}"

    # Common Flask Configs
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_URL = os.getenv("API_URL", "")
    API_KEY = os.getenv("API_KEY", "")
    SECRET_KEY = os.getenv("SECRET_KEY", os.urandom(24).hex())
    SESSION_COOKIE_SECURE = True
    JSON_SORT_KEYS = False
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    @classmethod
    def Initialize_database(cls):
        if cls.DB_TYPE == "mysql":
            import pymysql
            try:
                connection = pymysql.connect(
                    host=cls.MYSQL_HOST,
                    user=cls.MYSQL_USER,
                    password=cls.MYSQL_PASSWORD,
                    port=cls.MYSQL_PORT
                )
                with connection.cursor() as cursor:
                    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {cls.MYSQL_DB_NAME}")
                connection.commit()
            except pymysql.MySQLError as e:
                print(f"Error initializing MySQL database: {e}")
            finally:
                connection.close()

        elif cls.DB_TYPE == "postgresql":
            import psycopg2
            try:
                conn = psycopg2.connect(
                    dbname='postgres',
                    user=cls.POSTGRES_USER,
                    password=cls.POSTGRES_PASSWORD,
                    host=cls.POSTGRES_HOST,
                    port=cls.POSTGRES_PORT
                )
                conn.autocommit = True
                with conn.cursor() as cursor:
                    cursor.execute(f"SELECT 1 FROM pg_database WHERE datname='{cls.POSTGRES_DB_NAME}'")
                    exists = cursor.fetchone()
                    if not exists:
                        cursor.execute(f"CREATE DATABASE {cls.POSTGRES_DB_NAME}")
            except psycopg2.Error as e:
                print(f"Error initializing PostgreSQL database: {e}")
            finally:
                if conn:
                    conn.close()


class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'
    TEMPLATES_AUTO_RELOAD = True

class ProductionConfig(Config):
    DEBUG = False
    ENV = 'production'
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    PREFERRED_URL_SCHEME = 'https'
