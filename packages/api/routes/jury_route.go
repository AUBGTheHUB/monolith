package routes

import (
	"hub-backend/controllers"

	"github.com/gofiber/fiber/v2"
)

func JuryRoute(app *fiber.App) {
	app.Post("/api/jury", controllers.CreateJury)
	app.Put("/api/jury/:key", controllers.EditJury)
	app.Get("/api/jury/:key", controllers.GetJury)
	app.Get("/api/jury", controllers.GetAllJury)
	app.Delete("/api/jury/:key", controllers.DeleteJury)
}
