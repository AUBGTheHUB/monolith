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
	Generates a random string with fixed length,
	which is then sent to the client to be used as a BEARER TOKEN
	when making API calls
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

func SetToken() {
	token = GenerateToken(32)
}

func EnvMongoURI() string {
	err := godotenv.Load()
	if err != nil {
		log.Fatalf("Error loading .env file")
	}

	return os.Getenv("MONGOURI")
}
