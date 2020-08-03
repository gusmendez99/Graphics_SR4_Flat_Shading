"""
    Universidad del Valle de Guatemala
    Gustavo Mendez - 18500

    main.py - simple main file to create bmp files (render)
"""

from gl import Render
from utils import gl_color

render = Render()
render.load('./sonic.obj', translate=(375, 25, 0), scale = (24, 24, 100))
# Testing flat shading
# render.triangle(V3(10, 10, 1), V3(1000, 700, 1), V3(1000, 10, 1), color=gl_color.color(255, 0, 0))
render.glFinish(filename='out_flat_shading.bmp')