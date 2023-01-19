import bpy
import bmesh
from bpy_extras.object_utils import AddObjectHelper
from bpy_extras.io_utils import ImportHelper


from bpy.props import (
    FloatProperty, 
    BoolProperty,
    StringProperty
)


class MESH_OT_addImagePlane(bpy.types.Operator):
    """Add a textured plane"""
    bl_idname = "mesh.image_plane_add"
    bl_label = "Image Plane"
    bl_options = {'REGISTER', 'UNDO'}
    
    filepath: StringProperty(subtype='FILE_PATH')


#    alpha: EnumProperty(
#        name="Alpha",
#        description="Whether image has an alpha channel",
#        min=0.01, max=100.0,
#        default=False,
#    )
    billboard: BoolProperty(
        name="Billboard",
        description="Whether image should look at camera",
        default=False,
    )

    def execute(self, context):
        img = bpy.data.images.load(self.filepath)
        
        # Set the texture as the diffuse color of the material
        tex = bpy.data.textures.new("ImageTexture", type='IMAGE')
        
        # Create a new material
        mat = bpy.data.materials.new("ImageMaterial")
        mat.use_nodes = True
        tex_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
        tex_node.image = img
        diffuse_node = mat.node_tree.nodes["Principled BSDF"]
        mat.node_tree.links.new(diffuse_node.inputs['Base Color'], tex_node.outputs['Color'])
        mat.node_tree.nodes['Principled BSDF'].inputs["Roughness"].default_value = 1
        mat.node_tree.nodes['Principled BSDF'].inputs["Specular"].default_value = 0
        
        
        # Create a plane
        bpy.ops.mesh.primitive_plane_add()
        plane = context.active_object
        if self.billboard:
            plane.name = "ImagePlane_eyo"
        else:
            plane.name = "ImagePlane"
        
        # Assign the material to the plane
        plane.data.materials.append(mat)
        

        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(MESH_OT_addImagePlane.bl_idname, icon='MESH_CUBE')


# Register and add to the "add mesh" menu (required to use F3 search "Add Box" for quick access).
def register():
    bpy.utils.register_class(MESH_OT_addImagePlane)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)


def unregister():
    bpy.utils.unregister_class(MESH_OT_addImagePlane)
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)


if __name__ == "__main__":
    register()
