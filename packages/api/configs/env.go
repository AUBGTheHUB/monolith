package configs

import (
	"log"
	"math/rand"
	"os"
	"time"

	"github.com/joho/godotenv"
)

var token string = SetToken()

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

func IsTestENV() bool {
	godotenv.Load()
	return os.Getenv("IS_TEST") == "true"
}

func SetToken() string {
	godotenv.Load()
	var token string

	if os.Getenv("IS_TEST") == "true" {
		token = "TEST_TOKEN"
	} else if os.Getenv("IS_OFFLINE") == "true" {
		token = "OFFLINE_TOKEN"
	} else {
		token = GenerateToken(32)
	}

	return token
}

func EnvMongoURI() string {
	godotenv.Load()
	return os.Getenv("MONGOURI")
}
