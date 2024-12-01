from flask import Blueprint, render_template, request, jsonify
from .db_helper import execute_query
from openai import OpenAI
import sys, os

main = Blueprint('main', __name__)

@main.route('/')
def index():
    # chat_list 테이블에서 title 데이터 조회
    query = 'SELECT id, title FROM chat_list ORDER BY created DESC;'
    chatList = execute_query(query, fetchall=True)

    # 데이터베이스에서 읽어온 title을 템플릿으로 전달
    return render_template('index.html', chatList=chatList)

@main.route('/c/<int:chat_id>', methods=['GET'])
def load_chat(chat_id):
    """
    주어진 chat_id로 데이터베이스에서 채팅 메시지 내용을 가져옵니다.
    """
    try:
        query = "SELECT user_message, bot_response FROM chat_messages WHERE list_id = %s;"
        params = (chat_id,)
        chat_messages = execute_query(query, params, fetchall=True)

        # 채팅 내용을 JSON 형식으로 변환
        formatted_messages = []
        for user_msg, bot_msg in chat_messages:
            formatted_messages.append({"role": "user", "content": user_msg})
            formatted_messages.append({"role": "bot", "content": bot_msg})

        return jsonify({"chatMessages": formatted_messages})
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        msg = f"{fname}[{str(exc_tb.tb_lineno)}] : {str(exc_type)} - {str(e)}"
        return jsonify({"error": msg}), 500

@main.route('/send_message', methods=['POST'])
def send_message():
    """사용자 메시지를 받아 OpenAI API를 호출하고 DB에 저장"""
    data = request.get_json()
    userMessage = data.get('sendData', {}).get('message')
    newChat = data.get('sendData', {}).get('newChat')

    if not userMessage:
        return jsonify({"error": "No message provided"}), 400

    try:
        # OpenAI API 응답 가져오기
        botResponse = get_openai_response(userMessage)

        getListIdQuery = "SELECT MAX(id) FROM chat_list;"
        listID = execute_query(getListIdQuery, fetchone=True)
        listID = listID[0]

        newChatTitle = None
        if newChat:
            chatTitle = get_openai_response(f"'{userMessage}' 이 문장의 핵심 키워드를 찾아서 타이틀로 쓸 수 있는 간단한 문장을 12자 이하로 만들어줘. 그 외의 문장은 생략하고 따옴표와 쌍따옴표도 나오지 않게 부탁해.")
            print(chatTitle)
            createNewChatQuery = "INSERT INTO chat_list (title) VALUES (%s);"
            param = (chatTitle,)
            listID = execute_query(createNewChatQuery, param, return_lastrowid=True)
            newChatTitle = chatTitle

        # 메시지 저장
        query = "INSERT INTO chat_messages (list_id, user_message, bot_response) VALUES (%s, %s, %s);"
        params = (listID, userMessage, botResponse)
        execute_query(query, params)
        
        # JSON 응답 반환
        return jsonify({"bot_response": botResponse, "new_chat_title": newChatTitle, "new_chat_id": listID})
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        msg = f"{fname}[{str(exc_tb.tb_lineno)}] : {str(exc_type)} - {str(e)}"
        return jsonify({"error": msg}), 500
    
def get_openai_response(userMessage):
    openai = OpenAI()
    """OpenAI API를 호출하여 응답 가져오기"""
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": userMessage}]
    )

    return response.choices[0].message.content