#!/usr/bin/env python3
""" Load the environment variables. """

from dotenv import load_dotenv
from os import getenv
from pydantic import BaseModel

load_dotenv()


class Settings(BaseModel):
    """ Server config settings. """

    mongodb_url: str = getenv("MONGODB_URL") or "mongodb://localhost:27017"
    host: str = getenv("HOST") or "127.0.0.1"
    port: int = int(getenv("PORT")) or 8000
    db_name: str = getenv("DB_NAME")

    root_url: str = "http://127.0.0.1:8080"

    jwt_secret_key: str = getenv('JWT_SECRET_KEY')
    jwt_refresh_secret_key: str = getenv('JWT_REFRESH_SECRET_KEY')

    mail_server: str = getenv("MAIL_SERVER")
    mail_username: str = getenv("MAIL_USERNAME")
    mail_app_password: str = getenv("MAIL_APP_PASSWORD")

    mail_from: str = getenv("MAIL_FROM")
    mail_port: str = getenv("MAIL_PORT")
    mail_tls: str = getenv("MAIL_TLS")
    mail_ssl: str = getenv("MAIL_SSL")


CONFIG = Settings()
