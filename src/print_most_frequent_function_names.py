import collections
import os
import sys

sys.path.append(os.path.dirname(__file__))

from src.utils import (
    get_word_counts,
    get_function_names,
    get_lowercase_function_names
)


def extract_most_frequent_functions_names(trees, frequency=10):
    function_names = get_function_names(trees,
                                        extractor_function=get_lowercase_function_names)
    return collections.Counter(function_names).most_common(frequency)


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
        extractor_function=extract_most_frequent_functions_names,
        frequency=words_frequency
    )
