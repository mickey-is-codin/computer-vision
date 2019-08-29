EXEC=ocv
SRC_C=opencv_test.cpp

OCV_LINKER=`pkg-config --cflags --libs opencv`

CC=g++

$(EXEC) : $(SRC_C)
	$(CC) $(SRC_C) $(OCV_LINKER) -o $(EXEC)
