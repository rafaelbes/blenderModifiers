bl_info = {
    "name": "Cursor Array",
    "category": "Object",
}


import bpy

from math import radians

posAtual = 0
angle = 0
numberDegraus = 2


class ObjectCursorArray(bpy.types.Operator):
    """Object Cursor Array"""
    bl_idname = "object.cursor_array"
    bl_label = "Criar Escada"
    bl_options = {'REGISTER', 'UNDO'}
    
    name= bpy.props.StringProperty(name="Test Property", default="A0N2")
   
    def execute(self, context):
        scene = context.scene
        cursor = scene.cursor_location
        obj = scene.objects.active
        
        obj_size = context.active_object.dimensions
            
        string = self.name
        
        s = string.split("!")
        print(s)
        
        for str in s:
            global posAtual
            posAtual = 0
            print("string -> " + str)
            
            while (posAtual < len(str)-1):
                PecorrerString(str)
            
            for i in range(numberDegraus):

                obj_new = obj.copy()
                scene.objects.link(obj_new)

                bpy.ops.object.select_all( action = 'DESELECT' )
            
                obj_new.select = True
                
                bpy.ops.transform.rotate(value=radians(angle), axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='LOCAL')
                
                
                bpy.ops.transform.translate(value=(0, obj_size.y, obj_size.z), constraint_axis=(False, True, True), constraint_orientation='LOCAL')


                #bpy.ops.transform.rotate(value=radians(angle), orient_axis='Z', orient_type='LOCAL')
                #bpy.ops.transform.translate(value=(0, obj_size.y, obj_size.z), orient_type='LOCAL')
            
                obj = obj_new
        
        return {'FINISHED'}
    
    
def PecorrerString(string):
    global posAtual, angle, numberDegraus
    
    if string[posAtual] == 'A':
        posAtual += 1
        angle = integer(string)
        print("angulo -> "+ str(angle))
    if string[posAtual] == 'N':
        posAtual += 1
        numberDegraus = integer(string)
        
        print("numero de degraus -> " + str(numberDegraus))
        
    else:
        posAtual += 1
        
    
def integer(string):
    global posAtual
    
    if "-" in string[posAtual]:
        posAtual += 1
        return number(string) * (-1)
    else:
        return number(string)
    
def number(string):
    posicao = posAtual
    
    while (digit(string)):
        pass
    return int(string[posicao: posAtual])

def digit(string):
    global posAtual
    print ("["+str(posAtual)+":"+str(len(string))+"]")
    
    if(posAtual < len(string)):
    
        if (string[posAtual].isnumeric()):
            posAtual += 1
            return True
        else:
            return False
    
    return False
    
    
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
