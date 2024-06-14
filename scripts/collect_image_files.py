import argparse
import csv
import json
import os
import sys
import shutil

my_parser = argparse.ArgumentParser(description='COPY image files based on Megadetector detection categories')
my_parser.add_argument('-b', '--image_base', type=str,
                       action='store', dest='image_base', required=True,
                       help='The base directory where the images are stored')
my_parser.add_argument('-i', '--infile_csv', metavar='INFILE', type=str,
                       action='store', dest='infile_csv', required=True,
                       help='Target CSV that contains MD output information')
my_parser.add_argument('-o', '--out_base', type=str,
                       action='store', dest='out_base',
                       help='The base directory where you want the sorted images to be copied, default is ./')

args = my_parser.parse_args()

# setup dirs
if args.out_base:
    out_dir_path = os.path.join(os.getcwd(), args.out_base)
else:
    out_dir_path = os.getcwd()
animal_out = os.path.join(out_dir_path, "animal")
person_out = os.path.join(out_dir_path, "person")
vehicle_out = os.path.join(out_dir_path, "vehicle")
empty_out = os.path.join(out_dir_path, "empty")

os.makedirs(animal_out, exist_ok=True)
os.makedirs(person_out, exist_ok=True)
os.makedirs(vehicle_out, exist_ok=True)
os.makedirs(empty_out, exist_ok=True)

# some output stats
animal_count = 0
person_count = 0
vehicle_count = 0
empty_count = 0

with open(args.infile_csv) as rf:
    csv_reader = csv.reader(rf)
    header = next(csv_reader)
    for row in csv_reader:
        filepath = row[0]
        target_file = os.path.basename(filepath)
        subdirname = os.path.basename(os.path.dirname(filepath))
        # this file will be copied
        full_image_path = os.path.join(args.image_base, subdirname, target_file)
        obj_cats = row[2]
        # replace semicolons used to avoid CSV issues
        obj_count = int(row[1])
        # get the image dir, md file path may contain other dirs
        if obj_count == 0:
            # keep the subdir folder to avoid file name collisions
            dst = os.path.join(empty_out, subdirname)
            os.makedirs(dst, exist_ok=True)
            shutil.copy2(full_image_path, dst)
            empty_count += 1
        else:
            if obj_cats.find('animal') > -1:
                dst = os.path.join(animal_out, subdirname)
                os.makedirs(dst, exist_ok=True)
                shutil.copy2(full_image_path, dst)
                animal_count += 1
            elif obj_cats.find('person') > -1:
                dst = os.path.join(person_out, subdirname)
                os.makedirs(dst, exist_ok=True)
                shutil.copy2(full_image_path, dst)
                person_count += 1
            else:
                assert obj_cats == "vehicle"
                dst = os.path.join(vehicle_out, subdirname)
                os.makedirs(dst, exist_ok=True)
                shutil.copy2(full_image_path, dst)
                vehicle_count += 1

print("Finished! Your images have been copied to folders located in: %s"%(out_dir_path))
print()
print("The number of images moved to each directory are listed below,")
print("but please note that if an animal and a person or vehicle are found")
print("in the same image, it will be copied to the animal directory:")
# report
print("animal: %s" % animal_count)
print("person: %s" % person_count)
print("vehicle: %s" % vehicle_count)
print("empty: %s" % empty_count)