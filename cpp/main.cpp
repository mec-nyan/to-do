// main.cpp

#include "helper.hpp"
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
        if (input == 'q' or input == NCKEY_ESC) {
            running = false;
        } else if (input == 'i') {
            uint box_w = 40, box_h = 5;
            struct ncplane_options popts = {
                .rows = box_h,
                .cols = box_w,
                .y = static_cast<int>((height - box_h) / 2),
                .x = static_cast<int>((width - box_w) / 2),
                .name = "input_box",
            };

            ncplane* box = ncplane_create(std_plane, &popts);

            ncplane_printf_yx(box, 1, 2, "Add: ");
            notcurses_render(nc);

            std::string buffer;
            bool inserting = true;

            while (inserting) {
                ncplane_erase_region(box, 2, 2, 1, box_w - 4);
                ncplane_printf_yx(box, 2, 2, "%s", buffer.c_str());
                notcurses_render(nc);

                struct ncinput ni;
                int ch = notcurses_get_blocking(nc, &ni);

                if (ch == NCKEY_ESC) {
                    inserting = false;
                } else if (ch == NCKEY_ENTER or ch == '\n') {
                    if (not buffer.empty()) {
                        todos.push_back(buffer);
                    }
                    inserting = false;
                } else if (ch == NCKEY_BACKSPACE or ch == 127 or ch == '\b') {
                    if (not buffer.empty())
                        buffer.pop_back();
                } else if (ch >= 32 and ch < 127) {
                    buffer.push_back((char)ch);
                }
            }

            ncplane_destroy(box);
        }
    }

    notcurses_stop(nc);

    return 0;
}
