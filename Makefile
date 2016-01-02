# Unit-testing, docs, etc.

VIRTUALENV?=virtualenv

TEST?=nosetests
PEP8?=pep8
PROJECT_DIR=.


run: clean
	./scripts/run.sh


env: clean system_deps
	rm -fr env
	$(VIRTUALENV) --no-site-packages env
	./scripts/install_dependencies.sh development
	@echo "\n\n>> Run 'source env/bin/activate'"


deps: clean system_deps
	mkdir -p .download_cache
	./scripts/install_dependencies.sh development


system_deps:
	./scripts/install_system_dependencies.sh


separate_review:
	python scripts/separator.py


clean:
	find . -name "*.pyc" -exec rm -rf {} \;
	@echo "done"


bootstrap: clean env
	@echo "done"


pep8:
	$(PEP8) --ignore=E501 --exclude='' -r .


.PHONY: all env pip deps pep8 clean bootstrap