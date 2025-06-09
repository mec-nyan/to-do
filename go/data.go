package main

import (
	"encoding/json"
	"fmt"
	"os"
)

const	dataFile = "todos.json"

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
