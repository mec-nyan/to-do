package main

import (
	"fmt"
	"strings"

	"github.com/charmbracelet/bubbles/textinput"
	tea "github.com/charmbracelet/bubbletea"
	"github.com/charmbracelet/lipgloss"
)

type mode int

const (
	modeList mode = iota
	modeInput
)

type todo struct {
	Name    string `json:"name"`
	Checked bool   `json:"checked"`
}

type model struct {
	todos     []todo
	current   uint
	textInput textinput.Model
	mode      mode
	size      struct {
		width, height int
	}
}

func initialModel() model {
	ti := textinput.New()
	ti.Placeholder = "..."
	ti.Focus()
	ti.CharLimit = 200
	ti.Width = 70

	return model{
		todos:     loadTodos(),
		textInput: ti,
		mode:      modeList,
	}
}

func (m model) Init() tea.Cmd {
	return nil
}

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	switch msg := msg.(type) {

	case tea.WindowSizeMsg:
		m.size.width = msg.Width
		m.size.height = msg.Height

		if msg.Width < minWidth || msg.Height < minHeight {
			return m, tea.Quit
		}
		return m, nil

	case tea.KeyMsg:
		switch m.mode {
		case modeList:
			switch msg.String() {
			case "i":
				m.mode = modeInput
				m.textInput.SetValue("")
				return m, textinput.Blink
			// TODO: Add case for <esc>
			case "q":
				return m, tea.Quit
			case "j", "n":
				if m.current+1 < uint(len(m.todos)) {
					m.current++
				}
			case "k", "p":
				if m.current > 0 {
					m.current--
				}
			case " ", "\n":
				m.todos[m.current].Checked = !m.todos[m.current].Checked
				saveTodos(m.todos)
			// TODO: Add backspace, delete, etc.
			case "x":
				m.todos = append(m.todos[:m.current], m.todos[m.current+1:]...)
				saveTodos(m.todos)
			}

		case modeInput:
			switch msg.Type {
			case tea.KeyEnter:
				if val := m.textInput.Value(); val != "" {
					m.todos = append(m.todos, todo{Name: val})
					saveTodos(m.todos)
				}
				m.mode = modeList
				return m, nil
			case tea.KeyEsc:
				m.mode = modeList
				return m, nil
			}
		}
		if m.mode == modeInput {
			var cmd tea.Cmd
			m.textInput, cmd = m.textInput.Update(msg)
			return m, cmd
		}
	}

	return m, nil
}

func (m model) View() string {
	var s string

	// Header:
	header := "Todo List"
	header += lipgloss.NewStyle().Foreground(lipgloss.Color("#e0af68")).Render("  ")
	s += "\n"
	s += lipgloss.NewStyle().
		Align(lipgloss.Center).
		Width(m.size.width).
		Render(header)

	s += "\n\n"

	// Items:
	if len(m.todos) == 0 {
		s += "\tNothing to see here \x1b[31m "
	} else {
		for i, todo := range m.todos {
			if todo.Checked {
				s += lipgloss.NewStyle().Foreground(lipgloss.Color("#2ac3de")).Render("  󰱒 ")
			} else {
				s += lipgloss.NewStyle().Foreground(lipgloss.Color("#545c7e")).Render("  󰄱 ")
			}
			item := fmt.Sprintf("%2d  %s", i, todo.Name)
			if i == int(m.current) {
				s += lipgloss.NewStyle().Foreground(lipgloss.Color("#7aa2f7")).Render(item)
			} else {
				s += item
			}
			s += "\n"
		}
	}

	// Spacer:
	visibleLines := len(m.todos) + 3 // Header size.
	paddingLines := m.size.height - visibleLines - 5
	if paddingLines > 0 {
		s += strings.Repeat("\n", paddingLines)
	}

	footer := "[ i ] New item - [ q ] Quit"
	// Footer:
	if m.mode == modeInput {
		s += m.inputStyle().Render(m.textInput.View()) + "\n"
		footer = "[ Enter ] Add item - [ Escape ] Discard"
	} else {
		s += "\n\n\n"
	}
	s += "\n"

	s += lipgloss.NewStyle().Align(lipgloss.Center).
		Foreground(lipgloss.Color("#7aa2f7")).
		Width(m.size.width).Render(footer)

	return s
}

func (m model) inputStyle() lipgloss.Style {
	// TODO: Fix this magic "70".
	marginLeft := (m.size.width - 72) / 2
	if marginLeft < 0 {
		marginLeft = 0
	}

	return lipgloss.NewStyle().
		Border(thickRoundedBorder).
		Padding(0, 1).
		BorderForeground(lipgloss.Color("#2ac3de")).
		Width(72).
		MarginLeft(marginLeft)
}
