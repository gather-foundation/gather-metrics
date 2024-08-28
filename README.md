# GATHER METRICS

![GATHER icon](/static/gather-favicon.png)

GatherMetrics is a lightweight web application designed to assist clinicians in quickly calculating and analyzing key health metrics, including head circumference percentiles. The application provides an intuitive interface where users can input patient data and receive immediate, accurate results.

[![Commitizen friendly](https://img.shields.io/badge/commitizen-friendly-brightgreen.svg)](https://github.com/commitizen-tools/commitizen)

## Table of Contents

- [GATHER METRICS](#gather-metrics)
  - [Table of Contents](#table-of-contents)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
    - [Running Locally](#running-locally)
  - [Testing](#testing)
  - [Deployment](#deployment)
  - [Architecture](#architecture)
  - [Contributing](#contributing)
  - [License](#license)
  - [Contact](#contact)

## Getting Started

### Prerequisites

- Python 3.8+

### Installation

1. Clone the Repository:

```bash
git clone https://path/to/repo/gather-metrics.git
cd gather-metrics
```

2. Create a Virtual Environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install Dependencies:

```bash
pip install -r requirements.txt
```

### Running Locally

1. Start the FasAPI development server:

```bash
export ENVIRONMENT="development" && fastapi dev src/main.py
```

2. Access local site

Visit http://127.0.0.1:8000/ for the main site.

3. Access API documentation

Visit http://127.0.0.1:8000/docs for the Swagger documentation.

4. Example API call

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/head-circumference" -H "Content-Type: application/json" -d '{"age_years": 3, "sex": "M", "hcirc_value": 50}'
```

## Testing

[Explain how to run tests for the project.]

## Deployment

[Provide instructions on how to deploy the project to different environments (e.g., staging, production).]

## Architecture

[Describe the project's architecture and organization.]

## Contributing

[Explain how to contribute to the project. Include guidelines for opening issues, submitting pull requests, and code of conduct.]

## License

[Include information about the project's license.]

## Contact

[Provide contact information for the project maintainers or support team.]
