import numpy as np
import gmsh
import sys


class Well:
	def __init__(self, st):
		self.name = st[0]
		self.mode = st[1]
		self.r = float(st[2])
		self.x = float(st[3])
		self.y = float(st[4])
		self.Node = int(st[5])
		self.press = float(st[6])
		self.rate = float(st[7])
		self.index = None


def init_bound_info(path):
	xy_bound_file = open(path, 'r').readlines()
	index_size = 0

	for i in range(len(xy_bound_file)):
		if xy_bound_file[i].rstrip() == '$4 Что считать нулём':
			index_size = i
			break

	bound_point_size = index_size - 2

	xy_bound = np.zeros(bound_point_size, dtype = list)
	for i in range(bound_point_size):
		xy_bound[i] = xy_bound_file[i + 2].split()

	return xy_bound


def init_well_info(path_well_info):

	# well_size_file = open(path_well_size, 'r').readlines()
	# well_size = int(well_size_file[0].split()[0])

	xy_well_file = open(path_well_info, 'r').readlines()
	well_size = int(len(xy_well_file)) - 1
	xy_well_info = np.zeros(well_size, dtype = Well)

	for i in range(well_size):
		well = Well(xy_well_file[i + 1].split())
		well.index = i
		xy_well_info[i] = well

	return xy_well_info


def main():
	xy_contour = init_bound_info(r'C:\Stud\ST_LT\SL_ST_EXAMPLE\DIM-2\finemesh.con')
	xy_well = init_well_info(r'C:\Stud\ST_LT\SL_ST_EXAMPLE\DIM-2\result.wll')
	n_points = len(xy_contour)

	gmsh.initialize()
	# m = gmsh.model.add("grid")
	lc = 5

	points = []
	for i in range(n_points - 1):
		points.append(gmsh.model.geo.add_point(float(xy_contour[i][0]), float(xy_contour[i][1]), 0, lc))

	well_points = []
	for i in range(len(xy_well)):
		well_points.append(gmsh.model.occ.add_point(float(xy_well[i].x), float(xy_well[i].y), 0))

	edges = []
	for i in range(n_points - 2):
		edges.append(gmsh.model.geo.add_line(points[i], points[i + 1]))
	edges.append(gmsh.model.geo.add_line(points[n_points - 2], points[0]))

	faces = []
	faces.append(gmsh.model.geo.add_curve_loop(edges))
	surf = gmsh.model.geo.add_plane_surface(faces)
	gmsh.model.geo.synchronize()
	gmsh.model.mesh.generate()
	gmsh.write("test.msh")

	if '-nopopup' not in sys.argv:
		gmsh.fltk.run()

	gmsh.finalize()


if __name__ == '__main__':
	main()
else:
	raise SystemExit('Это не библиотека!')
