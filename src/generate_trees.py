import ast


def extract_python_files_from_path(os, path):
    file_names = []
    for dir_name, dirs, files in os.walk(path, topdown=True):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(dir_name, file)
                file_names.append(file_path)

    files_count = len(file_names)

    if files_count > 0:
        print('total {} files in path {}'.format(files_count, path))

    return file_names, files_count


def get_tree(file_name):
    with open(file_name, 'r', encoding='utf-8') as file_reader:
        main_file_content = file_reader.read()

        try:
            tree = ast.parse(main_file_content)
        except SyntaxError as e:
            print(e)
            tree = None

        return tree


def get_tree_with_file_name(file_name):
    with open(file_name, 'r', encoding='utf-8') as file_reader:
        main_file_content = file_reader.read()

        try:
            tree = ast.parse(main_file_content)
        except SyntaxError as e:
            print(e)
            tree = None

        return file_name, tree


def get_tree_with_file_content(file_name):
    with open(file_name, 'r', encoding='utf-8') as file_reader:
        main_file_content = file_reader.read()

        try:
            tree = ast.parse(main_file_content)
        except SyntaxError as e:
            print(e)
            tree = None

        return file_name, main_file_content, tree


def generate_trees_with_file_content(files):
    trees = []

    if len(files) > 0:
        for file_name in files:
            tree = get_tree_with_file_content(file_name)
            trees.append(tree)

        print('trees generated')

    return trees


def generate_trees_with_file_names(files):
    trees = []

    if len(files) > 0:
        for file_name in files:
            tree = get_tree_with_file_name(file_name)
            trees.append(tree)

        print('trees generated')

    return trees


def generate_trees(files):
    trees = []

    if len(files) > 0:
        for file_name in files:
            tree = get_tree(file_name)
            trees.append(tree)

        print('trees generated')

    return trees


def get_trees_with_file_names(os, path):
    files, files_count = extract_python_files_from_path(os, path)
    trees = generate_trees_with_file_names(files)
    return trees


def get_trees_with_file_content(os, path):
    files, files_count = extract_python_files_from_path(os, path)
    trees = generate_trees_with_file_content(files)
    return trees


def get_trees(os, path):
    files, files_count = extract_python_files_from_path(os, path)
    trees = generate_trees(files)
    return trees
