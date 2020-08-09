"""
    Universidad del Valle de Guatemala
    Gustavo Mendez - 18500

    main.py - simple main file to create bmp files (render)
"""

from gl import Render

render = Render()
render.load('./sonic.obj', translate=(375, 25, 0), scale = (24, 24, 100))
render.finish(filename='out_flat_shading.bmp')