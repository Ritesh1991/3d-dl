import sys
import argparse
import json
import bpy
import os
from io import StringIO


"""" --------------- CLI setup ------------- """
# CLI code from https://developer.blender.org/diffusion/B/browse/master/release/scripts/templates_py/background_job.py

# get the args passed to blender after "--", all of which are ignored by
# blender so scripts may receive their own arguments
argv = sys.argv

if "--" not in argv:
    argv = []  # as if no args are passed
else:
    argv = argv[argv.index("--") + 1:]  # get all args after "--"

# When --help or no args are given, print this help
usage_text = (
    "Run blender in background mode with this script:"
    "  blender --background --python " + __file__ + " -- [options]"
)

parser = argparse.ArgumentParser(description=usage_text)

parser.add_argument('project_dir',
                    help='path to source code')

# parser.add_argument('config_file',
#                     help='json file specifying rendering parameters')

parser.add_argument('object_folder',
                    help='path to folder containing object files')

parser.add_argument('output_folder',
                    help='path to folder to which poses should be saved')

parser.add_argument('renders_per_product', type=int, default=1,
                    help='number of renders to per product')

parser.add_argument('blender_attributes',
                    help='json dump of blender attributes')

args = parser.parse_args(argv)

if not argv:
    parser.print_help()
    exit(-1)

# print(args)


"""" --------------- Blender Setup ------------- """
# Ensure source directory in Blender python path
sys.path.append(os.path.join(args.project_dir))

import rendering.RenderInterface as Render

"""" --------------- Blender Setup ------------- """

if args.blender_attributes:
    io = StringIO(args.blender_attributes)
    blender_attributes = json.load(io)

print(blender_attributes)
"""" --------------- Helper functions for folder navigation ------------- """

def find_files(product_folder):
    """Naively return name of object and texture file in a folder"""
    object_file = ''
    texture_file = ''

    files = os.listdir(product_folder)

    for file in files:
        if file.endswith('.obj'):
            object_file = file
        elif file.endswith('.jpg'):
            texture_file = file

    return object_file, texture_file

"""" --------------- Rendering ------------- """

RI = Render.RenderInterface(num_images=args.renders_per_product)

# for product in config['classes']:
for product in os.listdir(args.object_folder):
    product_folder = os.path.join(args.object_folder, product)

    # Validate project
    if not os.path.isdir(product_folder):
        print("Couldn't find {} object folder! Skipping".format(product))
        continue

    # Create product folder in object_renders
    render_folder = os.path.join(args.output_folder, product)
    if not os.path.isdir(render_folder):
        print('Making render folder', render_folder)
        os.mkdir(render_folder)

    # Get model files
    object_file, texture_file = find_files(product_folder)

    # Configure model paths
    object_path = os.path.join(product_folder, object_file)
    texture_path = os.path.join(product_folder, texture_file)

    print(object_path, '\n', texture_path)
    print(render_folder)

    # Do the blender stuff
    RI.load_subject(object_path, texture_path, render_folder)

    if blender_attributes:
        for param in blender_attributes['attribute_distribution_params']:
            print(param)
            RI.set_attribute_distribution_params(param[0], param[1], param[2])

        for dist in blender_attributes['attribute_distribution']:
            print(dist)
            RI.set_attribute_distribution(dist[0], dist[1])

    RI.render_all(dump_logs = True)