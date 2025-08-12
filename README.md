# Flask REST API with Swagger UI and JWT Authentication

Welcome to this comprehensive REST API project using Flask, Swagger UI, and token-based security!

---

## Project Overview

This project demonstrates how to develop **production-ready REST APIs** with Python and Flask, including:

- Secure user registration and authentication with JWT tokens
- Resource-based API endpoints to create, read, update, and delete data
- API documentation and visualization using Swagger UI
- Database integration using SQLAlchemy and Flask-SQLAlchemy
- Token management with features like refresh and blacklisting for enhanced security
- Containerized deployment with Docker

---

## Features

- **RESTful API design**: Clean, resource-based endpoints
- **Authentication & Authorization**: Secure login with JWT tokens, including token refresh and blacklisting
- **Swagger UI Integration**: Interactive API documentation to explore endpoints easily
- **Database support**: Persistent data storage with SQLAlchemy
- **Docker support**: Easily run and deploy the API in isolated containers

---

## Technologies Used

- Python 
- Flask
- Flask-Smorest (for API building and Swagger integration)
- Flask-JWT-Extended (for JWT authentication)
- Flask-SQLAlchemy
- Docker (containerization)

---

## Getting Started

### Prerequisites

- Python 3.7+
- Docker
- Git 

### Installation

1. Clone this repository:
   ```bash
    git clone https://github.com/yourusername/flask-restapi-project.git
   cd flask-restapi-project
 2. Create a virtual environment and activate it:
     ```bash
     python -m venv venv
     source venv/bin/activate 
3. Install dependencies
     ```bash
     pip install -r requirements.txt
4. Set environment variables
    ```bash
5. Intialize the database
    ```bash
    flask db upgrade
6. Run the Flask app
   ```bash
    flask run
7.Open your browser and navigate to
   ```bash
   http://localhost:5000/api/docs

