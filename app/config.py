import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:Caroline12@localhost:5432/EnviroSenseAPI'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
