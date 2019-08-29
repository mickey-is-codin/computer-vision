CC=g++

EXEC=display-image
SRC_C=display_image.cpp

CV_LINK=`pkg-config --cflags --libs opencv`

$(EXEC) : $(SRC_C)
	$(CC) -o $(EXEC) $(SRC_C) $(CV_LINK)
