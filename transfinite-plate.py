# Maisie E-M, Jan 23
# sources: gmsh documentation and
# https://bbanerjee.github.io/ParSim/fem/meshing/gmsh/gmsh-meshing-for-code-aster/
# ------------------------------------------------------------------------------
#  gmsh & OpenCascade code to generate structured mesh
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

# ----------------------------------------------------------------------------- #
# 
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

# when the element size is fully specified by a mesh size field, set:
option.setNumber("Mesh.MeshSizeExtendFromBoundary", 0)
option.setNumber("Mesh.MeshSizeFromPoints", 0)
option.setNumber("Mesh.MeshSizeFromCurvature", 0)

# ----------------------------------------------------------------------------- #
# 
# GEOMETRY

# occmetry size definitions
lc = 1e-1
h = 0.05
hh = h/2
l = 0.5
ll = l/2

# mesh size definitions
nh = 3
nl = 20

# CREATE occMETRY

# add points; lower square plane 
A = model.occ.addPoint(0, 0, 0, lc)
B = model.occ.addPoint(l, 0, 0, lc)
C = model.occ.addPoint(l, l, 0, lc)
D = model.occ.addPoint(0, l, 0, lc)

# upper square plane 
E = model.occ.addPoint(0, 0, h, lc)
F = model.occ.addPoint(l, 0, h, lc)
G = model.occ.addPoint(l, l, h, lc)
H = model.occ.addPoint(0, l, h, lc)

# connect points with lines; lower square plane 
model.occ.addLine(A, B, 1)
model.occ.addLine(C, B, 2)
model.occ.addLine(C, D, 3)
model.occ.addLine(D, A, 4)

# upper square plane
model.occ.addLine(E, F, 5)
model.occ.addLine(G, F, 6)
model.occ.addLine(G, H, 7)
model.occ.addLine(H, E, 8)

# connect square planes 
model.occ.addLine(1, 5, 9)
model.occ.addLine(2, 6, 10)
model.occ.addLine(3, 7, 11)
model.occ.addLine(4, 8, 12)

# connect lines with loops
model.occ.addCurveLoop([4, 1, -2, 3], 101)
model.occ.addCurveLoop([8, 5, -6, 7], 102)
model.occ.addCurveLoop([12, 8, -9, -4], 103)
model.occ.addCurveLoop([5, -10, -1, 9], 104)
model.occ.addCurveLoop([-6, -11, 2, 10], 105)
model.occ.addCurveLoop([11, 7, -12, -3], 106)

# create surfaces on the loops
model.occ.addPlaneSurface([101], 201)
model.occ.addPlaneSurface([102], 202)
model.occ.addPlaneSurface([103], 203)
model.occ.addPlaneSurface([104], 204)
model.occ.addPlaneSurface([105], 205)
model.occ.addPlaneSurface([106], 206)

# model.occ.synchronize()
occ.synchronize()

# model.occ.mesh.setRecombine(201, 1)
# model.occ.mesh.setRecombine(2, quad)

# create volume between the surfaces
model.occ.addSurfaceLoop([201, 202, 203, 204, 205, 206], 128)
model.occ.addVolume([128], 1)

# model.addPhysicalGroup(1, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], 50)
# model.addPhysicalGroup(2, [201, 202, 203, 204, 205, 206], 51)
# model.addPhysicalGroup(3, [1], 52)

occ.synchronize()

# ----------------------------------------------------------------------------- #
# 
# SET UP TRANSFINITE INTERPOLATION

num_nodes = nh+1
for curve in [1, 2, 3, 4, 5, 6, 7, 8]:
    mesh.setTransfiniteCurve(curve, num_nodes)
num_nodes = nl+1
for curve in [9, 10, 11, 12]:
    mesh.setTransfiniteCurve(curve, num_nodes)
  
for surf in occ.getEntities(2):
    mesh.setTransfiniteSurface(surf[1])
  
for vol in occ.getEntities(3):
    mesh.setTransfiniteVolume(vol[1])

# ----------------------------------------------------------------------------- #
# 
#  MESH REFINEMENT

# embed a points around which to refine the mesh
ps = model.occ.addPoint(ll, ll, 0, lc)
pf = model.occ.addPoint(ll, ll, h, lc)
pm = model.occ.addPoint(ll, ll, hh, lc)
# l = model.occ.addLine(ps, pf)
model.occ.synchronize()
mesh.embed(0, [ps], 3, 1)
mesh.embed(0, [ps], 2, 201)
mesh.embed(0, [pf], 3, 1)
mesh.embed(0, [pm], 3, 1)
mesh.embed(0, [pf], 2, 202)
# mesh.embed(1, [l], 3, 1)

# model.occ.synchronize()
occ.synchronize()

# alternative mesh refinement methods:

# background fields - this doesn't work with transfinite tror jeg
# # define a distance field for mesh refinement around point p
# mesh.field.add("Distance", 1)
# mesh.field.setNumbers(1, "PointsList", [ps, pf, pm])

# # math eval to determine the mesh size (quadratic depending on distance to point p)
# mesh.field.add("MathEval", 2)
# mesh.field.setString(2, "F", "F1^2 +" + str(lc / 10))

# mesh.field.add("Min", 7)
# mesh.field.setNumbers(7, "FieldsList", [2])

# mesh.field.setAsBackgroundMesh(7)

# OR

# model.occ.mesh.setSize([(0, 1), (0, 2), (0, 3), (0, 4)], lc * 3)
# model.occ.mesh.setSize([(0, 5), (0, 6), (0, 7), (0, 8), (0, p)], lc )

# mesh refinement around embedded point
# model.occ.mesh.setSize([(0, 1)], lc / 4)
# model.occ.mesh.setSize([(0, 4)], lc / 4)

# OR

# "Bump" is a double-sided bias
# model.occ.mesh.setTransfiniteCurve(1, 30, "Bump", coef=-6)
# model.occ.mesh.setTransfiniteCurve(3, 30, "Bump", coef=-6)
# model.occ.mesh.setTransfiniteCurve(2, 30, "Bump", coef=-6)
# model.occ.mesh.setTransfiniteCurve(4, 30, "Bump", coef=-6)
# model.occ.mesh.setTransfiniteCurve(5, 30, "Bump", coef=-6)
# model.occ.mesh.setTransfiniteCurve(6, 30, "Bump", coef=-6)
# model.occ.mesh.setTransfiniteCurve(7, 30, "Bump", coef=-6)
# model.occ.mesh.setTransfiniteCurve(8, 30, "Bump", coef=-6)

# model.occ.mesh.setTransfiniteSurface(1)
# model.occ.mesh.setTransfiniteSurface(2)
# model.occ.mesh.setTransfiniteSurface(3)
# model.occ.mesh.setTransfiniteSurface(4)
# model.occ.mesh.setTransfiniteSurface(5)
# model.occ.mesh.setTransfiniteSurface(6)

# model.occ.mesh.setTransfiniteVolume(1)
# apply an elliptic smoother to the grid to have a more regular mesh:
option.setNumber("Mesh.Smoothing", 20)

# model.occ.synchronize()
occ.synchronize()

# ----------------------------------------------------------------------------- #
# 
# GENERATE MESH AND WRITE TO FILE

mesh.generate(3)
mesh.recombine()

thepath = "/Users/adminuser/meshes"; os.chdir(thepath)
gmsh.write("transfinite.msh")

# # launch the GUI to see the results:
# if '-nopopup' not in sys.argv:
#     gmsh.fltk.run()

# gmsh.finalize()