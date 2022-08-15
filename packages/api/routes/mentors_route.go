package routes

import (
	"hub-backend/controllers"

	"github.com/gofiber/fiber/v2"
)

func MentorsRoute(app *fiber.App) {
	// club members requests routes
	app.Post("/api/mentors", controllers.CreateMentor)
	app.Get("/api/mentors", controllers.GetAllMentors)
	app.Get("/api/mentors/:key", controllers.GetMentor)
	app.Put("/api/mentors/:key", controllers.EditMentor)
	app.Delete("/api/mentors/:key", controllers.DeleteMentor)
}
