import collections
import os
import sys

sys.path.append(os.path.dirname(__file__))

from src.utils import (
    get_word_counts,
    get_verbs_from_function_name,
    get_function_names,
    get_lowercase_function_names,
    flat
)


def extract_most_frequent_verbs(trees, frequency=10):
    function_names = get_function_names(trees,
                                        extractor_function=get_lowercase_function_names)

    verbs = []

    for function_name in function_names:
        verb_list = get_verbs_from_function_name(function_name)
        verbs.append(verb_list)

    flatten_verbs = flat(verbs)

    return collections.Counter(flatten_verbs).most_common(frequency)


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
        extractor_function=extract_most_frequent_verbs,
        frequency=words_frequency
    )
