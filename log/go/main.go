package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"time"

	"github.com/sirupsen/logrus"
)

// Define your log format
type LogFormat struct {
	Timestamp string      `json:"timestamp"`
	Message   string      `json:"message"`
	Level     string      `json:"level"`
	Service   string      `json:"service"`
	MetaData  interface{} `json:"meta_data"`
	Data      interface{} `json:"data"`
}

// Setup Logrus
var logger = logrus.New()

func handler(w http.ResponseWriter, r *http.Request, config Config) {
	// Get secret from Config
	apiSecret := config.ApiSecret

	// Your log message
	logMessage := LogFormat{
		Timestamp: time.Now().Format(time.RFC3339),
		Message:   "Secret is: " + apiSecret,
		Level:     "INFO",
		Service:   "web-api",
		MetaData: map[string]string{
			"user_name": "JoJo",
			"user_id":   "C168",
		},
		Data: map[string]string{
			"key_1": "value",
			"key_2": "value-2",
			"key_3": "value-3",
		},
	}

	// Convert struct to JSON
	// pretty JSON
	// logJSON, err := json.MarshalIndent(logMessage, "", "    ")
	// if you not want pretty json please use this
	logJSON, err := json.Marshal(logMessage)

	if err != nil {
		log.Println(err)
		return
	}

	// Log to console
	fmt.Println(string(logJSON))
	logger.Debug("Debug message")
	logger.Error("Error message")

	// Response to client
	w.Header().Set("Content-Type", "application/json")
	w.Write(logJSON)
}

func main() {
	// Load configuration
	config := LoadConfig()

	// Configure logger
	ConfigureLogger(logger, config.LogLevel)

	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		handler(w, r, config)
	})
	fmt.Println("ready started server on 0.0.0.0:8080, url: http://localhost:8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
