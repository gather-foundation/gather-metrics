# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

****

## [Unreleased] - 2024-08-27

### Build

- Set up mypy for type checking and black for code formatting.
- Set up commitizen for conventional commits and pre-commit hooks to enforce code quality checks.
- Configured pre-commit hooks to automate the running of linters and formatters on code changes.
- Setup basic rest api with head-circumference routes, service and model for domain logic
- Used dto to handle normalized user input

### Features

- **Head Circumference**:
  - Integrated model that calculates head circumference percentile based on sex, age, head circumference measurement of a patient.
  - Added form input validation using error html partials.
  - Added rate limiting and content security policy
