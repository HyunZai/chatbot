import os

class Config:
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'openai_api_key')
    # SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///app.db')
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
