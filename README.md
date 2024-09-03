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
  - [License](#license)
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

<a href="https://fastapi.tiangolo.com/" target="_blank" rel="noreferrer"><img src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxZW0iIGhlaWdodD0iMWVtIiB2aWV3Qm94PSIwIDAgMjU2IDI1NiI+PGcgZmlsbD0ibm9uZSI+PHJlY3Qgd2lkdGg9IjI1NiIgaGVpZ2h0PSIyNTYiIGZpbGw9IiMwNDk3ODkiIHJ4PSI2MCIvPjxwYXRoIGZpbGw9IiNmZmYiIGQ9Ik0xMjcuNSA0MUM3OS43NDMgNDEgNDEgNzkuNzQzIDQxIDEyNy41Uzc5Ljc0MyAyMTQgMTI3LjUgMjE0czg2LjUtMzguNzQzIDg2LjUtODYuNVMxNzUuMjU3IDQxIDEyNy41IDQxbS00LjUwNyAxNTUuODM5di01NC4yNThIOTIuODMxbDQzLjMzNi04NC40MnY1NC4yNThoMjkuMDM2eiIvPjwvZz48L3N2Zz4=" width="36" height="36" alt="FastAPI" /></a>
<a href="https://htmx.org/" target="_blank" rel="noreferrer"><img src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxZW0iIGhlaWdodD0iMWVtIiB2aWV3Qm94PSIwIDAgMjU2IDI1NiI+PGcgZmlsbD0ibm9uZSI+PGcgY2xpcC1wYXRoPSJ1cmwoI3NraWxsSWNvbnNIdG14TGlnaHQwKSI+PHBhdGggZmlsbD0iI2Y0ZjJlZCIgZD0iTTE5NiAwSDYwQzI2Ljg2MyAwIDAgMjYuODYzIDAgNjB2MTM2YzAgMzMuMTM3IDI2Ljg2MyA2MCA2MCA2MGgxMzZjMzMuMTM3IDAgNjAtMjYuODYzIDYwLTYwVjYwYzAtMzMuMTM3LTI2Ljg2My02MC02MC02MCIvPjxwYXRoIGZpbGw9IiMzZDcyZDciIGQ9Ik0xMDIuMjUgMTgwLjEyTDEzNy41OCA3NS42YTEuNzUgMS43NSAwIDAgMSAxLjg0LTEuMThsMTQuNjUgMS41YTEuNzUgMS43NSAwIDAgMSAxLjQ5IDIuMjlsLTM0LjUgMTAzLjA4YTEuNzUgMS43NSAwIDAgMS0xLjY2IDEuMmwtMTUuNS0uMDZhMS43NCAxLjc0IDAgMCAxLS43OTYtLjE5NmExLjc1IDEuNzUgMCAwIDEtLjg1NC0yLjExNCIvPjxwYXRoIGZpbGw9IiMxZjIzMjkiIGQ9Ik01OC43NCAxMzEuNDFxLTEuNzYuNjkuMDIgMS4zM3ExOC4xNyA2LjU3IDM1LjA0IDEyLjMzYTEuMzYgMS4zNiAwIDAgMSAuOTEgMS4yNWExODAgMTgwIDAgMCAxLS40MSAxNS45MmE1LjUgNS41IDAgMCAxLS4zNCAxLjU1cS0uMzYuOTMtMS4yOC41NWwtNTcuMTctMjMuNzNhLjY4LjY4IDAgMCAxLS40MS0uNjZsLjc0LTE1LjUzYTEuMDEgMS4wMSAwIDAgMSAuNjEtLjg4bDU1LjktMjMuOTZhMS4wNiAxLjA2IDAgMCAxIC44ODYuMDE3YTEuMSAxLjEgMCAwIDEgLjU4NC42ODNxLjQ1IDEuNTMuNTYgM3EuNTUgNy41LjMgMTQuOTVhLjc0Ljc0IDAgMCAxLS40OC42NmEzMTM5IDMxMzkgMCAwIDEtMzMuNzQgMTIuMjRxLS40My4xNS0uODcuMTdxLS42NC4wMy0uODUuMTFtMTM5LjctLjE3bC0zNS42OS0xMi40NmEuMzUuMzUgMCAwIDEtLjI0LS4zM3EtLjE1LTcuNC4wNi0xNS4wN2E5LjkgOS45IDAgMCAxIC41Ni0zLjEzcS4xOS0uNS43LS4zNnExLjcuNDcgMy4xOCAxLjA4cTI3LjE3IDExLjE4IDU0LjI5IDIyLjQ3cS41OC4yNC41OC44N2wuMDMgMTUuNzFhLjk3Ljk3IDAgMCAxLS41OS44OWwtNTYuOTEgMjMuNWExLjA0IDEuMDQgMCAwIDEtMS4yNzYtLjM5OWExIDEgMCAwIDEtLjE1NC0uNDUxcS0uODktOC45NS0uNDUtMTcuNThhLjg5Ljg5IDAgMCAxIC42LS43OXExOC40OS02LjIzIDM1LjMzLTEyLjY4cTEuNzMtLjY2LS4wMi0xLjI3Ii8+PC9nPjxkZWZzPjxjbGlwUGF0aCBpZD0ic2tpbGxJY29uc0h0bXhMaWdodDAiPjxwYXRoIGZpbGw9IiNmZmYiIGQ9Ik0wIDBoMjU2djI1NkgweiIvPjwvY2xpcFBhdGg+PC9kZWZzPjwvZz48L3N2Zz4=" width="36" height="36" alt="HTMX" /></a>

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
- HATEOAS: The API responses are enriched with hypermedia links that guide clients on how to interact with the various resources available.
- Dockerized Deployment: The application is containerized using Docker, allowing for consistent and scalable deployment across different environments, particularly on AWS App Runner.
This architecture ensures that the Gather Metrics application is robust, scalable, and easy to maintain, providing a seamless experience for clinicians and other users.

![Dependencies](/static/deps/deps.svg)


## Contributing

Want to contribute? Check out our [contribution guidelines](CONTRIBUTING.md).

## Contributors

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="left" valign="top" width="14.28%"><a href="https://github.com/deliso"><img src="https://avatars.githubusercontent.com/u/64223283?u=0ed4878647cf157cc91d2603afcb1d4d3dcdaeca&v=4" width="100px;" alt="Sergio Morales"/><br /><sub><b>Sergio Morales</b></sub></a><br /><a href="https://stalicla.com" title="Profile">STALICLA</a>
    </tr>
  </tbody>
</table>

## License

This project is licensed under the [MIT License](https://opensource.org/license/mit).

## Contact

Contact the project maintainers or support team at [developers@gatherfoundation.ch](mailto:developers@gatherfoundation.ch).
