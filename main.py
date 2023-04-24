import fileinput

with open('recipes.txt', 'r', encoding='utf-8') as f:
    cook_book = {}
    for line in f:
        recipe_name = f.readline().strip()
        ingredients_count = int(f.readline().strip())
        ingredients = []
        for i in range(ingredients_count):
            ingredient = f.readline().strip()
            ingredient_name, quantity, measure = ingredient.split('|')
            ingredients.append({
                'ingredient_name': ingredient_name,
                'quantity': quantity,
                'measure': measure
            })
        cook_book[recipe_name] = ingredients


def get_shop_list_by_dishes(dishes, person_count):
    ingredient_calculation = {}
    for dish in dishes:
        for ingredient in cook_book[dish]:
            i = 0
            for element in ingredient.values():
                if i == 0:
                    ingredient_name = element
                    i += 1
                elif i == 1:
                    if ingredient_name in ingredient_calculation.keys():
                        quantity = (ingredient_calculation[ingredient_name].get('quantity')) + int(
                            element) * person_count
                    else:
                        quantity = int(element) * person_count
                    i += 1
                else:
                    measure = element
                    ingredient_calculation[ingredient_name] = {'measure': measure, 'quantity': quantity}
                    i = 0
    print(ingredient_calculation)


def files_complementation(files, new_file_name):
    files_meta = {}
    for file in files:
        row_count = sum(1 for line in open(file, encoding="utf8"))
        files_meta[file] = row_count
    sorted_files_meta = dict(sorted(files_meta.items(), key=lambda item: item[1]))
    key_list = []
    for key, value in sorted_files_meta.items():
        key_list.append(key)

    with fileinput.FileInput(files=key_list, encoding="utf8") as input, open(new_file_name, 'w',
                                                                             encoding="utf8") as new_file:
        first_file = True
        for line in input:
            if input.isfirstline():
                if first_file:
                    file_name = input.filename()
                    new_file.write(f'Имя файла:{file_name}\n')
                    new_file.write(f'Количество строк в файле: {files_meta.get(file_name)}\n\n')
                    first_file = False
                else:
                    file_name = input.filename()
                    new_file.write(f'\n\nИмя файла:{file_name}\n')
                    new_file.write(f'Количество строк в файле: {files_meta.get(file_name)}\n\n')

            new_file.write(line)


get_shop_list_by_dishes(['Запеченный картофель', 'Омлет'], 2)

print(files_complementation(['1.txt', '2.txt', '3.txt'], 'complementation.txt'))
