# Maisie E-M, Jul 23

# ------------------------------------------------------------------------------
#                 triangular surface mesh for AP bullet core
#                 for input to topological-hex-2.0
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

gmsh.model.add("bullet-tri")

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

lc = 0.6
lcmin = lc - 0.2

# Finally, let's specify a global mesh size and mesh the partitioned model:
option.setNumber("Mesh.MeshSizeMin", lc)
option.setNumber("Mesh.MeshSizeMax", lcmin)

# Set the mesh size callback function
def meshSizeCallback(dim, tag, x, y, z, lc):
    # Check if the current point is the desired point (point 7)
    if tag == 7:
        # Return the desired mesh size
        return lc
    else:
        # Return the default mesh size
        return lc

# Register the callback function
mesh.setSizeCallback(meshSizeCallback)



gmsh.model.mesh.generate(2)

# optimise and refine the mesh
mesh.optimize("Relocate3D")  # added no extra run time
mesh.optimize("Netgen")# added no extra run time
# mesh.optimize("Laplace2D", niter=1)
# mesh.optimize("UntangleMeshGeometry", force=True, niter=1) # 1 min extra run time

mesh.refine()

# Save the mesh
gmsh.write('../meshes/bullet-tri.msh')

# End timer
end_time = time.perf_counter()
# Calculate elapsed time
elapsed_time = end_time - start_time
print("Elapsed time: ", elapsed_time)

# Finalize Gmsh
gmsh.finalize()


