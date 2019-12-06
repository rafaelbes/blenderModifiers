bl_info = {
    "name": "Criador de Relevo",
    "category": "Object",
}

import bpy
import bmesh
from random import uniform


class CreateRelief(bpy.types.Operator):
    """My Object Create Relief"""      # Use this as a tooltip for menu items and buttons.
    bl_idname = "object.create_relevo"        # Unique identifier for buttons and menu items to reference.
    bl_label = "Criador de relevo"         # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.
    
    deformacao= bpy.props.FloatProperty(name="Deformacao", default=0.555, min=0.0, max=10.0)
    
    def execute(self, context):        # execute() is called when running the operator.

        ob = context.edit_object
        me = ob.data
        bm = bmesh.from_edit_mesh(me)
        
        for vert in bm.verts:
            vert.select_set(True)
            
            
            bpy.ops.transform.translate(value=(0, 0, uniform(self.deformacao * -1, self.deformacao)), constraint_axis=(False, False, True), constraint_orientation='GIMBAL')

            #bpy.ops.transform.translate(value=(0, 0, uniform(self.deformacao * -1, self.deformacao)), orient_type='GIMBAL')
            
            vert.select_set(False)
        
        bmesh.update_edit_mesh(me)


        return {'FINISHED'}  


def menu_func(self, context):
    self.layout.operator(CreateRelief.bl_idname)
    
def register():
    bpy.utils.register_class(CreateRelief)
    bpy.types.VIEW3D_MT_edit_mesh.append(menu_func)


def unregister():
    bpy.utils.unregister_class(CreateRelief)
    bpy.types.VIEW3D_MT_edit_mesh.remove(menu_func)


if __name__ == "__main__":
    register()