<p align="center">
    <a href="https://github.com/builtree/handwrite">
        <img src="https://raw.githubusercontent.com/builtree/assets/handwrite/logo_white_background.svg" width=40%>
        </img>
    </a>
</p>

[![Tests](https://github.com/builtree/handwrite/workflows/Tests/badge.svg)](https://github.com/builtree/handwrite/actions)
[![PyPI version](https://img.shields.io/pypi/v/handwrite.svg)](https://pypi.org/project/handwrite)
[![Gitter chat](https://badges.gitter.im/gitterHQ/gitter.svg)](https://gitter.im/codEd-org/handwrite)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![CodeQL](https://github.com/builtree/handwrite/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/builtree/handwrite/actions/workflows/codeql-analysis.yml)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/builtree/handwrite.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/builtree/handwrite/context:python)

# Handwrite - Type in your Handwriting!

Ever had those long-winded assignments, that the teacher always wants handwritten?
Is your written work messy, cos you think faster than you can write?
Now, you can finish them with the ease of typing in your own font!

<p align="center">
        <img src="https://raw.githubusercontent.com/builtree/assets/handwrite/handwrite.gif">
        </img>
</p>

Handwrite makes typing written assignments efficient, convenient and authentic.

Handwrite generates a custom font based on your handwriting sample, which can easily be used in text editors and word processors like Microsoft Word & Libre Office Word!

Handwrite is also helpful for those with dysgraphia.

You can get started with Handwrite [here](https://builtree.github.io/handwrite/).

## Sample

You just need to fill up a form:

<p align="center">
        <img src="https://raw.githubusercontent.com/builtree/assets/handwrite/handwrite_filled_form.jpg" width=50%>
        </img>
</p>

Here's the end result!

<p align="center">
        <img src="https://raw.githubusercontent.com/builtree/assets/handwrite/handwrite_sentence.png">
        </img>
</p>

## Credits and Reference

1. [Potrace](http://potrace.sourceforge.net/) algorithm and package has been immensely helpful.

2. [Fontforge](https://fontforge.org/en-US/) for packaging and adjusting font parameters.

3. [Sacha Chua's](https://github.com/sachac) [project](https://github.com/sachac/sachac-hand/) proved to be a great reference for fontforge python.

4. All credit for svgtottf converter goes to this [project](https://github.com/pteromys/svgs2ttf) by [pteromys](https://github.com/pteromys). We made a quite a lot of modifications of our own, but the base script idea was derived from here.
