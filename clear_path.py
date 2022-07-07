import os
import json

dir_path = "/media/alek/ShareII/TEST"

dir_count = 0
lst_extension = []
dict_extension = {}

for root, dirs, files in os.walk(dir_path, topdown=False):
    dir_count += len(dirs)
    try:
        for file in files:
            file_name, file_extension = os.path.splitext(file)
            lst_extension.append(file_extension)
            os.remove(os.path.join(root, file))
    except PermissionError:
        print(f"Не достаточно прав доступа для удаления!{os.path.join(root, file)}")
        break

    try:
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    except PermissionError:
        print(f"Не достаточно прав доступа для удаления!{os.path.join(root, name)}")
        break

dict_extension = dict(zip(lst_extension, [lst_extension.count(i) for i in lst_extension]))
dict_extension['folder'] = dir_count

try:
    with open(f"{dir_path}/del_files.json", "wb") as f:
        f.write(json.dumps(dict_extension).encode("utf-8"))
except PermissionError:
    print(f"Не достаточно прав доступа для записи результатов выполнения в {dir_path}")
