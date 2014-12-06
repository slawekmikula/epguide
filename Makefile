VERSION=1.9.2
PKG_NAME=epguide

egg:
	mkdir dist; \
	cd src; \
	python setup.py bdist_egg
	mv src/dist/*.egg dist

pypi:
	cd src; \
	python setup.py register

dist: clean
	mkdir dist; \
	tar -czf dist/${PKG_NAME}-${VERSION}.tar.gz src/* --transform s/src/${PKG_NAME}-${VERSION}/

clean:
	find . -depth -name *.pyc -type f -delete
	rm -rf ./src/build
	rm -rf ./src/dist

