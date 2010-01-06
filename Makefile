build:
	python setup.py build

upload: build
	python setup.py sdist bdist_egg

publish: upload
	# remove development tag
	python setup.py build sdist bdist_egg upload

install: build
	sudo python setup.py install
