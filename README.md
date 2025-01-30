# car-rental
Car Rental Web Application

Project Description

This project is a web application that allows users to rent cars. Users can search for available cars at specific locations, select rental dates and times, and complete their reservations. Additionally, the application supports user registration and login.
Features
 Search for cars by office and date
 Location-based filtering using Google Maps API
 Language toggle (English / Turkish)
 Mobile-friendly and responsive design
 User authentication (login/register)
 Cloud hosting (Pythonanywhere)
Technologies Used
Frontend: HTML, CSS, JavaScript
Backend: Flask
Database: SQLite
APIs: Google Maps API (for location-based search)
Others: MVC Pattern, JWT Authentication, Render Deployment
Installation
To run the project locally, follow these steps:
Clone the repository:
git clone <repository-url>
cd car-rental-app
Install dependencies:
npm install
DATABASE_URL=<database_connection_string>
GOOGLE_MAPS_API_KEY=<your_google_api_key>
JWT_SECRET=<your_jwt_secret>

Start the server:

npm start

Open http://localhost:5000 in your browser to test the application.

📂 Project Structure

/car-rental-app
├── pycache/        
├── helpers/          
├── instance/          
├── models/          # Database models (User, Car, Office)
├── static/     
├── templates/           
├── app.py            
├── config.py        
├── requirements.txt     
└── README.md        


Explaination video: video link: 
https://drive.google.com/file/d/1m7fh0qjCBfCXKMNzBT0xFypQ7za_l0nN/view?usp=sharing

