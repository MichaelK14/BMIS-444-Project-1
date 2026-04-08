import streamlit as st
import psycopg2

st.set_page_config(page_title="Baseball Team Tracker", page_icon="⚾")

def get_connection():
    return psycopg2.connect(st.secrets["DB_URL"])

st.title("⚾ Baseball Team Tracker")
st.write("Welcome, Coach! Use the sidebar to manage your roster and game stats.")
st.markdown("---")

st.subheader("📊 Team at a Glance")

try:
    conn = get_connection()
    cur = conn.cursor()

    # Get counts for the dashboard metrics
    cur.execute("SELECT COUNT(*) FROM players;")
    player_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM games;")
    game_count = cur.fetchone()[0]

    # Calculate total team hits from the junction table
    cur.execute("SELECT SUM(hits) FROM player_stats;")
    total_hits = cur.fetchone()[0] or 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Players", player_count)
    col2.metric("Games Played", game_count)
    col3.metric("Total Team Hits", total_hits)

    st.markdown("---")
    st.subheader("📋 Recent Box Scores")
    
    # Many-to-Many Join to show who played in which game
    cur.execute("""
        SELECT g.game_date, p.name, s.hits, s.at_bats, g.opponent
        FROM player_stats s
        JOIN players p ON s.player_id = p.id
        JOIN games g ON s.game_id = g.id
        ORDER BY g.game_date DESC
        LIMIT 10;
    """)
    rows = cur.fetchall()

    if rows:
        st.table(
            [{"Date": r[0], "Player": r[1], "Hits": r[2], "AB": r[3], "Opponent": r[4]} for r in rows]
        )
    else:
        st.info("No stats recorded yet. Go to 'Add Stats' to log a game!")

    cur.close()
    conn.close()
except Exception as e:
    st.error(f"Database connection error: {e}")