package configs

import (
	"fmt"
	"strings"

	"github.com/gofiber/fiber/v2"
	"github.com/gofiber/fiber/v2/middleware/cors"
)

func GenerateCORSConfig() func(*fiber.Ctx) error {
	config := cors.ConfigDefault

	config.AllowOrigins = GenerateOrigins()
	return cors.New(config)
}

func GenerateOrigins() string {
	ALLOWED_LOCALHOST_PROTOCOLS := []string{"http", "https"}
	ALLOWED_LOCALHOST_DOMAINS := []string{"localhost", "127.0.0.1"}
	ALLOWED_LOCALHOST_PORTS := []string{"3000", "3001", "6969"}
	ALLOWED_PUBLIC_DOMAINS := []string{
		"https://dev.thehub-aubg.com",
		"https://thehub-aubg.com",
	}

	var origins []string

	for _, protocol := range ALLOWED_LOCALHOST_PROTOCOLS {
		for _, domain := range ALLOWED_LOCALHOST_DOMAINS {
			for _, port := range ALLOWED_LOCALHOST_PORTS {
				origin := fmt.Sprintf("%s://%s:%s", protocol, domain, port)
				origins = append(origins, origin)
			}
		}
	}

	origins = append(origins, ALLOWED_PUBLIC_DOMAINS...)

	return strings.Join(origins, ",")
}
