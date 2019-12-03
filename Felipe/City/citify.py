bl_info = {
    "name": "Cityfy",
    "category": "Object",
}

import bpy
import bmesh

import random

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
# Add-on
# ------------------------------------------

class Cityfy(bpy.types.Operator):
    """Generate city"""
    bl_idname = "object.cityfy"
    bl_label = "Cityfy"
    bl_options = {'REGISTER', 'UNDO'}

    width = bpy.props.FloatProperty(name="Width", default=100.0, min=1.0, max=1000.0)
    height = bpy.props.FloatProperty(name="Height", default=100.0, min=1.0, max=1000.0) 
     
    #otal = bpy.props.FloatProperty(name="Steps", default=2, min=1, max=100)
    centers = []
    rects = []
    
    def is_place_valid(self,x, y, w, h):
        rect = Rectangle(Point(x,y),w,h)
        
        if (not self.rects):
            for r in self.rects:
                if(r.is_colliding(rect)):
                    return False
        
        return True

    def place_building(bm, x, y, w, h):
        v4 = bm.verts.new((x,y,0))
        v3 = bm.verts.new((x,y+h,0))
        v2 = bm.verts.new((x+w,y+h,0))
        v1 = bm.verts.new((x+w,y,0))
        
        bm.verts.ensure_lookup_table()
        
        rect = Rectangle(Point(x,y),w,h)
        self.rects.append(rect)
        
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
    
    def execute(self, context):

        objs = bpy.context.selected_objects
        for o in objs:
            self.centers.append( (o.location.x, o.location.y) )
            o.select = False

        
        mesh = bpy.data.meshes.new("empty")
        obj = bpy.data.objects.new("city",mesh)

        scene = bpy.context.scene
        scene.objects.link(obj)  # put the object into the scene (link)
        scene.objects.active = obj  # set as the active object in the scene
        obj.select = True  # select object

        mesh = bpy.context.object.data
        bm = bmesh.new()
        
        
        '''
        scene = context.scene
        cursor = scene.cursor_location
        obj = scene.objects.active

        for i in range(self.total):
            obj_new = obj.copy()
            scene.objects.link(obj_new)

            factor = i / self.total
            obj_new.location = (obj.location * factor) + (cursor * (1.0 - factor))
        '''
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
        kmi.properties.width = 100.0
        kmi.properties.height = 100.0
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