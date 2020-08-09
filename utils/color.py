"""
    Universidad del Valle de Guatemala
    Gustavo Mendez - 18500

    color.py - simple color functions
"""

def normalizeColorArray(colors_array):
    return [round(i*255) for i in colors_array]

def color(r,g,b):
	return bytes([b, g, r])