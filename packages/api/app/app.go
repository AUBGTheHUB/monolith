package app

import (
	"hub-backend/configs"
	"hub-backend/routes"
	"log"

	"crypto/tls"

	"github.com/gofiber/fiber/v2"
	//fmt, encoding/json, strconv
)

func StartApp() {

	app := fiber.New()
	configs.ConnectDB()
	app.Use(configs.GenerateCORSConfig())
	routes.MembersRoute(app)
	routes.AdminRoute(app)
	routes.JobsRoute(app)
	routes.JuryRoute(app)
	routes.MentorsRoute(app)
	routes.SponsorsRoute(app)
	routes.PartnersRoute(app)
	configs.RunCronJobs()

	// ln -s ../../data/certs ./certs
	// volumes are taking care of this

	cer, err := tls.LoadX509KeyPair("certs/devenv.crt", "certs/devenv.key")

	if err != nil {
		// local development
		log.Fatal(app.Listen(":8000"))
	}

	config := &tls.Config{Certificates: []tls.Certificate{cer}}

	ln, err := tls.Listen("tcp", ":8000", config)
	if err != nil {
		panic(err)
	}

	log.Fatal(app.Listener(ln))
}
