# unstruc target plate meshes
 python code in open source gmsh library for complex meshes of target plates for ballistic impact simulations

<!---Here is the documentation for the meshing software for reference: https://gmsh.info/doc/texinfo/gmsh.html

Here you can find information on how to download and cite it: https://gmsh.info/
I think the easiest way is running <pip install --upgrade gmsh>. --->
 
 altering the target plate geometry:

- height is `h`

altering the element size: 

- `lcsmaller` and `lcsmallest` 
     
these are the target characteristic size in the two refinement cylinders

- the function `F`
 
 modulates the element size using a function of spatial coordinates from the line `l`. Reduce the number for a smoother refinement towards the centre line. 

- `r1` and `r2`
  
are parameters for changing the region size of the smaller and smallest elements.

`MeshSizeMax` takes the minimum of all the target mesh sizes, so the parameters don't exactly constrain it with the specific dimensions you give it, and it takes a bit of trial and error. You may need to find a combination of `lcsmaller`, `lcsmallest` and `F` that give you the required elements size in the impact zone  - remember to double check that in LS-Prepost.  The function removes any elements that are too small (set to around 0.01 mm).

example for `lc = 1e-1`:

| lcsmaller | lcsmallest |  `r1`  |   `r2`   |     `F`    | no. els  | run time |
|-----------|------------|--------|----------|------------|----------|----------|
| `lc`/50   | `lc`/100   | `l`/5  | `l`/6.66 | 2.5*`F1`^2 |  ~720k   | 174 s
| `lc`/100  | `lc`/200   | `l`/8  | `l`/10   | 2.5*`F1`^2 |  ~2.4mil | 928 s

## extruded-ustruct-quad-plate

 python code for a "layer-wise" unstructured hexahedral mesh with element size refined by a quadratic function in the area of impact on a surface that is extruded layer by layer over the thickness

## plate-ustruct-hex

 python code for a 3D plate cuboid hexahedral mesh with element size refined by a quadratic function in the area of impact and two mesh refinement cylinders
 
- [x] why won't the mesh refine around my embedded point p? 

A: because I forgot to embed the point in the surface as well as the volume. Must be done for a boundary point. 

## transfinite-plate.py

 python code for a 3D plate with non-refined by structured hex mesh 

## ustruc-cyl.py

 python code for a 3D cylindrical unstructured hexahedral mesh with element size refined by a quadratic function in the area of impact and two mesh refinement cylinders.

cylinder geometry is defined using OpenCascade
