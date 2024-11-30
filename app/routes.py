from flask import Blueprint, render_template, request, jsonify, current_app
from .db_helper import execute_query
from openai import OpenAI

main = Blueprint('main', __name__)

@main.route('/')
def index():
    # chat_list 테이블에서 title 데이터 조회
    query = 'SELECT title FROM chat_list ORDER BY created DESC;'
    chatTitles = execute_query(query, fetchall=True)

    # 데이터베이스에서 읽어온 title을 템플릿으로 전달
    return render_template('index.html', chat_titles=chatTitles)

@main.route('/send_message', methods=['POST'])
def send_message():
    """사용자 메시지를 받아 OpenAI API를 호출하고 DB에 저장"""
    data = request.get_json()
    userMessage = data.get('message')

    if not userMessage:
        return jsonify({"error": "No message provided"}), 400

    try:
        # OpenAI API 응답 가져오기
        botResponse = get_openai_response(userMessage)

        # 메시지 저장
        query = "INSERT INTO chat_messages (list_id, user_message, bot_response) VALUES (2, %s, %s)"
        params = (userMessage, botResponse)
        result = execute_query(query, params, fetchone=True)

        # JSON 응답 반환
        return jsonify({"bot_response": botResponse})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
def get_openai_response(userMessage):
    openai = OpenAI()
    """OpenAI API를 호출하여 응답 가져오기"""
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "피보나치 수열을 생성하는 파이썬 프로그램을 작성해주세요."}]
    )

    return response.choices[0].message.content