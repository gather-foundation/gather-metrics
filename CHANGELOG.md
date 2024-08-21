# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

****

## [Unreleased] - 2023-04-04

### Added

- Replaced `Husky` hooks with `Pre-commit` for running different checks, linters and formatters.
- Introduced a `Conda` environment for managing root-level dependencies such as `Commitizen` and `Pre-commit`.
- Updated `SETUP.md` with instructions for setting up a `Conda` environment and using `Pre-commit` with various linters.
- Added `pre-commit-config.yaml` and `environment.yml` files for configuring pre-commit hooks and managing the `Conda` environment, respectively.

### Removed

- Removed `Husky` and `npm` configurations from the root folder.

## [Unreleased] - 2023-03-19

### Added

- Implemented `Husky` hooks to run `lint-staged` and open the interactive `Commitizen` console on commit.
- Updated `SETUP.md` to include instructions on setting up linters for Python and TypeScript projects, as well as configuring Husky and lint-staged.

## [Unreleased] - 2023-03-17

### Added

- Initial project template with basic structure and files for a web project, including `README.md`.
- Created a `SETUP.md` file with repository structure and setup instructions.
- Added a `CHANGELOG.md` file to track changes in the project.
- Added `.gitignore` and `.dockerignore` files to handle common files and folders for web projects, including support for multiple programming languages and frameworks.
- Updated `README.md` to include a code block with a markdown format skeleton.
- Set up Commitizen for standardized commit messages.
- Added a basic CI pipeline configuration for continuous integration.
- Added a basic Docker configuration for containerization and deployment.
