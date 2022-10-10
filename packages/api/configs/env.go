package configs

import (
	"log"
	"os"

	"github.com/joho/godotenv"
)

var token string = "hubababuba"

func GenerateToken() string{
	random_string := "TOKEN"
	// implement logic for generating a rand 20 char string
	return random_string
}

func SetToken() string{
	token = 
}

func ReturnAuthToken() string {
	return token
}

func EnvMongoURI() string {
	err := godotenv.Load()
	if err != nil {
		log.Fatalf("Error loading .env file")
	}

	return os.Getenv("MONGOURI")
}


