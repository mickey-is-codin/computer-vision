CC=g++

EXEC=bin/image-display
SRC_C=display_image.cpp

CV_LINK=`pkg-config --cflags --libs opencv`
DEBUG=-D DEBUG

INPUT_IMG=input/addams.jpg

$(EXEC) : $(SRC_C)
	$(CC) -o $(EXEC) $(SRC_C) $(CV_LINK)

test : $(EXEC) $(SRC_C)
	$(EXEC) $(INPUT_IMG)

noimg : $(EXEC) $(SRC_C)
	$(EXEC)

debug : $(SRC_C)
	$(CC) -o $(EXEC) $(SRC_C) $(CV_LINK) $(DEBUG)

clean :
	rm $(EXEC)
