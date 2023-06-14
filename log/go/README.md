# Instruction

## Note
This step work on version below:
- `npm`: 9.7.1
- `node`: v20.3.0

## Step by Step
1. create the project
```zsh
go mod init <URL/PATH>/log/go
```

2. create environment config and logger and main.go
```
touch config.go && touch logger.go
```

3. place this to config.js
```go
package main

import (
	"os"
)

type Config struct {
	ApiSecret string
	LogLevel  string
}

func LoadConfig() Config {
	// If want to use .env enable this
	// err := godotenv.Load()
	// if err != nil {
	// 	log.Fatal("Error loading .env file")
	// }

	return Config{
		ApiSecret: os.Getenv("API_SECRET"),
		LogLevel:  os.Getenv("LOG_LEVEL"),
	}
}
```

4. place this to logger.js
```go
package main

import (
	"strings"

	"github.com/sirupsen/logrus"
)

func ConfigureLogger(logger *logrus.Logger, logLevel string) {
	switch strings.ToLower(logLevel) {
	case "debug":
		logger.SetLevel(logrus.DebugLevel)
	case "info":
		logger.SetLevel(logrus.InfoLevel)
	case "warn":
		logger.SetLevel(logrus.WarnLevel)
	case "error":
		logger.SetLevel(logrus.ErrorLevel)
	case "fatal":
		logger.SetLevel(logrus.FatalLevel)
	case "panic":
		logger.SetLevel(logrus.PanicLevel)
	default:
		logger.SetLevel(logrus.InfoLevel)
	}
}
```

5. place this to main.go
```go
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
	logJSON, err := json.MarshalIndent(logMessage, "", "    ")
	// if you not want pretty json please use this
	// logJSON, err := json.Marshal(logMessage)

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

	log.Fatal(http.ListenAndServe(":8080", nil))
}
```

6. install dependencies
```zsh
go get github.com/joho/godotenv
go get github.com/sirupsen/logrus
```

7. build and run 
```
export LOG_LEVEL=debug
export API_SECRET=Jumpbox

go build -o app && ./app
```