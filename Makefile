.PHONY: init freeze check format

init:
	python3 -m venv venv
	source venv/bin/activate && pip install -r requirements.txt
	echo "#!/usr/bin/env bash\nmake check" > .git/hooks/pre-commit
	chmod 755 .git/hooks/pre-commit

freeze:
	pip freeze > requirements.txt

check:
	source venv/bin/activate && python -m black --check .

format:
	source venv/bin/activate && python -m black .
