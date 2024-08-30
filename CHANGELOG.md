# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

****

[1.0.0] - 2024-08-30

## Initial Release

First official release of the Gather Metrics project.

### Features

#### Head Circumference Calculation:

- Integrated a model that calculates head circumference percentile based on sex, age, and head circumference measurement.
- Implemented form input validation and error handling to ensure accurate data entry.
- Provided API endpoints for calculating and retrieving percentile data, following RESTful principles.

### Security:

- Implemented rate limiting (100 requests/min per IP) to protect against abuse.
- Added a content security policy (CSP) middleware to enhance application security.
- Included HTTPS redirect middleware to enforce secure connections.
- Configured CORS support to manage cross-origin requests safely.

### User Interface:

- Designed a user-friendly interface with a focus on usability and accessibility.
- Developed modular templates using Jinja2 for easy customization and maintenance.
- Incorporated HTMX for dynamic content updates without full page reloads.

### Documentation:

- Provided comprehensive README and contribution guidelines.
- Included deployment instructions and security considerations for hosting the application.

### Testing:

- Set up automated tests to ensure code quality and correctness.
- Included tests for API endpoints, domain logic, and form validation.

### Build Setup

- Configured development tools including mypy for type checking, black for code formatting, and pre-commit hooks for enforcing code quality.
- Set up commitizen for conventional commits to maintain a consistent commit history.

### Deployment

- The application is containerized using Docker and is deployed on AWS App Runner via Amazon ECR.s
