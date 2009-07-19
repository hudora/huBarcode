build:
	python setup.py build

upload: build
	python setup.py sdist bdist_egg
	rsync -rvapP dist/* root@cybernetics.hudora.biz:/usr/local/www/data/dist/huBarcode/
	rsync -rvapP dist/* root@cybernetics.hudora.biz:/usr/local/www/data/nonpublic/eggs/

# publish:
# 	# remove development tag
# 	perl -npe 's/^tag_build = .dev/# tag_build = .dev/' -i setup.cfg
# 	svn commit
# 	python setup.py build sdist bdist_egg upload
# 	# add development tag
# 	perl -npe 's/^\# tag_build = .dev/tag_build = .dev/' -i setup.cfg
# 	rsync dist/* root@cybernetics.hudora.biz:/usr/local/www/apache22/data/dist/huDjango/
# 	echo "now bump version number in setup.py and commit"

install: build
	sudo python setup.py install
