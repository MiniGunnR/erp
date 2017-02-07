def is_member(user, group):
    return user.groups.filter(name=group).exists()


def is_in_multiple_groups(user):
    return user.groups.filter(name__in=['group1', 'group2']).exists()

