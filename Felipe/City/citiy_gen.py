import bpy
import bmesh

import random

print("init")

# ------------------------------------------
# PARAMETERS
# ------------------------------------------

c_precision = 0.01

width = 100.0
height = 100.0
radius = 20.0

# ------------------------------------------
# DATA STRUCTURES
# ------------------------------------------

class Point:
    def __init__(self,x = 0.0, y = 0.0): 
        self.x = x 
        self.y = y
    pass

class Rectangle:
    def __init__(self,p = Point(0.0, 0.0), w = 1.0, h = 1.0): 
        self.p = p
        self.w = w
        self.h = h
    
    def is_point_inside(point):
        return ((self.p.x < point.x and point.x < (self.p.x + self.w)) and 
                (self.p.y < point.y and point.y < (self.p.y + self.h)))
    
    def is_colliding(rect):
        p0 = rect.p
        p1 = Point(p0.x + rect.w, p0.y)
        p2 = Point(p0.x, p0.y + rect.h)
        p3 = Point(p0.x + rect.w, p0.y + rect.h)
        
        return (is_point_inside(p0) or is_point_inside(p1) or
                is_point_inside(p2) or is_point_inside(p3))

    pass

# ------------------------------------------
# AUXILIARY STRUCTURES
# ------------------------------------------

centers = []
objs = bpy.context.selected_objects
for o in objs:
    centers.append( (o.location.x, o.location.y) )
    o.select = False

rects = []

# ------------------------------------------
# MESH
# ------------------------------------------

mesh = bpy.data.meshes.new("empty")
obj = bpy.data.objects.new("city",mesh)

scene = bpy.context.scene
scene.objects.link(obj)  # put the object into the scene (link)
scene.objects.active = obj  # set as the active object in the scene
obj.select = True  # select object

mesh = bpy.context.object.data
bm = bmesh.new()

# ------------------------------------------
# FUNCTIONS
# ------------------------------------------

def is_place_valid(x, y, w, h):
    rect = Rectangle(Point(x,y),w,h)
    
    if (not rects):
        for r in rects:
            if(r.is_colliding(rect)):
                return False
    
    return True

def place_building(x, y, w, h):
    v4 = bm.verts.new((x,y,0))
    v3 = bm.verts.new((x,y+h,0))
    v2 = bm.verts.new((x+w,y+h,0))
    v1 = bm.verts.new((x+w,y,0))
    
    bm.verts.ensure_lookup_table()
    
    rect = Rectangle(Point(x,y),w,h)
    rects.append(rect)
    
    bm.faces.new( (v1,v2,v3,v4) )

def random_placement(c_x, c_y):
    rx = int(c_x/c_precision)
    ry = int(c_y/c_precision)
    
    d = int(radius/c_precision)
    
    x = random.randint(rx - d, rx + d)
    y = random.randint(ry - d, ry + d)
    
    x = float(x*c_precision)
    y = float(y*c_precision)
    
    return (x,y,5.0,5.0)

def rise_building(f):
    pass

# ------------------------------------------
# MAIN
# ------------------------------------------

for c in centers:
    for i in range(10):
        x,y,w,h = random_placement(c[0],c[1])
        
        invalid = 0
        
        while (not is_place_valid(x,y,w,h)):
            x,y,w,h = random_placement(c[0],c[1])
            invalid += 1
        
        print(invalid)

        place_building(x,y,w,h)


bm.to_mesh(mesh)  
bm.free() 

print("ended")