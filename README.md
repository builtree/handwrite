<p align="center">
    <a href="https://github.com/cod-ed/simulate">
        <img src="https://raw.githubusercontent.com/cod-ed/assets/handwrite/logo.svg" width=40%>
        </img>
    </a>
</p>

Tired of handwriting stuff? or want to generate a custom font of your handwriting?

Handwrite can generate custom font of your handwriting based on a writing sample.

# Installing
[Awating Release]

# Development

## Windows

1. Install [Potrace](http://potrace.sourceforge.net/#downloading) and make sure it's in your PATH.

2. Install [fontforge](https://fontforge.org/en-US/downloads/) and make sure scripting is enabled.

3. Clone the repository or your fork

`git clone https://github.com/cod-ed/handwrite`

4. (Optional) Make a virtual environment and activate it

`python -m venv .venv`
`.venv\Scripts\activate`

5. In the project directory run:

`pip install -e .`

6. Make sure the tests run:

`python setup.py test`

You are ready to go!
