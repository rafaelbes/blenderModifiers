import bpy
import bmesh

import random
import math

r = 0.5

z = 1

delta_z = 0.02

verts = []

for i in range(0,360,4):
    verts.append( (r*math.cos(i*math.pi/100), r*math.sin(i*math.pi/100), z*delta_z) )
    delta_z += 0.02

mesh = bpy.data.meshes.new("empty")
obj = bpy.data.objects.new("Spring",mesh)

scene = bpy.context.scene
scene.objects.link(obj)  # put the object into the scene (link)
scene.objects.active = obj  # set as the active object in the scene
obj.select = True  # select object

mesh = bpy.context.object.data
bm = bmesh.new()

for v in verts:
    bm.verts.new(v)

bm.to_mesh(mesh)  
bm.free() 