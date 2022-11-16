package main

import (
	"hub-backend/configs"
	"hub-backend/routes"
	"log"

	"crypto/tls"

	"github.com/gofiber/fiber/v2"
	"github.com/gofiber/fiber/v2/middleware/cors"
	//fmt, encoding/json, strconv
)

func main() {

	app := fiber.New()
	configs.ConnectDB()
	app.Use(cors.New(cors.ConfigDefault))
	routes.MembersRoute(app)
	routes.AdminRoute(app)
	routes.EventsRoute(app)
	routes.JobsRoute(app)
	routes.ArticlesRoutes(app)
	routes.JuryRoute(app)
	routes.MentorsRoute(app)
	routes.SponsorsRoute(app)
	routes.PartnersRoute(app)
	configs.RunCronJobs()

	// ln -s ../../data/certs ./certs

	cer, err := tls.LoadX509KeyPair("certs/devenv.crt", "certs/devenv.key")
	if err != nil {
		log.Fatal(err)
	}

	config := &tls.Config{Certificates: []tls.Certificate{cer}}

	// Create custom listener
	ln, err := tls.Listen("tcp", ":8000", config)
	if err != nil {
		panic(err)
	}

	// Start server with https/ssl enabled on http://localhost:443
	log.Fatal(app.Listener(ln))
}
