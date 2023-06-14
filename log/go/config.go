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
