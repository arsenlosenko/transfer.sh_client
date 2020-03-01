.PHONY: upload
.PHONY: deps
.PHONY: clean
.PHONY: install
.PHONY: check

build:
	python setup.py sdist bdist_wheel

install:
	python setup.py install

upload:
	twine upload dist/*

check:
	twine check dist/*

deps:
	pip install -r requirements.txt

clean:
	rm -rf build dist *.egg-info
