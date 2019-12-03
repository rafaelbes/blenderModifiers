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
    radius = bpy.props.FloatProperty(name="Area", default=60.0, min=1.0, max=1000.0) 
    min_w = bpy.props.FloatProperty(name="Min. Width", default=1.0, min=1.0, max=1000.0) 
    max_w = bpy.props.FloatProperty(name="Max. Width", default=5.0, min=1.0, max=1000.0) 
    min_h = bpy.props.FloatProperty(name="Min. Height", default=1.0, min=1.0, max=1000.0) 
    max_h = bpy.props.FloatProperty(name="Max. Height", default=5.0, min=1.0, max=1000.0) 
    n_buildings = bpy.props.IntProperty(name="Buildings", default=10, min=1, max=100000) 
    
    
    #otal = bpy.props.FloatProperty(name="Steps", default=2, min=1, max=100)
    centers = []
    rects = []
    
    c_precision = 0.01
    
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
        
        bm.faces.new( (v1,v2,v3,v4) )

    def random_placement(self,c_x, c_y):
        rx = int(c_x/self.c_precision)
        ry = int(c_y/self.c_precision)
        
        d = int(self.radius/self.c_precision)
        
        x = random.randint(rx - d, rx + d)
        y = random.randint(ry - d, ry + d)
        
        x = float(x*self.c_precision)
        y = float(y*self.c_precision)
        
        #ajustar tamanho das estruturas
        
        return (x,y,5.0,5.0)

    def rise_building(self,f):
        pass
    
    def execute(self, context):

        self.rects = []
        self.centers = []
        
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
                
                invalid = 0
                
                while (not self.is_place_valid(x,y,w,h)):
                    x,y,w,h = self.random_placement(c[0],c[1])
                    invalid += 1
                if (invalid > 0):
                    print(invalid)

                self.place_building(x,y,w,h, bm)


        bm.to_mesh(mesh)  
        bm.free() 
        
        obj.select = False
        
        for o in objs:
            o.select = True
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
        #kmi.properties.width = 100.0
        #kmi.properties.height = 100.0
        kmi.properties.radius = 60.0
        kmi.properties.min_w = 1.0
        kmi.properties.max_w = 5.0
        kmi.properties.min_h = 1.0
        kmi.properties.max_h = 5.0
        kmi.properties.seed = 1
        kmi.properties.n_buildings = 10
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