import ast
import os
import collections

from nltk import pos_tag


FREQUENCY_OF_WORDS = 200
PROJECT_LIST = [
    'django',
    'flask',
    'pyramid',
    'reddit',
    'requests',
    'sqlalchemy',
]


def flat(list_object):
    """ [(1,2), (3,4)] -> [1, 2, 3, 4]"""
    return sum([list(item) for item in list_object], [])


def is_verb(word):
    if not word:
        return False
    pos_info = pos_tag([word])
    return pos_info[0][1] == 'VB'


def extract_python_files_from_path(os, path, max_length=100):
    files = []
    for dir_name, dirs, files in os.walk(path, topdown=True):
        for file in files:
            if not file.endswith('.py'):
                continue

            if len(files) > max_length:
                break

            file_path = os.path.join(dir_name, file)
            files.append(file_path)

    files_count = len(files)

    print('total {} files'.format(files_count))

    return files, files_count


def generate_trees(files, with_file_names=False, with_file_content=False):
    trees = []

    for file_name in files:
        with open(file_name, 'r', encoding='utf-8') as file_reader:
            main_file_content = file_reader.read()

            try:
                tree = ast.parse(main_file_content)
            except SyntaxError as e:
                print(e)
                tree = None

            if with_file_names:
                if with_file_content:
                    trees.append((file_name, main_file_content, tree))
                else:
                    trees.append((file_name, tree))
            else:
                trees.append(tree)

    print('trees generated')

    return trees


def get_trees(path, with_file_names=False, with_file_content=False):
    files, files_count = extract_python_files_from_path(os, path, max_length=100)
    trees = generate_trees(files,
                           with_file_names=with_file_names,
                           with_file_content=with_file_content)
    return trees


def get_lowercase_function_names(trees):
    lowercase_node_names = []

    for tree in trees:
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                lowercase_node_names.append(node.name.lower())

    return flat(lowercase_node_names)


def get_all_function_names_from_tree(tree):
    return [node.id for node in ast.walk(tree) if isinstance(node, ast.Name)]


def filter_doubleslash_names(function_names):
    names = []
    for node_name in function_names:
        without_end_double_underscore = not node_name.endswith('__')
        without_start_double_underscore = not node_name.startswith('__')

        if without_end_double_underscore or without_start_double_underscore:
            names.append(node_name)
    return names


def get_function_names(trees, extractor_function):
    function_names = extractor_function(trees)
    filtered_function_names = filter_doubleslash_names(function_names)

    return filtered_function_names


def get_verbs_from_function_name(function_name):
    function_name_splits = function_name.split('_')
    return [word for word in function_name_splits if is_verb(word)]


def split_snake_case_name_to_words(name):
    name_splits = name.split('_')
    return [split for split in name_splits if split]


def extract_all_words(trees):
    function_names = get_function_names(trees,
                                        extractor_function=get_all_function_names_from_tree)

    formatted_function_names = []

    for function_name in function_names:
        formatted_function_name = split_snake_case_name_to_words(function_name)
        formatted_function_names.append(formatted_function_name)

    return flat(formatted_function_names)


def extract_most_frequent_verbs(trees, frequency=10):
    function_names = get_function_names(trees,
                                        extractor_function=get_lowercase_function_names)

    verbs = []

    for function_name in function_names:
        verb_list = get_verbs_from_function_name(function_name)
        verbs.append(verb_list)

    flatten_verbs = flat(verbs)

    return collections.Counter(flatten_verbs).most_common(frequency)


def extract_most_frequent_functions_names(trees, frequency=10):
    function_names = get_function_names(trees,
                                        extractor_function=get_lowercase_function_names)
    return collections.Counter(function_names).most_common(frequency)


def get_mostly_used_verbs_from_projects(os, project_list, extractor_function):
    words = []
    for project in project_list:
        path = os.path.join('.', project)
        trees = get_trees(path)
        words += extractor_function(trees)
    return words


if __name__ == "__main__":
    mostly_used_words = get_mostly_used_verbs_from_projects(
        os=os,
        project_list=PROJECT_LIST,
        extractor_function=extract_most_frequent_verbs
    )
    total_count_of_words = len(mostly_used_words)
    unique_words = set(mostly_used_words)

    total_count_output = 'total count of words: {} '.format(total_count_of_words)
    unique_count_output = 'count of unique words {}'.format(unique_words)

    print(total_count_of_words)
    print(unique_count_output)

    word_counter = collections.Counter(mostly_used_words)
    mostly_used_words_in_range = word_counter.most_common(FREQUENCY_OF_WORDS)

    for word, occurrence in mostly_used_words_in_range:
        print(word, occurrence)
