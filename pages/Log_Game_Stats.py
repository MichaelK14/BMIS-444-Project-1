import streamlit as st
import psycopg2

st.set_page_config(page_title="Log Game Stats", page_icon="📝")

def get_connection():
    return psycopg2.connect(st.secrets["DB_URL"])

st.title("📝 Log Player Performance")

try:
    conn = get_connection()
    cur = conn.cursor()

    # 1. Dynamic Dropdowns (Requirement!)
    cur.execute("SELECT id, name FROM players ORDER BY name;")
    player_options = {row[1]: row[0] for row in cur.fetchall()}

    cur.execute("SELECT id, opponent, game_date FROM games ORDER BY game_date DESC;")
    game_options = {f"{row[1]} ({row[2]})": row[0] for row in cur.fetchall()}

    with st.form("stats_form"):
        selected_player = st.selectbox("Select Player", options=player_options.keys())
        selected_game = st.selectbox("Select Game", options=game_options.keys())
        
        col1, col2 = st.columns(2)
        at_bats = col1.number_input("At Bats", min_value=1, step=1)
        hits = col2.number_input("Hits", min_value=0, step=1)
        
        # Calculations for display
        avg = hits/at_bats if at_bats > 0 else 0
        st.info(f"Calculated Batting Average for this entry: {avg:.3f}")

        submitted = st.form_submit_button("Save Performance")

        if submitted:
            # 2. Form Validation (Requirement!)
            if hits > at_bats:
                st.error("Validation Error: Hits cannot be greater than At Bats!")
            else:
                cur.execute("""
                    INSERT INTO player_stats (player_id, game_id, at_bats, hits) 
                    VALUES (%s, %s, %s, %s)
                """, (player_options[selected_player], game_options[selected_game], at_bats, hits))
                conn.commit()
                st.success("Stats recorded!")

    cur.close()
    conn.close()
except Exception as e:
    st.error(f"Error: {e}")
