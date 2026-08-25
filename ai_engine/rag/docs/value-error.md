# ValueError
tags: valueerror, invalid literal

ValueError means a function received an argument of the right type but an inappropriate value -- classically, int('abc') fails because 'abc' isn't a valid number even though it's a string. Fix by validating or checking input before conversion, and wrapping risky conversions in a try/except when the input isn't guaranteed to be well-formed.
