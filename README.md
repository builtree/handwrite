<p align="center">
    <a href="https://github.com/cod-ed/simulate">
        <img src="https://raw.githubusercontent.com/cod-ed/assets/handwrite/logo.svg" width=40%>
        </img>
    </a>
</p>

# Handwrite - Type in your Handwriting!

Ever had those long-winded assignments, that the teacher always wants handwritten?
Is your written work messy, cos you think faster than you can write?
Now, you can finish them with the ease of typing in your own font!

![handwrite](https://raw.githubusercontent.com/cod-ed/assets/handwrite/handwrite.gif)
Handwrite makes typing written assignments efficient, convenient and authentic.

Handwrite generates a custom font based on your handwriting sample, which can easily be used in text editors and word processors like Microsoft Word & Libre Office Word!

Handwrite is also helpful for those with dysgraphia.

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

# Usage

## Creating your Handwritten Sample 

1. Take a printout of the [sample form](https://github.com/cod-ed/handwrite/raw/main/handwrite_sample.pdf).
2. Fill the form using the image below as a reference.
3. Scan the filled form using a scanner, or Adobe Scan in your phone.
4. Save the `.jpg` image in your system.

Your form should look like this:
![Filled form](https://raw.githubusercontent.com/cod-ed/assets/handwrite/handwrite_filled_form.jpg)

## Creating your font
1. Make sure you have installed `handwrite`, `potrace` & `fontforge`.
2. In a terminal type `handwrite (PATHTOIMAGE) (OUTPUT_FONT_NAME)`.
(You can also type `handwrite -h`, to see all the arguments you can use).
3. Your font will be created as `OUTPUT_FONT_NAME.ttf`. Open it, and select install.
4. Select your font in your word processor and get to work!
