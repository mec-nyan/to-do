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
