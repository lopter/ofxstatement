all: bin/ofxstatement

.venv:
	virtualenv -p python3 --no-site-packages .venv

bin/buildout: .venv
	.venv/bin/python bootstrap.py
	touch bin/buildout

bin/ofxstatement: bin/buildout buildout.cfg setup.py
	./bin/buildout
	./bin/python setup.py develop
	touch bin/ofxstatement

.PHONY: coverage
coverage: bin/ofxstatement
	./bin/coverage run --source=src/ofxstatement ./bin/test
	./bin/coverage report