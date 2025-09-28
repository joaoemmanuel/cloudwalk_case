import streamlit as st
import pandas as pd
import sqlite3

# Connecting to SQLite database
conn = sqlite3.connect('../../data/cloudwalk_case.db')

# Defining CTEs
risk_qtycbk = """
    WITH RISK_QTYCBK AS( 
        SELECT
            USER_ID || '-' || DEVICE_ID AS TENTATIVA,
            COUNT(TRANSACTION_ID) AS TRANSACTIONS
        FROM
            TRANSACTIONAL_SAMPLE
        WHERE
            HAS_CBK = TRUE
        GROUP BY
            TENTATIVA
        HAVING
            DEVICE_ID NOT NULL
        ORDER BY 2 DESC)
        select * from RISK_QTYCBK
        """
risk_qtydevice = """
    WITH RISK_QTYDEVICE AS(
        SELECT 
            USER_ID,
            COUNT(DEVICE_ID)
        FROM 
            TRANSACTIONAL_SAMPLE
        GROUP BY 
            USER_ID
        HAVING 
            COUNT(DEVICE_ID) > 2
        ORDER BY 
            2 DESC)
SELECT * FROM RISK_QTYDEVICE
"""
risk_qtytries = """
    WITH RISK_QTYTRIES AS(
        SELECT
            USER_ID || '-' || MERCHANT_ID AS SALE,
            TRANSACTION_DATE,
            CARD_NUMBER,
            COUNT(*) AS TRANSACTIONS
        FROM
            TRANSACTIONAL_SAMPLE
        WHERE
            HAS_CBK = TRUE
        GROUP BY
            SALE, TRANSACTION_DATE, CARD_NUMBER
        HAVING
            COUNT(*) > 3
        ORDER BY
            4 DESC)
    SELECT * FROM RISK_QTYTRIES
"""
risk_values = """
    WITH RISK_VALUES AS(
        SELECT 
        USER_ID,
        TRANSACTION_AMOUNT,
        AVG(TRANSACTION_AMOUNT) AS MEDIA,
        CASE 
            WHEN TRANSACTION_AMOUNT > (2*(AVG(TRANSACTION_AMOUNT))) THEN 'RISK'
            ELSE 'NOT_RISK'
        END AS RISK_MEASUREMENT	
    FROM 
        TRANSACTIONAL_SAMPLE
    GROUP BY
        USER_ID
    ORDER BY 
        4 DESC)
    SELECT * FROM RISK_VALUES
"""
risk_transacttime = """
    WITH RISK_TRANSACTTIME AS(
        SELECT 
            * 
        FROM 
            TRANSACTIONAL_SAMPLE
        WHERE 
            TRANSACTION_TIME BETWEEN '00:00:00' AND '06:00:00'
        ORDER BY 
        USER_ID, TRANSACTION_DATE)
    SELECT * FROM RISK_TRANSACTTIME
"""
risk_cardcount = """
    WITH RISK_CARDCOUNT AS(
        SELECT
            USER_ID,
            COUNT(DISTINCT CARD_NUMBER)
        FROM
            TRANSACTIONAL_SAMPLE
        GROUP BY
            USER_ID
        HAVING
            COUNT(DISTINCT CARD_NUMBER) > 2
        ORDER BY 2 DESC)
SELECT * FROM RISK_CARDCOUNT
"""

df_qtycbk       = pd.read_sql_query(risk_qtycbk, conn)
df_qtydevice    = pd.read_sql_query(risk_qtydevice, conn)
df_qtytries     = pd.read_sql_query(risk_qtytries, conn)
df_values       = pd.read_sql_query(risk_values, conn)
df_transacttime = pd.read_sql_query(risk_transacttime, conn)
df_cardcount    = pd.read_sql_query(risk_cardcount, conn)

# Closing database connection
conn.close()

# Application title
st.title('Market Research - Sports Shoes on :blue[Mercado Livre]')

# Setting up the layout for KPI visualization
st.subheader('Main KPIs')
col1, col2, col3 = st.columns(3)

# KPI 1: Item Quantity Total
total_items = df_cardcount.shape[0]
col1.metric(label='Item quantity total', value=total_items, border=True)