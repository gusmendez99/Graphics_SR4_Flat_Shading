"""
    Universidad del Valle de Guatemala
    Gustavo Mendez - 18500

    gl.py - all logic to create a bmp file
"""

from utils.color import *
from utils.encoder import *
from obj import Obj
import random

from collections import namedtuple

V2 = namedtuple('Vertex2', ['x', 'y'])
V3 = namedtuple('Vertex3', ['x', 'y', 'z'])

# ===============================================================
# Math - Code given in class from @denn1s
# ===============================================================

def sum(v0, v1):
    """
        Input: 2 size 3 vectors
        Output: Size 3 vector with the per element sum
    """
    return V3(v0.x + v1.x, v0.y + v1.y, v0.z + v1.z)

def sub(v0, v1):
    """
        Input: 2 size 3 vectors
        Output: Size 3 vector with the per element substraction
    """
    return V3(v0.x - v1.x, v0.y - v1.y, v0.z - v1.z)

def mul(v0, k):
    """
        Input: 2 size 3 vectors
        Output: Size 3 vector with the per element multiplication
    """
    return V3(v0.x * k, v0.y * k, v0.z *k)

def dot(v0, v1):
    """
        Input: 2 size 3 vectors
        Output: Scalar with the dot product
    """
    return v0.x * v1.x + v0.y * v1.y + v0.z * v1.z

def length(v0):
    """
        Input: 1 size 3 vector
        Output: Scalar with the length of the vector
    """  
    return (v0.x**2 + v0.y**2 + v0.z**2)**0.5

def norm(v0):
    """
        Input: 1 size 3 vector
        Output: Size 3 vector with the normal of the vector
    """  
    v0length = length(v0)

    if not v0length:
        return V3(0, 0, 0)

    return V3(v0.x/v0length, v0.y/v0length, v0.z/v0length)


def bbox(*vertices):
    xs = [ vertex.x for vertex in vertices ]
    ys = [ vertex.y for vertex in vertices ]

    xs.sort()
    ys.sort()

    xmin = xs[0]
    xmax = xs[-1]
    ymin = ys[0]
    ymax = ys[-1]

    return xmin, xmax, ymin, ymax

def cross(v1, v2):
    return V3(
        v1.y * v2.z - v1.z * v2.y,
        v1.z * v2.x - v1.x * v2.z,
        v1.x * v2.y - v1.y * v2.x,
    )

def barycentric(A, B, C, P):
    cx, cy, cz = cross(
        V3(B.x - A.x, C.x - A.x, A.x - P.x),
        V3(B.y - A.y, C.y - A.y, A.y - P.y),
    )

    if abs(cz) < 1:
        return -1, -1, -1

    u = cx/cz
    v = cy/cz
    w = 1 - (cx + cy) / cz

    return w, v, u


class Render(object):
    # glInit dont needed, 'cause we have an __init__ func
    def __init__(self):
        self.framebuffer = []
        self.width = 800
        self.height = 800
        self.viewport_x = 0
        self.viewport_y = 0
        self.viewport_width = 800
        self.viewport_height = 800
        self.clear()

    def point(self, x, y, color):
        self.framebuffer[y][x] = color

    def create_window(self, width, height):
        self.height = height
        self.width = width

    def viewport(self, x, y, width, height):
        # Setting viewport initial values
        self.viewport_x = x
        self.viewport_y = y
        self.viewport_height = height
        self.viewport_width = width

    def clear(self):
        BLACK = color(0,0,0)
        self.framebuffer = [
            [BLACK for x in range(self.width)] for y in range(self.height)
        ]

        self.zbuffer = [
            [-float('inf') for x in range(self.width)]
            for y in range(self.height)
        ]
        
    def load(self, filename='default.obj', translate=[0,0], scale=[1,1]):
        model = Obj(filename)

        light = V3(0, 0, 1)

        for face in model.faces:
            vcount = len(face)

            if vcount == 3:
                face1 = face[0][0] - 1
                face2 = face[1][0] - 1
                face3 = face[2][0] - 1

                v1 = model.vertices[face1]
                v2 = model.vertices[face2]
                v3 = model.vertices[face3]

                x1 = round((v1[0] * scale[0]) + translate[0])
                y1 = round((v1[1] * scale[1]) + translate[1])
                z1 = round((v1[2] * scale[2]) + translate[2])

                x2 = round((v2[0] * scale[0]) + translate[0])
                y2 = round((v2[1] * scale[1]) + translate[1])
                z2 = round((v2[2] * scale[2]) + translate[2])

                x3 = round((v3[0] * scale[0]) + translate[0])
                y3 = round((v3[1] * scale[1]) + translate[1])
                z3 = round((v3[2] * scale[2]) + translate[2])

                a = V3(x1, y1, z1)
                b = V3(x2, y2, z2)
                c = V3(x3, y3, z3)

                normal = cross(sub(b, a), sub(c, a))
                intensity = dot(norm(normal), norm(light))
                grey = round(255 * intensity)
                if grey < 0:
                    continue

                intensity_color = color(grey, grey, grey)
                self.triangle(a, b, c, intensity_color)

            else:
                face1 = face[0][0] - 1
                face2 = face[1][0] - 1
                face3 = face[2][0] - 1
                face4 = face[3][0] - 1

                v1 = model.vertices[face1]
                v2 = model.vertices[face2]
                v3 = model.vertices[face3]
                v4 = model.vertices[face4]

                x1 = round((v1[0] * scale[0]) + translate[0])
                y1 = round((v1[1] * scale[1]) + translate[1])
                z1 = round((v1[2] * scale[2]) + translate[2])

                x2 = round((v2[0] * scale[0]) + translate[0])
                y2 = round((v2[1] * scale[1]) + translate[1])
                z2 = round((v2[2] * scale[2]) + translate[2])

                x3 = round((v3[0] * scale[0]) + translate[0])
                y3 = round((v3[1] * scale[1]) + translate[1])
                z3 = round((v3[2] * scale[2]) + translate[2])

                x4 = round((v4[0] * scale[0]) + translate[0])
                y4 = round((v4[1] * scale[1]) + translate[1])
                z4 = round((v4[2] * scale[2]) + translate[2])

                a = V3(x1, y1, z1)
                b = V3(x2, y2, z2)
                c = V3(x3, y3, z3)
                d = V3(x4, y4, z4)

                intensity = dot(norm(normal), norm(light))
                grey = round(255 * intensity)
                if grey < 0:
                    continue

                intensity_color = color(grey, grey, grey)

                self.triangle(a, b, c, intensity_color)
                self.triangle(a, c, d, intensity_color)


    def triangle(self, A, B, C, color):
        xmin, xmax, ymin, ymax = bbox(A, B, C)

        for x in range(xmin, xmax + 1):
            for y in range(ymin, ymax + 1):
                P = V2(x, y)
                w, v, u = barycentric(A, B, C, P)
                if w < 0 or v < 0 or u < 0:
                    # point is outside
                    continue

                z = A.z * u + B.z * v + C.z * w
                if z > self.zbuffer[y][x]:
                    self.point(x, y, color)
                    self.zbuffer[y][x] = z

    def finish(self, filename='out.bmp'):
        # starts creating a new bmp file
        f = open(filename, 'bw')

        f.write(char('B'))
        f.write(char('M'))
        f.write(dword(14 + 40 + self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(14 + 40))

        # image header
        f.write(dword(40))
        f.write(dword(self.width))
        f.write(dword(self.height))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword(self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))

        # Finishing placing points
        try:
            for x in range(self.height):
                for y in range(self.width):
                    f.write(self.framebuffer[x][y])
        except:
            print('Your obj file is too big. Try another scale/translate values')

        f.close()
        self.finish_zbuffer(filename='z_buffer.bmp')


    def finish_zbuffer(self, filename):
        # starts creating a new bmp file
        f = open(filename, 'wb')
        
        f.write(char('B'))
        f.write(char('M'))
        f.write(dword(14 + 40 + self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(14 + 40))

        # image header
        f.write(dword(40))
        f.write(dword(self.width))
        f.write(dword(self.height))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword(self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))

        z_min = float('inf')
        z_max = -float('inf')

        for x in range(self.height):
            for y in range(self.width):
                if self.zbuffer[x][y] != -float('inf'):
                    if self.zbuffer[x][y] > z_max:
                        z_max = self.zbuffer[x][y]

                    if self.zbuffer[x][y] < z_min:
                        z_min = self.zbuffer[x][y]

        for x in range(self.height):
            for y in range(self.width):
                z_value = self.zbuffer[x][y]

                if z_value == -float('inf'):
                    z_value = z_min

                z_value = round(((z_value - z_min) / (z_max - z_min)) * 255)
                z_color = color(z_value, z_value, z_value)
                f.write(z_color)

        f.close()
