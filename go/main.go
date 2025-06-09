package main

import (
	"fmt"
	"os"

	tea "github.com/charmbracelet/bubbletea"
)

const (
	minWidth = 80
	minHeight = 40
)

func main() {
	app := tea.NewProgram(initialModel(), tea.WithAltScreen())
	if _, err := app.Run(); err != nil {
		fmt.Println("Oops!:", err)
		os.Exit(1)
	}
}
