package controllers

import (
	"context"
	"hub-backend/configs"
	"hub-backend/responses"
	"net/http"
	"time"

	"github.com/go-playground/validator/v10"
	"github.com/gofiber/fiber/v2"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
)

var teamMembersCollection *mongo.Collection = configs.GetCollection(configs.DB, "hackathon_team_members")

var validateTeamMembers = validator.New()

// func CreateHackathonMember(c *fiber.Ctx) error {

// }

// func GetHackathonMember(c *fiber.Ctx) error {

// }

// func EditHackathonMember(c *fiber.Ctx) error {

// }

// func DeleteHackathonMember(c *fiber.Ctx) error {

// }

func GetHackathonMembersCount(c *fiber.Ctx) error {
	var membersCollection *mongo.Collection = configs.GetCollection(configs.DB, "hackathon_members")

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	var countOfMembers int = 0

	defer cancel()

	results, err := membersCollection.CountDocuments(ctx, bson.M{})

	if err != nil {
		return c.Status(http.StatusInternalServerError).JSON(responses.MemberResponse{Status: http.StatusInternalServerError, Message: "error", Data: &fiber.Map{"data": err.Error()}})
	}

	countOfMembers = int(results)

	return c.Status(http.StatusOK).JSON(
		responses.MemberResponse{Status: http.StatusOK, Message: "success", Data: &fiber.Map{"count_of_members": countOfMembers}},
	)

}
