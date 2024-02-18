import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': "https://attendance-app-1a0c6-default-rtdb.firebaseio.com/"
})

ref=db.reference("Students")

data={
    "1901500":
    {
        "Name":"Yashvendra Singh Raghav",
        "Major":"CSE",
        "Starting_year":2017,
        "Total_attendance":0,
        "Standing":"Poor ",
        "Year":"Final",
        "last_attendance_time": "2023-01-12 08:00:00"
    },
     "7009163":
    {
        "Name":"Leenu Raghuvanshy",
        "Major":"Biology",
        "Starting_year":2014,
        "Total_attendance":0,
        "Standing":"Average ",
        "Year":"Final",
        "last_attendance_time": "2023-01-12 08:00:00"
    },
     "8742061":
    {
        "Name":"Anshu Singh Raghav",
        "Major":"CSE",
        "Starting_year":2019,
        "Total_attendance":0,
        "Standing":"Good ",
        "Year":"Final",
        "last_attendance_time": "2023-01-12 08:00:00"
    },
     "9352108":
    {
        "Name":"Nikhil Singh Raghav",
        "Major":"CSE",
        "Starting_year":2022,
        "Total_attendance":0,
        "Standing":"Poor",
        "Year":"Second",
        "last_attendance_time": "2023-01-12 08:00:00"
    }
}

for key,value in data.items():
    ref.child(key).set(value)