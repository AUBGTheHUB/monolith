package routes

import (
	"hub-backend/controllers"

	"github.com/gofiber/fiber/v2"
)

func HackathonTeamMemberRoute(app *fiber.App) {
	// Hackathon members requests routes
	app.Post("/api/hackathon/members", controllers.CreateHackathonMember)
	app.Get("/api/hackathon/members/:key", controllers.GetHackathonMember)
	app.Put("/api/hackathon/members/:key", controllers.EditHackathonMember)
	app.Delete("/api/hackathon/members/:key", controllers.DeleteHackathonMember)
}
