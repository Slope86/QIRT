r"""Find the index of nth substring in a string.

This module contains a function to find the index of the nth occurrence of a substring in a string.
"""


def find_nth_substring(string: str, sub_string: str, n: int) -> int:
    """Find the index of nth substring in a string.

    Example:
        >>> find_nth_substring('123abcabcabc', 'abc', 2)
        6

    Args:
    ----
        string (str): The string to search.
        sub_string (str): The substring to search for.
        n (int): The nth substring to find.

    Returns:
        int: The index of the nth substring. Returns -1 if the nth substring is not found.

    """
    sub_string_index = string.find(sub_string)
    while sub_string_index >= 0 and n > 1:
        sub_string_index = string.find(sub_string, sub_string_index + len(sub_string))
        n -= 1
    return sub_string_index


if __name__ == "__main__":
    print(find_nth_substring("123abcabcabc", "abc", 2))
