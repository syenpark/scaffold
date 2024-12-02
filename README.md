# scaffold
This is a project scaffold for Python

## How to run?

- `src` should contain `.py` files for deployment.
- `notebooks` should have jupyter notebooks for exploration.
- `weights` should include pre-trained weights (models).
- [src/config.py](./src/config.py): for mainly configuration setting
- [src/utils](./src/utils/): for utilities like custom logging

## Poetry environment

### Pre-requisites
> NOTE: You can bypass these steps if you have completed them previously.

1. Install a [Git](https://git-scm.com/) client.

2. Set up [pyenv](https://github.com/pyenv/pyenv#installation) for Linux and macOS or [pyenv-win](https://github.com/pyenv-win/pyenv-win#installation) for Windows to manage your Python versions efficiently.

3. Install a recent CPython interpreter and enable it:

    ```shell
    pyenv install 3.12
    pyenv shell 3.12
    ```

4. Install [pipx](https://github.com/pypa/pipx/#install-pipx) (Please check your OS and how to install):

5. Install [Poetry via pipx](https://python-poetry.org/docs/#installing-with-pipx) (Please check your OS and how to install):

    ```shell
    pipx install poetry
    ```

### Installation

1. Create a virtual environment using Python's builtin [venv](https://docs.python.org/3/library/venv.html) in `<repo_path>`:
   
   This step places the virtual environment within the repository rather than using Poetry's central virtual environment directory, according to my personal preference.
   
    ```shell
    python -m venv .venv
    # Linux / macOS
    . .venv/bin/activate
    # Windows
    .venv\Scripts\activate
    ```

3. Install runtime and development dependencies:
    ```
    poetry install --with dev
    ```

4. Set up the git hook scripts (only once):

    run pre-commit install to set up the git hook scripts

    ```
    pre-commit install
    ```

    now pre-commit will run automatically on git commit!

### Usage

1. Activate the poetry environment

    ```
    poetry shell
    ```

2. How to install Python packages

    ```shell
    poetry add <package_name>
    ```

3. How to install dev Python packages

    ```shell
    poetry add --group dev <package_name>
    ```

4. When you want to git commit without pre-commit,

    ```shell
    git commit --no-verify
    ```
