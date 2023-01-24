# Maisie E-M, Jan 23

# ------------------------------------------------------------------------------
#  gmsh & OpenCascade code to generate refined mesh for ballistic impact sims
# ------------------------------------------------------------------------------

import gmsh
import math
import sys
import os

gmsh.initialize(sys.argv)

model = gmsh.model 
occ = model.occ
mesh = model.mesh
option = gmsh.option

model.add("t6")

# MESHING OPTIONS

option.setNumber("Mesh.RecombinationAlgorithm", 2)
option.setNumber("Mesh.Algorithm", 5)
option.setNumber("Mesh.RecombineAll", 1)
option.setNumber('Mesh.Recombine3DLevel', 2)
# option.setNumber("Mesh.Recombine3DAll", 1)
option.setNumber("Mesh.Algorithm3D", 1)
option.setNumber("Mesh.SubdivisionAlgorithm", 2)
option.setNumber("Mesh.RecombineOptimizeTopology", 5)
option.setNumber("Mesh.RecombineMinimumQuality", 0.001)
option.setNumber('Mesh.SecondOrderIncomplete', 1)

# geometry size definitions
lc = 1e-1
h = 0.05
hh = h/2
l = 0.5
ll = l/2

# mesh size definitions
nh = 3
nl = 20

# CREATE GEOMETRY

# add points; lower square plane 
A = model.geo.addPoint(0, 0, 0, lc)
B = model.geo.addPoint(l, 0, 0, lc)
C = model.geo.addPoint(l, l, 0, lc)
D = model.geo.addPoint(0, l, 0, lc)

# upper square plane 
E = model.geo.addPoint(0, 0, h, lc)
F = model.geo.addPoint(l, 0, h, lc)
G = model.geo.addPoint(l, l, h, lc)
H = model.geo.addPoint(0, l, h, lc)

# connect points with lines; lower square plane 
model.geo.addLine(A, B, 1)
model.geo.addLine(C, B, 2)
model.geo.addLine(C, D, 3)
model.geo.addLine(D, A, 4)

# upper square plane
model.geo.addLine(E, F, 5)
model.geo.addLine(G, F, 6)
model.geo.addLine(G, H, 7)
model.geo.addLine(H, E, 8)

# connect square planes 
model.geo.addLine(1, 5, 9)
model.geo.addLine(2, 6, 10)
model.geo.addLine(3, 7, 11)
model.geo.addLine(4, 8, 12)

# connect lines with loops
model.geo.addCurveLoop([4, 1, -2, 3], 101)
model.geo.addCurveLoop([8, 5, -6, 7], 102)
model.geo.addCurveLoop([12, 8, -9, -4], 103)
model.geo.addCurveLoop([5, -10, -1, 9], 104)
model.geo.addCurveLoop([-6, -11, 2, 10], 105)
model.geo.addCurveLoop([11, 7, -12, -3], 106)

# create surfaces on the loops
model.geo.addPlaneSurface([101], 201)
model.geo.addPlaneSurface([102], 202)
model.geo.addPlaneSurface([103], 203)
model.geo.addPlaneSurface([104], 204)
model.geo.addPlaneSurface([105], 205)
model.geo.addPlaneSurface([106], 206)

# model.geo.synchronize()
occ.synchronize()

# model.geo.mesh.setRecombine(201, 1)
# model.geo.mesh.setRecombine(2, quad)

# create volume between the surfaces
model.geo.addSurfaceLoop([201, 202, 203, 204, 205, 206], 128)
model.geo.addVolume([128], 1)

# 
#  MESH REFINEMENT

# embed a points around which to refine the mesh
ps = model.geo.addPoint(ll, ll, 0, lc)
pf = model.geo.addPoint(ll, ll, h, lc)
pm = model.geo.addPoint(ll, ll, hh, lc)
# l = model.geo.addLine(ps, pf)
model.geo.synchronize()
mesh.embed(0, [ps], 3, 1)
mesh.embed(0, [ps], 2, 201)
mesh.embed(0, [pf], 3, 1)
mesh.embed(0, [pm], 3, 1)
mesh.embed(0, [pf], 2, 202)
# mesh.embed(1, [l], 3, 1)

# define a distance field for mesh refinement around point p
mesh.field.add("Distance", 1)
mesh.field.setNumbers(1, "PointsList", [ps, pf, pm])

# math eval to determine the mesh size (quadratic depending on distance to point p)
mesh.field.add("MathEval", 2)
mesh.field.setString(2, "F", "F1^2 +" + str(lc / 10))

mesh.field.add("Min", 7)
mesh.field.setNumbers(7, "FieldsList", [2])

mesh.field.setAsBackgroundMesh(7)

# model.geo.synchronize()
occ.synchronize()

# model.addPhysicalGroup(1, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], 50)
# model.addPhysicalGroup(2, [201, 202, 203, 204, 205, 206], 51)
# model.addPhysicalGroup(3, [1], 52)

# model.geo.mesh.setSize([(0, 1), (0, 2), (0, 3), (0, 4)], lc * 3)

# model.geo.mesh.setSize([(0, 5), (0, 6), (0, 7), (0, 8), (0, p)], lc )

# mesh refinement around embedded point
# model.geo.mesh.setSize([(0, 1)], lc / 4)
# model.geo.mesh.setSize([(0, 4)], lc / 4)

# model.geo.mesh.Recombine3DLevel(0)
# model.geo.mesh.setRecombine(2, 1)
# option.setNumber("Recombine3DAll", 0)
# option.setNumber("Recombine3DLevel", 0)

# model.geo.mesh.setTransfiniteCurve(1, 30, "Bump", coef=-6)
# model.geo.mesh.setTransfiniteCurve(3, 30, "Bump", coef=-6)
# model.geo.mesh.setTransfiniteCurve(2, 30, "Bump", coef=-6)
# model.geo.mesh.setTransfiniteCurve(4, 30, "Bump", coef=-6)

# model.geo.mesh.setTransfiniteCurve(5, 30, "Bump", coef=-6)
# model.geo.mesh.setTransfiniteCurve(6, 30, "Bump", coef=-6)
# model.geo.mesh.setTransfiniteCurve(7, 30, "Bump", coef=-6)
# model.geo.mesh.setTransfiniteCurve(8, 30, "Bump", coef=-6)

# model.geo.mesh.setTransfiniteSurface(1)
# model.geo.mesh.setTransfiniteSurface(2)
# model.geo.mesh.setTransfiniteSurface(3)
# model.geo.mesh.setTransfiniteSurface(4)
# model.geo.mesh.setTransfiniteSurface(5)
# model.geo.mesh.setTransfiniteSurface(6)

# model.geo.mesh.setTransfiniteVolume(1)

# To create quadrangles instead of triangles, one can use the `setRecombine'
# constraint:
# model.geo.mesh.setRecombine(2, 1)
# model.geo.mesh.setRecombine(2, 2)
# model.geo.mesh.setRecombine(2, 3)
# model.geo.mesh.setRecombine(2, 4)
# model.geo.mesh.setRecombine(2, 5)
# model.geo.mesh.setRecombine(2, 6)

# # When the surface has only 3 or 4 points on its boundary the list of corners
# # can be omitted in the `setTransfiniteSurface()' call:
# model.geo.addPoint(0.2, 0.2, 0, 1.0, 7)
# model.geo.addPoint(0.2, 0.1, 0, 1.0, 8)
# model.geo.addPoint(0, 0.3, 0, 1.0, 9)
# model.geo.addPoint(0.25, 0.2, 0, 1.0, 10)
# model.geo.addPoint(0.3, 0.1, 0, 1.0, 11)
# model.geo.addLine(8, 11, 10)
# model.geo.addLine(11, 10, 11)
# model.geo.addLine(10, 7, 12)
# model.geo.addLine(7, 8, 13)
# model.geo.addCurveLoop([13, 10, 11, 12], 14)
# model.geo.addPlaneSurface([14], 15)
# for i in range(10, 14):
#     model.geo.mesh.setTransfiniteCurve(i, 10)
# model.geo.mesh.setTransfiniteSurface(15)

# The way triangles are generated can be controlled by specifying "Left",
# "Right" or "Alternate" in `setTransfiniteSurface()' command. Try e.g.
#
# model.geo.mesh.setTransfiniteSurface(15, "Alternate")

# When the element size is fully specified by a mesh size field (as it is in
# this example), it is thus often desirable to set

option.setNumber("Mesh.MeshSizeExtendFromBoundary", 0)
option.setNumber("Mesh.MeshSizeFromPoints", 0)
option.setNumber("Mesh.MeshSizeFromCurvature", 0)

# model.geo.synchronize()
occ.synchronize()

# Finally we apply an elliptic smoother to the grid to have a more regular
# mesh:
option.setNumber("Mesh.Smoothing", 20)

# GENERATE MESH AND WRITE TO FILE

mesh.generate(3)
mesh.recombine()

thepath = "/Users/adminuser/meshes"; os.chdir(thepath)
gmsh.write("oblong.msh")

# # launch the GUI to see the results:
# if '-nopopup' not in sys.argv:
#     gmsh.fltk.run()

# gmsh.finalize()
