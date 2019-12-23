from subprocess import check_call

def test():
    check_call(["python3", "tests/test_api.py"])

def publish():
    check_call(["python3", "setup.py", "bdist_wheel", "sdist"])
    check_call(["twine", "upload", "--skip-existing", "dist/*"])