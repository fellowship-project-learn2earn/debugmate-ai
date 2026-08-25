"""
Evaluation dataset -- Week 10 deliverable.

Real, common beginner errors paired with what a good answer should
contain. Used by evaluation.py to score analyze() output automatically.
"""

EVAL_CASES = [
    {
        "id": "case-1-nameerror",
        "language": "python",
        "code": "print(username)",
        "error": "NameError: name 'username' is not defined",
        "expected_error_type": "NameError",
        "expected_keywords": ["defined", "variable"],
    },
    {
        "id": "case-2-indexerror",
        "language": "python",
        "code": "items = [1, 2, 3]\nfor i in range(len(items) + 1):\n    print(items[i])",
        "error": "IndexError: list index out of range",
        "expected_error_type": "IndexError",
        "expected_keywords": ["index", "range", "length"],
    },
    {
        "id": "case-3-typeerror",
        "language": "python",
        "code": "age = 25\nprint('Age: ' + age)",
        "error": "TypeError: can only concatenate str (not \"int\") to str",
        "expected_error_type": "TypeError",
        "expected_keywords": ["type", "string", "int"],
    },
    {
        "id": "case-4-keyerror",
        "language": "python",
        "code": "user = {'name': 'Sam'}\nprint(user['age'])",
        "error": "KeyError: 'age'",
        "expected_error_type": "KeyError",
        "expected_keywords": ["key", "dictionary"],
    },
    {
        "id": "case-5-attributeerror-none",
        "language": "python",
        "code": "items = [3, 1, 2]\nresult = items.sort()\nprint(result.pop())",
        "error": "AttributeError: 'NoneType' object has no attribute 'pop'",
        "expected_error_type": "AttributeError",
        "expected_keywords": ["none", "sort"],
    },
    {
        "id": "case-6-modulenotfound",
        "language": "python",
        "code": "import requests\nresponse = requests.get('https://example.com')",
        "error": "ModuleNotFoundError: No module named 'requests'",
        "expected_error_type": "ModuleNotFoundError",
        "expected_keywords": ["install", "pip"],
    },
    {
        "id": "case-7-indentation",
        "language": "python",
        "code": "def greet(name):\nprint(f'Hello, {name}')",
        "error": "IndentationError: expected an indented block after function definition on line 1",
        "expected_error_type": "IndentationError",
        "expected_keywords": ["indent"],
    },
    {
        "id": "case-8-zerodivision",
        "language": "python",
        "code": "total = 10\ncount = 0\naverage = total / count",
        "error": "ZeroDivisionError: division by zero",
        "expected_error_type": "ZeroDivisionError",
        "expected_keywords": ["zero", "divide"],
    },
]
