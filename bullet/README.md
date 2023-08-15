# unstruc bullet meshes
 python code in open source gmsh library for meshing the bullet core

 dependancies: `gmsh` and `pygmsh` 

<!---Here is the documentation for the meshing software for reference: https://gmsh.info/doc/texinfo/gmsh.html--->

<!---Here you can find information on how to download and cite it: https://gmsh.info/
I think the easiest way is running <pip install --upgrade gmsh--->

general process:
 - step file is imported
 - target mesh size 
 - meshing and recombination algorithms specified
 - tet mesh generated
 - tets recombined into hex _[hex only]_
 - 3D _(or 2D for shell)_ mesh generated
 - 3D mesh optimised

*note that blossom full quad is better than simple for preserving shapes when recombining. simple just divides the tets and uses midpoints. BUT blossom full quad is not yet available for curved surface as I understand it.*

- [ ] **check for updates on this! (gmsh gitlab)**

## bullet-core-tet.py

 python code for a __solid__ unstructured tetrahedral mesh in the shape of the AP bullet core as defined by a step file. 

 results:

|   `lc`   | no. els  | run time |
|----------|----------|----------|
| 0.90     | ~65k     | < 1 s    |
| 0.95     | ~52k     | < 1 s    |
| 0.10     | ~45k     | < 1 s    |
 
## bullet-core-hex.py

 python code for a __solid__ unstructured hexahedral mesh in the shape of the AP bullet core as defined by a step file. 

 the code contains a lot of commented matter that may be used to divide up the volume into sections of various sizes.

 `lc` defines the target element size [unitless as I understand it] set as `MeshSizeMax`

 `lcmin` is a slightly smaller target element size set as `MeshSizeMin` 

 the `meshSizeCallBack` function is used to loop the elements and enforce an absolute minimum of `lc = 0.5`

initial trials:

- bullet-core-fine

        lc = 0.6
        run time: 1 hour++
        425,888 elements
        
- bullet-core-course

        lc = 0.8
        run time: ~30 mins
        99,232 elements

- bullet-core-coursest

        lc = 1.0
        run time: ~9 mins
        34,592 elements

results:

|    lc    | no. els  | run time |
|----------|----------|----------|
| 1.10     | ~76k     | 800 s    |
| 1.20     | ~60k     | 707 s    |
| 1.30     | ~49k     | 625 s    |
| 1.40     | ~40k     | 554 s    |

assorted problems and fixes:
 
- [x] rebuild the bullet .step with a flat nose
  
this was tried but it didn't actually improve the quality or size of the elements in the nose. Because it's originally a tet mesh then recombined, it actaully handles the pointed shape better imo.

- [x] remake the bullet step file by revolving a shape to get rid of the separating section lines that create a 'boundary' in the mesh
  
note that this didn't help, even revolving there are the lines.

- [x] remake the bullet step file by quarter-revolving the end nose
  
this was necessary to have construction lines sort of 'guiding' the mesh generation to the pointed tip. otherwise, the tip was wonky with elements all over the place.

- [ ] could try re-building the .step with smaller rotation increments to help shape the tip

- [ ] find a way to make the initial tet mesh finer so the curve is smoother but without splitting into too many tiny hex elements

not sure this can be done. best way so far is HXT 3D and Laplace, but it takes forever (20 mins course mesh)

## bullet-shell.py

 python code for a __shell__ unstructured hexahedral mesh in the shape of the AP bullet core as defined by a step file. 

 