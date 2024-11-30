from flask import Flask
import openai

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config') # config.py의 Config 클래스를 뜻함

    # 애플리케이션 컨텍스트 내에서 openai API 키 설정
    openai.api_key = app.config['OPENAI_API_KEY']
    
    from .routes import main
    app.register_blueprint(main)
    
    return app
