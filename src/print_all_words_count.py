import os
import collections
import sys

sys.path.append(os.path.dirname(__file__))

from src.utils import get_words


def extract_count_of_words(os, project_list, frequency):
    words = get_words(os, project_list)

    total_count_of_words = len(words)
    unique_words = set(words)
    count_of_unique_words = len(unique_words)

    total_count_output = 'total count of words: {} '.format(total_count_of_words)
    unique_count_output = 'count of unique words {}'.format(count_of_unique_words)

    print(total_count_output)
    print(unique_count_output)

    word_counter = collections.Counter(words)
    mostly_used_words_in_range = word_counter.most_common(frequency)

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

    extract_count_of_words(
        os=os,
        project_list=projects,
        frequency=words_frequency
    )
