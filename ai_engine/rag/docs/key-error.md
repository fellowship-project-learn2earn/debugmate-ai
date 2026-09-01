# KeyError
tags: keyerror, dictionary key

KeyError means code tried to access a dictionary key that doesn't exist. Fix by checking spelling/case of the key, printing dict.keys() to see what's actually there, or using dict.get(key, default) instead of dict[key] when the key might legitimately be missing.
