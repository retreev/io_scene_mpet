from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import bpy
from bpy_extras.image_utils import load_image
import os
import time

from .mpet import Mpet


# Attempts to find PangYa's texture_dds folder, containing DDS textures.
def find_dds_textures_folder(dirname):
    parent = os.path.dirname(dirname)
    texdir = os.path.join(dirname, 'texture_dds')
    if os.path.exists(texdir):
        return texdir
    elif dirname != parent:
        return find_dds_textures_folder(parent)
    else:
        return None


def load_mpet(scene, file, matrix):
    dirname = os.path.dirname(file.name)
    filename = os.path.basename(file.name)

    model = Mpet()
    model.load(file)

    materials = []

    # Make materials for each texture.
    for texture in model.textures:
        fn = texture.fn.decode('utf-8')
        tex = bpy.data.textures.new(fn, type='IMAGE')

        base, ext = os.path.splitext(fn)
        if ext == ".dds":
            tex.image = load_image(fn, find_dds_textures_folder(dirname))
        else:
            tex.image = load_image(fn, dirname)

        mat = bpy.data.materials.new(fn)

        mtex = mat.texture_slots.add()
        mtex.texture = tex
        mtex.texture_coords = 'UV'

        materials.append(mat)

    # Make meshes for each mesh.
    for mesh in model.meshes:
        bmesh = bpy.data.meshes.new(filename)

        # Flatten vertices down to [x,y,z,x,y,z...] array.
        verts = [[v.x, v.y, v.z] for v in mesh.vertices]
        verts = [coord for vert in verts for coord in vert]
        bmesh.vertices.add(len(mesh.vertices))
        bmesh.vertices.foreach_set("co", verts)

        # Polygons
        num_faces = len(mesh.polygons)
        bmesh.polygons.add(num_faces)
        bmesh.loops.add(num_faces * 3)
        faces = []
        for p in mesh.polygons:
            faces.extend((
                p.indices[0].index,
                p.indices[1].index,
                p.indices[2].index
            ))
        bmesh.polygons.foreach_set("loop_start", range(0, num_faces * 3, 3))
        bmesh.polygons.foreach_set("loop_total", (3,) * num_faces)
        bmesh.polygons.foreach_set("use_smooth", (True,) * num_faces)
        bmesh.loops.foreach_set("vertex_index", faces)

        # UV maps
        uvtex = bmesh.uv_textures.new()
        uvlayer = bmesh.uv_layers.active.data[:]
        for index, bpolygon in enumerate(bmesh.polygons):
            polygon = mesh.polygons[index]

            i = bpolygon.loop_start
            for index in polygon.indices:
                uvlayer[i].uv = index.u, 1.0 - index.v
                i += 1

        # Materials
        for material in materials:
            bmesh.materials.append(material)

        for index, material in enumerate(mesh.texmap):
            bmesh.polygons[index].material_index = material

        bmesh.validate()
        bmesh.update()

        obj = bpy.data.objects.new(filename, bmesh)
        obj.matrix_world = obj.matrix_world * matrix
        scene.objects.link(obj)


def load(operator, context, filepath, matrix):
    time1 = time.clock()
    print('importing pangya model: %r' % (filepath))

    with open(filepath, 'rb') as file:
        load_mpet(context.scene, file, matrix)

    print('import done in %.4f sec.' % (time.clock() - time1))

    return {'FINISHED'}
