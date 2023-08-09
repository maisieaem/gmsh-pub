# Maisie E-M, Jul 23

# ------------------------------------------------------------------------------
#                 triangular surface mesh for AP bullet core
#                 for input to hxt meshing
# ------------------------------------------------------------------------------

import gmsh
import sys
import os
import math
import pygmsh
import numpy as np
import time

# Initialize gmsh
gmsh.initialize()

gmsh.model.addPlugin("hxt")

# Create a new model
gmsh.model.add("my_model")

# Import the geometry from the STEP file
gmsh.merge("bullet-outer.step")

# Set the model to use the HXT module for meshing
gmsh.option.setNumber("Mesh.Algorithm", gmsh.option.getNumber("Mesh.Algorithm").replace("1", "8"))

# Generate the hexahedral mesh
gmsh.model.mesh.generate(3)

# Save the mesh to a file (optional)
gmsh.write("hxt-trial.msh")

# Finalize gmsh
gmsh.finalize()