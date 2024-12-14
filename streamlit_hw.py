import streamlit as st
import pymysql
import pandas as pd
import plotly.express as px

# 데이터베이스 연결
dbConn = pymysql.connect(user='root', passwd='0405', host='localhost', db='insurance')
cursor = dbConn.cursor(pymysql.cursors.DictCursor)

# 발생 빈도에 따라 상위 10개의 질병 데이터를 가져오는 함수
def get_top_10_diseases():
    query = """
    SELECT RESL_NM1, COUNT(*) AS occurrence
    FROM claimdata
    GROUP BY RESL_NM1
    ORDER BY occurrence DESC
    LIMIT 10
    """
    cursor.execute(query)
    result = cursor.fetchall()
    return pd.DataFrame(result)

# 선택한 질병에 대한 지역별 데이터를 가져오는 함수
def get_region_data_for_disease(disease_name):
    query = f"""
    SELECT custdata.region AS region, COUNT(*) AS count
    FROM claimdata
    JOIN cnttdata ON claimdata.CLAIM_ID = cnttdata.CLAIM_ID
    JOIN custdata ON cnttdata.CUST_ID = custdata.CUST_ID
    WHERE RESL_NM1 = '{disease_name}'
    GROUP BY region
    """
    cursor.execute(query)
    result = cursor.fetchall()
    return pd.DataFrame(result)

# 선택한 질병에 대한 연도별 트렌드를 가져오는 함수
def get_yearly_trend_for_disease(disease_name):
    query = f"""
    SELECT YEAR(claimdata.CLAIM_DATE) AS year, COUNT(*) AS count
    FROM claimdata
    WHERE RESL_NM1 = '{disease_name}'
    GROUP BY year
    ORDER BY year ASC
    """
    cursor.execute(query)
    result = cursor.fetchall()
    return pd.DataFrame(result)

# 지역별 총 청구 데이터를 가져오는 함수
def get_total_claims_by_region():
    query = """
    SELECT custdata.region AS region, COUNT(*) AS total_claims
    FROM claimdata
    JOIN cnttdata ON claimdata.CLAIM_ID = cnttdata.CLAIM_ID
    JOIN custdata ON cnttdata.CUST_ID = custdata.CUST_ID
    GROUP BY region
    """
    cursor.execute(query)
    result = cursor.fetchall()
    return pd.DataFrame(result)

# Streamlit 앱 레이아웃
st.title("보험 데이터 분석")

# 상위 10개의 질병
st.subheader("상위 10개의 질병")
top_10_diseases = get_top_10_diseases()
disease_options = top_10_diseases['RESL_NM1'].tolist()
selected_disease = st.selectbox("분석할 질병을 선택하세요:", disease_options)

# 선택한 질병에 대한 지역별 발생 빈도 표시
if selected_disease:
    st.subheader(f"{selected_disease}의 지역별 발생 빈도")
    region_data = get_region_data_for_disease(selected_disease)
    if not region_data.empty:
        fig = px.bar(region_data, x='region', y='count', title=f"{selected_disease}의 지역별 발생 빈도")
        st.plotly_chart(fig)
    else:
        st.write("선택한 질병에 대한 데이터가 없습니다.")

# 추가 분석
st.subheader("추가 분석")

# 선택한 질병에 대한 연도별 트렌드
st.write(f"{selected_disease}의 연도별 트렌드")
yearly_trend = get_yearly_trend_for_disease(selected_disease)
if not yearly_trend.empty:
    fig_trend = px.line(yearly_trend, x='year', y='count', markers=True, title=f"{selected_disease}의 연도별 트렌드")
    st.plotly_chart(fig_trend)
else:
    st.write("선택한 질병에 대한 연도별 데이터가 없습니다.")

# 지역별 총 청구 데이터
st.subheader("지역별 총 청구 데이터")
total_claims_region = get_total_claims_by_region()
if not total_claims_region.empty:
    fig_total = px.pie(total_claims_region, names='region', values='total_claims', title="지역별 총 청구 데이터")
    st.plotly_chart(fig_total)
else:
    st.write("지역별 총 청구 데이터가 없습니다.")

# 데이터베이스 연결 종료
dbConn.close()
