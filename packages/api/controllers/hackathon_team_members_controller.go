package controllers

import (
	"context"
	"hub-backend/configs"
	"hub-backend/models"
	"hub-backend/responses"
	"net/http"
	"time"

	"github.com/go-playground/validator/v10"
	"github.com/gofiber/fiber/v2"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
)

var teamMembersCollection *mongo.Collection = configs.GetCollection(configs.DB, "hackathon_members")

var validateTeamMembers = validator.New()

func CreateHackathonMember(c *fiber.Ctx) error {
		ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	
		bearer_token := c.Get("BEARER-TOKEN")
	
		var member models.TeamMember
		defer cancel()
		if bearer_token != configs.ReturnAuthToken() {
			return c.Status(http.StatusUnauthorized).JSON(responses.MemberResponse{Status: http.StatusUnauthorized, Message: "error", Data: &fiber.Map{"Reason": "Authentication failed"}})
		}
	
		// validate request body
		if err := c.BodyParser(&member); err != nil {
			return c.Status(http.StatusBadRequest).JSON(responses.MemberResponse{Status: http.StatusBadRequest, Message: "error", Data: &fiber.Map{"data": err.Error()}})
		}
	
		if validationErr := validateTeamMembers.Struct(&member); validationErr != nil {
			return c.Status(http.StatusBadRequest).JSON(responses.MemberResponse{Status: http.StatusBadRequest, Message: "error", Data: &fiber.Map{"data": validationErr.Error()}})
		}
	
		newHackathonTeamMember := models.TeamMember{
			ID:                    member.ID,
			FullName:              member.FullName,
			TeamNoTeam:            member.TeamNoTeam,
			TeamName:              member.TeamName,
			Email:                 member.Email,
			School:                member.School,
			Age:                   member.Age,
			Location:              member.Location,
			HeardAboutUs:          member.HeardAboutUs,
			PreviousParticipation: member.PreviousParticipation,
			PartDetails:           member.PartDetails,
			Experience:            member.Experience,
			ProgrammingLevel:      member.ProgrammingLevel,
			StrongSides:           member.StrongSides,
			ShirtSize:             member.ShirtSize,
			Internship:            member.Internship,
			JobInterests:          member.JobInterests,
			SponsorShare:          member.SponsorShare,
			NewsLetter:            member.NewsLetter}
	
		result, err := teamMembersCollection.InsertOne(ctx, newHackathonTeamMember)
	
		if err != nil {
			return c.Status(http.StatusInternalServerError).JSON(responses.MemberResponse{Status: http.StatusInternalServerError, Message: "error", Data: &fiber.Map{"data": err.Error()}})
		}
	
		return c.Status(http.StatusCreated).JSON(responses.MemberResponse{Status: http.StatusCreated, Message: "success", Data: &fiber.Map{"data": result}})
	}

// func GetHackathonMember(c *fiber.Ctx) error {

// }

// func EditHackathonMember(c *fiber.Ctx) error {

// }

// func DeleteHackathonMember(c *fiber.Ctx) error {

// }

func GetHackathonMembersCount(c *fiber.Ctx) error {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	var countOfMembers int = 0

	defer cancel()

	results, err := teamMembersCollection.CountDocuments(ctx, bson.M{})

	if err != nil {
		return c.Status(http.StatusInternalServerError).JSON(responses.MemberResponse{Status: http.StatusInternalServerError, Message: "error", Data: &fiber.Map{"data": err.Error()}})
	}

	countOfMembers = int(results)

	return c.Status(http.StatusOK).JSON(
		responses.MemberResponse{Status: http.StatusOK, Message: "success", Data: &fiber.Map{"count_of_members": countOfMembers}},
	)

}
