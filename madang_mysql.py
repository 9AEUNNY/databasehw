import streamlit as st
import pymysql
import pandas as pd

# 데이터베이스 연결 설정
dbConn = pymysql.connect(user='root', passwd='0405', host='localhost', db='madang', charset='utf8')
cursor = dbConn.cursor(pymysql.cursors.DictCursor)

# Streamlit에서 고객명을 입력받기
name = st.text_input("고객명")

# 고객명이 입력된 경우 SQL 쿼리 실행
if name:
    sql = """
    SELECT c.name, b.bookname, o.orderdate, o.saleprice 
    FROM Customer c, Book b, Orders o
    WHERE c.custid = o.custid AND o.bookid = b.bookid AND c.name = %s
    """
    cursor.execute(sql, (name,))
    result = cursor.fetchall()
    
    # 결과를 데이터프레임으로 변환하고 Streamlit에 출력
    result_df = pd.DataFrame(result)
    st.write(result_df)

# 연결 종료
cursor.close()
dbConn.close()
