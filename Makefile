VERSION=1.4.3
PKG_NAME=epguide

egg:
	cd src; \
	python setup.py bdist_egg

pypi:
	cd src; \
	python setup.py register

dist: clean
	cd src; \
	mkdir dist; \
	tar -czf dist/${PKG_NAME}-${VERSION}.tar.gz *

clean:
	rm -rf *.pyc
	rm -rf ./src/build
	rm -rf ./src/dist

