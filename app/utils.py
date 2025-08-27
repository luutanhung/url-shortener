import string


def base62encode(num: int) -> str:
    chars = string.digits + string.ascii_letters
    if num == 0:
        return chars[0]
    base62 = []
    while num > 0:
        num, rem = divmod(num, 62)
        base62.append(chars[rem])
    return "".join(reversed(base62))


def base62decode(s: str) -> int:
    chars = string.digits + string.ascii_letters
    char_map = {char: i for i, char in enumerate(chars)}
    num = 0
    for char in s:
        num = num * 62 + char_map[char]
    return num
