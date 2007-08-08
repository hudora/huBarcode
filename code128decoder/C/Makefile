
CFLAGS=-I/opt/local/include -L/opt/local/lib
all: barcode1 barcode2

% : %.c
	$(CC) $(CFLAGS) $(CPPFLAGS) -g $< -o $@ -ljpeg

