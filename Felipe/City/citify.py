bl_info = {
    "name": "Cityfy",
    "category": "Object",
}

import bpy
import bmesh

import random

import math

import functools

from math import *
from mathutils import Vector

print("Using Citify")



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
    
    def is_point_inside(self, point):
        return ((self.p.x < point.x and point.x < (self.p.x + self.w)) and \
                (self.p.y < point.y and point.y < (self.p.y + self.h)))
    
    def is_colliding(self, rect):
        p0 = rect.p
        p1 = Point(p0.x + rect.w, p0.y)
        p2 = Point(p0.x, p0.y + rect.h)
        p3 = Point(p0.x + rect.w, p0.y + rect.h)
        
        return (self.is_point_inside(p0) or self.is_point_inside(p1) or \
                self.is_point_inside(p2) or self.is_point_inside(p3))

    pass

#class Building:
#    def __init__(self, base, ):
        
# ------------------------------------------
# Add-on
# ------------------------------------------

class Cityfy(bpy.types.Operator):
    """Generate city"""
    bl_idname = "object.cityfy"
    bl_label = "Cityfy"
    bl_options = {'REGISTER', 'UNDO'}

    #width = bpy.props.FloatProperty(name="Width", default=100.0, min=1.0, max=1000.0)
    #height = bpy.props.FloatProperty(name="Height", default=100.0, min=1.0, max=1000.0) 
    seed = bpy.props.IntProperty(name="Seed", default=1, min=0, max=9999999) 
    simplyfied = bpy.props.BoolProperty(name="Simplified", default=True)
    radius = bpy.props.FloatProperty(name="Area", default=60.0, min=1.0, max=1000.0) 
    min_w = bpy.props.FloatProperty(name="Min. Width", default=1.0, min=1.0, max=1000.0) 
    max_w = bpy.props.FloatProperty(name="Max. Width", default=5.0, min=1.0, max=1000.0) 
    min_h = bpy.props.FloatProperty(name="Min. Height", default=1.0, min=1.0, max=1000.0) 
    max_h = bpy.props.FloatProperty(name="Max. Height", default=5.0, min=1.0, max=1000.0) 
    n_buildings = bpy.props.IntProperty(name="Buildings", default=10, min=1, max=100000) 
    floor_height = bpy.props.FloatProperty(name="Floor Height", default=3.0, min=0.001, max=1000.0) 
    max_floors = bpy.props.IntProperty(name="Max. Floors", default=20, min=1, max=99999) 
    prob = bpy.props.FloatProperty(name="Dist. Big Buildings", default=0.5, min=0.000001, max=100000.0) 
    #ndex = bpy.props.IntProperty(name="Dist. Big Buildings", default=5, min=0, max=10) 
    
    #otal = bpy.props.FloatProperty(name="Steps", default=2, min=1, max=100)
    centers = []
    rects = []
    
    c_precision = 0.01
    
    bases = []
    
    def is_place_valid(self, x, y, w, h):
        rect = Rectangle(Point(x,y),w,h)
        
        if (len(self.rects) > 0):
            for r in self.rects:
                if(r.is_colliding(rect)):
                    return False
        
        return True

    def place_building(self, x, y, w, h, bm):
        v4 = bm.verts.new((x,y,0))
        v3 = bm.verts.new((x,y+h,0))
        v2 = bm.verts.new((x+w,y+h,0))
        v1 = bm.verts.new((x+w,y,0))
        
        bm.verts.ensure_lookup_table()
        
        rect = Rectangle(Point(x,y),w,h)
        self.rects.append(rect)
        
        self.bases.append(bm.faces.new( (v1,v2,v3,v4) ))

    def compare(self, lhs, rhs):
        return ((rhs[2]*rhs[3])-(lhs[2]*lhs[3]))
        
    def random_placement(self,c_x, c_y):
        rx = int(c_x/self.c_precision)
        ry = int(c_y/self.c_precision)
        
        d = int(self.radius/self.c_precision)
        
        coords = []
        
        #x, y, w, h = (0,0,0.0,0.0)
        
        x = random.randint(rx - d, rx + d)
        y = random.randint(ry - d, ry + d)
            
        x = float(x*self.c_precision)
        y = float(y*self.c_precision)
            
        for i in range(0,10):            
            w = float(int(random.uniform(self.min_w, self.max_w)/self.c_precision)*self.c_precision)
            h = float(int(random.uniform(self.min_h, self.max_h)/self.c_precision)*self.c_precision)
            

            coords.append((x, y, w, h))
        
        sorted(coords, key=functools.cmp_to_key(self.compare))
        #for x in coords:
        #    print(x[2]*x[3])
        
        d = math.sqrt( (x-c_x)**2 + (y-c_y)**2)
        
        index = 0
        
        if (d < 0.1):
            index = 0
        elif (d > self.prob):
            index = 9
        else:
            index = int(9.0*(d/self.prob))

        
        #return coords[index]
        return (coords[index][0],coords[5][1],coords[index][2],coords[index][3])

    def rise_building(self):
        obj = bpy.context.selected_objects[0]
        me = obj.data

        #s = len(mesh.polygons)

        polys = me.polygons


        for i in range(0,len(polys)):
            floors = random.randint(0,self.max_floors)
            
            polys[i].select = True
            
            bpy.ops.object.mode_set(mode = 'EDIT')
            
            
            for x in range(0,floors):
                        
                bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(0, 0, self.floor_height), "constraint_axis":(False, False, True), "constraint_orientation":'NORMAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'RANDOM', "proportional_size":11.9182, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})

                bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(0, 0, 0), "constraint_axis":(False, False, True), "constraint_orientation":'NORMAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'RANDOM', "proportional_size":11.9182, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
                bpy.ops.transform.resize(value=(1.05, 1.05, 1.05), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='RANDOM', proportional_size=11.9182)
                bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(0, 0, self.floor_height*0.05), "constraint_axis":(False, False, True), "constraint_orientation":'NORMAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'RANDOM', "proportional_size":11.9182, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})

                bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(0, 0, 0), "constraint_axis":(False, False, True), "constraint_orientation":'NORMAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'RANDOM', "proportional_size":11.9182, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
                bpy.ops.transform.resize(value=(0.955, 0.955, 0.955), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='RANDOM', proportional_size=11.9182)


            bpy.ops.mesh.select_all(action='TOGGLE')

            bpy.ops.object.mode_set(mode = 'OBJECT')
        
        
    def rise_building2(self, bm):
        

        for b in self.bases:
            #area = f.calc_area()
            
            floors = random.randint(0,self.max_floors)
            
            top = bmesh.ops.extrude_face_region(bm, geom=[b])
            bmesh.ops.translate(bm, vec=Vector((0,0,self.floor_height*floors)), verts=[v for v in top["geom"] if isinstance(v,bmesh.types.BMVert)])

            bm.normal_update()
        
        
    def execute(self, context):

        self.rects = []
        self.centers = []
        self.bases = []
        
        random.seed(self.seed)

        objs = context.selected_objects
        for o in objs:
            self.centers.append( (o.location.x, o.location.y) )
            o.select = False

        
        mesh = bpy.data.meshes.new("empty")
        obj = bpy.data.objects.new("city",mesh)

        scene = context.scene
        scene.objects.link(obj)  # put the object into the scene (link)
        scene.objects.active = obj  # set as the active object in the scene
        obj.select = True  # select object

        mesh = bpy.context.object.data
        bm = bmesh.new()
        
        for c in self.centers:
            for i in range(self.n_buildings):
                x,y,w,h = self.random_placement(c[0],c[1])
                
                while (not self.is_place_valid(x,y,w,h)):
                    x,y,w,h = self.random_placement(c[0],c[1])

                self.place_building(x,y,w,h, bm)

        if (self.simplyfied):
            self.rise_building2(bm)
        
        bm.to_mesh(mesh)  
        bm.free() 
        
        if (not self.simplyfied):
            self.rise_building()
        
        obj.select = False
        
        for o in objs:
            o.select = True

        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(Cityfy.bl_idname)

# store keymaps here to access after registration
addon_keymaps = []


def register():
    bpy.utils.register_class(Cityfy)
    bpy.types.VIEW3D_MT_object.append(menu_func)

    # handle the keymap
    wm = bpy.context.window_manager
    # Note that in background mode (no GUI available), keyconfigs are not available either,
    # so we have to check this to avoid nasty errors in background case.
    kc = wm.keyconfigs.addon
    if kc:
        km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
        kmi = km.keymap_items.new(Cityfy.bl_idname, 'SPACE', 'PRESS', ctrl=True, shift=True)
        #kmi.properties.width = 100.0
        #kmi.properties.height = 100.0
        kmi.properties.radius = 60.0
        kmi.properties.min_w = 1.0
        kmi.properties.max_w = 5.0
        kmi.properties.min_h = 1.0
        kmi.properties.max_h = 5.0
        kmi.properties.seed = 1
        kmi.properties.n_buildings = 10
        kmi.properties.floor_height = 1.0
        kmi.properties.max_floors = 20
        kmi.properties.prob = 0.5
        addon_keymaps.append((km, kmi))

def unregister():
    # Note: when unregistering, it's usually good practice to do it in reverse order you registered.
    # Can avoid strange issues like keymap still referring to operators already unregistered...
    # handle the keymap
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    bpy.utils.unregister_class(Cityfy)
    bpy.types.VIEW3D_MT_object.remove(menu_func)


if __name__ == "__main__":
    register()
    
print("End")