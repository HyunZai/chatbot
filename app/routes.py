from flask import Blueprint, render_template
from .db_helper import execute_query

main = Blueprint('main', __name__)

@main.route('/')
def index():
    # chat_list 테이블에서 title 데이터 조회
    query = 'SELECT title FROM chat_list ORDER BY created DESC;'
    chat_titles = execute_query(query, fetchall=True)

    # 데이터베이스에서 읽어온 title을 템플릿으로 전달
    return render_template('index.html', chat_titles=chat_titles)