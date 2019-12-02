bl_info = {
    "name": "Cursor Array",
    "category": "Object",
}


import bpy

from math import radians

posAtual = 0

#from bpy import context

##Recebe a scene atual
#scene = context.scene

## Recebe o 3d cursor
#cursor = scene.cursor.location

## Recebe o objeto ativo (suponha que so temos um)
#obj = context.active_object

## Agora faca uma copia do objeto
#obj_new = obj.copy()

## O objeto nao entra automaticamente em uma nova cena
#scene.collection.objects.link(obj_new)

## Agora podemos colocar o objeto
#obj_new.location = cursor


class ObjectCursorArray(bpy.types.Operator):
    """Object Cursor Array"""
    bl_idname = "object.cursor_array"
    bl_label = "Criar Escada"
    bl_options = {'REGISTER', 'UNDO'}
    
    total: bpy.props.IntProperty(name="Steps", default=2, min=1, max=100)
    rotacao: bpy.props.IntProperty(name="rotacao", default=0, min=-360, max=360)
    
    def execute(self, context):
        scene = context.scene
        cursor = scene.cursor.location
        obj = context.active_object
        
        obj_size = context.active_object.dimensions
        
        
        for i in range(self.total):

            msg = "LUCAS"
            printarMsg(msg)
            
            print(str(posAtual))
            obj_new = obj.copy()
            scene.collection.objects.link(obj_new)

            bpy.ops.object.select_all( action = 'DESELECT' )
            
            obj_new.select_set(True)
            
            #obj_new.rotation_euler[2] = 1
    
            #obj_new.location.x += (i+0.5)   
            #obj_new.location.y += obj_size.y * (i+1)
            #obj_new.location.z += obj_size.z * (i+1)
            
            bpy.ops.transform.rotate(value=radians(self.rotacao), orient_axis='Z', orient_type='LOCAL')
            bpy.ops.transform.translate(value=(0, obj_size.y, obj_size.z), orient_type='LOCAL')
            
            obj = obj_new
        
        return {'FINISHED'}
    
    
    
def printarMsg(msg):
    print(msg)
    
    global posAtual 
    posAtual = 5
    
    msg = 'lima'
    
    
def menu_func(self, context):
    self.layout.operator(ObjectCursorArray.bl_idname)
    
def register():
    bpy.utils.register_class(ObjectCursorArray)
    bpy.types.VIEW3D_MT_object.append(menu_func)
    
def unregister():
    bpy.utils.unregister_class(ObjectCursorArray)
    bpy.types.VIEW3D_MT_OBJECT.remove(menu_func)
    
    
if __name__ == "__main__":
    register()
