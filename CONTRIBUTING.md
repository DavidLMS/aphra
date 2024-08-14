<!-- omit in toc -->
# Contributing to 🌐💬 Aphra

First off, thanks for taking the time to contribute! Your help is greatly appreciated.

All types of contributions are encouraged and valued, whether it's code, documentation, suggestions for new features, or bug reports. Please read through the following guidelines before contributing to ensure a smooth process for everyone involved.

> And if you like the project, but just don't have time to contribute, that's fine. There are other easy ways to support the project and show your appreciation, which we would also be very happy about:
> - Star the project
> - Tweet about it
> - Refer this project in your project's README
> - Mention the project at local meetups and tell your friends/colleagues

<!-- omit in toc -->
## Table of Contents

- [I Have a Question](#i-have-a-question)
- [I Want To Contribute](#i-want-to-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Your First Code Contribution](#your-first-code-contribution)
  - [Improving The Documentation](#improving-the-documentation)
- [Styleguides](#styleguides)
  - [Commit Messages](#commit-messages)

## I Have a Question

If you want to ask a question, we assume that you have read the available [Documentation](https://github.com/DavidLMS/aphra/blob/main/README.md).

Before you ask a question, it is best to search for existing [Issues](https://github.com/DavidLMS/aphra/issues) that might help you. If you find a relevant issue but still need clarification, feel free to comment on it. Additionally, it’s a good idea to search the web for answers before asking.

If you still need to ask a question, we recommend the following:

- Open an [Issue](https://github.com/DavidLMS/aphra/issues/new).
- Provide as much context as you can about what you're running into.
- Provide project and platform versions (Python, OS, etc.), depending on what seems relevant.

We (or someone in the community) will then take care of the issue as soon as possible.

## I Want To Contribute

> ### Legal Notice <!-- omit in toc -->
> When contributing to this project, you must agree that you have authored 100% of the content, that you have the necessary rights to the content, and that the content you contribute may be provided under the project license.

### Reporting Bugs

#### Before Submitting a Bug Report

A good bug report shouldn't leave others needing to chase you up for more information. Please investigate carefully, collect information, and describe the issue in detail in your report. Follow these steps to help us fix any potential bugs as quickly as possible:

- Ensure you are using the latest version.
- Verify that your issue is not due to misconfiguration or environmental issues. Make sure you have read the [documentation](https://github.com/DavidLMS/aphra/blob/main/README.md).
- Check if the issue has already been reported by searching the [bug tracker](https://github.com/DavidLMS/aphra/issues?q=label%3Abug).
- Gather as much information as possible about the bug:
  - Stack trace (if applicable)
  - OS, platform, and version (Windows, Linux, macOS, etc.)
  - Python version and any relevant package versions
  - Steps to reliably reproduce the issue

#### How Do I Submit a Good Bug Report?

> Do not report security-related issues, vulnerabilities, or bugs with sensitive information in public forums. Instead, report these issues privately by emailing [your contact email].

We use GitHub issues to track bugs and errors. If you run into an issue with the project:

- Open an [Issue](https://github.com/DavidLMS/aphra/issues/new). (Since we can't be sure yet if it’s a bug, avoid labeling it as such until confirmed.)
- Explain the behavior you expected and what actually happened.
- Provide as much context as possible and describe the steps someone else can follow to recreate the issue. This usually includes a code snippet or an example project.

Once it's filed:

- The project team will label the issue accordingly.
- A team member will try to reproduce the issue. If the issue cannot be reproduced, the team will ask for more information and label the issue as `needs-repro`.
- If the issue is reproducible, it will be labeled `needs-fix` and potentially other relevant tags.

### Suggesting Enhancements

This section guides you through submitting an enhancement suggestion for 🌐💬 Aphra, whether it's a new feature or an improvement to existing functionality.

#### Before Submitting an Enhancement

- Ensure you are using the latest version.
- Check the [documentation](https://github.com/DavidLMS/aphra/blob/main/README.md) to see if your suggestion is already supported.
- Search the [issue tracker](https://github.com/DavidLMS/aphra/issues) to see if the enhancement has already been suggested. If so, add a comment to the existing issue instead of opening a new one.
- Make sure your suggestion aligns with the scope and aims of the project. It's important to suggest features that will be beneficial to the majority of users.

#### How Do I Submit a Good Enhancement Suggestion?

Enhancement suggestions are tracked as [GitHub issues](https://github.com/DavidLMS/aphra/issues).

- Use a **clear and descriptive title** for the suggestion.
- Provide a **detailed description** of the enhancement, including any relevant context.
- **Describe the current behavior** and **explain what you would expect instead**, along with reasons why the enhancement would be beneficial.
- Include **screenshots or diagrams** if applicable to help illustrate the suggestion.
- Explain why this enhancement would be useful to most `🌐💬 Aphra` users.

### Your First Code Contribution

#### Pre-requisites

You should first [fork](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo) the `🌐💬 Aphra` repository and then clone your forked repository:

```bash
git clone https://github.com/<YOUR_GITHUB_USER>/aphra.git
````

Once in the cloned repository directory, create a new branch for your contribution:

```bash
git checkout -B <feature-description>
````

### Contributing Workflow

1. Make sure your code follows the style guide and passes linting with `pylint`.
2. Write tests for any new functionality you add.
3. Ensure all tests pass before submitting a pull request.
4. Document any changes to APIs or core functionality.
5. Submit your pull request, providing a clear and descriptive title and description of your changes.

### Improving The Documentation

Contributions to documentation are welcome! Well-documented code is easier to understand and maintain. If you see areas where documentation can be improved, feel free to submit your suggestions.

## Styleguides

### Commit Messages

- Use clear and descriptive commit messages.
- Follow the general format: `Short summary (50 characters or less)` followed by an optional detailed explanation.

### Code Style

- Ensure your code adheres to the project's coding standards and passes all linting checks with `pylint`.

## License

By contributing to 🌐💬 Aphra, you agree that your contributions will be licensed under the MIT License.