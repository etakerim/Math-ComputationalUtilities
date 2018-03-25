# Math In Code
Couple of demonstrations for showing common mathematical concepts in action, in the context of computer programs.

## Want to contribute?
If you find the bug or want to fix something in the project involve via submiting the pull request. Advice from non-coders is also welcome. Please do so by opening a new issue. Want to see new project or get better explanaton of existing ones? Get in touch. Every help is much appreciated.

## Logic Tables

### How it came about?
When I was solving long and tidious excerices involving completing large logic tables in my math class, I knew there must be a better way. Motivation was to create automatic script to help me check whether I came up with right solution.

### How it is implemented?
Overview of general functionality is included within the project folder. However, it is written in Slovak language, so here is the summary of the document.

1.  **Notation** - valid and properly parenthesized logical expression must be converted to available key symbols. Valid is e.g.: `~(A & B) => (C | D)`
1. **Tokenization** - Based on the rules of logic, symbols will be seperated and categorised based on their meaning. `&` = "and operator", `C` = variable, ...
1. **Shunting yard** -  For easier manipulation down the road, traditional infix notation is converted to postfix. `C => ~(A & B)` is the same as `C A B & ~ =>`. Data are in the end organized on the stack in an evaluation order.
1. **Table creation** - Number of variables determine number of rows in the table. Lists of booleans are generated and assosiated with given variable. Then they are merged in a vector fashion based on input expression. Results are formatted and displayed.

### How to run it?
Download `logic_tables.py` and run it with python3 interpreter. No external dependencies are required.

## Matrices

### How it came about?
Vectors feel to a lot of students like a foreign topic with no real aplication. Manipulating with those arrows in space is even stranger. Motivation was to write basic readable code containing linear transformations for 3D graphics beginners, who want to see the details.

### How it is implemented?
Presentation slides (`Vektory.pdf`) describe the basic ideas and concepts to further understand the code. Main workhorses of the program are *Simple DirectMedia Library 2* (draw to screen, handle events) and a function *transform()*, which does matrix-vector multiply to apply matrix to every vetrex in the scene.

You can run (result is dependent on origin's poistion):

* Scaling - (+/-)
* Move - (Up/Down/Left/Right keys)
* Rotate - (i/o)
* Move origin - click

There are two different files:

* `real_coords.c` - Manipulations are done in real screen coordinates (e.g. 1280x720) and axis are rotated as they are in computer graphics (y - poining down)
* `transform_vieport.c` - More sophisticated example. Space where the triangle lives (2D Carthesian plain, -10 to 10) is projected onto graphics window with viewport transformation. This code was made with built-in modulatity. You can change viewport, displayed polygon or add custom transformation easily.

### How to run it?
You have to have C compiler (gcc) and SDL2 Library installed. In order to run the program you have to **change font location** to your own.

If you run **debian derivated distro**, for SDL installation run:
```zsh
$ sudo apt-get install 'libsdl2*'
```
To compile and run :
```zsh
$ gcc --std=c99 transform_viewport.c -lSDL2 -lSDL2_ttf -lSDL2_gfx -lm -o program
$ ./program
```

## MyGithubAvatar
### How it came about?
Originally meant to be part of gui project, to demonstate different ways of manipulating with objects mathematically. When testing classes nice complex and yet simple image was created. After I joined github it became my avatar and this code was left as a reminder of how it was all done.

### How it is implemented?
Main generator is in `graphobjects.py` along side with classes, which carries the drawing procedures. Final image `logo-koch.png` containes Koch snowflake with two Roses and a fractal tree inside a lissajous curve flower pot.

### How to run it?
You would ever want to use it only as a library for your own pictures. Be noted, API is not as polished as I have wished it to be, so some operations may be very clunky.

#### Dependencies
You have to install Pillow image library:
```zsh
$ pip3 install pillow
```
#### Usage
Then copy `vector.py` and `graphobjects.py` to your project directory. After that simply include and use:
```python
import graphobjects as go

with go.MathLogo(Image.new('RGB', IMG_SIZE), 'image.png') as ico:
    center = (600 / 2, 600 / 2)
    ico.rectangle((0, 0, 300, 300), fill=(235, 235, 235))
    go.KochFractal(ico, lwidth=LINE_WIDTH, color=(33, 145, 237)).snowflake(*center, 220)
```

#### TODO
Create installable package
