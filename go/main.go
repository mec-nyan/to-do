package main

import (
	"encoding/json"
	"fmt"
	"os"
	"strings"

	"github.com/charmbracelet/bubbles/textinput"
	tea "github.com/charmbracelet/bubbletea"
)

type mode int

const (
	modeList mode = iota
	modeInput

	dataFile = "todos.json"
)

func loadTodos() []string {
	data, err := os.ReadFile(dataFile)
	if err != nil {
		return []string{}
	}

	var todos []string
	if err := json.Unmarshal(data, &todos); err != nil {
		fmt.Println("Error loading todos:", err)
		return []string{}
	}

	return todos
}

func saveTodos(todos []string) {
	data, err := json.MarshalIndent(todos, "", "  ")
	if err != nil {
		fmt.Println("Error saving todos:", err)
		return
	}
	err = os.WriteFile(dataFile, data, 0644)
	if err != nil {
		fmt.Println("Error writing file:", err)
	}
}

type model struct {
	todos     []string
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
	ti.Width = 80

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
		return m, nil

	case tea.KeyMsg:
		switch m.mode {
		case modeList:
			switch msg.String() {
			case "i":
				m.mode = modeInput
				m.textInput.SetValue("")
				return m, textinput.Blink
			case "q":
				return m, tea.Quit
			}
		case modeInput:
			switch msg.Type {
			case tea.KeyEnter:
				if val := m.textInput.Value(); val != "" {
					m.todos = append(m.todos, val)
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
	s += "\n  \x1b[33m  \x1b[0mTodo List\n\n"

	// Items:
	if len(m.todos) == 0 {
		s += "\tNothing to see here \x1b[31m "
	} else {
		for i, todo := range m.todos {
			s += fmt.Sprintf("\t%3d - %s\n", i, todo)
		}
	}

	// Spacer:
	visibleLines := len(m.todos) + 3 // Header size.
	paddingLines := m.size.height - visibleLines - 2
	if paddingLines > 0 {
		s += strings.Repeat("\n", paddingLines)
	}

	// Footer:
	if m.mode == modeInput {
		s += m.textInput.View()
	} else {
		s += "  \x1b[32m[ i ] Add - [ q ] Quit"
	}

	return s
}

func main() {
	app := tea.NewProgram(initialModel(), tea.WithAltScreen())
	if _, err := app.Run(); err != nil {
		fmt.Println("Oops!:", err)
		os.Exit(1)
	}
}
