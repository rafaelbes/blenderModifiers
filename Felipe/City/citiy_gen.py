import bpy
import bmesh

import random

import data_structures

#configuracoes
c_precision = 0.01

width = 100
height = 100
radius = 20









centers = []
objs = bpy.context.selected_objects
for o in objs:
    centers.append( (o.location.x, o.location.y) )
    o.select = False

rects = []




mesh = bpy.data.meshes.new("empty")
obj = bpy.data.objects.new("city",mesh)

scene = bpy.context.scene
scene.objects.link(obj)  # put the object into the scene (link)
scene.objects.active = obj  # set as the active object in the scene
obj.select = True  # select object

mesh = bpy.context.object.data
bm = bmesh.new()

def is_place_valid(x, y, w, h):
    rect = Rectangle(Point(x,y),w,h)
    
    for r in rects:
        if(r.is_colliding(rect))
            return False
    
    return True

#posiciona a base da construcao
def place_building(x, y, w, h):
    
    v4 = bm.verts.new((x,y,0))
    v3 = bm.verts.new((x,y+h,0))
    v2 = bm.verts.new((x+w,y+h,0))
    v1 = bm.verts.new((x+w,y,0))
    
    bm.verts.ensure_lookup_table()
    
    rect = Rectangle(Point(x,y),w,h)
    rects.append(rect)
    
    bm.faces.new( (v1,v2,v3,v4) )

def random_placement(c_x,c_y):
    pass

def rise_building(f):
    pass


for c in centers:
    for i in range(10):
        x,y,w,h = random_placement(c[0],c[1])

        while (not is_place_valid(x,y,w,h)):
            x,y,w,h = random_placement(0,0)


        bulding_base(x,y,w,h)


bm.to_mesh(mesh)  
bm.free() 

#print(collisions[c_index(5)][c_index(10)])

#bpy.context.space_data.transform_orientation = 'NORMAL'
