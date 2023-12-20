# iati-technical-test
This project is designed for the IATI technical test, providing a comprehensive service with an integrated API. It's configured for easy setup and deployment using Docker.

## Initial Data
The system automatically loads initial data when starting the service. This is designed to facilitate development:

Automatic Loading: Only occurs in development environments.
Database Check: Data loading is triggered only if the database is empty, ensuring no duplication.

## API Documentation
Access comprehensive API documentation to understand and interact with the available endpoints:

- Swagger UI: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/

Documentation is dynamically generated from the codebase using the [drf-yasg](https://pypi.org/project/drf-yasg/) library, ensuring up-to-date information.

## Requirements
Ensure you have the following tools installed to run the service:

- Docker
- Docker Compose

## Environment Setup
Create a .env file in the project root with the necessary environment variables. For development purposes, use the following template:

```bash
#### DB ####
PSQL_DB_HOST=postgres
PSQL_DB_PORT=5432
PSQL_DB_DATABASE=iati
PSQL_DB_USERNAME=postgres
PSQL_DB_PASSWORD=1234
#### DJANGO ####
SECRET_KEY=development-secret-key
#### EMAIL ####
EMAIL_HOST_USER=pclararobles@gmaail.com
```
This configuration is suitable for development. For production, ensure to use secure and unique values.

## Commands to run the application
Use these commands to manage the application's lifecycle:

### Build the Application

```bash
$ docker-compose build
```
### Run the Application
```bash
$ docker-compose run --rm manage migrate
```
### Run the Application
```bash
$ docker-compose up -d iati-test
```
### Stop the Application

```bash
$ docker-compose down
```
### Run the Tests
```bash
$ docker-compose run --rm test-unit
```
