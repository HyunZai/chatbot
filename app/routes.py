from flask import Blueprint, render_template
import mysql.connector

main = Blueprint('main', __name__)

# MySQL 연결 설정
def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',        # MySQL 서버 주소
        user='root',             # MySQL 사용자명
        password='1234',     # MySQL 비밀번호
        database='flask_chatbot' # 데이터베이스 이름
    )
    return connection

@main.route('/')
def index():
    # MySQL 연결
    conn = get_db_connection()
    cursor = conn.cursor()

    # chat_list 테이블에서 title 데이터 조회
    cursor.execute('SELECT title FROM chat_list ORDER BY created DESC;')
    chat_titles = cursor.fetchall()

    # 연결 종료
    cursor.close()
    conn.close()

    # 데이터베이스에서 읽어온 title을 템플릿으로 전달
    return render_template('index.html', chat_titles=chat_titles)