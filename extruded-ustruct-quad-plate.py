# ------------------------------------------------------------------------------
#                    concentrated mesh in 2D extruded
# ------------------------------------------------------------------------------

# In addition to specifying target mesh sizes at the points of the geometry (see
# `t1.py') or using a background mesh (see `t7.py'), you can use general mesh
# size "Fields".

import gmsh
import sys
import os

gmsh.initialize(sys.argv)

gmsh.model.add("t10")

# Let's create a simple rectangular geometry:
lc = .15
gmsh.model.geo.addPoint(0.0, 0.0, 0, lc, 1)
gmsh.model.geo.addPoint(1, 0.0, 0, lc, 2)
gmsh.model.geo.addPoint(1, 1, 0, lc, 3)
gmsh.model.geo.addPoint(0, 1, 0, lc, 4)
gmsh.model.geo.addPoint(0.5, .5, 0, lc, 5)

gmsh.model.geo.addLine(1, 2, 1)
gmsh.model.geo.addLine(2, 3, 2)
gmsh.model.geo.addLine(3, 4, 3)
gmsh.model.geo.addLine(4, 1, 4)

gmsh.model.geo.addCurveLoop([1, 2, 3, 4], 5)

gmsh.model.geo.addPlaneSurface([5], 6)

gmsh.model.geo.mesh.setRecombine(2, 6)

# We could also combine MathEval with values coming from other fields. For
# example, let's define a `Distance' field around point 5
gmsh.model.mesh.field.add("Distance", 4)
gmsh.model.mesh.field.setNumbers(4, "PointsList", [5])

# We can then create a `MathEval' field with a function that depends on the
# return value of the `Distance' field 4, i.e., depending on the distance to
# point 5 (here using a cubic law, with minimum element size = lc / 100)
gmsh.model.mesh.field.add("MathEval", 5)
gmsh.model.mesh.field.setString(5, "F", "F4^2 +" + str(lc / 10))


# Let's use the minimum of all the fields as the mesh size field:
gmsh.model.mesh.field.add("Min", 7)
gmsh.model.mesh.field.setNumbers(7, "FieldsList", [5])

gmsh.model.mesh.field.setAsBackgroundMesh(7)

# The API also allows to set a global mesh size callback, which is called each
# time the mesh size is queried
def meshSizeCallback(dim, tag, x, y, z, lc):
    return lc / 8

gmsh.model.mesh.setSizeCallback(meshSizeCallback)

# -clmin value -might need these
# Set minimum mesh element size (Mesh.MeshSizeMin)

# -clmax value
# Set maximum mesh element size (Mesh.MeshSizeMax)

# To determine the size of mesh elements, Gmsh locally computes the minimum of
#
# 1) the size of the model bounding box;
# 2) if `Mesh.MeshSizeFromPoints' is set, the mesh size specified at geometrical
#    points;
# 3) if `Mesh.MeshSizeFromCurvature' is positive, the mesh size based on
#    curvature (the value specifying the number of elements per 2 * pi rad);
# 4) the background mesh size field;
# 5) any per-entity mesh size constraint;
#
# The value can then be further modified by the mesh size callback, if any,
# before being constrained in the interval [`Mesh.MeshSizeMin',
# `Mesh.MeshSizeMax'] and multiplied by `Mesh.MeshSizeFactor'.  In addition,
# boundary mesh sizes are interpolated inside surfaces and/or volumes depending
# on the value of `Mesh.MeshSizeExtendFromBoundary' (which is set by default).
#
# When the element size is fully specified by a mesh size field (as it is in
# this example), it is thus often desirable to set

gmsh.option.setNumber("Mesh.MeshSizeExtendFromBoundary", 0)
gmsh.option.setNumber("Mesh.MeshSizeFromPoints", 0)
gmsh.option.setNumber("Mesh.MeshSizeFromCurvature", 0)

# This will prevent over-refinement due to small mesh sizes on the boundary.

# Finally, while the default "Frontal-Delaunay" 2D meshing algorithm
# (Mesh.Algorithm = 6) usually leads to the highest quality meshes, the
# "Delaunay" algorithm (Mesh.Algorithm = 5) will handle complex mesh size fields
# better - in particular size fields with large element size gradients:

gmsh.option.setNumber("Mesh.Algorithm", 5)

# Extrude the mesh
h = 0.1
ov = gmsh.model.geo.extrude([(2, 6)], 0, 0, h, [10], [1], recombine=True)

gmsh.model.geo.synchronize()

gmsh.model.geo.mesh.setTransfiniteCurve(22, 20,  meshType="Bump", coef=2)
gmsh.model.geo.mesh.setTransfiniteCurve(18, 20,  meshType="Bump", coef=2)
gmsh.model.geo.mesh.setTransfiniteCurve(13, 20, meshType="Bump", coef=2)
gmsh.model.geo.mesh.setTransfiniteCurve(14, 20, meshType="Bump", coef=2)

# gmsh.model.geo.mesh.setTransfiniteSurface(1, "Left", [1, 2, 3, 4])

gmsh.model.geo.mesh.setTransfiniteVolume(1, [1, 2, 3, 4, 6, 7, 15, 11])

# gmsh.model.mesh.embed(1, tl, 3, 1)

# gmsh.model.mesh.recombine()

gmsh.model.geo.synchronize()

gmsh.option.setNumber("Mesh.Smoothing", 100)

gmsh.model.mesh.generate(3)

thepath = "/Users/adminuser/meshes"; os.chdir(thepath)
gmsh.write("extrude.msh")

# # Launch the GUI to see the results:
# if '-nopopup' not in sys.argv:
#     gmsh.fltk.run()

# gmsh.finalize()