# These targets are not files
.PHONY: contribute travis test lint coverage

test:
	pep8 --ignore E128,E201,E202 --max-line-length=120 --exclude='migrations' .
