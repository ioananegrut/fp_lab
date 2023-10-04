import streamlit as st
import pandas as pd
import streamlit_authenticator as stauth
from supabase import create_client

# Initialize database connection
@st.cache_resource
def init_connection():
    url = st.secrets["supabase_url"]
    key = st.secrets["supabase_key"]
    return create_client(url, key)

supabase = init_connection()
## Add student log-in

## Get the encrypted user credentials from the DB
def run_user_query():
    return supabase.table("credentials").select("*").execute()
credentials_rows = run_user_query()
credentials_df = pd.DataFrame(credentials_rows.data)

## Format the creddentials as required
config={"credentials":[]}
for index, row in credentials_df.iterrows():
    user_dict = {"password": row["password"],
                 "name":row["name"]}
    config["credentials"][row["usernames"]]=user_dict

# AUTHENTICATE in the app
authenticator = stauth.Authenticate(config["credentials"],
                                    "blabla", 
                                    "xx", 
                                    cookie_expiry_days=0)
name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password incorecte")
if authentication_status == None:
    st.warning("Introduceti username/ pass")

if authentication_status:
    # Add a logout button
    authenticator.logout("Logout", "sidebar")

    st.title("Laborator Fundamentele Programării - student {}".format(name))

    # Fetch the student data from the database
    def run_query():
        return supabase.table("fplab").select("*").execute()
    rows = run_query()
    data = pd.DataFrame(rows.data)
    student_data = data[data["student_id"]==name]

    # Display the data 
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