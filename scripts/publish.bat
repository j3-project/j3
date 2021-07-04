rd /q /s dist
python setup.py sdist 
twine upload dist/*
