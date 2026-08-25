# NameError
tags: nameerror, not defined, undefined variable

NameError happens when Python encounters a name (variable or function) it hasn't seen defined yet in the current scope. Common causes: the variable is misspelled, it was defined inside a function/if-block and isn't visible outside it, or it's used before the line that creates it. Fix by checking spelling exactly (Python is case-sensitive), and tracing execution order top-to-bottom to confirm the variable exists before the line that uses it.
