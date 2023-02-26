package controllers

import (
	"context"
	"hub-backend/configs"
	"hub-backend/models"
	"hub-backend/responses"
	"net/http"
	"reflect"
	"time"

	"github.com/gofiber/fiber/v2"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
	"go.mongodb.org/mongo-driver/mongo"
)

var hackathonTeamCollection *mongo.Collection = configs.GetCollection(configs.DB, "hackathonTeam")

func CreateHackathonTeam(c *fiber.Ctx) error {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)

	bearer_token := c.Get("BEARER-TOKEN")

	var team models.Team
	defer cancel()

	if bearer_token != configs.ReturnAuthToken() {
		return c.Status(http.StatusUnauthorized).JSON(responses.MemberResponse{Status: http.StatusUnauthorized, Message: "error", Data: &fiber.Map{"data": "Unauthorized"}})
	}

	if err := c.BodyParser(&team); err != nil {
		return c.Status(http.StatusBadRequest).JSON(responses.MemberResponse{Status: http.StatusBadRequest, Message: "error", Data: &fiber.Map{"data": err.Error()}})
	}

	if len(team.TeamMembers) == 0 {
		return c.Status(http.StatusBadRequest).JSON(responses.MemberResponse{Status: http.StatusBadRequest, Message: "error", Data: &fiber.Map{"data": "Empty team"}})
	}

	if validationErr := validate.Struct(&team); validationErr != nil {
		return c.Status(http.StatusBadRequest).JSON(responses.MemberResponse{Status: http.StatusBadRequest, Message: "error", Data: &fiber.Map{"data": validationErr.Error()}})
	}
	
	var oldTeam models.Team

	err := hackathonTeamCollection.FindOne(ctx, bson.M{"teamname": team.TeamName}).Decode(&oldTeam)
	if err == nil {
		return c.Status(http.StatusInternalServerError).JSON(responses.MemberResponse{Status: http.StatusInternalServerError, Message: "error", Data: &fiber.Map{"data": "Team already exists"}})
	}

	var checkTeamMembers models.TeamMember

	for i := 0; i < len(team.TeamMembers); i++ {
		key_from_hex, _ := primitive.ObjectIDFromHex(team.TeamMembers[i])
		err := teamMembersCollection.FindOne(ctx, bson.M{"_id": key_from_hex}).Decode(&checkTeamMembers)

		if err != nil {
			return c.Status(http.StatusInternalServerError).JSON(responses.MemberResponse{Status: http.StatusInternalServerError, Message: "error", Data: &fiber.Map{"data": "Team member with id "+team.TeamMembers[i]+" doesn't exist"}})
	}
	}

	result, err := hackathonTeamCollection.InsertOne(ctx, team)
	if err != nil {
		return c.Status(http.StatusInternalServerError).JSON(responses.MemberResponse{Status: http.StatusInternalServerError, Message: "error", Data: &fiber.Map{"data": err.Error()}})
	}

	return c.Status(http.StatusCreated).JSON(responses.MemberResponse{Status: http.StatusCreated, Message: "success", Data: &fiber.Map{"data": result}})
}

func GetHackathonTeams(c *fiber.Ctx) error {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)

	var teams []models.Team
	defer cancel()

	results, err := hackathonTeamCollection.Find(ctx, bson.M{})

	if err != nil {
		return c.Status(http.StatusInternalServerError).JSON(responses.MemberResponse{Status: http.StatusInternalServerError, Message: "error", Data: &fiber.Map{"data": err.Error()}})
	}

	defer results.Close(ctx)

	for results.Next(ctx) {
		var singleTeam models.Team
		if err = results.Decode(&singleTeam); err != nil {
			return c.Status(http.StatusInternalServerError).JSON(responses.MemberResponse{Status: http.StatusInternalServerError, Message: "error", Data: &fiber.Map{"data": err.Error()}})
		}

		teams = append(teams, singleTeam)
	}

	return c.Status(http.StatusOK).JSON(
		responses.MemberResponse{Status: http.StatusOK, Message: "success", Data: &fiber.Map{"data": teams}},
	)
}

func GetHackathonTeam(c *fiber.Ctx) error {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	hackathon_team_key := c.Params("key", "key was not provided")
	var team models.Team
	defer cancel()

	key_from_hex, _ := primitive.ObjectIDFromHex(hackathon_team_key)

	err := hackathonTeamCollection.FindOne(ctx, bson.M{"_id": key_from_hex}).Decode(&team)
	if err != nil {
		return c.Status(http.StatusInternalServerError).JSON(responses.MemberResponse{Status: http.StatusInternalServerError, Message: "error", Data: &fiber.Map{"data": err.Error() + "key: " + hackathon_team_key}})
	}
	// empty array of TeamMembers with length the same...
	// iterate over the TeamMembers in the Team object
	// 		save the found member in the empty array
	// set the array as a property in the Team object

	teamMembers := make([]models.TeamMember, len(team.TeamMembers))

	var displayTeamMembers models.TeamMember

	for i := 0; i < len(team.TeamMembers); i++ {
		key_from_hex, _ := primitive.ObjectIDFromHex(team.TeamMembers[i])
		_ = teamMembersCollection.FindOne(ctx, bson.M{"_id": key_from_hex}).Decode(&displayTeamMembers)
		teamMembers[i] = displayTeamMembers
	}

	newTeam := map[string]interface{}{
		"TeamName": team.TeamName,
		"TeamMembers": teamMembers,
	}

	
	return c.Status(http.StatusOK).JSON(responses.MemberResponse{Status: http.StatusOK, Message: "success", Data: &fiber.Map{"data": newTeam}})
}

func EditHackathonTeams(c *fiber.Ctx) error {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	hackathon_team_key := c.Params("key", "key was not provided")
	var team models.EditTeam

	bearer_token := c.Get("BEARER-TOKEN")
	defer cancel()

	if bearer_token != configs.ReturnAuthToken() {
		return c.Status(http.StatusUnauthorized).JSON(responses.MemberResponse{Status: http.StatusUnauthorized, Message: "error", Data: &fiber.Map{"data": "Unauthorized"}})
	}

	if err := c.BodyParser(&team); err != nil {
		return c.Status(http.StatusBadRequest).JSON(responses.MemberResponse{Status: http.StatusBadRequest, Message: "error", Data: &fiber.Map{"data": err.Error()}})
	}

	if validationErr := validate.Struct(&team); validationErr != nil {
		return c.Status(http.StatusBadRequest).JSON(responses.MemberResponse{Status: http.StatusBadRequest, Message: "error", Data: &fiber.Map{"data": validationErr.Error()}})
	}

	team_map := models.EditTeam{}

	if team.TeamName != "" {
		team_map.TeamName = team.TeamName
	}
	if len(team.TeamMembers) != 0 {
		team_map.TeamMembers = team.TeamMembers
	}

	update := bson.M{}
	v := reflect.ValueOf(team_map)
	typeOfS := v.Type()

	for i := 0; i < v.NumField(); i++ {
		update[typeOfS.Field(i).Name] = v.Field(i).Interface()
	}

	key_from_hex, _ := primitive.ObjectIDFromHex(hackathon_team_key)

	result, err := hackathonTeamCollection.UpdateOne(ctx, bson.M{"_id": key_from_hex}, bson.M{"$set": update})

	if err != nil {
		return c.Status(http.StatusInternalServerError).JSON(responses.MemberResponse{Status: http.StatusInternalServerError, Message: "error", Data: &fiber.Map{"data": err.Error()}})
	}

	if result.MatchedCount != 1 {
		return c.Status(http.StatusNotFound).JSON(responses.MemberResponse{Status: http.StatusNotFound, Message: "error", Data: &fiber.Map{"data": "Job not found"}})
	}

	return c.Status(http.StatusOK).JSON(responses.MemberResponse{Status: http.StatusOK, Message: "Updated!"})

}

func DeleteHackathonTeams(c *fiber.Ctx) error {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	hackathon_team_key := c.Params("key", "key was not provided")
	bearer_token := c.Get("BEARER-TOKEN")
	defer cancel()

	if bearer_token != configs.ReturnAuthToken() {
		return c.Status(http.StatusUnauthorized).JSON(responses.MemberResponse{Status: http.StatusUnauthorized, Message: "error", Data: &fiber.Map{"Reason": "Authentication failed!"}})
	}

	key_from_hex, _ := primitive.ObjectIDFromHex(hackathon_team_key)

	result, err := hackathonTeamCollection.DeleteOne(ctx, bson.M{"_id": key_from_hex})

	if err != nil {
		return c.Status(http.StatusInternalServerError).JSON(responses.MemberResponse{Status: http.StatusInternalServerError, Message: "error", Data: &fiber.Map{"data": err.Error()}})
	}

	if result.DeletedCount < 1 {
		return c.Status(http.StatusNotFound).JSON(responses.MemberResponse{Status: http.StatusNotFound, Message: "error", Data: &fiber.Map{"Reason": "Team not found!"}})
	}

	return c.Status(http.StatusOK).JSON(responses.MemberResponse{Status: http.StatusOK, Message: "Team successfully deleted!"})
}
