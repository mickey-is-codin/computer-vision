CC=g++

EXEC=bin/image-display
SRC_C=display_image.cpp

CV_LINK=`pkg-config --cflags --libs opencv`
DEBUG=-D DEBUG
VAL=valgrind --tool=memcheck --leak-check=yes --show-reachable=yes --num-callers=20

INPUT_IMG=input/addams.jpg

$(EXEC) : $(SRC_C)
	$(CC) -o $(EXEC) $(SRC_C) $(CV_LINK)

test : $(EXEC) $(SRC_C)
	$(EXEC) $(INPUT_IMG)

noimg : $(EXEC) $(SRC_C)
	$(EXEC)

memtest: $(EXEC) $(SRC_C)
	$(VAL) $(EXEC)

debug : $(EXEC) $(SRC_C)
	$(CC) -o $(EXEC) $(SRC_C) $(CV_LINK) $(DEBUG)

clean :
	rm $(EXEC)
