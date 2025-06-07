IN = main.cpp
OUT = main.o
COMPILER_FLAGS = -std=c++17 -lnotcurses -lnotcurses-core -Wall -Werror -Wpedantic \
    -I/opt/homebrew/include \
    -I/opt/homebrew/opt/ncurses/include

$(OUT): $(IN)
	@clang++ $(COMPILER_FLAGS) -o $(OUT) $(IN)

run: $(OUT)
	@if [ -e ./$(OUT) ]; then ./$(OUT); fi

clean:
	@if [ -e ./$(OUT) ]; then rm ./$(OUT); fi
