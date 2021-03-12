import os


def check_import_order():
    os.system("isort --check ./special_students/ --skip __init__.py --gitignore --dont-follow-links --verbose")


def check_code_formatting():
    os.system("black --check ./special_students/ --exclude __init__.py --verbose")


def sort_import_order():
    os.system("isort ./special_students/ ./tests/ --skip __init__.py --gitignore --dont-follow-links --verbose")


def do_code_formatting():
    os.system("black ./special_students/ ./tests/ --exclude __init__.py --verbose")


def linter():
    os.system("pylama ./special_students/ ./tests/")


def run_tests():
    os.system("pytest ./tests/ --verbose --color=yes --code-highlight=yes")
