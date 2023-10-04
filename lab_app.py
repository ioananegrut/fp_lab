import streamlit as st
import pandas as pd

# import pickle
import yaml
from yaml import SafeLoader
from pathlib import Path
import streamlit_authenticator as stauth

from supabase import create_client
## Add student log-in
# names = ["a1", "a2", "a3"]
# usernames = ["a1", "a2", "a3"]
# file_path = Path(__file__).parent / "hashed_pw.pkl"
# with file_path.open("rb") as file:
#     passwords = pickle.load(file)

# credentials=dict()
# for (username, password) in zip(usernames, passwords):
#     print(username)
#     print(password)
    # credentials["usernames"].append(username)

# print(credentials)
# print(passwords)
## USER CREDENTIALS
with open("config.yaml") as f:
    config = yaml.load(f, Loader=SafeLoader)

authenticator = stauth.Authenticate(config["credentials"],
                                    config["cookie"]["name"], 
                                    config["cookie"["key"]], 
                                    cookie_expiry_days=config["cookie"]["expiry_days"])
name, authentication_status, username = authenticator.login("Login", "main")
# print(name, authentication_status, username)


if authentication_status == False:
    st.error("Username/password incorecte")
if authentication_status == None:
    st.warning("Introduceti username/ pass")

if authentication_status:
    # Add a logout button
    authenticator.logout("Logout", "sidebar")

    st.title("Laborator Fundamentele Programării - student {}".format(name))

    # Query the database
    @st.cache_resource
    def init_connection():
        url = st.secrets["supabase_url"]
        key = st.secrets["supabase_key"]
        return create_client(url, key)

    supabase = init_connection()

    def run_query():
        return supabase.table("fplab").select("*").execute()

    rows = run_query()
    data = pd.DataFrame(rows.data)

    student_data = data[data["student_id"]==name]

    st.subheader("Evoluția notelor:")
    st.bar_chart(data=student_data, x ="lab", y = "nota")

    st.subheader("Situația prezenței:")
    st.write("Numar minim de prezențe pentru a intra în examen: 12")
    attendance_summary = student_data.groupby(["prezenta"]).count()["lab"]
    # Display the attendance
    try:
        attended = attendance_summary["da"]
    except KeyError:
        attended = 0
    st.write("Numarul dumneavoastră de prezențe: {}".format(attended))

    # Display the non-attendence
    try: 
        miss = attendance_summary["nu"] 
    except KeyError: 
        miss = 0
    st.write("Numarul dumneavoastră de absențe: {}".format(miss))

    if st.button("Detalii prezență"):
        st.table(student_data[["lab", "prezenta"]].reset_index(drop=True))

