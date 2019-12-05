bl_info = {
            "name": "Skin4Springs",
            "category": "Object",            
}

import bpy
import bmesh


class Skin4Springs(bpy.types.Operator):
    """Skin4Spring Modifier"""
    bl_idname = "object.skin4springs"
    bl_label = "Skin4Springs"
    bl_options = {'REGISTER', 'UNDO'}
    
    frac = bpy.props.IntProperty(name="Fração", default=15, min=2)
    altura = bpy.props.FloatProperty(name="Altura dos paralelepípedos", default=0.05, min=0.01)
    fechar_face = bpy.props.BoolProperty(name="Inserir face final", default=False)
    tirar_face_interna = bpy.props.BoolProperty(name="Não inserir faces internas", default=False)

    def execute(self,context):
        
        # Pegando o objeto selecionado e alocando uma nova malha bmesh
        mesh = bpy.context.object.data
        bm = bmesh.new()
        
        # Coletando os parãmetros inseridos pelo usuário
        frac = self.frac
        altura = self.altura
        fechar_face = self.fechar_face
        tirar_face_interna = self.tirar_face_interna

        # Convertendo o objeto selecionado numa malha do bmesh
        bpy.ops.object.mode_set(mode='EDIT')
        bm.from_mesh(mesh)
        bpy.ops.object.mode_set(mode='OBJECT')  # return to object mode

        # Vetores utilizados para manter a sequência de criação dos vértices
        reserva = bm.verts[:]
        lista_para_faces = []

        bm.verts.ensure_lookup_table()
        
        # Gerando as espirais secundárias e criando suas respectivas arestas
        for i in reserva:
            bm.verts.ensure_lookup_table()
            bm.verts.ensure_lookup_table()
            v1 = bm.verts.new((i.co.x + i.co.x/frac, i.co.y + i.co.y/frac, i.co.z))  # add a new vert
            lista_para_faces.append(v1)
            bm.verts.ensure_lookup_table()
            v2 = bm.verts.new((i.co.x + i.co.x/frac, i.co.y + i.co.y/frac, i.co.z + altura))
            lista_para_faces.append(v2)
            bm.verts.ensure_lookup_table()
            v3 = bm.verts.new((i.co.x - i.co.x/frac, i.co.y - i.co.y/frac, i.co.z))    
            lista_para_faces.append(v3)
            bm.verts.ensure_lookup_table()
            v4 = bm.verts.new((i.co.x - i.co.x/frac, i.co.y - i.co.y/frac, i.co.z + altura))
            lista_para_faces.append(v4)
            bm.verts.ensure_lookup_table()
            bm.edges.new((v1, v2))
            bm.verts.ensure_lookup_table()
            bm.edges.new((v3, v4))
            bm.verts.ensure_lookup_table()
            bm.edges.new((v1,v3))
            bm.verts.ensure_lookup_table()
            bm.edges.new((v2,v4))
            bm.verts.ensure_lookup_table()
            bm.verts.remove(i)

        # Gerando as faces do objeto
        for i in range(0,len(lista_para_faces),4):
            # Condição para não acessar posições inválidas da memória
            if i+7 > len(lista_para_faces):
                break
            # Condição para remover as faces internas e não haver faces repetidas
            if i == 0 and fechar_face == False:
                bm.faces.new((lista_para_faces[i], lista_para_faces[i+1], lista_para_faces[i+3],lista_para_faces[i+2]))
            # Condição para remover as faces internas
            if tirar_face_interna == False or i==len(lista_para_faces)-8 and fechar_face == False:
                bm.faces.new((lista_para_faces[i+4], lista_para_faces[i+5], lista_para_faces[i+7], lista_para_faces[i+6]))        
            bm.faces.new((lista_para_faces[i+1], lista_para_faces[i+5], lista_para_faces[i+7], lista_para_faces[i+3]))
            bm.faces.new((lista_para_faces[i], lista_para_faces[i+4], lista_para_faces[i+6], lista_para_faces[i+2]))
            bm.faces.new((lista_para_faces[i], lista_para_faces[i+4], lista_para_faces[i+5], lista_para_faces[i+1]))
            bm.faces.new((lista_para_faces[i+6], lista_para_faces[i+2], lista_para_faces[i+3], lista_para_faces[i+7]))
        
        # Fechando a ultima face, caso o usuário deseje
        if fechar_face == True:
            i = len(lista_para_faces)-1
            bm.faces.new((lista_para_faces[1], lista_para_faces[i-2], lista_para_faces[i], lista_para_faces[3]))
            bm.faces.new((lista_para_faces[0], lista_para_faces[i-3], lista_para_faces[i-1], lista_para_faces[2]))
            bm.faces.new((lista_para_faces[0], lista_para_faces[i-3], lista_para_faces[i-2], lista_para_faces[1]))
            bm.faces.new((lista_para_faces[i-1], lista_para_faces[2], lista_para_faces[3], lista_para_faces[0]))
        
        # Transformar a malha modificada para uma malha normal do blender
        bm.to_mesh(mesh)  
        
        # Consertar as normais da malha
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.select_all(action='TOGGLE')
        bpy.ops.mesh.normals_make_consistent(inside=False)
        bpy.ops.mesh.select_all(action='TOGGLE')
        bpy.ops.object.mode_set(mode = 'OBJECT')
        
        bm.free()  # Liberar a malha e não permitir mais edições
        
        return {'FINISHED'}

# Funções necessárias para inserção do operador no menu
def menu_func(self, context):
    self.layout.operator(Skin4Springs.bl_idname)
    
def register():
    bpy.utils.register_class(Skin4Springs)
    bpy.types.VIEW3D_MT_object.append(menu_func)

def unregister():
    bpy.utils.unregister_class(Skin4Springs)
    bpy.types.VIEW3D_MT_object.remove(menu_func)
    
if __name__ == "__main__":
    register()    