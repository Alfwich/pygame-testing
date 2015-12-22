CC = g++
OBJS = test_dll.cpp
OUTPUT = test_dll.dll test_dll.o
OUT_LIBS = libtest.a

all: $(OBJS)
	$(CC) -c $(OBJS)
	$(CC) -shared -o $(OUTPUT) -Wl,--out-implib,$(OUT_LIBS)
