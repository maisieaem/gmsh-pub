# Maisie E-M, Jul 23

# ------------------------------------------------------------------------------
#                 tetrahedral solid mesh for AP bullet core
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

gmsh.model.add("bullet-tet")

writeFile = '../meshes/bullet-core-tet-lc095.msh'

# Start timer
start_time = time.perf_counter()

# ----------------------------------------------------------------------------- #
# 
# MESHING OPTIONS

lc = 0.95
lcmin = lc - 0.2

# recombination tet -> hex algorithm specification
# 5 and 8 are ok - 5 handles mesh gradients better. 1 decides for itself
option.setNumber("Mesh.Algorithm", 1)
# 1: MeshAdapt, 2: Automatic, 3: Initial mesh only, 5: Delaunay, 6: Frontal-Delaunay, 
# 7: BAMG, 8: Frontal-Delaunay for Quads, 9: Packing of Parallelograms, 11: Quasi-structured Quad

option.setNumber("Mesh.Algorithm3D", 10)
# 1: Delaunay, 3: Initial mesh only, 4: Frontal, 7: MMG3D, 9: R-tree, 10: HXT

option.setNumber('Mesh.SecondOrderLinear', 1)

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

# Load a STEP file (using `importShapes' instead of `merge' allows to directly
# # retrieve the tags of the highest dimensional imported entities):
# path = os.path.dirname(os.path.abspath(__file__))
# v = gmsh.model.occ.importShapes(os.path.join(path, os.pardir, 'bullet-outer.step'))

# import the bullet STEP file
step_file_path = os.path.abspath('/Users/adminuser/Documents/PhD/bullet models/step files/bullet-core.step')
v = gmsh.model.occ.importShapes(step_file_path)

# specify a global mesh size and mesh the partitioned model:
option.setNumber("Mesh.MeshSizeMin", lc)
option.setNumber("Mesh.MeshSizeMax", lcmin)

# mesh constraints
# function loops through all elements and adjusts the min size
def meshSizeCallback(dim, tag, x, y, z, lc):
    return max(0.5, lc)

# Register the callback function
mesh.setSizeCallback(meshSizeCallback)

gmsh.model.occ.synchronize()

gmsh.model.mesh.generate(3)

# optimise and refine the mesh
mesh.optimize("Relocate3D")  # added no extra run time
mesh.optimize("Netgen")# added no extra run time
mesh.optimize("Laplace2D", niter=1)
# mesh.optimize("UntangleMeshGeometry", force=True, niter=1) # 1 min extra run time

mesh.refine()

# Save the mesh
gmsh.write(writeFile)

# End timer
end_time = time.perf_counter()
# Calculate elapsed time
elapsed_time = end_time - start_time
print("Elapsed time: ", elapsed_time)

# Finalize Gmsh
gmsh.finalize()


