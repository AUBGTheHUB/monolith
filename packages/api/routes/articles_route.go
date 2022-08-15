package routes

import (
	"hub-backend/controllers"

	"github.com/gofiber/fiber/v2"
)

func ArticlesRoutes(app *fiber.App) {
	app.Post("/api/article", controllers.CreateArticle)
	app.Get("/api/article", controllers.GetAllArticles)
	app.Put("/api/article/:key", controllers.EditArticle)
	app.Get("/api/article/:key", controllers.GetArticle)
	app.Delete("/api/article/:key", controllers.DeleteArticle)
}
