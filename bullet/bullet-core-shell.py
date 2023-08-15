# Maisie E-M, Jul 23
#
# ------------------------------------------------------------------------------
#                unstructured hex 2D shell mesh for AP bullet core
# ------------------------------------------------------------------------------

import gmsh
import sys
import os
import math
import pygmsh
import numpy as np
import time

gmsh.initialize(sys.argv)

model = gmsh.model 
option = gmsh.option
mesh = model.mesh

gmsh.model.add("bullet")

# Start timer
start_time = time.perf_counter()

# ----------------------------------------------------------------------------- #
# 
# MESHING OPTIONS

lc = 1.2
lcmin = lc -0.1

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

# import the bullet STEP file
step_file_path = os.path.abspath('/Users/adminuser/Documents/PhD/bullet models/step files/bullet-core.step')
v = gmsh.model.occ.importShapes(step_file_path)

# get the bounding box of the volume:
# xmin, ymin, zmin, xmax, ymax, zmax = gmsh.model.occ.getBoundingBox(
#     v[0][0], v[0][1])

# We want to slice the model into N slices, and either keep the volume slices
# or just the surfaces obtained by the cutting:

# N = 1  # Number of slices
# dir = 'X' # Direction: 'X', 'Y' or 'Z'
# surf = False  # Keep only surfaces?

# dx = (xmax - xmin)
# dy = (ymax - ymin)
# dz = (zmax - zmin)
# L = dz if (dir == 'X') else dx
# H = dz if (dir == 'Y') else dy

# # Create the first cutting plane:
# s = []
# s.append((2, gmsh.model.occ.addRectangle(xmin, ymin, zmin, L, H)))
# if dir == 'X':
#     gmsh.model.occ.rotate([s[0]], xmin, ymin, zmin, 0, 1, 0, -math.pi/2)
# elif dir == 'Y':
#     gmsh.model.occ.rotate([s[0]], xmin, ymin, zmin, 1, 0, 0, math.pi/2)
# tx = dx / N if (dir == 'X') else 0
# ty = dy / N if (dir == 'Y') else 0
# tz = dz / N if (dir == 'Z') else 0
# gmsh.model.occ.translate([s[0]], tx, ty, tz)

# # Create the other cutting planes:
# for i in range(1, N-1):
#     s.extend(gmsh.model.occ.copy([s[0]]))
#     gmsh.model.occ.translate([s[-1]], i * tx, i * ty, i * tz)

# # Fragment (i.e. intersect) the volume with all the cutting planes:
# gmsh.model.occ.fragment(v, s)

# Now remove all the surfaces (and their bounding entities) that are not on the
# boundary of a volume, i.e. the parts of the cutting planes that "stick out" of
# the volume:
# gmsh.model.occ.remove(gmsh.model.occ.getEntities(2), True)

# remove excess points

gmsh.model.occ.synchronize()

# if surf:
    # If we want to only keep the surfaces, retrieve the surfaces in bounding
    # boxes around the cutting planes...
#     eps = 1e-4
#     s = []
#     for i in range(1, N):
#         xx = xmin if (dir == 'X') else xmax
#         yy = ymin if (dir == 'Y') else ymax
#         zz = zmin if (dir == 'Z') else zmax
#         s.extend(gmsh.model.getEntitiesInBoundingBox(
#             xmin - eps + i * tx, ymin - eps + i * ty, zmin - eps + i * tz,
#             xx + eps + i * tx, yy + eps + i * ty, zz + eps + i * tz, 2))
#     # ...and remove all the other entities (here directly in the model, as we
#     # won't modify any OpenCASCADE entities later on):
#     dels = gmsh.model.getEntities(2)
#     for e in s:
#         dels.remove(e)
#     gmsh.model.removeEntities(gmsh.model.getEntities(3))
#     gmsh.model.removeEntities(dels)
#     gmsh.model.removeEntities(gmsh.model.getEntities(1))
#     gmsh.model.removeEntities(gmsh.model.getEntities(0))

# gmsh.model.removeEntities(gmsh.model.getEntities(1))
# gmsh.model.occ.remove([(2, 9)], recursive=True)

# gmsh.model.occ.remove([(1, 3)], recursive=True)

# gmsh.model.occ.synchronize()

# specify a global mesh size and mesh the partitioned model:
option.setNumber("Mesh.MeshSizeMin", lcmin)
option.setNumber("Mesh.MeshSizeMax", lc)

# mesh constraints
# function loops through all elements and adjusts the min size
def meshSizeCallback(dim, tag, x, y, z, lc):
    return max(0.5, lc)

mesh.setSizeCallback(meshSizeCallback)

mesh.generate(3)

# get and delete all volume entities
volumes = gmsh.model.getEntities(dim=3)

for volume in volumes:
    gmsh.model.removeEntities([volume])

# optimise and refine the mesh
# mesh.optimize("Relocate3D") # added no extra run time
# mesh.optimize("Laplace2D", niter=1)
# mesh.optimize("UntangleMeshGeometry", force=True, niter=1) # 1 min extra run time
# mesh.optimize("QuadCavityRemeshing", force=True) # doesn't work; no error?
# mesh.optimize("QuadQuasiStructured", force=True, niter=1) # throws an error

# try re-building with lines down the quarters 

mesh.refine()

# Save the mesh
gmsh.write('../meshes/bullet-shell-trial.msh')

# End timer
end_time = time.perf_counter()
# Calculate elapsed time
elapsed_time = end_time - start_time
print("Elapsed time: ", elapsed_time)

# Finalize Gmsh
gmsh.finalize()


