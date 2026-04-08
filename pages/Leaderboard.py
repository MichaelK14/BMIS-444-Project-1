import streamlit as st
import psycopg2
import pandas as pd

st.set_page_config(page_title="Leaderboard", page_icon="🏆")

def get_connection():
    return psycopg2.connect(st.secrets["DB_URL"])

st.title("🏆 Team Leaderboard")

search = st.text_input("Search for a player by name")

query = """
    SELECT 
        p.name, 
        SUM(s.at_bats) as total_ab, 
        SUM(s.hits) as total_hits,
        ROUND(CAST(SUM(s.hits) AS DECIMAL) / NULLIF(SUM(s.at_bats), 0), 3) as batting_avg
    FROM players p
    LEFT JOIN player_stats s ON p.id = s.player_id
"""

if search:
    query += " WHERE p.name ILIKE %s GROUP BY p.name ORDER BY batting_avg DESC"
    params = (f"%{search}%",)
else:
    query += " GROUP BY p.name ORDER BY batting_avg DESC"
    params = None

try:
    conn = get_connection()
    df = pd.read_sql_query(query, conn, params=params)
    
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("No data found.")
    conn.close()
except Exception as e:
    st.error(f"Error: {e}")
