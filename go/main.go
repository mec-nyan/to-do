package main

import (
	"fmt"
	"os"

	"github.com/charmbracelet/bubbles/textinput"
	tea "github.com/charmbracelet/bubbletea"
)

type mode int

const (
	modeList mode = iota
	modeInput
)

type model struct {
	todos     []string
	textInput textinput.Model
	mode      mode
}

func initialModel() model {
	ti := textinput.New()
	ti.Placeholder = "..."
	ti.Focus()
	ti.CharLimit = 200
	ti.Width = 80

	return model{
		todos:     []string{},
		textInput: ti,
		mode:      modeList,
	}
}

func (m model) Init() tea.Cmd {
	return nil
}

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	switch msg := msg.(type) {

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
	s := "  Todo List\n\n"
	if len(m.todos) == 0 {
		s += "\tNothing to see here  \n\n"
	} else {
		for i, todo := range m.todos {
			s += fmt.Sprintf("\t%3d - %s\n", i, todo)
		}
	}
	s += "\n"

	if m.mode == modeInput {
		s += m.textInput.View() + "\n"
	} else {
		s += "\n[ i ] Add - [ q ] Quit\n"
	}

	return s
}

func main() {
	app := tea.NewProgram(initialModel())
	if _, err := app.Run(); err != nil {
		fmt.Println("Oops!:", err)
		os.Exit(1)
	}
}
