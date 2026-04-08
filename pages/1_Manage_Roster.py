import streamlit as st
import psycopg2

st.set_page_config(page_title="Manage Roster", page_icon="🧢")

def get_connection():
    return psycopg2.connect(st.secrets["DB_URL"])

st.title("🧢 Manage Team Roster")

# Form to add a new player
with st.form("add_player_form"):
    st.subheader("Add New Player")
    name = st.text_input("Player Name (e.g., Shohei Ohtani)")
    pos = st.selectbox("Position", ["P", "C", "1B", "2B", "3B", "SS", "LF", "CF", "RF", "DH"])
    jersey = st.number_input("Jersey Number", min_value=0, max_value=99, step=1)
    
    submitted = st.form_submit_button("Add to Roster")

    if submitted:
        if name:
            try:
                conn = get_connection()
                cur = conn.cursor()
                # Use parameterized query to prevent SQL injection
                cur.execute(
                    "INSERT INTO players (name, position, jersey_number) VALUES (%s, %s, %s);",
                    (name, pos, jersey)
                )
                conn.commit()
                cur.close()
                conn.close()
                st.success(f"✅ {name} has been added to the team!")
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please enter a player name.")

st.markdown("---")
st.subheader("Current Roster")

try:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, position, jersey_number FROM players ORDER BY name;")
    players = cur.fetchall()
    cur.close()
    conn.close()

    if players:
        # Create a clean list of dictionaries for the table
        roster_data = [{"ID": p[0], "Name": p[1], "Pos": p[2], "No.": p[3]} for p in players]
        st.table(roster_data)
    else:
        st.info("The roster is currently empty.")
except Exception as e:
    st.error(f"Error loading roster: {e}")
    