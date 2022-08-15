package routes

import (
	"hub-backend/controllers"

	"github.com/gofiber/fiber/v2"
)

func JobsRoute(app *fiber.App) {
	// validate Admin
	app.Post("/api/job", controllers.CreateJob)
	app.Get("/api/job", controllers.GetAllJobs)
	app.Get("/api/job/:key", controllers.GetJob)
	app.Delete("/api/job/:key", controllers.DeleteJob)
	app.Put("/api/job/:key", controllers.EditJob)

}
