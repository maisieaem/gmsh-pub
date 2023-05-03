# gmsh
 python code in open source gmsh library for complex meshes

Here is the documentation for the meshing software for reference: https://gmsh.info/doc/texinfo/gmsh.html

Here you can find information on how to download and cite it: https://gmsh.info/
I think the easiest way is running <pip install --upgrade gmsh>.
 
## files

### extruded-ustruct-quad-plate

 python code for a "surface level" unstructured hexahedral mesh with element size refined by a quadratic function in the area of impact extruded layer by layer over the thickness

### plate-ustruct-hex

 python code for a 3D plate cuboid hexahedral mesh with element size refined by a quadratic function in the area of impact and two mesh refinement cylinders
 
- [x] why won't the mesh refine around my embedded point p? A: because I forgot to embed the point in the surface as well as the volume. Must be done for a boundary point. 

### transfinite-plate.py

 python code for a 3D plate with non-refined by structured hex mesh 

### ustruc-cyl.py

 python code for a 3D cylindrical unstructured hexahedral mesh with element size refined by a quadratic function in the area of impact and two mesh refinement cylinders.

cylinder geometry is defined using OpenCascade

Parameters for altering the plate height is h (line 119).

Parameters for altering the element size are: 

— lcsmaller, lcsmallest (line 114 & 115 - these are the target characteristic size in the two refinement cylinders)
— the function after “F” (line 171 - modulates the element size using a function of spatial coordinates from the line l. Reduce the number to ~6 for a smoother refinement towards the centre line). 

Parameters for changing the region size of the smaller and smallest elements are: r1 and r2 (lines 124 & 125).

On line 199 it takes the minimum of all the target mesh sizes, so the parameters don't exactly constrain it with the specific dimensions you give it, and it takes a bit of trial and error. You may need to find a combination of lcsmaller, lcsmallest and F that give you the required elements size in the impact zone  - remember to double check that in LS-Prepost.  The function used on line 207 removes any elements that are too small (smaller than around 0.01 mm I think).
