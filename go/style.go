package main

import "github.com/charmbracelet/lipgloss"

var thickRoundedBorder = lipgloss.Border {
	Top: "━",
	Bottom: "━",
	Left: "┃",
	Right: "┃",
	TopLeft: "╭",
	TopRight: "╮",
	BottomLeft: "╰",
	BottomRight: "╯",
}

var inputStyle = lipgloss.NewStyle().
	Border(thickRoundedBorder).
	Padding(0, 1).
	BorderForeground(lipgloss.Color("#2ac3de"))
