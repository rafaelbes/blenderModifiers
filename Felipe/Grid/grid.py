import bpy
import bmesh

import random

delta = 1

height = 200

width = 200

min_z = -1
max_z = 1

verts = []

for y in range(0,height):
    for x in range(0,width):
        verts.append( (x*delta, y*delta, random.randint(min_z, max_z)) )


mesh = bpy.data.meshes.new("empty")
obj = bpy.data.objects.new("brid_obj",mesh)

scene = bpy.context.scene
scene.objects.link(obj)  # put the object into the scene (link)
scene.objects.active = obj  # set as the active object in the scene
obj.select = True  # select object

mesh = bpy.context.object.data
bm = bmesh.new()

for v in verts:
    bm.verts.new(v)

def coord(y,x):
    return y*width + x
    
for y in range(0,height-1):
    for x in range(0,width-1):
        bm.verts.ensure_lookup_table()
        v1 = bm.verts[coord(y,x)]
        
        v2 = bm.verts[coord(y,x+1)]
        v3 = bm.verts[coord(y+1,x+1)]
        v4 = bm.verts[coord(y+1,x)]
        bm.faces.new((v1, v2, v3, v4 ))
        #bm.faces.ensure_lookup_faces

    
bm.to_mesh(mesh)  
bm.free() 

bpy.ops.object.mode_set(mode = 'EDIT')
bpy.ops.mesh.select_all(action='TOGGLE')
bpy.ops.mesh.normals_make_consistent(inside=False)
bpy.ops.mesh.faces_shade_smooth()
bpy.ops.mesh.vertices_smooth()
bpy.ops.mesh.select_all(action='TOGGLE')
bpy.ops.object.mode_set(mode = 'OBJECT')