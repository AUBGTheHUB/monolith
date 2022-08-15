package routes

import (
	"hub-backend/controllers"

	"github.com/gofiber/fiber/v2"
)

func SponsorsRoute(app *fiber.App) {
	app.Post("/api/sponsors", controllers.CreateSponsor)
	app.Get("/api/sponsors", controllers.GetAllSponsors)
	app.Get("/api/sponsors/:key", controllers.GetSponsor)
	app.Put("/api/sponsors/:key", controllers.EditSponsor)
	app.Delete("/api/sponsors/:key", controllers.DeleteSponsor)
}
