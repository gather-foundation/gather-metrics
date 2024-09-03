# GATHER Metrics

![GATHER icon](/static/gather_favicon.png)

Gather Metrics is a lightweight web application designed to assist clinicians in quickly calculating head circumference percentiles based on the latest available data. The application provides an intuitive interface where users can input patient data and receive immediate, accurate results.

Visit the live version of the tool at [metrics.gatherfoundation.ch](https://metrics.gatherfoundation.ch)

[![Commitizen friendly](https://img.shields.io/badge/commitizen-friendly-brightgreen.svg)](https://github.com/commitizen-tools/commitizen)  [![Coverage Status](./reports/coverage/coverage-badge.svg?dummy=8484744)](./reports/coverage/index.html) [![Tests Status](./reports/junit/tests-badge.svg?dummy=8484744)](./reports/junit/tests-badge.svg)

## Table of Contents

- [GATHER Metrics](#gather-metrics)
  - [Table of Contents](#table-of-contents)
  - [GATHER Foundation](#gather-foundation)
  - [API Usage](#api-usage)
    - [Example Request](#example-request)
    - [Example Response](#example-response)
    - [Rate Limiting](#rate-limiting)
  - [Deployment](#deployment)
    - [Local Deployment](#local-deployment)
    - [Production Deployment](#production-deployment)
  - [Architecture](#architecture)
    - [FastAPI](#fastapi)
    - [HTMX](#htmx)
    - [Overview](#overview)
  - [Contributing](#contributing)
  - [Contributors](#contributors)
  - [Contact](#contact)

## GATHER Foundation

[GATHER Foundation](https://gatherfoundation.ch) stands for **G**lobal **A**lliance **T**owards **H**armonized **E**-health **R**ecords for Precision Medicine in Neurodevelopmental Disorders (NDDs).

As a recently established initiative, GATHER Foundation aims to promote and support the generation of minimum requirement frameworks for the curation and collection of harmonized clinical, genetic and molecular data in the field of NDDs.

## API Usage

The Head Circumference Percentile API allows you to calculate the percentile of a patient's head circumference based on their age, sex, and head circumference measurements.

### Example Request

Endpoint: `POST /api/v1/head-circumference`

```json
{
    "age_unit": "months",
    "age_value": 6,
    "sex": "M",
    "hcirc_value": 42.0,
    "hcirc_unit": "cm"
}
```

### Example Response

```json
{
    "hcirc_percentile": 75.0
}
```

For detailed documentation and additional options, please refer to the [OpenAPI documentation](https://metrics.gatherfoundation.ch/docs).

### Rate Limiting

This endpoint is rate-limited to 100 requests per minute per IP address. If you exceed this limit, you will receive a 429 Too Many Requests response.

## Deployment

This project is deployed using Docker and is privately managed by the GATHER Foundation on AWS App Runner via Amazon ECR (Elastic Container Registry).

### Local Deployment
If you wish to run the project locally, you can do so using Docker:

1. Build the Docker Image:

```bash
docker build -t gather-metrics:latest .
```

2. Run the Docker Container:

```bash
docker run -p 8000:8000 gather-metrics:latest
```

This will start the application on http://localhost:8000, allowing you to interact with it locally.

### Production Deployment

The production deployment of this project is managed privately by the GATHER Foundation. The Docker image is built and pushed to Amazon ECR, and then deployed on AWS App Runner.

*Note: The deployment process is controlled by the organization, and contributors do not have direct access to the production environment.*

For more details on contributing to the project or setting up a development environment, please refer to the [Contributing](#contributing) section.

## Architecture

The Gather Metrics project leverages FastAPI for the backend, Jinja2 for templating, HTMX for interactivity and follows REST principles.

### FastAPI
FastAPI is a modern web framework for building APIs with Python. It’s chosen for its:

- Performance: FastAPI is one of the fastest Python web frameworks available, thanks to Starlette and Pydantic under the hood.
- Ease of Use: With its intuitive design, FastAPI allows for quick development without sacrificing functionality.
Automatic Documentation: FastAPI automatically generates OpenAPI and Swagger documentation, making it easy to explore and test the API.
 Jinja2 Templating: FastAPI also integrates with Jinja2 for server-side templating. This allows the application to render dynamic HTML content on the server before sending it to the client. Jinja2 is used in conjunction with HTMX to create responsive and dynamic user interfaces without relying heavily on JavaScript.

### HTMX

HTMX is used to enhance the interactivity of the application by enabling dynamic content updates based on user interactions without requiring a full page reload. It allows you to use standard HTML attributes to send requests to the server and update parts of the page with the server’s response.

### Overview

- Backend: FastAPI serves as the core of the application, handling HTTP requests, interacting with the database, and providing RESTful endpoints.
- Dockerized Deployment: The application is containerized using Docker, allowing for consistent and scalable deployment across different environments, particularly on AWS App Runner.

This architecture ensures that the Gather Metrics application is robust, scalable, and easy to maintain.


## Contributing

Want to contribute? Check out our [contribution guidelines](CONTRIBUTING.md).

## Contributors

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="left" valign="top" width="14.28%"><a href="https://github.com/SamuelValentini"><img src="https://avatars.githubusercontent.com/u/7236635?v=4" width="100px;" alt="Sergio Morales"/><br /><sub><b>Samuel Valentini</b></sub></a><br /><a href="https://stalicla.com" title="Profile">STALICLA</a></td>
      <td align="left" valign="top" width="14.28%"><a href="https://github.com/deliso"><img src="https://avatars.githubusercontent.com/u/64223283?u=0ed4878647cf157cc91d2603afcb1d4d3dcdaeca&v=4" width="100px;" alt="Sergio Morales"/><br /><sub><b>Sergio Morales</b></sub></a><br /><a href="https://stalicla.com" title="Profile">STALICLA</a></td>
    </tr>
  </tbody>
</table>

## Contact

Contact the project maintainers or support team at [developers@gatherfoundation.ch](mailto:developers@gatherfoundation.ch).
