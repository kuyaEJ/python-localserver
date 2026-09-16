all:
	gcc -Wall -o test test.c
	gcc -Wall -o testc testclient.c
test:
	./test
	./testc
