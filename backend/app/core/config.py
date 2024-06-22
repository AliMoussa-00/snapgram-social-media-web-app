#!/usr/bin/env python3
""" Load the environment variables. """

from dotenv import load_dotenv
from os import getenv

load_dotenv()

MONGODB_URL = getenv("MONGODB_URL")
HOST = getenv("HOST")
PORT = int(getenv("PORT"))
DB_NAME = getenv("DB_NAME")
