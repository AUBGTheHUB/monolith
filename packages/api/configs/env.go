package configs

import (
	"log"
	"math/rand"
	"os"
	"time"

	"github.com/joho/godotenv"
)

var token string = GenerateToken(32)

func GenerateToken(n int) string {
	rand.Seed(time.Now().UnixNano())

	random_string := "TOKEN"
	// implement logic for generating a rand 20 char string

	var chars = []rune("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0987654321")
	str := make([]rune, n)
	for i := range str {
		str[i] = chars[rand.Intn(len(chars))]
	}

	random_string = string(str)
	return random_string
}

func SetToken() {
	token = GenerateToken(32)
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
