CC=g++

EXEC=bin/make-bw
SRC_C=make_bw.cpp

CV_LINK=`pkg-config --cflags --libs opencv`
DEBUG=-D DEBUG
VAL=valgrind --leak-check=yes

INPUT_IMG=input/iris.jpg

$(EXEC) : $(SRC_C)
	$(CC) -o $(EXEC) $(SRC_C) $(CV_LINK)

test : $(EXEC) $(SRC_C)
	$(EXEC) $(INPUT_IMG)

memtest: $(EXEC) $(SRC_C)
	$(VAL) $(EXEC) $(INPUT_IMG)

noimg : $(EXEC) $(SRC_C)
	$(EXEC)

debug : $(EXEC) $(SRC_C)
	$(CC) -o $(EXEC) $(SRC_C) $(CV_LINK) $(DEBUG)

clean :
	rm $(EXEC)
