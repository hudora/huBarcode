build:
	python setup.py build

upload: build
	python setup.py sdist bdist_egg
	rsync -rvapP dist/* root@cybernetics.hudora.biz:/usr/local/www/data/dist/huBarcode/
	rsync -rvapP dist/* root@cybernetics.hudora.biz:/usr/local/www/data/nonpublic/eggs/

publish: upload
	# remove development tag
	python setup.py build sdist bdist_egg upload

install: build
	sudo python setup.py install
