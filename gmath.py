import math
from display import *


  # IMPORANT NOTE

  # Ambient light is represeneted by a color value

  # Point light sources are 2D arrays of doubles.
  #      - The fist index (LOCATION) represents the vector to the light.
  #      - The second index (COLOR) represents the color.

  # Reflection constants (ka, kd, ks) are represened as arrays of
  # doubles (red, green, blue)

AMBIENT = 0
DIFFUSE = 1
SPECULAR = 2
LOCATION = 0
COLOR = 1
SPECULAR_EXP = 4

#lighting functions

def get_lighting(normal, view, ambient, light, areflect, dreflect, sreflect ):
    normalize(normal)
    normalize(light[LOCATION])
    normalize(view)
    #print(view)

    a = calculate_ambient(ambient, areflect)
    d = calculate_diffuse(light, dreflect, normal)
    s = calculate_specular(light, sreflect, view, normal)

    color = []
    [color.append(a[i] + d[i] + s[i]) for i in range(3)]
    return limit_color(color)
    #return [ x + y for x in calculate_ambient for y in limit_color(calculate_diffuse)]

def calculate_ambient(light, areflect):
    a = []
    [a.append(int(light[i] * areflect[i])) for i in range(3)]
    return limit_color(a)


def calculate_diffuse(light, dreflect, normal):
    d = []
    calc = dot_product( light[LOCATION] , normal )
    [d.append(light[COLOR][i] * dreflect[i] * calc) for i in range(3)]
    return limit_color(d)

def calculate_specular(light, sreflect, view, normal):
    f = []

    dot = 2 * dot_product(light[LOCATION], normal)
    [f.append( normal[i] * dot - light[LOCATION][i]) for i in range(3)]

    g = max((dot_product(f, view)) , 0 )
    g = pow(g, SPECULAR_EXP)

    s = []
    [s.append(light[COLOR][i] * sreflect[i] * g) for i in range(3)]

    return limit_color(s)

def limit_color(color):
    return [0 if x < 0
            else 255 if x > 255
            else int(x) for x in color]

#vector functions
#normalize vetor, should modify the parameter
def normalize(vector):
    magnitude = math.sqrt( vector[0] * vector[0] +
                           vector[1] * vector[1] +
                           vector[2] * vector[2])
    for i in range(3):
        vector[i] = vector[i] / magnitude

#Return the dot porduct of a . b
def dot_product(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

#Calculate the surface normal for the triangle whose first
#point is located at index i in polygons
def calculate_normal(polygons, i):

    A = [0, 0, 0]
    B = [0, 0, 0]
    N = [0, 0, 0]

    A[0] = polygons[i+1][0] - polygons[i][0]
    A[1] = polygons[i+1][1] - polygons[i][1]
    A[2] = polygons[i+1][2] - polygons[i][2]

    B[0] = polygons[i+2][0] - polygons[i][0]
    B[1] = polygons[i+2][1] - polygons[i][1]
    B[2] = polygons[i+2][2] - polygons[i][2]

    N[0] = A[1] * B[2] - A[2] * B[1]
    N[1] = A[2] * B[0] - A[0] * B[2]
    N[2] = A[0] * B[1] - A[1] * B[0]

    return N
