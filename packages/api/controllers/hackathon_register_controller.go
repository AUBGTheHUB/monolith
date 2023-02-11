package controllers

import (
	"context"
	"hub-backend/models"
	"hub-backend/responses"
	"net/http"
	"time"

	"github.com/gofiber/fiber/v2"
	"go.mongodb.org/mongo-driver/bson"
)

func RegisterTeamMember(c *fiber.Ctx) error {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	var member models.TeamMember
	defer cancel()
	if *member.TeamNoTeam {
		cursor, _ := teamMembersCollection.Find(
			ctx, bson.D{{"teamname", member.TeamName}},
		)
		var results []models.TeamMember

		_ = cursor.All(ctx, &results)

		if len(results) > 0 {
			println(results)
		}
	}
	return c.Status(http.StatusCreated).JSON(responses.MemberResponse{Status: http.StatusCreated, Message: "success"})
}
