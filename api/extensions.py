from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_redis import FlaskRedis
# from flask_security import Security
from flask_mail import Mail
from flask_caching import Cache
# from raven.contrib.flask import Sentry


db = SQLAlchemy(
    session_options={"autoflush": False, "autocommit": False})
migrate = Migrate(compare_type=True)
redis_store = FlaskRedis()
# security = Security()
mail = Mail()
cache = Cache()
# sentry = Sentry()
