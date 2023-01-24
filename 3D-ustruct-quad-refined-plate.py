# Maisie E-M, Jan 23

# ----------------------------------------------------------------------------- #
#  gmsh & OpenCascade code to generate refined mesh for ballistic impact sims
# ----------------------------------------------------------------------------- #

import gmsh
import math
import sys
import os
import numpy as np

gmsh.initialize(sys.argv)

model = gmsh.model 
occ = model.occ
mesh = model.mesh
option = gmsh.option

model.add("t6")

# ----------------------------------------------------------------------------- #
# 
# MESHING OPTIONS

# recombination tet -> hex algorithm specification
option.setNumber("Mesh.RecombinationAlgorithm", 2)
option.setNumber("Mesh.Algorithm", 5)
option.setNumber("Mesh.RecombineAll", 1)
option.setNumber('Mesh.Recombine3DLevel', 2)
option.setNumber("Mesh.Algorithm3D", 1)
option.setNumber("Mesh.SubdivisionAlgorithm", 2)
option.setNumber("Mesh.RecombineOptimizeTopology", 5)
option.setNumber("Mesh.RecombineMinimumQuality", 0.1)
option.setNumber('Mesh.SecondOrderIncomplete', 1)

# when the element size is fully specified by a mesh size field, set:
option.setNumber("Mesh.MeshSizeExtendFromBoundary", 0)
option.setNumber("Mesh.MeshSizeFromPoints", 0)
option.setNumber("Mesh.MeshSizeFromCurvature", 0)

# ----------------------------------------------------------------------------- #
# 
# GEOMETRY

# geometry size definitions
lc = 1e-0
h = 0.05
hh = h/2
l = 0.5
ll = l/2
dx = 0.0001
startline = 0 + dx
stopline = h - dx


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

# define geometry groups (just for labelling)
# model.addPhysicalGroup(1, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], 50)
# model.addPhysicalGroup(2, [201, 202, 203, 204, 205, 206], 51)
# model.addPhysicalGroup(3, [1], 52)

occ.synchronize()
model.geo.synchronize()

# ----------------------------------------------------------------------------- #
# 
# MESH REFINEMENT 

# define a line via two points around which to refine the mesh
ps = model.geo.addPoint(ll, ll, startline, lc)
pf = model.geo.addPoint(ll, ll, stopline, lc)
l = model.geo.addLine(ps, pf)

occ.synchronize()
model.geo.synchronize()

# embed new points into the surfaces and volume
mesh.embed(0, [ps], 2, 201)
mesh.embed(0, [ps], 3, 1)
mesh.embed(0, [pf], 2, 202)
mesh.embed(0, [pf], 3, 1)
mesh.embed(1, [l], 3, 1)

# define a distance field for mesh refinement around points
mesh.field.add("Distance", 1)
mesh.field.setNumbers(1, "CurvesList", [l])

# frustum defined mesh size

mesh.field.add("Frustum", 3)
mesh.field.setNumber(3, "InnerR1", 0.2)
mesh.field.setNumber(3, "InnerR2", 0.2)
mesh.field.setNumber(3, "InnerV1", 0.01) 
mesh.field.setNumber(3, "InnerV2", 0.01) 
mesh.field.setNumber(3, "OuterR1", 0.5) 
mesh.field.setNumber(3, "OuterR2", 0.5) 
mesh.field.setNumber(3, "OuterV1", 0.1) 
mesh.field.setNumber(3, "OuterV2", 0.1)
mesh.field.setNumber(3, "X1", ll)
mesh.field.setNumber(3, "Y1", ll)
mesh.field.setNumber(3, "Z1", 0)
mesh.field.setNumber(3, "X2", ll)
mesh.field.setNumber(3, "Y2", ll) 
mesh.field.setNumber(3, "Z2", h)

mesh.field.add("Cylinder", 4)
mesh.field.setNumber(4, "Radius", 0.2)
mesh.field.setNumber(4, "VIn", 0.01) 
mesh.field.setNumber(4, "VOut", 0.1) 
mesh.field.setNumber(4, "XAxis", ll) 
mesh.field.setNumber(4, "XCenter", ll) 
mesh.field.setNumber(4, "YAxis", ll) 
mesh.field.setNumber(4, "YCenter", ll) 
mesh.field.setNumber(4, "ZCenter", 1) 
mesh.field.setNumber(4, "ZAxis", hh)

# math eval to determine the mesh size (quadratic depending on distance to line l)
mesh.field.add("MathEval", 2)
mesh.field.setString(2, "F", "F3^2 +" + str(lc / 10))

# define a field that mandates the minimum element size of all fields
mesh.field.add("Min", 7)
mesh.field.setNumbers(7, "FieldsList", [4])

mesh.field.setAsBackgroundMesh(7)

occ.synchronize()

# apply an elliptic smoother to the grid to have a more regular mesh:
option.setNumber("Mesh.Smoothing", 100)

occ.synchronize()

# alternative mesh refinement methods:

# model.geo.mesh.setSize([(0, 1), (0, 2), (0, 3), (0, 4)], lc * 3)
# model.geo.mesh.setSize([(0, 5), (0, 6), (0, 7), (0, 8), (0, p)], lc )

# mesh refinement around embedded point
# model.geo.mesh.setSize([(0, 1)], lc / 4)
# model.geo.mesh.setSize([(0, 4)], lc / 4)

# ----------------------------------------------------------------------------- #
# 
# GENERATE MESH AND WRITE TO FILE 

mesh.generate(3)
mesh.recombine()

thepath = "/Users/adminuser/meshes"; os.chdir(thepath)
gmsh.write("ustruct-refined.msh")

# # launch the GUI to see the results:
# if '-nopopup' not in sys.argv:
#     gmsh.fltk.run()

# gmsh.finalize()
