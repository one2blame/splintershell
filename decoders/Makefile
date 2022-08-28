CC = x86_64-linux-gnu-gcc
CFLAGS = -m64 -c -Wall -o
OBJCOPY = x86_64-linux-gnu-objcopy
OBJCOPYFLAGS = --strip-all --output-target=binary --only-section=.text
SOURCES = $(wildcard *.S)
BINARIES = $(SOURCES:.S=.bin)

all: $(BINARIES)

%.o: %.S
	$(CC) $(CFLAGS) $@ $<

$(BINARIES): %.bin: %.o
	$(OBJCOPY) $(OBJCOPYFLAGS) $< $@
	cp $@ $(DECODER_BIN_DIR)

.PHONY: $(BINARIES)
