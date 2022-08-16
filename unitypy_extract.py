# This assumes you've installed python, have UnityPy pip3 installed, have the assets decrypted in the folder you're running this
# You run it like this:
# python extract.py [folder with files] [folder to extract to]
# EXAMPLE:
# python extract.py . out
# (assuming you have a folder with *.unity3d
import os, UnityPy, sys
from PIL import Image

def unpack_all_assets(source_folder : str, destination_folder : str):
    # iterate over all files in source folder
    for root, dirs, files in os.walk(source_folder):
        for file_name in files:
            # generate file_path
            file_path = os.path.join(root, file_name)
            # load that file via UnityPy.load
            env = UnityPy.load(file_path)

            # iterate over internal objects
            for obj in env.objects:
                # process specific object types
                if obj.type.name in ["Mesh" , "Texture2D"]:
                    # parse the object data
                    data = obj.read()
                    # create destination path
                    dest = os.path.join(destination_folder,file_name.split("_")[0])
                    try:
                        os.makedirs(dest)
                    except:
                        print("",end="")
                    print("Writing data to: "+dest)
                    if obj.type.name == "Texture2D":
                        print("Found Texture2D")
                        ff = data.name + ".png"
                        out = os.path.join(destination_folder,file_name.split("_")[0],ff)
                        data.image.save(out)
                    if obj.type.name == "Mesh":
                        print("Found mesh")
                        # Create file name path
                        ff = data.name + ".obj"
                        out = os.path.join(destination_folder,file_name.split("_")[0],ff)
                        print("Saving to "+dest)
                        with open(out, "wt", newline = "") as f:
                            # newline = "" is important
                            f.write(data.export())

print()
print("Usage:")
print("python extract.py [folder with files] [folder to extract to]")
print()
unpack_all_assets(sys.argv[1],sys.argv[2])
