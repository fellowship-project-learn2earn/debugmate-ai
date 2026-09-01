# AttributeError
tags: attributeerror, has no attribute, nonetype

AttributeError means code tried to use a method or property that doesn't exist on that object -- often because the object is actually None (a very common cause: forgetting that a function like list.sort() or list.append() returns None, not the list itself), or because of a typo in the method name. Fix by printing type(x) and checking what x actually is right before the failing line.
