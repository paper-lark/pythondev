.PHONY: init freeze check format

init:
	echo "#!/usr/bin/env bash\npoetry run black --check ." > .git/hooks/pre-commit
	chmod 755 .git/hooks/pre-commit
