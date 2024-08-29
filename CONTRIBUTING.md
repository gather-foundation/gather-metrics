# Contributing to Gather Metrics
Thank you for your interest in contributing to Gather Metrics! As a small team, we appreciate your support and ask that you follow these guidelines to help us manage contributions effectively.

## Issues

### 1. Feature Proposals:
If you have an idea for a new feature, please open an issue to discuss it before starting any work. This helps ensure that your idea aligns with the project's goals.

### 2. Search Before Posting:
Before submitting a new issue, search through existing issues to see if your idea or bug report has already been mentioned. If it has, consider contributing to the discussion.

### 3. Detailed Reports:
When submitting a bug report, the more detail you can provide, the easier it will be for us to address the issue. Include steps to reproduce, screenshots, or error messages where applicable.

### 4. React and Comment:
If you find an issue that you’re also experiencing, give it a reaction or leave a comment. This helps us prioritize the most impactful issues.

### 5. Contributing Ideas:
If you're unsure where to start, look for issues tagged with "help wanted".

## Setting Up a Development Environment

### Prerequisites

- Python 3.12+

### Installation

1. First, fork the repository on GitHub by clicking the "Fork" button on the repository's page. This will create a copy of the repository under your own GitHub account.

```bash
git clone https://gitub/gatherfoundation/tools/gather-metrics.git
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
fastapi dev src/main.py
```

2. Access local site

Visit http://127.0.0.1:8000/ for the main site.

3. Access API documentation

Visit http://127.0.0.1:8000/docs for the Swagger documentation.

4. Example API call

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/head-circumference" -H "Content-Type: application/json" -d '{"age_years": 3, "sex": "M", "hcirc_value": 50}'
```

### Running Tests:

To ensure your environment is correctly set up and your changes are safe, run the tests with:

```bash
pytest --cov=src
```

## Pull Requests

### Technical Requirements

- Linting and Type Hints:
Ensure your code follows the project's coding standards. Run linters, formatters and Mypy before submitting your PR. Feel free to setup the pre-commit and mypy configuration from the repo.

- Branching:
Submit all pull requests against the `development` branch. Documentation updates can be made against main.

- No Compiled Files:
Avoid including compiled files or static assets in your PR. Only submit source files.

- Testing:
Include relevant tests in the `/tests` directory. Ensure that all tests pass before submitting your PR.

- Commit Structure:
Feel free to use multiple commits for clarity. We will squash commits when merging.

- Review Process:

1. Open Discussion:
PRs are open for discussion, but please ensure that major feature additions have been discussed via an issue beforehand.

2. Keep PRs Focused:
Small, focused PRs are easier to review and more likely to be merged quickly. Large, unfocused PRs may be split or closed with recommendations on how to proceed.

3. Bugfixes:
Direct PRs for bug fixes are welcome, especially for issues already documented. If you're unsure whether something is a bug, open an issue for clarification before submitting a fix.

- Avoid Unsolicited Refactors:
Refactoring PRs without functional changes will generally be closed unless specifically requested.

## Additional Contribution Guidelines

- Documentation:
Contributions to the documentation are always welcome. Improving clarity, fixing typos, and adding new examples are great ways to help the community.

- Community Contributions:
There are many ways to contribute beyond code. Improving docs, suggesting usage patterns, and helping other users in the community are all valuable contributions.

- Communication:
If you believe an issue or PR was closed incorrectly, or you have additional questions, please reach out to our team at [developers@gatherfoundation.ch](mailto:developers@gatherfoundation.ch) or re-open the discussion respectfully.
