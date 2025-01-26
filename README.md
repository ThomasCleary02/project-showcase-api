# Portfolio Backend with Django REST Framework

This repository contains the backend code for the project showcase feature of my portfolio website. The backend is built using Django and Django REST Framework (DRF) and is powered by a PostgreSQL database. It provides API endpoints for managing and retrieving project data dynamically.

## Features
- RESTful API for managing project data.
- PostgreSQL database integration.
- CRUD operations for project entries.
- Filtering projects by technologies used.
- Easy extensibility for future features.

## Technologies Used
- **Django**: Backend framework.
- **Django REST Framework (DRF)**: For building API endpoints.
- **PostgreSQL**: Database for storing project data.
- **Python**: Programming language.

## Prerequisites
Before running this project, ensure you have the following installed:
- Python 3.8 or later
- PostgreSQL
- pip (Python package manager)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/portfolio-backend.git
   cd portfolio-backend
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the database:**
   - Update the `DATABASES` setting in `settings.py` with your PostgreSQL credentials.

5. **Apply migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

## API Endpoints

- `GET /projects/` - Retrieve a list of all projects.
- `POST /projects/` - Add a new project (requires authentication).
- `GET /projects/<id>/` - Retrieve details of a specific project.
- `PUT /projects/<id>/` - Update a specific project (requires authentication).
- `DELETE /projects/<id>/` - Delete a specific project (requires authentication).

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes and push to your branch.
4. Submit a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.


