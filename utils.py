
def isdigit_or_dot(s):
    return all([str.isdigit(c) or c == '.' for c in s])