import ast
import os
import collections

import nltk
from nltk import pos_tag

nltk.download('averaged_perceptron_tagger')


def flat(list_object):
    """ [(1,2), (3,4)] -> [1, 2, 3, 4]"""
    return sum([list(item) for item in list_object], [])


def is_verb(word):
    verb_tags = ['VB', 'VBZ', 'VBN', 'VBG', 'VBD', 'VBP']
    if not word:
        return False
    pos_info = pos_tag([word])
    verb_tag = pos_info[0][1]
    return verb_tag in verb_tags


def extract_python_files_from_path(os, path):
    file_names = []
    for dir_name, dirs, files in os.walk(path, topdown=True):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(dir_name, file)
                file_names.append(file_path)

    files_count = len(file_names)

    print('total {} files'.format(files_count))

    return file_names, files_count


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

    return lowercase_node_names


def get_all_names_from_tree(trees):
    function_names = []

    for tree in trees:
        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                function_names.append(node.id)

    return function_names


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
    names = get_function_names(trees,
                               extractor_function=get_all_names_from_tree)

    formatted_names = []

    for name in names:
        formatted_name = split_snake_case_name_to_words(name)
        formatted_names.append(formatted_name)

    return flat(formatted_names)


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


def get_word_counts(os, project_list, extractor_function):
    word_counts = []
    for project in project_list:
        path = os.path.join('.', project)
        trees = get_trees(path)
        word_counts += extractor_function(trees)

    for word_count in word_counts:
        print(word_count[0], word_count[1])


def get_all_words_statistics(os, project_list):
    words = []

    for project in project_list:
        path = os.path.join('.', project)
        trees = get_trees(path)
        words += extract_all_words(trees)

    total_count_of_words = len(words)
    unique_words = set(words)
    count_of_unique_words = len(unique_words)

    total_count_output = 'total count of words: {} '.format(total_count_of_words)
    unique_count_output = 'count of unique words {}'.format(count_of_unique_words)

    print(total_count_output)
    print(unique_count_output)

    word_counter = collections.Counter(words)
    mostly_used_words_in_range = word_counter.most_common(words_frequency)

    for word, occurrence in mostly_used_words_in_range:
        print(word, occurrence)


if __name__ == "__main__":

    words_frequency = 200
    projects = [
        'django',
        'flask',
        'pyramid',
        'reddit',
        'requests',
        'sqlalchemy',
    ]

    get_word_counts(
        os=os,
        project_list=projects,
        extractor_function=extract_most_frequent_verbs
    )

    get_word_counts(
        os=os,
        project_list=projects,
        extractor_function=extract_most_frequent_functions_names
    )

    get_all_words_statistics(
        os=os,
        project_list=projects
    )
