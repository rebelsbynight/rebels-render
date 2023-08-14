import bpy
import os
import random
import json
import sys
from os import path

OUTPUT_DIRECTORY = "rendered"
ARCTIC_WHITE_COLOR = 25

def main():
    collection_data = {}
    script_args = sys.argv[sys.argv.index("--") + 1:]
    collection_mapping_path = script_args[0]

    with open(collection_mapping_path) as f:
        collection_data = json.loads(f.read())

    initial_state = set(bpy.data.objects)

    # Render each NFT for the current color palette
    for token_id, blender_values in collection_data.items():
        print(f"")
        print(f"**** Rendering token {token_id}")
        print(f"")

        balaclava_value = blender_values["balaclava"]
        background_value = blender_values["background"]
        clothing_value = blender_values["clothing"]
        mask_value = blender_values["mask"]
        color_palette_value = blender_values["color_palette"]

        # If the Rebel has already been rendered, skip
        if path.exists(f"./{OUTPUT_DIRECTORY}/rebel-{token_id}.png") and path.getsize(f"./{OUTPUT_DIRECTORY}/rebel-{token_id}.png") > 3000000:
            continue

        # Set resolution
        bpy.data.scenes["Scene"].eevee.taa_render_samples = 100
        bpy.data.scenes["Scene"].render.resolution_x = 2000
        bpy.data.scenes["Scene"].render.resolution_y = 2000


        """-------INPUTS------------"""
        # Configure which assets to import

        # Set the mask
        mask = int(mask_value)

        # Set the cloth
        cloth = int(clothing_value)

        # Set the balaclava
        balaclava = int(balaclava_value)

        # Set the background
        background = int(background_value)

        # Set the color palette
        palette = int(color_palette_value)

        """------FUNCTIONS-----------"""
        def read_json_file(filepath):
            with open(filepath, 'r') as file:
                data = json.load(file)
            return data

        #access all of the mapped data in json format
        blend_dir = bpy.path.abspath('//')

        #DATA MAPPED TO A JSON FILE
        REBELS_DATA = read_json_file(os.path.join(blend_dir,'..', 'scripting', 'rebels_data.json'))

        # Append a specific object from a specific file
        def append_from_file(filepath, name, is_collection=False):
            # Append the object or collection from the file
            with bpy.data.libraries.load(filepath) as (data_from, data_to):
                if is_collection:
                    data_to.collections = [name]
                else:
                    data_to.objects = [name]

            # Create the "REBEL" collection if it doesn't exist
            rebel_collection = bpy.data.collections.get("REBEL")
            if not rebel_collection:
                rebel_collection = bpy.data.collections.new("REBEL")
                bpy.context.scene.collection.children.link(rebel_collection)

            # Append the object or collection to the "REBEL" collection
            if is_collection:

                for collection in data_to.collections:
                    for obj in collection.objects:
                        rebel_collection.objects.link(obj)
            else:

                for obj in data_to.objects:
                    rebel_collection.objects.link(obj)

            # Select the appended object or collection
            for obj in rebel_collection.objects:
                obj.select_set(True)
            bpy.context.view_layer.objects.active = rebel_collection.objects[0]

        def check_collection_exists(filepath, collection_name):
            with bpy.data.libraries.load(filepath) as (data_from, data_to):
                # Check if the collection exists in the file
                if collection_name in data_from.collections:
                    return True
            return False


        """-----------IMPORT ONLY NECESSARY OBJECTS TO THE SCENE--------------"""
        # BACKGROUNDS
        append_from_file("//backgrounds.blend", REBELS_DATA['backgrounds'][str(background)])

        # BALACLAVAS
        append_from_file("//balaclava.blend", REBELS_DATA['balaclavas'][str(balaclava)])

        # CLOTHES

        #find cloth file
        if check_collection_exists("//cloth_1.blend", REBELS_DATA['clothes'][str(cloth)]):
            append_from_file("//cloth_1.blend", REBELS_DATA['clothes'][str(cloth)], True)

        elif check_collection_exists("//cloth_2.blend", REBELS_DATA['clothes'][str(cloth)]):
            append_from_file("//cloth_2.blend", REBELS_DATA['clothes'][str(cloth)], True)


        # MASKS

        #find mask file
        if check_collection_exists("//mask_1.blend", REBELS_DATA['masks'][str(mask)]):
            append_from_file("//mask_1.blend", REBELS_DATA['masks'][str(mask)], True)
        elif check_collection_exists("//mask_2.blend", REBELS_DATA['masks'][str(mask)]):
            append_from_file("//mask_2.blend", REBELS_DATA['masks'][str(mask)], True)
        elif check_collection_exists("//mask_3.blend", REBELS_DATA['masks'][str(mask)]):
            append_from_file("//mask_3.blend", REBELS_DATA['masks'][str(mask)], True)

        # Technical Mask is part of a separate sub-collection that must be imported from mask_2.blend
        if "Technical Mask" in REBELS_DATA['masks'][str(mask)]:
            append_from_file("//mask_2.blend", 'Tech.001', True)


        # Set the color palette
        lib = bpy.data.libraries["EMERALD.blend"] #EMERALD.blend is the name of the first version of the linked librarie. It should not be changed


        lib.filepath = "//Color Palette/" + str(palette) + ".blend" # Change the number to set a color palette.
        lib.reload() # might not be necessary

        # Activate the special light for Arctic White color palette
        if palette == ARCTIC_WHITE_COLOR:
            bpy.data.objects["Arctic White Special Light"].hide_render = False
            bpy.data.objects["ULTI 1"].hide_render = True
            bpy.data.objects["ULTI 2"].hide_render = True
            bpy.data.objects["ULTI 3"].hide_render = True

            #Ambient occlusion setting for Arctic White color palette
            bpy.data.scenes["Scene"].eevee.gtao_distance = 10
            bpy.data.scenes["Scene"].eevee.gtao_factor = 3.90

        else:
            bpy.data.objects["Arctic White Special Light"].hide_render = True
            bpy.data.objects["ULTI 1"].hide_render = False
            bpy.data.objects["ULTI 2"].hide_render = False
            bpy.data.objects["ULTI 3"].hide_render = False

            #Ambient occlusion setting for Arctic White color palette
            bpy.data.scenes["Scene"].eevee.gtao_distance = 1
            bpy.data.scenes["Scene"].eevee.gtao_factor = 3


        # Set the output file
        bpy.data.scenes["Scene"].render.filepath = f"./{OUTPUT_DIRECTORY}/rebel-{token_id}.png"

        bpy.ops.render.render(write_still=True)
        print(f"")
        print(f"**** ---> Rendered token {token_id}")
        print(f"")

        # Cleanup the Blender objects that are loaded
        bpy.data.libraries.remove(bpy.data.libraries["EMERALD.blend"], do_unlink=True)
        for obj in list(bpy.data.objects):
            if obj not in initial_state:
                for collection in obj.users_collection:
                    try:
                        collection.objects.unlink(obj)
                        bpy.data.objects.remove(obj)
                    except:
                        pass


if __name__ == "__main__":
    sys.exit(main())
