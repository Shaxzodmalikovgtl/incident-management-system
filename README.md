# Incident Management System - Backend 

The Incident Management System is developed using Python and Django Rest Framework (DRF). This system allows users to manage and report incidents with various details and functionalities.

## Features

- User registration and authentication.
- User profile with details such as name, email, phone number, address, city, and country.
- Create, view, edit, and delete incidents.
- Each incident includes information about the reporter, details, date and time of reporting, priority, and status.
- Auto-generation of unique incident IDs.
- Search incidents by Incident ID.
- Control over incident editing:
  - Users can only edit their own incidents.
  - Closed incidents are not editable.

## Installation

1. Clone the repository to your local machine:
   git clone https://github.com/yourusername/incident-management-system.git


2. Change into the project directory:
   cd incident-management-system

3. Install project dependencies:
   pip install -r requirements.txt
   
4. Set up the database:
  python manage.py migrate

5. Create a superuser (admin) account:
  python manage.py createsuperuser

6. Start the development server:
  python manage.py runserver

7. Access the application at `http://localhost:8000/`.

## API Endpoints

### User Authentication and Registration
- `POST /api/register/`: Register a new user.
- `POST /api/token/`: Obtain a JWT token for user authentication.
- `POST /api/token/refresh/`: Refresh a JWT token.

### User Management
- `GET /api/users/`: List all users.
- `GET /api/users/{user_id}/`: Retrieve a specific user by ID.
- `PUT /api/users/{user_id}/`: Update a specific user by ID.
- `DELETE /api/users/{user_id}/`: Delete a specific user by ID.

### Incident Management
- `POST /api/incidents/`: Create a new incident.
- `GET /api/incidents/`: List all incidents created by the logged-in user.
- `GET /api/incidents/?incidentid=INCIDENT_ID`: Retrieve a specific incident by ID.
- `PUT /api/incidents/?incidentid=INCIDENT_ID`: Update a specific incident by ID (if not closed).
- `DELETE /api/incidents/?incidentid=INCIDENT_ID`: Delete a specific incident by ID (if not closed).

### Get Information from Pin Code
- `GET /api/pincode/{pincode}/`: Retrieve information (City and Country) based on the entered Pin Code.

### Swagger Documentation
-  /swagger/


## Contributing

Contributions are welcome! To contribute to this project, follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and test them.
4. Commit your changes and push them to your fork.
5. Create a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Special thanks to the Django and DRF communities for their amazing work.

Happy coding!
