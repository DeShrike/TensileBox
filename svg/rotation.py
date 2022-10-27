import math

class Rotation():
    def __init__(self, cx:float, cy:float, angle:float):
        self.cx = cx
        self.cy = cy
        self.angle = angle


def rotate(r:Rotation, x:float, y:float):
    return rotate_point(r.cx, r.cy, x, y, r.angle)

def rotate_point(cx:float, cy:float, px:float, py:float, angle:float):
    radians = angle / 360 * 2 * math.pi
    s = math.sin(radians)
    c = math.cos(radians)

    # translate to origin
    rx = px - cx
    ry = py - cy

    # rotate
    xnew = rx * c - ry * s
    ynew = rx * s + ry * c

    # translate back
    xnew += cx
    ynew += cy
    
    return (xnew, ynew)

