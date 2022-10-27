import os
import math
from svg.constants import *
from svg.layer import Layer
from svg.group import Group
from svg.path import Path
from svg.ellipse import Ellipse
from svg.helpers import create_rounded_box, save, create_cross, distance2, add_rounded_corner, add_bezier
from svg.rotation import Rotation
from config import *

class Gaten():
	def __init__(self):
		self.gat_length = 10
		self.gat_width = THICKNESS + 0.1

		half_diagonal_length = math.sqrt( (BASE_WIDTH * BASE_WIDTH) + (BASE_HEIGHT * BASE_HEIGHT) ) / 2

		gat1center = half_diagonal_length / 3
		gat2center = (half_diagonal_length / 3) * 2

		self.gat1x = gat1center * math.cos(math.radians(45))
		self.gat1y = gat1center * math.sin(math.radians(45))

		self.gat2x = gat2center * math.cos(math.radians(45))
		self.gat2y = gat2center * math.sin(math.radians(45))

		# self.gat_distance = half_diagonal_length / 3
		self.gat_distance = distance2(self.gat1x, self.gat1y, self.gat2x, self.gat2y)


def create_horizontal_plate(root, offset_x:int, offset_y:int):
	#######################
	plate = Group(f"plate")
	root.groups.append(plate)

	centercross = create_cross(offset_x + BASE_WIDTH / 2, offset_y + BASE_HEIGHT / 2, 5, "centercross", BLACK)
	plate.add_group(centercross)

	c = create_rounded_box(offset_x, offset_y, BASE_WIDTH, BASE_HEIGHT, rounding=10)
	plate.add_path(c)

	#######################
	holes = Group(f"holes")
	plate.add_group(holes)

	gaten = Gaten()

	#h1cross = create_cross(offset_x + gaten.gat1x, offset_y + gaten.gat1y, 5, "h1cross", BLACK)
	#plate.add_group(h1cross)
	#h2cross = create_cross(offset_x + gaten.gat2x, offset_y + gaten.gat2y, 5, "h2cross", BLACK)
	#plate.add_group(h2cross)

	angle = 45	# degrees TODO : calculate angle based on BASE_WIDTH and BASE_HEIGHT

	def makehole(x:float, y:float) -> Path:
		r = Rotation(x, y, angle)
		x1 = x - (gaten.gat_length / 2)
		y1 = y - (gaten.gat_width / 2)
		x2 = x + (gaten.gat_length / 2)
		y2 = y + (gaten.gat_width / 2)

		holepath = Path(f"hole_{x:.3f}_{y:.3f}", True)
		holepath.color = RED
		holepath.move((offset_x, offset_y))
		holepath.add_node(x1, y1, r)
		holepath.add_node(x2, y1, r)
		holepath.add_node(x2, y2, r)
		holepath.add_node(x1, y2, r)
		return holepath

	gat1 = makehole(gaten.gat1x, gaten.gat1y)
	gat2 = makehole(gaten.gat2x, gaten.gat2y)

	holes.add_path(gat1)
	holes.add_path(gat2)

	#######################
	wirehole_margin = 7
	wirehole_radius = WIREHOLE_RADIUS

	wireholes = Group(f"wireholes")
	plate.add_group(wireholes)

	wirehole_tl = Ellipse(offset_x + wirehole_margin, offset_y + wirehole_margin, wirehole_radius, RED)
	wirehole_tr = Ellipse(offset_x + BASE_WIDTH - wirehole_margin, offset_y + wirehole_margin, wirehole_radius, RED)
	wirehole_bl = Ellipse(offset_x + wirehole_margin, offset_y + BASE_HEIGHT - wirehole_margin, wirehole_radius, RED)
	wirehole_br = Ellipse(offset_x + BASE_WIDTH - wirehole_margin, offset_y + BASE_HEIGHT - wirehole_margin, wirehole_radius, RED)

	wireholes.add_ellipse(wirehole_tl)
	wireholes.add_ellipse(wirehole_tr)
	wireholes.add_ellipse(wirehole_bl)
	wireholes.add_ellipse(wirehole_br)

def create_vertical_stand(root, offset_x, offset_y):
	stand = Group(f"stand")
	root.groups.append(stand)

	half_diagonal_length = math.sqrt( (BASE_WIDTH * BASE_WIDTH) + (BASE_HEIGHT * BASE_HEIGHT) ) / 2
	stand_width = half_diagonal_length * 0.65	# 80% of base plate radius
	foot_height = STAND_WIDTH
	arm_width = STAND_HEIGHT / 2

	stand_height = STAND_HEIGHT + foot_height / 2

	outline = Path(f"stand_outline", True)
	outline.color = MAGENTA

	gaten = Gaten()

	gatenwidth = gaten.gat_distance + gaten.gat_length
	firstgat_start = (stand_width - gatenwidth) / 2
	gat_gap = gatenwidth - (2 * gaten.gat_length)

	print(f"Gatenwidth: {gatenwidth}")
	print(f"firstgat_start: {firstgat_start}")
	print(f"gat_gap: {gat_gap}")

	outline.move((offset_x, offset_y))

	pin_size = THICKNESS * 1.05

	## Corner 0
	outline.add_node(0, 0)
	## Gat 1
	outline.add_node(firstgat_start, 0)
	outline.add_node(firstgat_start, -pin_size)
	outline.add_node(firstgat_start + gaten.gat_length, -pin_size)
	outline.add_node(firstgat_start + gaten.gat_length, 0)

	## Gat 2
	outline.add_node(firstgat_start + gaten.gat_length + gat_gap, 0)
	outline.add_node(firstgat_start + gaten.gat_length + gat_gap, -pin_size)
	outline.add_node(firstgat_start + gaten.gat_length + gat_gap + gaten.gat_length, -pin_size)
	outline.add_node(firstgat_start + gaten.gat_length + gat_gap + gaten.gat_length, 0)

	## Corner 1
	outline.add_node(stand_width, 0)

	## Corner 2
	add_rounded_corner(outline, stand_width, foot_height, 10, "BR")
	#outline.add_node(stand_width, foot_height)

	## Corner 3
	add_rounded_corner(outline, foot_height, foot_height, 20, "TL", reverse=True)
	#outline.add_node(foot_height, foot_height)

	## Corner 4
	add_rounded_corner(outline, foot_height, foot_height + stand_height - 2 * foot_height, 10, "BL", reverse=True)
	#outline.add_node(foot_height, foot_height + stand_height - 2 * foot_height)

	## Corner 5
	add_rounded_corner(outline, stand_width + 14, foot_height + stand_height - 2 * foot_height, 7, "TR")
	#outline.add_node(stand_width + 14, foot_height + stand_height - 2 * foot_height)

	## Corner 6
	add_rounded_corner(outline, stand_width + 14, stand_height, 7, "BR")
	#outline.add_node(stand_width + 14, stand_height)

	## Corner 7
	add_rounded_corner(outline, 0, stand_height, 25, "BL")
	#outline.add_node(0, stand_height)

	b_start = (outline.last_x(), outline.last_y())
	b_end = (0, 0)
	b_height = outline.last_y() - 0
	b_c1 = (0, outline.last_y() - b_height / 3)
	b_c2 = (10, b_height / 3)
	add_bezier(outline, b_start, b_end, b_c1, b_c2)

	stand.add_path(outline)

	wirehole_radius = WIREHOLE_RADIUS
	holexo = half_diagonal_length / 3 * 2 + firstgat_start

	wirehole = Ellipse(offset_x + holexo, offset_y + stand_height - foot_height / 2, wirehole_radius, RED)
	stand.add_ellipse(wirehole)


def create():
	root = Layer("Root")

	offset_x = 5
	offset_y = 5
	create_horizontal_plate(root, offset_x, offset_y)

	offset_x += BASE_WIDTH + 5
	# offset_y += BASE_HEIGHT
	create_vertical_stand(root, offset_x, offset_y)

	save(root, os.path.join(OUTPUT_FOLDER, "tensile_box.svg"), "TENSILE", PAPER_WIDTH, PAPER_HEIGHT)


def main():
	create()

if __name__ == "__main__":
	main()

