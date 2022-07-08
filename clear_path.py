""" На входе: путь до директории, что сделать:
    a) удалить всё содержимое директории кроме корневой папки
    b) вывести информацию о том, сколько было удалено файлов того или иного типа
    (по расширению, папки считаем одним из типов файлов)
    c) сохранить информацию из пункта b) на диск в формате json, где расширение это ключ, кол-во значение"""


import os
import json

dir_path = input("\nВведите путь для очистки директории: ")

dir_count = 0
file_count = 0
len_files = 0
len_dirs = 0
lst_extension = []
dict_extension = {}


for root, dirs, files in os.walk(dir_path, topdown=False):  # Перебираем все файлы и папки из глубины, к кореневой папке
    len_files += len(files)
    len_dirs += len(dirs)

    for file in files:  # Перебор файлов, расширения в список и удаление
        try:
            file_name, file_extension = os.path.splitext(file)
            os.remove(os.path.join(root, file))
            lst_extension.append(file_extension)
            file_count += 1
        except PermissionError:
            print(f"Файл {os.path.join(root, file)}, не удалён, проверьте разрешения и повторите!")
            continue

    for folder in dirs:  # Удаление пустых папок
        try:
            os.rmdir(os.path.join(root, folder))
            dir_count += 1
        except OSError:
            print(f"Папка {os.path.join(root, folder)}, не удалена, проверьте разрешения и повторите!")
            continue


dict_extension = dict(zip(lst_extension, [lst_extension.count(i) for i in lst_extension]))  # Создание словаря
if dir_count > 0:
    dict_extension['folder'] = dir_count

try:
    with open(f"{dir_path}/del_files.json", "wb") as f:  # Сохранение в файл в корневой папке
        f.write(json.dumps(dict_extension).encode("utf-8"))
except PermissionError:
    print(f"Не достаточно прав доступа для записи результатов выполнения в {dir_path}")

print(f"\nКоличество файлов: {len_files}, удалено: {file_count}")
print(f"Количество папок: {len_dirs}, удалено: {dir_count} \n")
print(f"Список удаленных файлов по расширениям и количество их значений, в : {dir_path}/del_files.json")
