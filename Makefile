.PHONY: upload
.PHONY: deps
.PHONY: clean
.PHONY: install

build:
	python setup.py sdist bdist_wheel

install:
	python setup.py install

upload:
	twine upload dist/*

deps:
	pip install -r requirements.txt

clean:
	rm -rf build dist *.egg-info
