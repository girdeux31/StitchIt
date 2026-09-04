.ONESHELL:
.DEFAULT_GOAL := help

project_name := stitchit

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

.PHONY: help
help:  ## Show help
	@python3 -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

.PHONY: build
build: clean  ## Build package (source and wheel)
	@python3 -m build

.PHONY: upload-test
upload-test:  ## Upload package to test-pypi, remove it first if package already in test-pypi
	@python3 -m twine upload --verbose --repository testpypi dist/*

.PHONY: upload
.ONESHELL:
upload:  ## Upload package to real pypi
	@read -p "Did you have the correct version and configuration? press y/n: " key; \
	if [ "$$key" = "y" ] || [ "$$key" = "Y" ]; then \
		python3 -m twine upload --verbose dist/*; \
	else \
		echo "Aborted."; \
		exit 1; \
	fi

.PHONY: clean
clean:  ## Clean trash
	@rm -rf "dist"
	@rm -rf "src/${project_name}.egg-info"
	
.PHONE: all
all: build upload clean  ## Generate package, upload to real pypi and clean

