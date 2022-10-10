package main

import (
	"hub-backend/configs"
	"hub-backend/routes"
	"log"

	"github.com/gofiber/fiber/v2"
	"github.com/gofiber/fiber/v2/middleware/cors"
	// fmt, encoding/json, strconv
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
	log.Fatal(app.Listen(":8000"))
	configs.GenerateToken(32)
}
