import streamlit as st
import psycopg2

st.set_page_config(page_title="Edit Box Scores", page_icon="⚙️")

def get_connection():
    return psycopg2.connect(st.secrets["DB_URL"])

st.title("⚙️ Manage & Edit Stats")

try:
    conn = get_connection()
    cur = conn.cursor()

    # 1. Fetch data
    cur.execute("""
        SELECT s.id, p.name, g.opponent, s.at_bats, s.hits 
        FROM player_stats s
        JOIN players p ON s.player_id = p.id
        JOIN games g ON s.game_id = g.id
        ORDER BY s.id DESC;
    """)
    rows = cur.fetchall()

    # 2. Check if there is actually data to show
    if not rows:
        st.info("⚾ No stats have been recorded yet. Go to 'Log Game Stats' to add some performance data!")
    else:
        st.write(f"Showing {len(rows)} recorded performances:")
        st.markdown("---")

        for r in rows:
            stat_id, p_name, g_opp, ab, h = r
            
            # Create a clean "Row" for each stat entry
            with st.container():
                col1, col2, col3 = st.columns([4, 1, 1])
                
                col1.write(f"**{p_name}** vs {g_opp} ({h} for {ab})")
                
                # Update Functionality
                if col2.button("📝", key=f"btn_edit_{stat_id}", help="Edit this entry"):
                    st.session_state[f"edit_{stat_id}"] = True

                # Delete Functionality
                if col3.button("🗑️", key=f"btn_del_{stat_id}", help="Delete this entry"):
                    st.session_state[f"confirm_delete_{stat_id}"] = True

                # Confirmation logic for Delete
                if st.session_state.get(f"confirm_delete_{stat_id}"):
                    st.warning(f"Confirm delete for entry #{stat_id}?")
                    col_a, col_b = st.columns(2)
                    if col_a.button("Yes, Delete", key=f"yes_{stat_id}"):
                        cur.execute("DELETE FROM player_stats WHERE id = %s", (stat_id,))
                        conn.commit()
                        st.success("Deleted!")
                        st.rerun()
                    if col_b.button("Cancel", key=f"no_{stat_id}"):
                        st.session_state[f"confirm_delete_{stat_id}"] = False
                        st.rerun()

                # Edit Form
                if st.session_state.get(f"edit_{stat_id}"):
                    with st.form(f"form_{stat_id}"):
                        st.write(f"Editing stats for {p_name}")
                        new_h = st.number_input("Hits", value=h, min_value=0)
                        new_ab = st.number_input("At Bats", value=ab, min_value=1)
                        
                        col_save, col_cancel = st.columns(2)
                        if col_save.form_submit_button("Save Changes"):
                            cur.execute("UPDATE player_stats SET hits = %s, at_bats = %s WHERE id = %s", 
                                        (new_h, new_ab, stat_id))
                            conn.commit()
                            st.session_state[f"edit_{stat_id}"] = False
                            st.success("Updated!")
                            st.rerun()
                
                st.markdown("---") # Visual separator between rows

    cur.close()
    conn.close()
except Exception as e:
    st.error(f"Database error: {e}")
