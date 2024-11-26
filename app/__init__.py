from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config') # config.py의 Config 클래스를 뜻함
    
    from .routes import main
    app.register_blueprint(main)
    
    return app
