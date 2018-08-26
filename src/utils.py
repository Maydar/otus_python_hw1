import ast
import nltk
from nltk import pos_tag
from src.generate_trees import get_trees

nltk.download('averaged_perceptron_tagger')


def flat(list_object):
    """ [(1,2), (3,4)] -> [1, 2, 3, 4]"""
    return sum([list(item) for item in list_object], [])


def is_verb(word):
    if not word:
        return False
    pos_info = pos_tag([word])
    verb_tag = pos_info[0][1]
    return 'VB' in verb_tag


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


def get_words(os, project_list):
    words = []

    for project in project_list:
        path = os.path.join('../', project)
        trees = get_trees(os=os, path=path)
        print(trees)
        words += extract_all_words(trees)

    return words


def get_word_counts(os, project_list, extractor_function, frequency):
    word_counts = []
    for project in project_list:
        path = os.path.join('../', project)
        trees = get_trees(os=os, path=path)
        word_counts += extractor_function(trees, frequency)

    for word_count in word_counts:
        print(word_count[0], word_count[1])