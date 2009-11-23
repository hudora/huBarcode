# setting the PATH seems only to work in GNUmake not in BSDmake
PATH := ./testenv/bin:$(PATH)

default: dependencies check test

hudson: clean dependencies test statistics
	find barcodeserver -name '*.py' | xargs /usr/local/hudorakit/bin/hd_pep8
	/usr/local/hudorakit/bin/hd_pylint -f parseable barcodeserver | tee pylint.out

check:
	-find barcodeserver -name '*.py' | xargs /usr/local/hudorakit/bin/hd_pep8
	-/usr/local/hudorakit/bin/hd_pylint barcodeserver

test:
	python manage.py test --verbosity=1 barcodeserver

dependencies:
	virtualenv testenv
	pip -q install -E testenv -r requirements.txt
	# the following line is needed for Django applications
	# sh -c 'echo p | svn co https://cybernetics.hudora.biz/intern/svn/code/projects/html/trunk/templates generic_templates'

statistics:
	sloccount --wide --details barcodeserver > sloccount.sc

build:
	python setup.py build sdist

upload: build
	rsync dist/* root@cybernetics.hudora.biz:/usr/local/www/apache22/data/nonpublic/eggs/

install: build
	sudo python setup.py install

runserver: dependencies
	python manage.py runserver

clean:
	rm -Rf testenv build dist html test.db sloccount.sc pylint.out
	find . -name '*.pyc' -or -name '*.pyo' -delete

.PHONY: test build clean install upload check statistics dependencies
