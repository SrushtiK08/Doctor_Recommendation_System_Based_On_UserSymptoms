import streamlit as st
import pandas as pd
from pymongo import MongoClient
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC

# Setup MongoDB connection
uri = "mongodb+srv://yourusername:password@cluster8.lmidtnd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster8"

client = MongoClient(uri)
db = client['doctor_database']
appointments = db['appointments']
doctors = db['doctors']

# Load CSV files
disease_symptoms_df = pd.read_csv('disease_and_symptoms.csv')
specialist_doctor_df = pd.read_csv('specialist_and_doctor.csv')

# Function to predict doctor based on symptoms
def predict_doctor(symptoms):
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(disease_symptoms_df['Symptoms'])
    y = disease_symptoms_df['Diseases']
    classifier = LinearSVC(dual=False)
    classifier.fit(X, y)
    X_user_symptoms = vectorizer.transform(symptoms)
    predicted_disease = classifier.predict(X_user_symptoms)
    return predicted_disease[0]

# Function to book an appointment
def book_appointment(doctor_name, user_id, date):
    appointment_datetime = datetime.strptime(f"{date}", '%Y-%m-%d')
    appointments.insert_one({
        'doctor_name': doctor_name,
        'user_id': user_id,
        'appointment_time': appointment_datetime,
        'status': 'scheduled'
    })
    st.success('Appointment booked successfully!')
    

# Function to update the doctor's rating in MongoDB
def update_doctor_rating(doctor_name, user_id, new_rating):
    # Check if user has a completed appointment with this doctor
    if appointments.find_one({'doctor_name': doctor_name, 'user_id': user_id, 'status': 'scheduled'}): #, 'status': 'completed' this feature can be added at the later stage
        doctor = doctors.find_one({'Name': doctor_name})
        if doctor:
            current_rating = doctor.get('Rating', 0)
            rating_count = doctor.get('RatingCount', 0)
            new_average = ((current_rating * rating_count) + new_rating) / (rating_count + 1)
            doctors.update_one(
                {'Name': doctor_name},
                {'$set': {'Rating': new_average, 'RatingCount': rating_count + 1}}
            )
            
            st.success('Rating updated successfully!')
        else:
            st.error('Doctor not found')
    else:
        st.error("You can only rate doctors after booking an appointment.")

st.title('Doctor Recommendation, Booking, and Rating System')

# User inputs


# Generating userid
user_id = 123 #generate in dynamic way at later stage
user_id = str(user_id)

selected_symptoms = st.multiselect('Select your symptoms:', disease_symptoms_df['Symptoms'].unique())

if selected_symptoms:
    predicted_disease = predict_doctor(selected_symptoms)
    if predicted_disease:
        filtered_specialists = specialist_doctor_df[specialist_doctor_df['Disease'] == predicted_disease]
        doctors_list = list(filtered_specialists['Specialization'])
        recommended_doctors = list(doctors.find({'Specialty': {'$in': doctors_list}}))
        recommended_doctors.sort(key=lambda x: x.get('Rating', 0), reverse=True)

        if recommended_doctors:
            doctor_options = {f"{doc['Name']} - {doc['Specialty']} - {doc['Rating']}": doc['Name'] for doc in recommended_doctors}
            doctor_name = st.selectbox('Select a doctor to book an appointment:', options=list(doctor_options.keys()), format_func=lambda x: x)
            appointment_date = st.date_input("Select the appointment date", min_value=datetime.today())
            if st.button('Book Appointment'):
                book_appointment(doctor_options[doctor_name], user_id, appointment_date)
            # Rating section after appointment
            st.subheader("Rate a Doctor")
            rating = st.slider('Select your rating:', 1, 5, 1)
            if st.button('Rate Doctor'):
                update_doctor_rating(doctor_options[doctor_name], user_id, rating)
        else:
            st.error("No doctors available for the selected symptoms.")
    else:
        st.error("No prediction could be made based on the symptoms.")





