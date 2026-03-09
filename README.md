# 🧭 Travel-Planner: Your Ultimate Trip Companion

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)

**Plan smarter, not harder.** Travel-Planner is a robust management application that helps passionate travellers organize trips and curate a personal collection of must-visit places. Stop juggling spreadsheets and bookmarks—get a centralized hub for all your travel ideas.

## ✨ Key Features

*   **🗺️ Trip Management**: Create detailed itineraries for your upcoming adventures. Set dates, destinations, and keep all trip-related info in one place.
*   **📍 Place Collection**: Build a personal wishlist of places—restaurants, landmarks, hidden gems—and easily associate them with your planned trips.
*   **🔍 Smart Discovery**: (Planned) Find popular places and recommendations based on your destination.
*   **🔗 Centralized Hub**: No more scattered notes! Everything from flight details to that café a friend recommended is stored here.

## 🛠️ Technology Stack

Built with a modern, efficient backend to ensure speed and reliability:

*   **Core Framework**: **FastAPI** for high-performance API development.
*   **Database**: **SQLite** (with SQLAlchemy ORM) for easy setup and portability. Easily swappable for PostgreSQL/MySQL in production.
*   **Migrations**: **Alembic** for seamless database schema version control.
*   **Testing**: **Pytest** for comprehensive unit and integration tests.
*   **Environment**: **Docker** and **Docker Compose** for containerized development and deployment.
*   **Code Quality**: **Flake8** for linting, ensuring clean and consistent code.

🚀 Getting Started

Get your own instance of Travel-Planner up and running in minutes.

Prerequisites

* Docker and Docker Compose (Install Docker: https://docs.docker.com/get-docker/)
* OR Python 3.9+ and pip (for local setup)

Installation & Setup

1. Clone the repository
   git clone https://github.com/tradewcs/Travel-Planner.git
   cd Travel-Planner

2. Set up environment variables
   cp .env.sample .env

3. Run with Docker (Recommended)
   docker-compose up --build
   The API will be available at http://localhost:8000.

4. Alternative: Local Installation
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements/local.txt
   
   Run the database migrations and start the server:
   alembic upgrade head
   uvicorn app.main:app --reload

Running Tests

pytest -v

📚 API Documentation

Once the application is running, explore the interactive API docs:

* Swagger UI: http://localhost:8000/docs
* ReDoc: http://localhost:8000/redoc

🗺️ Roadmap

[x] Core project structure and database models
[x] Basic CRUD endpoints for trips and places
[x] Initial test suite
[ ] User authentication and personalized collections
[ ] Integration with maps APIs (Google Maps, OpenStreetMap)
[ ] Frontend web interface or mobile app
[ ] Sharing trips and collections with friends

🤝 Contributing

Contributions are welcome! Any contributions you make are greatly appreciated.

1. Fork the Project
2. Create your Feature Branch (git checkout -b feature/AmazingFeature)
3. Commit your Changes (git commit -m 'Add some AmazingFeature')
4. Push to the Branch (git push origin feature/AmazingFeature)
5. Open a Pull Request

📄 License

Distributed under the MIT License.

📬 Contact

Project Link: https://github.com/tradewcs/Travel-Planner

---

Happy Travels! 🌎✈️