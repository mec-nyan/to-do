// main.cpp

#include <notcurses/notcurses.h>
#include <string>
#include <vector>

int main() {

    struct notcurses_options opts{{}};
    opts.flags = NCOPTION_INHIBIT_SETLOCALE;

    struct notcurses* nc = notcurses_init(&opts, nullptr);
    if (not nc) {
        return 1;
    }

    struct ncplane* std_plane = notcurses_stdplane(nc);
    // ncplane_set_fg_rgb(std_plane, 0xFFFFFF);

    std::vector<std::string> todos;

    // Main loop.
    bool running{true};
    while (running) {
        ncplane_erase(std_plane);

        // 1. Set title.
        std::string title{"󰙏  My todos"};
        ncplane_printf_yx(std_plane, 1, 4, "%s", title.c_str());

        // 2. Todo list or help message.
        if (todos.empty()) {
            ncplane_printf_yx(std_plane, 3, 8, "Press 'i' to enter your first item.");
        } else {
            int y{3};
            for (auto& todo : todos) {
                ncplane_printf_yx(std_plane, y++, 8, "- %s", todo.c_str());
            }
        }

        // 3. Status line/help.
        uint height, width;
        ncplane_dim_yx(std_plane, &height, &width);
        ncplane_printf_yx(std_plane, height - 2, 4, "[ i ] Add - [ q ] Quit");

        // 4. Refresh.
        notcurses_render(nc);

        // 5. Handle input
        struct ncinput ni;
        uint input = notcurses_get_blocking(nc, &ni);
        if (input == 'q') {
            running = false;
        } else if (input == 'i') {
            // ...
        }
    }

    notcurses_stop(nc);

    return 0;
}
