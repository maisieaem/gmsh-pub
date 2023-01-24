# gmsh
 python code in open source gmsh library for complex meshes
 
## files

### extruded-ustruct-quad-plate

 python code for an surface level unstructured hexahedral mesh with element size refined by a quadratic function in the area of impact

extruded layer by layer over thickness

### 3D-ustruct-quad-refined-plate

 python code for an unstructured hexahedral mesh with element size refined by a quadratic function in the area of impact
 
- [ ] why won't the volume mesh with quads?
- [x] why won't the mesh refine around my embedded point p? A: because I forgot to embed the point in the surface as well as the volume. Must be done for a boundary point. 

### transfinite-plate.py

 python code for a 3D plate with non-refined by structured hex mesh 