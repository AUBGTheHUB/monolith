package routes

import (
	"hub-backend/controllers"

	"github.com/gofiber/fiber/v2"
)

func HackathonRegisterRoutes(app *fiber.App){
	app.Post("/api/hackathon/register", controllers.RegisterTeamMember)
}
