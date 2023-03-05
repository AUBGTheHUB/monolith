package controllers

import (
	"context"
	"hub-backend/configs"
	"hub-backend/models"
	"hub-backend/responses"
	"net/http"
	"reflect"
	"strings"
	"time"

	"github.com/go-playground/validator/v10"
	"github.com/gofiber/fiber/v2"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
	"go.mongodb.org/mongo-driver/mongo"
)

var noTeamParticipantsCollection *mongo.Collection = configs.GetCollection(configs.DB, "noTeamParticipants")

var validateNoTeamParticipants = validator.New()

func CreateNoTeamHackathonParticipant(c *fiber.Ctx) error {

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

	if validationErr := validateNoTeamParticipants.Struct(&member); validationErr != nil {
		return c.Status(http.StatusBadRequest).JSON(responses.MemberResponse{Status: http.StatusBadRequest, Message: "error", Data: &fiber.Map{"data": validationErr.Error()}})
	}

	newNoTeamParticipant := models.TeamMember{
		FullName:              member.FullName,
		TeamNoTeam:            member.TeamNoTeam,
		TeamName:              member.TeamName,
		Email:                 member.Email,
		School:                member.School,
		Age:                   member.Age,
		Location:              member.Location,
		HeardAboutUs:          member.HeardAboutUs,
		PreviousParticipation: member.PreviousParticipation,
		Experience:            member.Experience,
		ProgrammingLevel:      member.ProgrammingLevel,
		StrongSides:           member.StrongSides,
		ShirtSize:             member.ShirtSize,
		Internship:            member.Internship,
		JobInterests:          member.JobInterests,
		SponsorShare:          member.SponsorShare,
		NewsLetter:            member.NewsLetter}

	if CheckIfNoTeamParticipantExists(newNoTeamParticipant) {
		return c.Status(http.StatusBadRequest).JSON(responses.MemberResponse{Status: http.StatusBadRequest, Message: "This email is already present in the DB", Data: &fiber.Map{"data": newNoTeamParticipant.Email}})
	}

	result, err := noTeamParticipantsCollection.InsertOne(ctx, newNoTeamParticipant)

	if err != nil {
		return c.Status(http.StatusInternalServerError).JSON(responses.MemberResponse{Status: http.StatusInternalServerError, Message: "error", Data: &fiber.Map{"data": err.Error()}})
	}

	return c.Status(http.StatusCreated).JSON(responses.MemberResponse{Status: http.StatusCreated, Message: "success", Data: &fiber.Map{"data": result}})

}

func GetNoTeamParticipant(c *fiber.Ctx) error {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	member_key := c.Params("key", "key was not provided")

	bearer_token := c.Get("BEARER-TOKEN")

	var member models.TeamMember
	defer cancel()

	if bearer_token != configs.ReturnAuthToken() {
		return c.Status(http.StatusUnauthorized).JSON(responses.MemberResponse{Status: http.StatusUnauthorized, Message: "error", Data: &fiber.Map{"Reason": "Authentication failed"}})
	}

	key_from_hex, _ := primitive.ObjectIDFromHex(member_key)
	err := noTeamParticipantsCollection.FindOne(ctx, bson.M{"_id": key_from_hex}).Decode(&member)
	if err != nil {
		return c.Status(http.StatusInternalServerError).JSON(responses.MemberResponse{Status: http.StatusInternalServerError, Message: "error", Data: &fiber.Map{"data": err.Error() + "key: " + member_key}})
	}
	return c.Status(http.StatusOK).JSON(responses.MemberResponse{Status: http.StatusOK, Message: "success", Data: &fiber.Map{"data": member}})
}

func EditNoTeamParticipant(c *fiber.Ctx) error {

	//TODO: Maybe change message if body is only of non-existings fields
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	member_key := c.Params("key", "key was not provided")
	var member models.EditTeamMember
	defer cancel()
	var member_map models.EditTeamMember
	key_from_hex, _ := primitive.ObjectIDFromHex(member_key)
	err1 := noTeamParticipantsCollection.FindOne(ctx, bson.M{"_id": key_from_hex}).Decode(&member_map)

	if err1 != nil {
		return c.Status(http.StatusNotFound).JSON(responses.MemberResponse{Status: http.StatusNotFound, Message: "No such memb"})
	}
	bearer_token := c.Get("BEARER-TOKEN")

	defer cancel()
	if bearer_token != configs.ReturnAuthToken() {
		return c.Status(http.StatusUnauthorized).JSON(responses.MemberResponse{Status: http.StatusUnauthorized, Message: "error", Data: &fiber.Map{"Reason": "Authentication failed"}})
	}

	if err := c.BodyParser(&member); err != nil {
		return c.Status(http.StatusBadRequest).JSON(responses.MemberResponse{Status: http.StatusBadRequest, Message: "Empty Body"})
	}

	if validationErr := validateNoTeamParticipants.Struct(&member); validationErr != nil {
		return c.Status(http.StatusBadRequest).JSON(responses.MemberResponse{Status: http.StatusBadRequest, Message: "Body is not compatible"})
	}

	if member.FullName != "" {
		member_map.FullName = member.FullName
	}
	if member.TeamNoTeam {
		member_map.TeamNoTeam = member.TeamNoTeam
	}
	if member.TeamName != "" {
		member_map.TeamName = member.TeamName
	}
	if member.Email != "" {
		member_map.Email = member.Email
	}
	if member.School != "" {
		member_map.School = member.School
	}
	if member.Age != 0 {
		member_map.Age = member.Age
	}
	if member.Location != "" {
		member_map.Location = member.Location
	}
	if member.ShirtSize != "" {
		member_map.ShirtSize = member.ShirtSize
	}

	update := bson.M{}
	v := reflect.ValueOf(member_map)
	typeOfS := v.Type()

	for i := 0; i < v.NumField(); i++ {
		update[strings.ToLower(typeOfS.Field(i).Name)] = v.Field(i).Interface()
	}

	result, err := noTeamParticipantsCollection.UpdateOne(ctx, bson.M{"_id": key_from_hex}, bson.M{"$set": update})

	if err != nil {
		return c.Status(http.StatusInternalServerError).JSON(responses.MemberResponse{Status: http.StatusInternalServerError, Message: err.Error()})
	}

	if result.MatchedCount != 1 {
		return c.Status(http.StatusNotFound).JSON(responses.MemberResponse{Status: http.StatusNotFound, Message: "Document not found"})
	}

	return c.Status(http.StatusOK).JSON(responses.MemberResponse{Status: http.StatusOK, Message: "User was updated"})

}

func DeleteNoTeamParticipant(c *fiber.Ctx) error {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	member_key := c.Params("key", "key was not provided")
	bearer_token := c.Get("BEARER-TOKEN")
	defer cancel()

	if bearer_token != configs.ReturnAuthToken() {
		return c.Status(http.StatusUnauthorized).JSON(responses.MemberResponse{Status: http.StatusUnauthorized, Message: "error", Data: &fiber.Map{"Reason": "Authentication failed"}})
	}

	key_from_hex, _ := primitive.ObjectIDFromHex(member_key)

	result, err := noTeamParticipantsCollection.DeleteOne(ctx, bson.M{"_id": key_from_hex})
	if err != nil {
		return c.Status(http.StatusInternalServerError).JSON(responses.MemberResponse{Status: http.StatusInternalServerError, Message: "Error", Data: &fiber.Map{"Reason": err.Error(), "Key": member_key}})
	}

	if result.DeletedCount < 1 {
		return c.Status(http.StatusNotFound).JSON(
			responses.MemberResponse{Status: http.StatusNotFound, Message: "error", Data: &fiber.Map{"data": "User with specified ID not found!"}},
		)
	}

	return c.Status(http.StatusOK).JSON(
		responses.MemberResponse{Status: http.StatusOK, Message: "success", Data: &fiber.Map{"data": "User successfully deleted!"}},
	)
}

func GetNoTeamParticipantsCount(c *fiber.Ctx) error {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	var countOfNoTeamParticipants int = 0
	bearer_token := c.Get("BEARER-TOKEN")

	defer cancel()

	if bearer_token != configs.ReturnAuthToken() {
		return c.Status(http.StatusUnauthorized).JSON(responses.MemberResponse{Status: http.StatusUnauthorized, Message: "error", Data: &fiber.Map{"Reason": "Authentication failed"}})
	}

	results, err := noTeamParticipantsCollection.CountDocuments(ctx, bson.M{})

	if err != nil {
		return c.Status(http.StatusInternalServerError).JSON(responses.MemberResponse{Status: http.StatusInternalServerError, Message: "error", Data: &fiber.Map{"data": err.Error()}})
	}

	countOfNoTeamParticipants = int(results)

	return c.Status(http.StatusOK).JSON(
		responses.MemberResponse{Status: http.StatusOK, Message: "success", Data: &fiber.Map{"count_of_members_without_team": countOfNoTeamParticipants}},
	)

}
func CheckIfNoTeamParticipantExists(newNoTeamParticipant models.TeamMember) bool {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()
	cursor, _ := noTeamParticipantsCollection.Find(
		ctx,
		bson.D{{"email", newNoTeamParticipant.Email}},
	)
	var results []models.TeamMember

	_ = cursor.All(ctx, &results)

	return len(results) > 0
}
