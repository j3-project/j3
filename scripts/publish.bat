rd /q /s dist
python setup.py sdist bdist bdist_wheel
twine upload dist/*
