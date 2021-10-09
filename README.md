# Light Speed Battle

[日本語版](./README-ja.md)

This is a FPS game where you can experience special relativity.

![SS1](./play_screenshot_1.png)
![SS2](./play_screenshot_2.png)

## Usage

dependency

* Python3
* OpenGL
* SDL2

How to build

1. Install Python3
2. Install OpenGL
    * At macOS `brew install glfw`
3. If it doesn't work with the SDL2 included in this repository, install SDL2 on your own.
    * At macOS `brew install sdl2`
4. Install Python lib

    ```
    pip install pipenv
    pipenv install -d
    ```
5. Built by Cython

    ```
    python cython_setup.py build_ext --inplace
    ```
6. Let's play!

    ```
    pipenv run python LSBattle3D.py
    ```
