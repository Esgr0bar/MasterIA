# Continuous Integration and Deployment

## Overview

We use continuous integration (CI) to automatically test and deploy our project. This ensures that new changes do not break existing functionality and that our documentation is always up-to-date.

### GitHub Actions

Our project is set up with GitHub Actions for CI/CD. The following workflows are defined:

- **Test Workflow**: Automatically runs the unit tests defined in the `tests/` directory.
- **Documentation Deployment**: Deploys the `mkdocs` documentation to GitHub Pages whenever changes are pushed to the `main` branch.

### Setting Up CI/CD

1. **Test Workflow**:
   - The test workflow runs `pytest` to execute all unit tests.
   - Ensure all tests pass before merging to `main`.

2. **Documentation Deployment**:
   - `mkdocs gh-deploy` is used to deploy the latest documentation to GitHub Pages.

## Workflow Files

You can find the CI workflow files in the `.github/workflows/` directory.

For more details on setting up and customizing CI/CD workflows, refer to the [GitHub Actions Documentation](https://docs.github.com/en/actions).
