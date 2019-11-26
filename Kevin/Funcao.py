import bpy
import bmesh

import random
import math

def gerarMola(r, grau, delta_z, z):

    verts = []

    add = delta_z

    for i in range(0,grau,4):
        verts.append( (r*math.cos(i*math.pi/100), r*math.sin(i*math.pi/100), z*delta_z) )
        delta_z += add

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
    
gerarMola(2,720,0.02,1) 