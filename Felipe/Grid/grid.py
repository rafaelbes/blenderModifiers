import bpy
import bmesh

import random

delta = 0.2

height = 30

width = 40

delta_z = 0.3

verts = []

for y in range(0,height):
    for x in range(0,width):
        verts.append( (x*delta, y*delta, delta_z*random.random()-0.5) )


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
