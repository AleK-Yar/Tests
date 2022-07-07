''' На входе: путь до директории, что сделать:
    a) удалить всё содержимое директории кроме корневой папки
    b) вывести информацию о том, сколько было удалено файлов того или иного типа
    (по расширению, папки считаем одним из типов файлов)
    c) сохранить информацию из пункта b) на диск в формате json, где расширение это ключ, кол-во значение'''


import os
import json

dir_path = input("Введите путь для очистки директории: ")

dir_count = 0
lst_extension = []
dict_extension = {}

for root, dirs, files in os.walk(dir_path, topdown=False):  # Перебираем все файлы и папки из глубины, к кореневой папке
    dir_count += len(dirs)
    try:
        for file in files:  # Перебор файлов, расширения в список и удаление
            file_name, file_extension = os.path.splitext(file)
            lst_extension.append(file_extension)
            os.remove(os.path.join(root, file))
    except PermissionError:
        print(f"Не достаточно прав доступа для удаления!{os.path.join(root, file)}")
        break

    try:
        for folder in dirs:  # Удаление пустых папок
            os.rmdir(os.path.join(root, folder))
    except PermissionError:
        print(f"Не достаточно прав доступа для удаления!{os.path.join(root, folder)}")
        break

dict_extension = dict(zip(lst_extension, [lst_extension.count(i) for i in lst_extension]))  # Создание словаря
if dir_count > 0:
    dict_extension['folder'] = dir_count

try:
    with open(f"{dir_path}/del_files.json", "wb") as f:  # Сохранение в файл в корневой папке
        f.write(json.dumps(dict_extension).encode("utf-8"))
except PermissionError:
    print(f"Не достаточно прав доступа для записи результатов выполнения в {dir_path}")

print(f"Список расширений и количество их значений, в : {dir_path}/del_files.json")
