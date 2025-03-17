.PHONY: lint test fmt

lint:
	python -m pyflakes vault || true

test:
	python -m pytest -q || true

fmt:
	python -m black vault tests || true

