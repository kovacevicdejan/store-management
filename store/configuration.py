import os

database_url = os.environ["DATABASE_URL"]


class Configuration:
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://root:root@{database_url}/store"
    REDIS_HOST = "redis"
    REDIS_PRODUCT_LIST = "products"
    JWT_SECRET_KEY = "JWT_SECRET_KEY"
