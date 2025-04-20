# Cancer Detection System

A full-stack web application for cancer detection using machine learning. The system consists of three main components:
- Frontend (React.js)
- Backend (Spring Boot)
- ML Service (Python)

## Features

- User authentication (Login/Signup)
- OAuth2 authentication with GitHub and Google
- Role-based access control (Admin/User)
- Breast cancer prediction using machine learning
- User management for administrators
- Responsive and animated UI with glass morphism effects

## Tech Stack

### Frontend
- React.js 18
- React Router DOM v7
- Semantic UI React
- Framer Motion for animations
- Axios for API calls

### Backend
- Spring Boot
- Spring Security with JWT
- OAuth2 for social login
- JPA/Hibernate
- MySQL Database

### ML Service
- Python
- Flask
- Scikit-learn
- NumPy
- Pandas

## Prerequisites

- Node.js (v14 or higher)
- Java JDK 11 or higher
- Python 3.8 or higher
- MySQL Server
- Maven

## Installation & Setup

### Frontend Setup
```bash
# Navigate to frontend directory
cd Frontend

# Install dependencies
npm i

# Start development server
npm start
```

### Backend Setup
```bash
# Navigate to backend directory
cd Backend-SpringBoot

# Build the project
mvn clean install

# Run the application
mvn spring-boot:run
```

### ML Service Setup
```bash
# Navigate to python service directory
cd Backend-Python

# Install requirements
pip install -r requirements.txt

# Start Flask server
python app.py

# Test python UI
cd testing
python test_app.py

## Project Structure

cancer-detection-system/
├── Frontend/                # React frontend
├── Backend-SpringBoot/      # Spring Boot backend
└── Backend-Python/          # Python ML service


## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Acknowledgments

- Thanks to all contributors who have helped with this project
- Special thanks to the open source community
