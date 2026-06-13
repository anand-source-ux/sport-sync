import streamlit as st
import pandas as pd
import os
from datetime import date

st.set_page_config(
    page_title="Campus Sports Hub",
    page_icon="🏆",
    layout="wide"
)

BOOKINGS_FILE = "bookings.csv"
ACTIVITY_FILE = "activities.csv"

# Create files if not exist
if not os.path.exists(BOOKINGS_FILE):
    pd.DataFrame(columns=[
        "Student",
        "Sport",
        "Date",
        "Slot"
    ]).to_csv(BOOKINGS_FILE,index=False)

if not os.path.exists(ACTIVITY_FILE):
    pd.DataFrame(columns=[
        "Student",
        "Sport",
        "Duration (mins)",
        "Calories",
        "Date"
    ]).to_csv(ACTIVITY_FILE,index=False)

bookings = pd.read_csv(BOOKINGS_FILE)
activities = pd.read_csv(ACTIVITY_FILE)

sports = [
    "Gymnasium",
    "Swimming",
    "Basketball",
    "Football",
    "Snooker",
    "Table Tennis",
    "Tennis",
    "Cricket"
]

menu = st.sidebar.radio(
    "Menu",
    [
        "Book Slot",
        "Track Activity",
        "Dashboard"
    ]
)

# -------------------------
# BOOK SLOT
# -------------------------
if menu == "Book Slot":

    st.title("🏆 Sports Slot Booking")

    student = st.text_input("Student Name")

    sport = st.selectbox(
        "Select Sport",
        sports
    )

    booking_date = st.date_input(
        "Choose Date",
        min_value=date.today()
    )

    slot = st.selectbox(
        "Time Slot",
        [
            "6 AM - 7 AM",
            "7 AM - 8 AM",
            "8 AM - 9 AM",
            "4 PM - 5 PM",
            "5 PM - 6 PM",
            "6 PM - 7 PM"
        ]
    )

    if st.button("Book Slot"):

        duplicate = bookings[
            (bookings["Sport"] == sport) &
            (bookings["Date"] == str(booking_date)) &
            (bookings["Slot"] == slot)
        ]

        if len(duplicate) > 0:
            st.error("Slot already booked")
        else:
            new = pd.DataFrame({
                "Student":[student],
                "Sport":[sport],
                "Date":[booking_date],
                "Slot":[slot]
            })

            bookings = pd.concat(
                [bookings,new],
                ignore_index=True
            )

            bookings.to_csv(
                BOOKINGS_FILE,
                index=False
            )

            st.success("Booking Successful!")

    st.subheader("Current Bookings")
    st.dataframe(bookings)

# -------------------------
# TRACK ACTIVITY
# -------------------------
elif menu == "Track Activity":

    st.title("📊 Activity Tracker")

    student = st.text_input("Student Name")

    sport = st.selectbox(
        "Sport",
        sports
    )

    duration = st.number_input(
        "Duration (mins)",
        min_value=1
    )

    calories = st.number_input(
        "Calories Burned",
        min_value=0
    )

    if st.button("Save Activity"):

        new = pd.DataFrame({
            "Student":[student],
            "Sport":[sport],
            "Duration (mins)":[duration],
            "Calories":[calories],
            "Date":[date.today()]
        })

        activities = pd.concat(
            [activities,new],
            ignore_index=True
        )

        activities.to_csv(
            ACTIVITY_FILE,
            index=False
        )

        st.success("Activity Saved")

# -------------------------
# DASHBOARD
# -------------------------
elif menu == "Dashboard":

    st.title("📈 Sports Dashboard")

    total_hours = activities["Duration (mins)"].sum()/60

    total_calories = activities["Calories"].sum()

    col1,col2 = st.columns(2)

    col1.metric(
        "Total Hours Played",
        round(total_hours,2)
    )

    col2.metric(
        "Calories Burned",
        int(total_calories)
    )

    st.subheader("Activities")

    st.dataframe(activities)

    if len(activities) > 0:

        sport_summary = activities.groupby(
            "Sport"
        )["Duration (mins)"].sum()

        st.bar_chart(sport_summary)