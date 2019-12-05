bl_info = {
    "name": "Exploder",
    "category": "Object",
}

import bpy, bmesh
from math import *
from mathutils import Vector

class Exploder(bpy.types.Operator):
    """Object Exploder"""
    bl_idname = "object.exploder"
    bl_label = "Exploder"
    bl_options = {'REGISTER', 'UNDO'}

    distance = bpy.props.FloatProperty(name="Distance", default=1.0, min=0.0, max=9999999.0)

    def execute(self, context):
        obj = context.active_object
        me = obj.data
        
        invert = False
        
        for x in me.polygons:
            if (x.select):
                invert = True
                break
                
        
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.select_all(action='TOGGLE')
        
        if (invert):
            bpy.ops.mesh.select_all(action='TOGGLE')
        
        bpy.ops.mesh.edge_split()
        bpy.ops.mesh.select_all(action='TOGGLE')        
        bpy.ops.object.mode_set(mode = 'OBJECT')
        
        me = obj.data
        vertices = me.vertices
        for v in vertices:
            n = v.normal
            
            p = v.co
            p[0] += n[0]*self.distance
            p[1] += n[1]*self.distance
            p[2] += n[2]*self.distance
            
            v.co = p
        
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(Exploder.bl_idname)

# store keymaps here to access after registration
addon_keymaps = []


def register():
    bpy.utils.register_class(Exploder)
    bpy.types.VIEW3D_MT_object.append(menu_func)

    # handle the keymap
    wm = bpy.context.window_manager
    # Note that in background mode (no GUI available), keyconfigs are not available either,
    # so we have to check this to avoid nasty errors in background case.
    kc = wm.keyconfigs.addon
    if kc:
        km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
        kmi = km.keymap_items.new(Exploder.bl_idname, 'Q', 'PRESS', ctrl=True, shift=True)
        kmi.properties.distance = 1.0
        addon_keymaps.append((km, kmi))

def unregister():
    # Note: when unregistering, it's usually good practice to do it in reverse order you registered.
    # Can avoid strange issues like keymap still referring to operators already unregistered...
    # handle the keymap
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    bpy.utils.unregister_class(Exploder)
    bpy.types.VIEW3D_MT_object.remove(menu_func)


if __name__ == "__main__":
    register()