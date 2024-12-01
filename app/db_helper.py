from flask import current_app
import mysql.connector

def get_db_connection():
    """ MySQL 데이터베이스 연결 생성. """
    connection = mysql.connector.connect(
        host=current_app.config['DB_HOST'],
        user=current_app.config['DB_USER'],
        password=current_app.config['DB_PASSWORD'],
        database=current_app.config['DB_DATABASE']
    )
    return connection

def execute_query(query, params=None, fetchone=False, fetchall=False, return_lastrowid=False):
    """
    쿼리를 실행하는 헬퍼 함수.
    
    Args:
        query (str): 실행할 SQL 쿼리.
        params (tuple): 쿼리에 전달할 매개변수.
        fetchone (bool): 단일 결과를 가져올지 여부.
        fetchall (bool): 여러 결과를 가져올지 여부.
        return_lastrowid (bool): INSERT 쿼리 후 삽입된 ID를 반환할지 여부.
    
    Returns:
        tuple/list/int: 쿼리 결과 또는 마지막 삽입된 ID.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params or ())
        if fetchone:
            result = cursor.fetchone()
        elif fetchall:
            result = cursor.fetchall()
        elif return_lastrowid:
            conn.commit()
            result = cursor.lastrowid
        else:
            conn.commit()
            result = None
    finally:
        cursor.close()
        conn.close()
    return result