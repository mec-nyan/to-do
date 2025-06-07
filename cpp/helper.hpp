#include <notcurses/notcurses.h>

inline void center_plane(ncplane* box, ncplane* std_plane) {
    uint std_y, std_x, box_y, box_x;
    ncplane_dim_yx(std_plane, &std_y, &std_x);
    ncplane_dim_yx(box, &box_y, &box_x);
    ncplane_move_yx(box, (std_y - box_y) / 2, (std_x - box_x) / 2);
}

inline void rounded_border(ncplane* box) {
    uint64_t chan{0};
    ncchannels_set_fg_rgb(&chan, 0x7aa2f7);

    nccell ul, ur, bl, br, hl, vl;

    ul = NCCELL_INITIALIZER(0, 0, chan);
    ur = NCCELL_INITIALIZER(0, 0, chan);
    bl = NCCELL_INITIALIZER(0, 0, chan);
    br = NCCELL_INITIALIZER(0, 0, chan);
    hl = NCCELL_INITIALIZER(0, 0, chan);
    vl = NCCELL_INITIALIZER(0, 0, chan);

    nccell_load(box, &ul, "╭");
    nccell_load(box, &ur, "╮");
    nccell_load(box, &bl, "╰");
    nccell_load(box, &br, "╯");
    nccell_load(box, &hl, "━");
    nccell_load(box, &vl, "┃");

    uint height, width;
    ncplane_dim_yx(box, &height, &width);
    ncplane_box(box, &ul, &ur, &bl, &br, &hl, &vl, height - 1, width - 1, 0);
}

inline void rounded_border_grad(ncplane* box) {

    uint64_t chan_ul, chan_ur, chan_bl, chan_br;

    ncchannels_set_fg_rgb(&chan_ul, 0x7aa2f7);
    ncchannels_set_fg_rgb(&chan_bl, 0x7aa2f7);
    ncchannels_set_fg_rgb(&chan_ur, 0x2ac3de);
    ncchannels_set_fg_rgb(&chan_br, 0x2ac3de);

    ncchannels_set_bg_default(&chan_ul);
    ncchannels_set_bg_default(&chan_ur);
    ncchannels_set_bg_default(&chan_bl);
    ncchannels_set_bg_default(&chan_br);

    nccell ul, ur, bl, br, hl, vl;

    ul = NCCELL_INITIALIZER(0, 0, chan_ul);
    ur = NCCELL_INITIALIZER(0, 0, chan_ur);
    bl = NCCELL_INITIALIZER(0, 0, chan_bl);
    br = NCCELL_INITIALIZER(0, 0, chan_br);
    hl = NCCELL_INITIALIZER(0, 0, 0);
    vl = NCCELL_INITIALIZER(0, 0, 0);

    nccell_load(box, &ul, "╭");
    nccell_load(box, &ur, "╮");
    nccell_load(box, &bl, "╰");
    nccell_load(box, &br, "╯");
    nccell_load(box, &hl, "━");
    nccell_load(box, &vl, "┃");

    uint height, width;
    ncplane_dim_yx(box, &height, &width);

    uint ctlw = NCBOXGRAD_TOP | NCBOXGRAD_BOTTOM | NCBOXGRAD_LEFT | NCBOXGRAD_RIGHT;

    ncplane_box(box, &ul, &ur, &bl, &br, &hl, &vl, height - 1, width - 1, ctlw);
}
