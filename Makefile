build:
	python setup.py build

upload: build
	python setup.py sdist bdist_egg

publish: upload
	# remove development tag
	python setup.py build sdist bdist_egg upload

install: build
	sudo python setup.py install

check:
	-pyflakes hubarcode/ examples/
	# PEP8 scheitert and den QR-code Tabellen.
	-pep8 -r --ignore=E501 hubarcode/ean13/ hubarcode/datamatrix/ hubarcode/code128/ examples/
	-pylint -iy --max-line-length=110 -d E1101 hubarcode/ean13/ hubarcode/datamatrix/ hubarcode/code128/ examples/ examples/

test: testenv
	PYTHONPATH=.:./hubarcode python examples/code128.py TESTTEXT
	PYTHONPATH=.:./hubarcode python test/test_coverage.py

.PHONY: test testenv
