import os
src_dir = "C:/Program Files/VTK/lib"

file_names = os.listdir(src_dir)
fp = open("../../../predict/out.txt", "w")
for file_name in file_names:
    if( ".lib" in file_name):
        fp.write(file_name+"\n")
fp.close()

