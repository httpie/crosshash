default: list-tasks

clean:
	rm -rf dist/ tests/.pytest_cache/ node_modules/
	find . -name '__pycache__' -delete -print -o -name '*.pyc' -delete -print

test:
	poetry run pytest tests/tests.py

install: install-py install-js

release: release-py release-js

install-py:
	poetry --version || python3 -m pip install poetry
	poetry env use python3.11
	poetry install

install-js:
	npm install

release-py:
	poetry build
	poetry run twine upload --verbose --repository=crosshash dist/*

release-js:
	npm publish

# Default task to get a list of tasks when `make' is run without args.
# <https://stackoverflow.com/questions/4219255>
list-tasks:
	@echo Available tasks:
	@echo ----------------
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'
	@echo

