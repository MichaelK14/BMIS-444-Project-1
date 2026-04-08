import streamlit as st
import psycopg2

st.set_page_config(page_title="Edit Box Scores", page_icon="⚙️")

def get_connection():
    return psycopg2.connect(st.secrets["DB_URL"])

st.title("⚙️ Manage & Edit Stats")

try:
    conn = get_connection()
    cur = conn.cursor()

    # Read: Show all stats
    cur.execute("""
        SELECT s.id, p.name, g.opponent, s.at_bats, s.hits 
        FROM player_stats s
        JOIN players p ON s.player_id = p.id
        JOIN games g ON s.game_id = g.id
    """)
    rows = cur.fetchall()

    for r in rows:
        stat_id, p_name, g_opp, ab, h = r
        col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
        
        col1.write(f"**{p_name}** vs {g_opp}")
        
        # Update Functionality
        if col2.button(f"Edit {stat_id}"):
            st.session_state[f"edit_{stat_id}"] = True

        # Delete Functionality with Confirmation
        if col3.button(f"Delete {stat_id}"):
            st.session_state[f"confirm_delete_{stat_id}"] = True

        # Confirmation step (Requirement!)
        if st.session_state.get(f"confirm_delete_{stat_id}"):
            if st.button(f"Are you sure you want to delete entry {stat_id}?"):
                cur.execute("DELETE FROM player_stats WHERE id = %s", (stat_id,))
                conn.commit()
                st.rerun()

        # Edit Form
        if st.session_state.get(f"edit_{stat_id}"):
            with st.form(f"form_{stat_id}"):
                new_h = st.number_input("New Hits", value=h)
                if st.form_submit_button("Update"):
                    cur.execute("UPDATE player_stats SET hits = %s WHERE id = %s", (new_h, stat_id))
                    conn.commit()
                    st.success("Updated!")
                    st.rerun()

    cur.close()
    conn.close()
except Exception as e:
    st.error(f"Error: {e}")
