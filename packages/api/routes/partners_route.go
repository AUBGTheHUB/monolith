package routes

import (
	"hub-backend/controllers"

	"github.com/gofiber/fiber/v2"
)

func PartnersRoute(app *fiber.App) {
	app.Post("/api/partners", controllers.CreatePartner)
	app.Get("/api/partners", controllers.GetAllPartners)
	app.Get("/api/partners/:key", controllers.GetPartner)
	app.Put("/api/partners/:key", controllers.EditPartner)
	app.Delete("/api/partners/:key", controllers.DeletePartner)
}
