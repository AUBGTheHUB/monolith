package routes

import (
	"hub-backend/controllers"

	"github.com/gofiber/fiber/v2"
)

func NoTeamParticipantsRoute(app *fiber.App) {
	// Participants without a team requests routes
	app.Get("/api/hackathon/participants_no_team", controllers.GetNoTeamParticipants)
	app.Post("/api/hackathon/participants_no_team", controllers.CreateNoTeamHackathonParticipant)
	app.Get("/api/hackathon/participants_no_team/:key", controllers.GetNoTeamParticipant)
	app.Put("/api/hackathon/participants_no_team/:key", controllers.EditNoTeamParticipant)
	app.Delete("/api/hackathon/participants_no_team/:key", controllers.DeleteNoTeamParticipant)
	app.Get("/api/hackathon/participants_no_team_count", controllers.GetNoTeamParticipantsCount)

}
