# Contributing


Thanks for taking the time to contribute to `iso639-lang`!

If you want to add or improve a feature, please create a GitHub issue to discuss your proposal before you submit a pull request.


## Pull Request Guidelines

- Keep your pull request focused on a single feature or change.
- Include tests for any new features or changes.
- Update the documentation if necessary.
- Make sure all tests pass.
- Ensure that your code follows the project's code style.


## Creating a Development Environment

Fork the repository.

```
https://github.com/LBeaudoux/iso639/fork
```

Clone the repository.

```sh
git clone https://github.com/your-username/iso639.git
cd iso639
```

Create a virtual environment.

```sh
python3 -m venv env_iso639
source env_iso639/bin/activate
```

Build and install `iso639-lang` in 'editable' mode.

```sh
pip install -e .
pip install -r requirements-dev.txt
```


## Running Tests

```sh
pytest tests dev_tests
```

The main tests are located in `tests/`. They run faster and don't require access to the original ISO 639 data files located in `dev_iso639/downloads/`.

The tests in `dev_tests` are slower because they check that the `iso639-lang` library is fully consistent with the official ISO 639 tables.

Pushing changes to your forked repository should trigger a [workflow](https://github.com/LBeaudoux/iso639/actions/workflows/ci.yml) that tests your code across multiple operating systems and Python versions.


## Running Code Style Checks

```sh
flake8
black --check .
isort --check-only .
```

`iso639-lang` uses `flake8` for linting, `black` for formatting and `isort` for sorting imports. The configuration of these tools is available in the `.flake8` and `pyproject.toml` files.


## Submitting Changes

Specify a new remote upstream repository to sync with the forked repository.

```sh
git remote add upstream https://github.com/LBeaudoux/iso639.git
```

Check that your local repository has a remote link to both your forked repository (origin) and `LBeaudoux/iso639` (upstream).

```sh
git remote -v
```

Make sure your local master branch is up to date.

```sh
git checkout master
git pull upstream master
``` 

Create a new branch for your changes.
   
```sh
git checkout -b new-branch-name
```

Commit your changes with a clear and concise commit message.

```sh
git commit -m "Add a brief description of your changes"
```

Push your changes to your forked repository.

```sh
git push origin new-branch-name
```

Navigate to your forked repository and click on the 'New Pull Request' button. Select your branch and provide a description of your changes.

