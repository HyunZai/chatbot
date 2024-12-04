# flask-openai-chatbot
Chatbot using OpenAI's API

### Python version 3.9.20
파이썬 v3.9.20을 설치 후 아래 실행 절차를 따라주십시오.

Install that version of Python before proceeding

```
$ git clone https://github.com/HyunZai/flask-openai-chatbot.git
$ pip install pipenv
$ pipenv install
$ pipenv shell
```

프로젝트 경로에 있는 `.env` 파일에 DB 연결 정보와 OpenAI API KEY를 입력 후 저장하십시오.

Input your DB connection information and OpenAI API KEY in the .env file located in the project path

sql/DDL.sql로 데이터베이스 테이블을 생성하십시오.

Create a database table through `sql/DDL.sql`

```
$ flask run
```
