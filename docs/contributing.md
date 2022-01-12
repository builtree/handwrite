# Development

## Linux

1. Install Potrace using apt

    ```console
    sudo apt-get install potrace
    ```

2. Install fontforge

    ```console
    sudo apt-get install fontforge
    ```

    ???+ warning
        Since the PPA for fontforge is no longer maintained, apt might not work for some users.
        The preferred way to install is using the AppImage from: https://fontforge.org/en-US/downloads/

3. Clone the repository or your fork

    ```console
    git clone https://github.com/builtree/handwrite
    ```

4. (Optional) Make a virtual environment and activate it

    ```console
    python -m venv .venv
    source .venv/bin/activate
    ```

5. In the project directory run:

    ```console
    pip install -e .[dev]
    ```

6. Make sure the tests run:

    ```console
    python setup.py test
    ```

7. Install pre-commit hooks before contributing:

    ```console
    pre-commit install
    ```

You are ready to go!

## Windows

1. Install [Potrace](http://potrace.sourceforge.net/#downloading) and make sure it's in your PATH.

2. Install [fontforge](https://fontforge.org/en-US/downloads/) and make sure scripting is enabled.

3. Clone the repository or your fork

    ```console
    git clone https://github.com/builtree/handwrite
    ```

4. (Optional) Make a virtual environment and activate it

    ```console
    python -m venv .venv
    .venv\Scripts\activate
    ```

5. In the project directory run:

    ```console
    pip install -e .[dev]
    ```

6. Make sure the tests run:

    ```console
    python setup.py test
    ```

7. Install pre-commit hooks before contributing:

    ```console
    pre-commit install
    ```

You are ready to go!
