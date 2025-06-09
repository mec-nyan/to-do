// v2.cpp

#include <ncpp/NotCurses.hh>
#include <print>

auto main() -> int {

    ncpp::NotCurses nc;

    uint height, width;
    auto std_plane = nc.get_stdplane(&height, &width);

    std_plane->putstr(0, 0, "Press any key to quit.");
    nc.render();

    nc.get(true);

	std::string msg{"Are you sure?"};
	uint msg_pad = 4;

    const uint box_h = 5;
    const uint box_w = msg.size() + msg_pad * 2;
    const uint box_x = (width - box_w) / 2;
    const uint box_y = (height - box_h) / 2;

    ncpp::Plane box(box_h, box_w, box_y, box_x, 0, &nc);

    ncpp::Cell ul, ur, ll, lr, hl, vl;
    nccell_load(box, ul, "╭");
    nccell_load(box, ur, "╮");
    nccell_load(box, ll, "╰");
    nccell_load(box, lr, "╯");
    nccell_load(box, hl, "━");
    nccell_load(box, vl, "┃");

	ul.set_fg_rgb8(0x7a, 0xa2, 0xf7);
	ur.set_fg_rgb8(0x2a, 0xc3, 0xde);
	ll.set_fg_rgb8(0x7a, 0xa2, 0xf7);
	lr.set_fg_rgb8(0x2a, 0xc3, 0xde);
	vl.set_fg_default();
	hl.set_fg_default();
	ul.set_bg_default();
	ur.set_bg_default();
	ll.set_bg_default();
	lr.set_bg_default();
	vl.set_bg_default();
	hl.set_bg_default();

    uint ctlword = NCBOXGRAD_TOP | NCBOXGRAD_BOTTOM | NCBOXGRAD_LEFT | NCBOXGRAD_RIGHT;
    box.perimeter(ul, ur, ll, lr, hl, vl, ctlword);

    box.putstr(2, msg_pad, "Are you sure?");

    nc.render();
    nc.get(true);

    nc.stop();

    return 0;
}
