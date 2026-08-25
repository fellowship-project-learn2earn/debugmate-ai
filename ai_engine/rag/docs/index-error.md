# IndexError
tags: indexerror, list index out of range, index out of range

IndexError ('list index out of range') means code tried to access a position in a list/tuple/string that doesn't exist -- often off-by-one (using len(x) instead of len(x)-1, or looping one step too far). Fix by printing len(x) before the access, and double-checking loop bounds (range(len(x)) is usually correct, range(len(x)+1) is a common bug).
