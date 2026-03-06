# Python Engineer Test Assessment - Travel Planner

## Overview

This task involves building a CRUD application for a travel management system. The goal is to create a system that showcases your understanding of building RESTful APIs, interacting with databases, and integrating third-party services. The test assessment is expected to be completed within 2 hours.

## Business Context

Travel Company requires a management application to help travellers plan trips and collect desired places to visit. The system needs to manage travel projects, places retrieved from a public API, and notes that users attach to places.

From the user's perspective, a project consists of a collection of places they want to visit:
- One project can contain multiple places (minimum: 1, maximum: 10)
- Travellers can add notes to a specific place
- Notes can be updated over time
- Places can be marked as visited
- When all places in a project are marked as visited, the project is automatically marked as completed

## Backend Requirements

### Travel Projects

| Feature | Description |
|---------|-------------|
| **Create** | Create a travel project with Name (required), Description (optional), and Start Date (optional) |
| **Delete** | Remove travel projects from the system<br>**Note:** A project cannot be deleted if any of its places are already marked as visited |
| **Update** | Update travel project information (Name, Description, Start Date) |
| **List** | List all travel projects |
| **Get** | Retrieve a single travel project by ID |

### Places / Project Places

| Feature | Description |
|---------|-------------|
| **Create project with places** | Create a project with an array of places in one single request<br>Places are imported from a third-party API<br>Each place is identified by an external ID from the API |
| **Add place to project** | Add a place to an existing project<br>Must validate that the place exists in the third-party API before storing |
| **Update place** | Update `notes` for a place within a project<br>Mark a place in a project as `visited` |
| **List places** | List all places for a specific project |
| **Get place** | Retrieve a single place within a specific project |

### General Requirements

#### Framework
Choose any of the following:
- FastAPI
- Django
- Flask

#### Database
- Any database can be used (SQLite is sufficient)

#### Third-Party API
- Use the **Art Institute of Chicago API** to fetch and validate places
- API Documentation: [https://api.artic.edu/docs/#collections](https://api.artic.edu/docs/#collections)
- Example endpoint: `GET https://api.artic.edu/api/v1/artworks/search`

#### Validations
- Endpoints must validate request bodies and return appropriate HTTP status codes
- Validate that a place exists in the Art Institute API before adding it to a project
- Enforce the maximum limit of 10 places per project
- Prevent adding the same external place to the same project more than once

## Bonus Points

Additional points will be awarded for implementing any of the following:

### Docker
- Dockerfile and/or docker-compose configuration for running the application locally

### Postman Collection
- A complete Postman collection covering all endpoints and common use cases

### Extended Business Logic
- Pagination and filtering for listing endpoints
- Caching responses from the third-party API
- Basic authentication

### Code Quality
- Clear project structure
- Meaningful commit history

## Sharing the Results

1. **Create a repository** on GitHub
2. **Add a README** explaining:
   - How to build and start the application
   - Setup steps
   - Environment variables
   - Example requests
3. **Documentation**: Define all endpoints in a Postman collection (or provide OpenAPI/Swagger documentation) and add a link to it in the README
4. **Submit**: Once the repository is ready, share the link with the recruiter
5. **Timeline**: Review will be completed within 5–7 business days with feedback

