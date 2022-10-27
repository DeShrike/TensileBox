from .group import Group
from .path import Path
from .text import Text
from . import constants
from .rotation import Rotation
import math

#######################################################################################
# Helpers
#######################################################################################

def distance(p1, p2) -> float:
    return distance2(p1[0], p1[1], p2[0], p2[1])

def distance2(x1:float, y1:float, x2:float, y2:float) -> float:
    return math.sqrt( ((x2 - x1) ** 2) + ((y2 - y1) ** 2))

def lerp(value:float, a:float, b:float) -> float:
	return (b - a) * value + a;

def lerp_point(value: float, p1:(float, float), p2:(float, float)) -> (float, float):
	return ( lerp(value, p1[0], p2[0]), lerp(value, p1[1], p2[1]) )

def add_bezier(path:Path, start:(float, float), stop:(float, float), c1:(float, float), c2:(float, float), steps:int = 10) -> None:
	for step in range(steps + 1):
		v = (1.0 / steps) * step
		a1 = lerp_point(v, start, c1)
		a2 = lerp_point(v, c1, c2)
		a3 = lerp_point(v, c2, stop)
		b1 = lerp_point(v, a1, a2)
		b2 = lerp_point(v, a2, a3)
		d1 = lerp_point(v, b1, b2)
		path.add_node(*d1)

def create_cross(cx:float, cy:float, length:float, id:str, color:str) -> Group:
    g = Group(id)
    p1 = Path(f"{id}A", False)
    p1.color = color
    p1.add_node(cx - length, cy)
    p1.add_node(cx + length, cy)
    g.add_path(p1)

    p2 = Path(f"{id}B", False)
    p2.color = color
    p2.add_node(cx, cy - length)
    p2.add_node(cx, cy + length)
    g.add_path(p2)

    return g

def create_line(x1:float, y1:float, x2:float, y2:float, id:str):
    p = path.Path(id, False)
    p.color = constants.RED
    p.add_node(x1, y1)
    p.add_node(x2, y2)
    return p

def create_hole(x1:float, y1:float, w:float, h:float, id:str):
    p = path.Path(id, True)
    p.color = constants.GREEN
    p.add_node(x1, y1)
    p.add_node(x1 + w, y1)
    p.add_node(x1 + w, y1 + h)
    p.add_node(x1, y1 + h)
    return p

def add_rounded_corner(path, x:float, y:float, r:float, corner:str, reverse:bool=False):
    if corner == "TL":
        start_angle = math.pi + (math.pi / 2)
        end_angle = math.pi / 2 + (math.pi / 2)
        cx = x + r
        cy = y + r
    elif corner == "TR":
        start_angle = math.pi / 2 + (math.pi / 2)
        end_angle = 0 + (math.pi / 2)
        cx = x - r
        cy = y + r
    elif corner == "BR":
        start_angle = 0 + (math.pi / 2)
        end_angle = -math.pi / 2 + (math.pi / 2)
        cx = x - r
        cy = y - r
    elif corner == "BL":
        start_angle = -math.pi / 2 + (math.pi / 2)
        end_angle = -math.pi + (math.pi / 2)
        cx = x + r
        cy = y - r

    if reverse:
	    a = end_angle
	    steps = 8
	    step = -(math.pi / 2) / steps
	    while a < start_angle:
	        xx = math.sin(a) * r + cx
	        yy = math.cos(a) * r + cy
	        path.add_node(xx, yy)
	        a -= step
	    a = start_angle
    else:
	    a = start_angle
	    steps = 8
	    step = (math.pi / 2) / steps
	    while a > end_angle:
	        xx = math.sin(a) * r + cx
	        yy = math.cos(a) * r + cy
	        path.add_node(xx, yy)
	        a -= step
	    a = end_angle

    xx = math.sin(a) * r + cx
    yy = math.cos(a) * r + cy
    path.add_node(xx, yy)

def create_rounded_box(x:int, y:int, w:int, h:int, rounding:int = 3, color:str = constants.MAGENTA):
    p = Path(f"rounded_box_{x}_{y}", True)
    p.color = color
    add_rounded_corner(p, x + 0, y + 0, rounding, "TL")
    add_rounded_corner(p, x + w, y + 0, rounding, "TR")
    add_rounded_corner(p, x + w, y + h, rounding, "BR")
    add_rounded_corner(p, x + 0, y + h, rounding, "BL")
    return p

def add_vert_pins(path, x:float, y:float, count:int, spacing:float, indent:float, thickness:float, direction:int, rotation:Rotation = None):
    # adds pins on a vertical line
    # x, y: start point
    # count: numbers of pins
    # spacing: distance between pin centers
    # indent: size of pin
    # thickness: thickness of pin
    # direction: 1 or -1: y-direction
    for _ in range(count):
        y += (spacing - (thickness / 2.0)) * direction
        path.add_node(x, y, rotation)
        x += indent
        path.add_node(x, y, rotation)
        y += thickness * direction
        path.add_node(x, y, rotation)
        x -= indent
        path.add_node(x, y, rotation)
        y -= (thickness / 2.0) * direction

def add_horz_pins(path, x:float, y:float, count:int, spacing:float, indent:float, thickness:float, direction:int, rotation:Rotation = None):
    # adds pins on a horizontal line
    # x, y: start point
    # count: numbers of pins
    # spacing: distance between stub centers
    # indent: size of pin
    # thickness: thickness of pin
    # direction: 1 or -1: x-direction
    for _ in range(count):
        x += (spacing - (thickness / 2.0)) * direction
        path.add_node(x, y, rotation)
        y += indent
        path.add_node(x, y, rotation)
        x += thickness * direction
        path.add_node(x, y, rotation)
        y -= indent
        path.add_node(x, y, rotation)
        x -= (thickness / 2.0) * direction

def add_horz_pins_ex(path, x:float, y:float, count:int, spacing:float, data, direction:int, slid_data = None):
    # adds pins on a horizontal line
    # x, y: start point
    # count: numbers of pins
    # spacing: distance between stub centers
    # indent: size of pin (depth)
    # thickness: thickness of pin (width)
    # direction: 1 or -1: x-direction
    for ix in range(count):
        indent = data[ix][0]
        thickness = data[ix][1]

        if slid_data is not None and ix > 0:
            slid_width = slid_data[1]
            slid_depth = slid_data[0]
            dx = spacing / 2
            sx = x + ((dx - (slid_width / 2)) * direction)
            path.add_node(sx, y)
            y += slid_depth
            path.add_node(sx, y)
            sx += slid_width * direction
            path.add_node(sx, y)
            y -= slid_depth
            path.add_node(sx, y)

        x += (spacing - (thickness / 2.0)) * direction
        path.add_node(x, y)
        y += indent
        path.add_node(x, y)
        x += thickness * direction
        path.add_node(x, y)
        y -= indent
        path.add_node(x, y)
        x -= (thickness / 2.0) * direction

def add_text(root, name:str):
    g = Group("legend")
    root.groups.append(g)
    t = Text(50, 40, constants.BLACK,   name)
    g.texts.append(t)
    t = Text(50, 45, constants.RED,     "Red: Etch")
    g.texts.append(t)
    t = Text(50, 50, constants.BLUE,    "Blue: Cut")
    g.texts.append(t)
    t = Text(50, 55, constants.GREEN,   "Green: Cut")
    g.texts.append(t)
    t = Text(50, 60, constants.MAGENTA, "Magenta: Cut")
    g.texts.append(t)

def save(root, filename, id, w:int, h:int):
    print(f"Writing file {filename}")
    with open(filename, "w") as fd:
        header = constants.SVG_START
        header = header.replace("{{FILENAME}}", filename)
        header = header.replace("{{ID}}", id)
        header = header.replace("{{PAPERWIDTH}}", str(w))
        header = header.replace("{{PAPERHEIGHT}}", str(h))
        fd.write(header)
        root.write_to_file(fd)
        fd.write(constants.SVG_END)
