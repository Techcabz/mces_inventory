import os
from urllib.parse import urlparse
from celery.schedules import crontab

class Config:
    # Base directory
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    UPLOAD_FOLDER = os.path.abspath(os.path.join(os.getcwd(), "app/static/storage/app"))
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    # Email (Flask-Mail) Config
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'true').lower() == 'true'
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL', 'false').lower() == 'true'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', 'techcabz@gmail.com')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', 'bjlpviadxlllsqea')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', MAIL_USERNAME)

    # Celery Config (using SQLite for broker and backend)
    CELERY_BROKER_URL = 'sqla+sqlite:///celerydb.sqlite'
    CELERY_RESULT_BACKEND = 'db+sqlite:///results.sqlite'
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TIMEZONE = 'Asia/Manila'


    CELERY_BEAT_SCHEDULE = {
        'auto-cancel-everyday-6pm': {
            'task': 'app.tasks.scheduled_tasks.auto_cancel_expired_borrowings_task',
            'schedule': crontab(hour=18, minute=0),
        },
        'due-reminder-everyday-6pm': {
            'task': 'app.tasks.scheduled_tasks.send_due_reminders_task',
            'schedule': crontab(hour=18, minute=0),
        }
    }
    # Decide database type: 'sqlite' or 'mysql'
    DB_TYPE = os.getenv("DB_TYPE", "mysql").lower()

    if DB_TYPE == "mysql":
        MYSQL_DATABASE_URL = os.getenv("MYSQL_DATABASE_URL", "mysql+pymysql://root:@localhost/mces_inventory")
        parsed_url = urlparse(MYSQL_DATABASE_URL)

        SQLALCHEMY_DATABASE_URI = MYSQL_DATABASE_URL
        MYSQL_USER = parsed_url.username
        MYSQL_PASSWORD = parsed_url.password
        MYSQL_HOST = parsed_url.hostname
        MYSQL_PORT = parsed_url.port or 3306
        MYSQL_DB_NAME = parsed_url.path.lstrip("/")
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
    def initialize_sqlite_db(cls):
        celery_db = os.path.join(os.getcwd(), 'celerydb.sqlite')
        results_db = os.path.join(os.getcwd(), 'results.sqlite')

        if not os.path.exists(celery_db):
            with open(celery_db, 'w'):
                pass
        if not os.path.exists(results_db):
            with open(results_db, 'w'):
                pass
            
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
                try:
                    with connection.cursor() as cursor:
                        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {cls.MYSQL_DB_NAME}")
                    connection.commit()
                finally:
                    connection.close()
            except pymysql.MySQLError as e:
                print(f"Error initializing database: {e}")

class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'
    TEMPLATES_AUTO_RELOAD = True

class ProductionConfig(Config):
    DEBUG = False
    ENV = 'production'
    SESSION_COOKIE_SECURE = True
