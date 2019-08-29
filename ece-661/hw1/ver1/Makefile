CC=g++

EXEC=bin/hw1
SRC_C=hw1.cpp

CV_LINK=`pkg-config --cflags --libs opencv`
DEBUG=-D DEBUG
VAL=valgrind --leak-check=yes

INPUT_IMG=input/adams1.jpg
OUTPUT_IMG=results/adams1_fixed.jpg

$(EXEC) : $(SRC_C)
	$(CC) -o $(EXEC) $(SRC_C) $(CV_LINK)

test : $(EXEC) $(SRC_C)
	$(EXEC) $(INPUT_IMG) $(OUTPUT_IMG)

memtest: $(EXEC) $(SRC_C)
	$(VAL) $(EXEC) $(INPUT_IMG) $(OUTPUT_IMG)

noimg : $(EXEC) $(SRC_C)
	$(EXEC)

debug : $(EXEC) $(SRC_C)
	$(CC) -o $(EXEC) $(SRC_C) $(CV_LINK) $(DEBUG)

clean :
	rm $(EXEC)
