import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:123456@localhost/petshop'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)
