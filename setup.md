# Setting up a new project

## Repo structure

```bash
.
├── src
│   └── (project-specific files and folders)
├── .dockerignore
├── .gitignore
├── .gitlab-ci.yml
├── .pre-commit-config.yaml
├── CHANGELOG.md
├── docker-compose.yml
├── Dockerfile
├── environment.yml
├── README.md
└── setup.md
```

- `src`: The main folder where your project-specific code and configuration files will reside. This folder should be organized according to your chosen architecture pattern, language, and framework. As you develop your project, you may need to create additional sub-folders and files within the `src` folder to accommodate your project's needs.

- `.dockerignore`: The .dockerignore file is used to specify files and folders that should be excluded from the Docker build context, which is sent to the Docker daemon when building an image.

- `.gitignore`: A file that specifies which files and folders should not be tracked by Git. This typically includes generated files, build artifacts, log files, and local configuration files.

- `.gitlab-ci.yml`: The GitLab CI/CD pipeline configuration file. This file defines the build, test, and deployment stages for your project. You may need to update this file as your project evolves to accommodate new dependencies, frameworks, or features.

- `pre-commit-config.yaml`: This file configures Pre-commit hooks to automatically run checks and format code before each commit.

- `CHANGELOG.md`: This file provides a concise, human-readable history of the project's changes, following the "Keep a Changelog" guidelines and semantic versioning (SemVer) principles. It documents new features, bug fixes, and improvements, allowing developers, project managers, and users to easily track updates and understand the project's evolution.

- `docker-compose.yml`: The Docker Compose configuration file used to define and run multi-container Docker applications. This file specifies the services, networks, and volumes required to run your project. You may need to update this file as you add new services or external dependencies to your project.

- `Dockerfile`: The Docker configuration file used to build the Docker image for your project. This file defines the base image, dependencies, build steps, and other configurations required to run your project in a Docker container. You may need to update this file as your project evolves.

- `environment.yml`: This file defines the Conda environment, specifying dependencies and packages for reproducible development environments.

- `README.md`: A documentation file that provides an overview of the project, its purpose, and how to use or contribute to it. This file should be updated as your project evolves to reflect the current state of the project.

- `setup.md`: A documentation file that guides users through the process of setting up the project, including configuring the development environment, installing dependencies, and initializing the project structure. This file should be updated as your project evolves to reflect the current setup process.

## Overview

This guide is designed to help you set up a new web project using a template directory structure. The template is pattern, language, and framework-agnostic, allowing you to adapt it to any architecture pattern, language, or framework that suits your project needs.

The `src` folder is where the specific architecture pattern and technology stack will be implemented. For example, for a microservices architecture, you could create a sub-folder in `src` for each microservice, and each microservice could have its own Dockerfile, GitLab CI pipeline, and so on. Similarly, for a monolithic architecture, you could have all the code for the project in a single sub-folder of `src`, along with any required configuration files, Dockerfile, GitLab CI pipeline, and so on.

The code examples and instructions are in Python and Javascript, but the setup instructions should work for other languages as well with the necessary modifications.

The instructions provided in this guide are meant to be a starting point for configuring your project. You may need to modify these instructions to fit your specific use case or technology stack. In addition, some steps may require additional setup or configuration depending on your environment.

## Initial Project Setup

Follow these steps to set up this template for your Stalicla web project:

### Switching from the Template Repo to Your Own Project Repo

1. Clone the 'web-apps' branch of the template repo into your local machine with the name of your project:

```bash
git clone --branch web-apps --single-branch git@gitlab.local.stalicladds.com:dds/templates/stalicla-development-templates.git <your-project-name>
```

2. Navigate to the project folder:

```bash
cd <your-project-name>
```
3. Create an orphan branch to start a fresh commit history

```bash
git checkout --orphan temp
git commit -am "Initial commit"
```

After cloning the template repository, you should disconnect it from the template repo and connect it to your own project repository. This ensures that you don't accidentally commit changes to the template repository. Follow these steps:

4. Remove the existing remote connection to the template repository:

```bash
git remote remove origin
```

5. Create a new repository for your project on Gitlab (choose the same name used for cloning the template in step 1) and take note of its url.

6. Connect your local project to the newly created remote repository:

```bash
git remote add origin <your-new-repository-url>
```
7. Create and push the 'main' branch:

```bash
git checkout -b main
git push -u origin main

```
8. Create push the 'development' branch:

```bash
git checkout -b development
git push -u origin development
```

9. Delete the original branch:

```bash
git branch -D <original-template-branch>
```

10. Create a feature branch to start developing
```bash
git checkout -b 'feat_<feature_name>'
```

Now your project is connected to your own repository, and you can safely commit and push changes without affecting the template repository.

The content of both main and development branches is the same as the "web apps" branch of the original template repo.

### Setting up Conda environment

A Python environment (with Conda) was chosen to set up Commitizen and Pre-commit hooks at the root level of the repository, which ensures a consistent setup process; however, this choice does not impose any restrictions on the programming language used for the rest of the project (within the src folder), allowing developers the freedom to choose their preferred language.

1. Make sure you have python3 and Conda installed in your system. You can check this by running:

```bash
python3 --version
conda --version
```

If they are not installed, download and install [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or [Anaconda](https://www.anaconda.com/products/distribution).

2. Create and activate a Conda environment using the `environment.yml` by running the following commands:

```bash
conda env create --name <your_project_name> --file environment.yml
conda activate <your_project_name>
```

The Conda environment created from the environment.yml file already includes Commitizen and Pre-commit.

### Setting up pre-commit hooks

1. Install and update the hooks specified in the `pre-commit-config.yaml` file:

```bash
pre-commit install
```

2. Test that the hooks have been correctly installed with:

```bash
pre-commit run --all-files
```

3. In order to update hooks to latest version, use:

```bash
pre-commit autoupdate
```

To set up specific hooks, exceptions or other configurations for your project, modify the `.pre-commit-config.yaml` file accordingly.

### Running Commitizen and Pre-commit hooks

1. When you want to make a commit, use the following command to launch Commitizen:

```bash
cz c
```

This command will trigger a console that prompts you with a series of questions to generate a well-formatted commit message.

Once the commit message has been correctly passed, Pre-commit will run the checks specified in the `pre-commit-config.yaml` file.

2. In case of errors, some will be automatically fixed, while others will require manual correction, for example:

```bash
Check Trailing whitespace in the code?...................................Passed
Check: Wrong end-of-files?...............................................Passed
Check: Json syntax errors?...........................(no files to check)Skipped
Check: yaml syntax errors?...............................................Passed
Check: Large files commited?.............................................Passed
Check: private keys commited?............................................Passed
Check: AWS credentials commited?.........................................Passed
Check: Commiting onto protected branches?................................Passed
Check: hardcoded secrets commited?.......................................Passed
Format Python code style.............................(no files to check)Skipped
Format JS/HTML/CSS/JSON/YAML code style..................................Failed
- hook id: prettier
- files were modified by this hook

src/project/test.js


Check: Dockerfile linting errors?........................................Passed
Check: Gitlab CI syntax errors?..........................................Passed
```

3. Once all errors have been fixed (if any), stage the modified files with `git add` and run Commitizen again.

4. If the changes are not substantial (e.g. formatting), you may use the `retry` flag to avoid re-typing the commit message.

```bash
cz c --retry
```

5. Some of the Pre-commit hooks (e.g. "commitizen-branch") are set to be run manually.

### Setting Up Linter

To set up a code linter for your project that can be run as a pre-commit hook, follow the steps below:

### 1. Set up a Linter for your project

First, set up the linter for your specific programming language within the `src` folder, ensuring they are scoped to your project code.

Here are some resources to help you find and set up the recommended linters for Python and TypeScript:

- [Python: Flake8 (Official Documentation)](https://flake8.pycqa.org/en/latest/)
- [TypeScript/Javascript: ESLint (Official Documentation)](https://eslint.org/docs/latest/use/getting-started)

For other programming languages, please refer to their official documentation or community guidelines for setting up linters.

### 2. Configure Pre-commit hook based on your project's Linter setup

Your repository already contains and example hook for ESLint (currently commented out). Follow the [instructions](https://github.com/pre-commit/mirrors-eslint) to configure the pre-commit hook in accordance with your project's linter setup.

## Start developing

Once you've set up the linter and updated pre-commit hook, you can start developing your project in the `src` folder (see [src.md](src/src.md))

As you develop your project and add new dependencies, frameworks, or features, you might need to update the GitLab CI/CD configuration and the Docker setup accordingly. Here are some general guidelines:

### Update GitLab CI/CD Configuration

The `.gitlab-ci.yml` file defines the build, test, and deployment stages for your project using GitLab CI/CD. The provided template contains a basic pipeline that covers building, testing, and pushing Docker images. As you adapt the template to fit the needs of your specific project, you may need to modify this file to accommodate new dependencies, frameworks, or features.

For example, you might need to update the build and test steps to include additional tasks specific to your project, such as installing new dependencies, running a different testing framework, or generating reports. Additionally, you may need to adjust the deployment stages to target specific environments or platforms, depending on your project's requirements.

Refer to Stalicla's CI/CD SOP for further information on how to manage the pipeline.

### Update Docker Configuration

The Docker structure consists of a `Dockerfile` and a `docker-compose.yml` file. The `Dockerfile` defines how the Docker image for your project is built, including the base image, dependencies, build steps, and other configurations required to run your project in a Docker container. As you adapt the template to your specific project, you might need to modify the `Dockerfile` to include new dependencies or change the base image to one that better suits your project's language or framework.

The `docker-compose.yml` file is provided as a starting point for orchestrating multi-container applications. While it is not integrated into the pipeline by default, you can modify your pipeline stages to utilize docker-compose for building, testing, and deploying your application if needed.

Refer to Stalicla's Docker SOP for further information on how to containerize your project.
