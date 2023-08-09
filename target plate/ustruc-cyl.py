# Maisie E-M, April 23

# -------------------------------------------------------------------------------------- #
#  gmsh code to generate refined cylinderical plate mesh for ballistic impact simulations
# -------------------------------------------------------------------------------------- #

import gmsh
import math
import sys
import os
import numpy as np
import time

gmsh.initialize(sys.argv)

model = gmsh.model 
mesh = model.mesh
option = gmsh.option

model.add("t6")

# Start timer
start_time = time.perf_counter()

# ----------------------------------------------------------------------------- #
# 
# MESHING OPTIONS

# recombination tet -> hex algorithm specification
# 5 and 8 are ok - 5 handles mesh gradients better. 1 decides for itself
option.setNumber("Mesh.Algorithm", 1)
# 1: MeshAdapt, 2: Automatic, 3: Initial mesh only, 5: Delaunay, 6: Frontal-Delaunay, 
# 7: BAMG, 8: Frontal-Delaunay for Quads, 9: Packing of Parallelograms, 11: Quasi-structured Quad

option.setNumber("Mesh.Algorithm3D", 10)
# 1: Delaunay, 3: Initial mesh only, 4: Frontal, 7: MMG3D, 9: R-tree, 10: HXT

option.setNumber("Mesh.RecombinationAlgorithm", 0)
# 0: simple, 1: blossom, 2: simple full-quad, 3: blossom full-quad

option.setNumber("Mesh.SubdivisionAlgorithm", 2)
# 0: none, 1: all quadrangles, 2: all hexahedra, 3: barycentric

option.setNumber("Mesh.RecombineNodeRepositioning", 0)

# turn on recombination:
option.setNumber("Mesh.RecombineAll", 1)
option.setNumber("Mesh.Recombine3DAll", 1)

option.setNumber('Mesh.Recombine3DLevel', 0)
# 0: hex, 1: hex+prisms, 2: hex+prism+pyramids

option.setNumber("Mesh.RecombineOptimizeTopology", 10)
# Number of topological optimization passes (removal of diamonds, ...) of recombined surface meshes
# Default value: 5 

option.setNumber("Mesh.RecombineMinimumQuality", 10)
# Default value: 0.01

option.setNumber("Mesh.Recombine3DConformity", 4)
# 0: nonconforming, 1: trihedra, 2: pyramids+trihedra, 
# 3:pyramids+hexSplit+trihedra, 4:hexSplit+trihedra

option.setNumber('Mesh.SecondOrderLinear', 1)

option.setNumber('Mesh.QuadqsTopologyOptimizationMethods', 111)
# 0: default (all),100: pattern-based CAD faces,010: disk quadrangulation remeshing,
# 001: cavity remeshing,xxx: combination of multiple methods (e.g. 111 for all)

option.setNumber('Mesh.QuadqsRemeshingBoldness', 0.5)
# From 0 (no quality decrease during remeshing) to 1 (quality can tend to 0 during remeshing).
# Default value: 0.66

option.setNumber('Mesh.QuadqsSizemapMethod', 3)
# 0: default, 1: cross-field,2: cross-field + CAD small features adaptation,
# 3: from background mesh (e.g. sizes in current triangulation),
# 4: cross-field + CAD small features adaptation (clamped by background mesh)
# option.setNumber('Mesh.SmoothCrossField', 2) 

# apply an elliptic smoother to the grid to have a more regular mesh:
option.setNumber("Mesh.Smoothing", 100)
option.setNumber("Mesh.SmoothNormals", 1)
option.setNumber("Mesh.SmoothCrossField", 1)

option.setNumber("Mesh.ElementOrder", 1)
# option.setNumber("Mesh.HighOrderOptimize", 1)

# when the element size is fully specified by a mesh size field, set:
option.setNumber("Mesh.MeshSizeExtendFromBoundary", 0)
# 0: never; 1: for surfaces and volumes; 2: for surfaces and volumes, 
# but use smallest surface element edge length instead of longest length in 3D Delaunay; 
# -2: only for surfaces; -3: only for volumes

option.setNumber("Mesh.MeshSizeFromPoints", 0)
option.setNumber("Mesh.MeshSizeFromCurvature", 0)

# ----------------------------------------------------------------------------- #
# 
# GEOMETRY

# mesh size definitions
#   lc = generic mesh size
#   lcmin = minimum refined mesh size
#   lcmax = max refined mesh size
#   lcsmaller = outer cylinder of semi-refined mesh size
#   lcsmallest = inner cylinder of fully refined mesh size
#   r1 = radius of semi-refined outer cylinder
#   r2 = radius of refined inner cylinder
# 
# plate geometry definitions
#   h = height; rcyl = radius

lc = 1e-1
lcsmaller = lc/60
lcsmallest= lc/140
lcmin = 0.00005
lcmax = 1

h = 0.005
hh = h/2
rcyl = 0.03025
rrcyl = rcyl/2

r1 = rcyl/2
r2 = rcyl/3

# mesh size constraints
option.setNumber("Mesh.MeshSizeMax", lcmax)
option.setNumber("Mesh.MeshSizeMin", lcmin)

# add lower and upper circles
# label = model.occ.addCircle(x, y, z, radius)
C1 = model.occ.addCircle(0, 0, 0, rcyl)
C2 = model.occ.addCircle(0, 0, h, rcyl)

# add circle curve loops
model.occ.addCurveLoop([C1], 101)
model.occ.addCurveLoop([C2], 102)

# circle surfaces
model.occ.addPlaneSurface([101], 201)
model.occ.addPlaneSurface([102], 202)

# join circles and make volume
model.occ.addThruSections([101, 102], 301, makeSolid=True, smoothing=True)

model.occ.synchronize()

# ----------------------------------------------------------------------------- #
# 
# MESH REFINEMENT 

# define a line via two points around which to refine the mesh
ps = model.occ.addPoint(0, 0, 0, lc)
pf = model.occ.addPoint(0, 0, h, lc)
l = model.occ.addLine(ps, pf)

model.occ.synchronize()

# embed line into the volume
model.occ.fragment([(1, l)], [(3, 301)])

model.occ.synchronize()

# define a distance field for mesh refinement around line l
mesh.field.add("Distance", 1)
mesh.field.setNumbers(1, "CurvesList", [l])

# math eval to determine the mesh size (quadratic depending on distance to line l)
mesh.field.add("MathEval", 2)
mesh.field.setString(2, "F", "8.8*F1^2 +" + str(lcsmallest))

# define two cylinder fields
# inside and outside of which mesh size is determined
mesh.field.add("Cylinder", 4)
mesh.field.setNumber(4, "Radius", r1)
mesh.field.setNumber(4, "VIn", lcsmaller) 
mesh.field.setNumber(4, "VOut", lc) 
mesh.field.setNumber(4, "XAxis", 0) 
mesh.field.setNumber(4, "XCenter", 0) 
mesh.field.setNumber(4, "YAxis", 0) 
mesh.field.setNumber(4, "YCenter", 0) 
mesh.field.setNumber(4, "ZCenter", 0) 
mesh.field.setNumber(4, "ZAxis", 1)

mesh.field.add("Cylinder", 5)
mesh.field.setNumber(5, "Radius", r2)
mesh.field.setNumber(5, "VIn", lcsmallest) 
mesh.field.setNumber(5, "VOut", lc) 
mesh.field.setNumber(5, "XAxis", 0) 
mesh.field.setNumber(5, "XCenter", 0) 
mesh.field.setNumber(5, "YAxis", 0) 
mesh.field.setNumber(5, "YCenter", 0) 
mesh.field.setNumber(5, "ZCenter", 0) 
mesh.field.setNumber(5, "ZAxis", 1)

# define a field that mandates the minimum element size of all fields
mesh.field.add("Min", 7)
mesh.field.setNumbers(7, "FieldsList", [2, 4, 5])

mesh.field.setAsBackgroundMesh(7)  

# mesh constraints
def meshSizeCallback(dim, tag, x, y, z, lc):
    return max(lc, 0.0001)

gmsh.model.mesh.setSizeCallback(meshSizeCallback)

model.occ.synchronize()

# ----------------------------------------------------------------------------- #
# 
# GENERATE MESH AND WRITE TO FILE 

# generate 3D mesh
mesh.generate(3)

# optimise and refine the mesh
# mesh.optimize("Relocate3D")
# mesh.optimize("Netgen")
mesh.optimize("Laplace2D", niter=3)
# mesh.optimize("UntangleMeshGeometry", force=True, niter=1)
# mesh.optimize("QuadCavityRemeshing", force=True)
# mesh.optimize("QuadQuasiStructured", force=True, niter=3)

mesh.refine()

thepath = "/Users/adminuser/meshes"; os.chdir(thepath)
gmsh.write("ustruct-cylinder.msh")

# End timer
end_time = time.perf_counter()
# Calculate elapsed time
elapsed_time = end_time - start_time
print("Elapsed time: ", elapsed_time)

# # launch the GUI to see the results:
# if '-nopopup' not in sys.argv:
#     gmsh.fltk.run()
# gmsh.finalize()
