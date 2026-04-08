import streamlit as st
import psycopg2
from datetime import date

st.set_page_config(page_title="Add Game", page_icon="🏟️")

def get_connection():
    return psycopg2.connect(st.secrets["DB_URL"])

st.title("🏟️ Schedule a New Game")

# Form to add a game
with st.form("add_game_form"):
    st.subheader("Game Details")
    opponent = st.text_input("Opponent Name (e.g., Spokane Indians)")
    game_date = st.date_input("Game Date", value=date.today())
    location = st.selectbox("Location", ["Home", "Away", "Neutral"])
    
    submitted = st.form_submit_button("Add Game to Schedule")

    if submitted:
        # Form Validation (Requirement!)
        if not opponent.strip():
            st.error("⚠️ Opponent name is required.")
        else:
            try:
                conn = get_connection()
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO games (opponent, game_date, location) VALUES (%s, %s, %s);",
                    (opponent, game_date, location)
                )
                conn.commit()
                cur.close()
                conn.close()
                st.success(f"✅ Game against {opponent} on {game_date} recorded!")
            except Exception as e:
                st.error(f"Error: {e}")

st.markdown("---")
st.subheader("📅 Scheduled Games")

# Display existing games
try:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT opponent, game_date, location FROM games ORDER BY game_date DESC;")
    games = cur.fetchall()
    cur.close()
    conn.close()

    if games:
        st.table([{"Opponent": g[0], "Date": g[1], "Location": g[2]} for g in games])
    else:
        st.info("No games scheduled yet.")
except Exception as e:
    st.error(f"Error loading games: {e}")
