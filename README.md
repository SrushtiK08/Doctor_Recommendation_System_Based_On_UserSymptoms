# Doctor_Recommendation_System_Based_On_UserSymptoms

### Table of Contents :

1. Prerequisites
2. Project Desing
3. Usage
4. Key Features
5. Scopes for Future
6. Demo Link
7. Conclusion

### Prerequisites
- Python
- Pandas
- Streamlit
- scikit-learn
- streamlit components
- pymongo

### Project Design
- disease_and_symptoms.csv: This file contains the probable symptoms of the disease. 
- doctors.csv: This file contains the doctor's information like name. speciality, years of experience, ratings and number of ratings recevied
- specialist_and_doctor.csv: This CSV file is a mapping of disease predicted and speciality of doctors.


## Usage
1. You need first install all the necessary dependencies using pip install pandas scikit-learn pymongo streamlit_components

2. Place all three CSV files in the same directory

3. You need to create database in MongoDB and connect with the app.
   
4. In app.py, replace your username and password in Mongouri
   
5. To run project use command streamlit run app.py

6. You will be able to access doctor recommendation system in web browser at the URL (Default localhost:8501)

7. Once the application is up select the desired symptoms from the dropdown list
   
9. Application will provide you the recommeded doctors along menu to select appointment booking date and rating slider (Scale 1-5)
    
11. Book Appointment with doctor and than provide your ratings to doctor

## Features

- Dynamic and Interactive User Interface
- Dynamic Recommendations of disease and doctors
- Doctors are Recommendaded based on Ratings and Doctor's Profile
- Appointment Booking along with the Doctor recommendation


## Limitations
- Data used here to predicted disease based on symptoms is dummy.
- Since, data is dummy we cannot completely rely on the recommedation provided by system.
- It will predicted the closest diseases as per the symptoms provided by users.
- Appointment booking can be improvised

