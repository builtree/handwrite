# Getting Started with Handwrite!

## Creating your Handwritten Sample

1. Take a printout of the [sample form](https://github.com/builtree/handwrite/raw/main/handwrite_sample.pdf).

2. Fill the form using the image below as a reference.

3. Scan the filled form using a scanner, or Adobe Scan in your phone.

4. Save the `.jpg` image in your system.

Your form should look like this:

<p align="center">
        <img src="https://raw.githubusercontent.com/builtree/assets/handwrite/handwrite_filled_form.jpg" width=50%>
        </img>
</p>

## Creating your font

1.  Make sure you have installed `handwrite`, `potrace` & `fontforge`.

2.  In a terminal type `handwrite [PATH TO IMAGE] [OUTPUT DIRECTORY]`.
    (You can also type `handwrite -h`, to see all the arguments you can use).

3.  (Optional) Config file containing custom options for your font can also be passed using
    the `--config [CONFIG FILE]` argument.

    ???+ note 
        - If you expicitly pass the metadata (filename, family or style) as CLI arguments, they are given a preference over the default config file data.

         - If no config file is provided for an input then the [default config file](https://github.com/builtree/handwrite/blob/main/handwrite/default.json) is used.

4.  Your font will be created as `OUTPUT DIRECTORY/OUTPUT FONT NAME.ttf`. Install the font in your system.

5.  Select your font in your word processor and get to work!
    Here's the end result!

<p align="center">
        <img src="https://raw.githubusercontent.com/builtree/assets/handwrite/handwrite_sentence.png">
        </img>
</p>

## Configuring

TO DO
