# Contributing guidelines

Thank you for your interest in contributing! We welcome contributions from
everyone. Here are some guidelines to help you get started.

## Table of Contents

1. [How to Contribute](#how-to-contribute)
   - [Reporting Bugs](#reporting-bugs)
   - [Suggesting Features](#suggesting-features)
   - [Contributing Code](#contributing-code)
2. [Development Workflow](#development-workflow)
   - [Setting Up Your Environment](#setting-up-your-environment)
   - [Pre-commit Hooks](#pre-commit-hooks)
   - [Conventional Commits](#conventional-commits)
   - [Semantic Versioning](#semantic-versioning)

## How to Contribute

### Reporting Bugs

If you find a bug, please report it by opening an issue. Include as much detail
as possible:
- A clear and descriptive title.
- Steps to reproduce the issue.
- Expected and actual results.
- Screenshots, if applicable.
- Any relevant logs or error messages.

### Suggesting Features

We welcome feature suggestions! To propose a new feature, please open an issue
with:
- A clear and descriptive title.
- A detailed description of the feature.
- Any relevant examples or use cases.

### Contributing Code

We accept code contributions through merge requests. Before you start working
on a fix or feature, ensure there's an open issue and it's been discussed with
the maintainers. This helps us avoid duplication of effort and ensures your
work aligns with the project goals.

## Development Workflow

### Setting Up Your Environment

1. Fork the repository and clone your fork:
2. Set up pre-commit hooks:
   ```sh
    pre-commit install --install-hooks
   ```
3. Install the required dependencies using [poetry](https://python-poetry.org/):
   ```sh
   poetry install
   ```

### Pre-commit Hooks

This project uses [pre-commit](https://pre-commit.com/#intro) hooks to ensure
code quality and consistency. These hooks will automatically run checks and
format your code before you can make a commit. If any checks fail, they must be
fixed before the commit can proceed. You can manually run the hooks on all
files with:
```sh
pre-commit run --all-files
```

### Conventional Commits

We follow the [Conventional Commits](https://www.conventionalcommits.org/)
specification for formatting our commit messages. This provides a consistent
way to communicate the intent of your changes and helps automate the release
process. Each commit message should have the following structure:
```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

`type` can be one of the following:
- `feat`: A new feature.
- `fix`: A bug fix.
- `docs`: Documentation only changes.
- `style`: Changes that do not affect the meaning of the code (white-space,
  formatting, missing semi-colons, etc).
- `refactor`: A code change that neither fixes a bug nor adds a feature.
- `perf`: A code change that improves performance.
- `test`: Adding missing or correcting existing tests.
- `build`: Changes that affect the build system or external dependencies.
- `ci`: Changes to our CI configuration files and scripts.
- `chore`: Other changes that don't modify sources or tests.
- `revert`: Reverts a previous commit

A commit that introduces a breaking change to the public API (correlating with
`MAJOR` in Semantic Versioning) must be marked as such. This is done by:
- Appending a `!` after the type/scope.
- Optionally adding a `BREAKING CHANGE: <description>` footer following the
[git-trailer-format](https://git-scm.com/docs/git-interpret-trailers)
convention.

Using a tool like [commitizen](https://commitizen-tools.github.io/commitizen/)
may take away some of the burden of formatting commit messages.

### Semantic Versioning

We use [Semantic Versioning](https://semver.org/) (SemVer) for our releases.
This means that each release version number will have the format
`MAJOR.MINOR.PATCH`:
- `MAJOR` version increments when there are incompatible API changes.
- `MINOR` version increments when functionality is added in a
  backwards-compatible manner.
- `PATCH` version increments when backwards-compatible bug fixes are made.

Ensure your contributions follow these guidelines to keep our project consistent and manageable.

## Additional Resources

- [Issue Tracker](../-/issues)
- [Pull Requests](../-/merge_requests)
- [Documentation](../-/wikis)

Thank you for contributing! We appreciate your effort and look forward to
working with you. If you have any questions, feel free to ask by opening an
issue or contacting the maintainers.
