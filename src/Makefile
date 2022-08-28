MYPY = mypy
MYPY_FLAGS = --pretty --package

all: $(PACKAGE_NAME)

$(PACKAGE_NAME):
	$(MYPY) $(MYPY_FLAGS) $@

.PHONY: $(PACKAGE_NAME)
