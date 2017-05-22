def is_member(user, group):
    return user.groups.filter(name=group).exists()


def is_in_multiple_groups(user):
    return user.groups.filter(name__in=['group1', 'group2']).exists()


def month_string_to_number(string):
    m = {
        'jan':1,
        'feb':2,
        'mar':3,
        'apr':4,
        'may':5,
        'jun':6,
        'jul':7,
        'aug':8,
        'sep':9,
        'oct':10,
        'nov':11,
        'dec':12
    }
    s = string.strip()[:3].lower()
    try:
        out = m[s]
        return out
    except:
        raise ValueError('Not a month')

