"""utilities"""


def base_36_encode(number: int) -> str:
    """
    :param number: base 10 integer
    :return: base 36 string
    """

    encoded: str = ''
    while number > 0:
        number, remainder = divmod(number, 36)
        encoded = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'[remainder] + encoded

    return encoded
