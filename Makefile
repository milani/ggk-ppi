CC = g++
CFLAGS = -g -std=c++11
 
ggk: ggk.cpp
	$(CC) $(CFLAGS) -o $@ $^

orca: orca.cpp
	$(CC) $(CFLAGS) -o $@ $^

.PHONY: clean
clean:
	rm -f ggk ggk.o
	rm -f orca orca.o
