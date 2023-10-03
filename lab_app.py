import streamlit as st
import pandas as pd

import pickle
from pathlib import Path
import streamlit_authenticator as stauth

## Add student log-in
names = ["a1", "a2", "a3"]
usernames = ["a1", "a2", "a3"]
file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    passwords = pickle.load(file)

# credentials=dict()
# for (username, password) in zip(usernames, passwords):
#     print(username)
#     print(password)
    # credentials["usernames"].append(username)

# print(credentials)
# print(passwords)

credentials = {
    "usernames": {"a1": {"name": "a1",
                         "password":"$2b$12$Jc3dP1NPEE3tagjcwtNhNOsVbdWMA.k7uRtBVYkxwmrsNuQ6Xjswi"},
                  "a2":{"name":"a2",
                        "password":"$2b$12$te9QHMxSOgN0XbCPYD/5uOwSrG4lR4qmBqOP.Np0ROQEVx4pWb82."}}
}

authenticator = stauth.Authenticate(credentials,
                                     "dashboard", "abcdef", cookie_expiry_days=0)
name, authentication_status, username = authenticator.login("Login", "main")
if authentication_status == False:
    st.error("Username/password incorecte")
if authentication_status == None:
    st.warning("Introduceti username/ pass")

if authentication_status:
    # Add a logout button
    authenticator.logout("Logout", "sidebar")
    # Import excel_file
    data = pd.read_excel("../lab_summary.xlsx")
    # print(data.head())

    student_id = name

    st.title("Laborator Fundamentele Programării - student {}".format(student_id))

    # Query the database
    student_data = data[data["student_id"]==name]
    # print(student_data)

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
    # print(attendance_summary)
