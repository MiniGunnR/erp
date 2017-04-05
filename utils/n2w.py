def _num_in_words(num):
    stack = {
        0: 'zero',
        1: 'one',
        2: 'two',
        3: 'three',
        4: 'four',
        5: 'five',
        6: 'six',
        7: 'seven',
        8: 'eight',
        9: 'nine',
        10: 'ten',
        11: 'eleven',
        12: 'twelve',
        13: 'thirteen',
        14: 'fourteen',
        15: 'fifteen',
        16: 'sixteen',
        17: 'seventeen',
        18: 'eighteen',
        19: 'nineteen',
        20: 'twenty',

        30: 'thirty',
        40: 'forty',
        50: 'fifty',
        60: 'sixty',
        70: 'seventy',
        80: 'eighty',
        90: 'ninety'
    }
    try:
        return stack[num]
    except KeyError:
        tens = num // 10
        ones = num % 10
        joint = "{tens}{ones}".format(tens=stack[tens * 10], ones=stack[ones])
        return joint


def _len_in_words(num):
    d = {}

    crore_hundred = num // 1000000000
    d['crore_hundred'] = crore_hundred
    num %= 1000000000

    crore = num // 10000000
    d['crore'] = crore
    num %= 10000000

    lakh = num // 100000
    d['lakh'] = lakh
    num %= 100000

    thousand = num // 1000
    d['thousand'] = thousand
    num %= 1000

    hundred = num // 100
    d['hundred'] = hundred
    num %= 100

    d['ten'] = num

    return d


def final(num):
    num = int(round(num))
    arr = _len_in_words(num)
    word = ""

    if "crore_hundred" in arr and arr['crore_hundred'] != 0:
        word += _num_in_words(arr['crore_hundred']) + " hundred "
    if "crore" in arr and arr['crore'] != 0:
        word += _num_in_words(arr['crore']) + " crore "
    if "lakh" in arr and arr['lakh'] != 0:
        word += _num_in_words(arr['lakh']) + " lakh "
    if "thousand" in arr and arr['thousand'] != 0:
        word += _num_in_words(arr['thousand']) + " thousand "
    if "hundred" in arr and arr['hundred'] != 0:
        word += _num_in_words(arr['hundred']) + " hundred "
    if "ten" in arr and arr['ten'] != 0:
        word += "and "
    if "ten" in arr and arr['ten'] != 0:
        word += _num_in_words(arr['ten'])

    if word[-1:] == " ":
        word += "only"
    else:
        word += " only"

    return word

