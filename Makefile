.PHONY: test examples release-to-pypi

test:
	pytest

examples:
	env PYTHONPATH=. python3 examples/call.py
	env PYTHONPATH=. python3 examples/pool.py
	env PYTHONPATH=. python3 examples/output.py

release-to-pypi:
	python3 setup.py sdist
	python3 setup.py bdist_wheel --universal
	twine upload dist/*
