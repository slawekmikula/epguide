VERSION=1.3
PKG_NAME=epguide

egg:
	python ./src/setup.py bdist_egg

pypi:
	python ./src/setup.py register

dist:
	tar -czf ${PKG_NAME}-${VERSION}.tar.gz src/*

clean:
	rm -rf *.pyc
