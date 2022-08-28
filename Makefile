PACKAGE_DIR = $(shell pwd)/src
PACKAGE_NAME = splintershell
DECODER_SRC_DIR = decoders
DECODER_BIN_DIR = $(PACKAGE_DIR)/$(PACKAGE_NAME)/encoding/schemes/bin
export PACKAGE_NAME
export DECODER_BIN_DIR

all: fmt lint decoders package

fmt:
	isort $(PACKAGE_DIR)
	black $(PACKAGE_DIR)

lint:
	$(MAKE) -C $(PACKAGE_DIR)

decoders:
	mkdir -p $(DECODER_BIN_DIR)
	$(MAKE) -C $(DECODER_SRC_DIR)

package:
	python3 -m build

.PHONY: all fmt lint decoders package install clean

install: all
	pip install dist/*.whl

clean:
	rm -rf dist
	find . -type f -name *.bin -exec rm -rf {} \+ || true
	find . -type f -name *.o -exec rm -rf {} \+ || true
	find **/*.egg-info -type d -exec rm -rf {} \+ || true
	find . -type d -name .mypy_cache -exec rm -rf {} \+ || true
	find . -type d -name __pycache__ -exec rm -rf {} \+ || true
