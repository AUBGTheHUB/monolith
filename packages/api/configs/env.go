package configs

import (
	"log"
	"math/rand"
	"os"
	"time"

	"github.com/joho/godotenv"
)

var token string = GenerateToken(32)

/*
Generates a random string with fixed length
*/
func GenerateToken(lengthOfToken int) string {

	rand.Seed(time.Now().UnixNano())

	var chars = []rune("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0987654321!@#$%^&*()_+-=~?><:{}[]|")
	str := make([]rune, lengthOfToken)
	for i := range str {
		str[i] = chars[rand.Intn(len(chars))]
	}

	return string(str)
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
