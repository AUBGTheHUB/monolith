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

	var no_team_participant models.TeamMember
	defer cancel()

	if bearer_token != configs.ReturnAuthToken() {
		return c.Status(http.StatusUnauthorized).JSON(responses.MemberResponse{Status: http.StatusUnauthorized, Message: "error", Data: &fiber.Map{"Reason": "Authentication failed"}})
	}

	// validate request body
	if err := c.BodyParser(&no_team_participant); err != nil {
		return c.Status(http.StatusBadRequest).JSON(responses.MemberResponse{Status: http.StatusBadRequest, Message: "error", Data: &fiber.Map{"data": err.Error()}})
	}

	if validationErr := validateNoTeamParticipants.Struct(&no_team_participant); validationErr != nil {
		return c.Status(http.StatusBadRequest).JSON(responses.MemberResponse{Status: http.StatusBadRequest, Message: "error", Data: &fiber.Map{"data": validationErr.Error()}})
	}

	newNoTeamParticipant := models.TeamMember{
		FullName:                       no_team_participant.FullName,
		HasTeam:                        no_team_participant.HasTeam,
		TeamName:                       no_team_participant.TeamName,
		Email:                          no_team_participant.Email,
		University:                     no_team_participant.University,
		Age:                            no_team_participant.Age,
		Location:                       no_team_participant.Location,
		HeardAboutUs:                   no_team_participant.HeardAboutUs,
		PreviousHackathonParticipation: no_team_participant.PreviousHackathonParticipation,
		PreviousHackAUBGParticipation:  no_team_participant.PreviousHackAUBGParticipation,
		HasExperience:                  no_team_participant.HasExperience,
		ProgrammingLevel:               no_team_participant.ProgrammingLevel,
		StrongSides:                    no_team_participant.StrongSides,
		ShirtSize:                      no_team_participant.ShirtSize,
		WantInternship:                 no_team_participant.WantInternship,
		JobInterests:                   no_team_participant.JobInterests,
		ShareInfoWithSponsors:          no_team_participant.ShareInfoWithSponsors,
		WantJobOffers:                  no_team_participant.WantJobOffers}

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
	no_team_participant_key := c.Params("key", "key was not provided")

	bearer_token := c.Get("BEARER-TOKEN")

	var no_team_participant models.TeamMember
	defer cancel()

	if bearer_token != configs.ReturnAuthToken() {
		return c.Status(http.StatusUnauthorized).JSON(responses.MemberResponse{Status: http.StatusUnauthorized, Message: "error", Data: &fiber.Map{"Reason": "Authentication failed"}})
	}

	key_from_hex, _ := primitive.ObjectIDFromHex(no_team_participant_key)
	err := noTeamParticipantsCollection.FindOne(ctx, bson.M{"_id": key_from_hex}).Decode(&no_team_participant)
	if err != nil {
		return c.Status(http.StatusInternalServerError).JSON(responses.MemberResponse{Status: http.StatusInternalServerError, Message: "error", Data: &fiber.Map{"data": err.Error() + "key: " + no_team_participant_key}})
	}
	return c.Status(http.StatusOK).JSON(responses.MemberResponse{Status: http.StatusOK, Message: "success", Data: &fiber.Map{"data": no_team_participant}})
}

func EditNoTeamParticipant(c *fiber.Ctx) error {

	//TODO: Maybe change message if body is only of non-existings fields
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	no_team_participant_key := c.Params("key", "key was not provided")
	var no_team_participant models.EditTeamMember
	defer cancel()
	var no_team_participant_map models.EditTeamMember
	key_from_hex, _ := primitive.ObjectIDFromHex(no_team_participant_key)
	err1 := noTeamParticipantsCollection.FindOne(ctx, bson.M{"_id": key_from_hex}).Decode(&no_team_participant_map)

	if err1 != nil {
		return c.Status(http.StatusNotFound).JSON(responses.MemberResponse{Status: http.StatusNotFound, Message: "No such memb"})
	}
	bearer_token := c.Get("BEARER-TOKEN")

	defer cancel()
	if bearer_token != configs.ReturnAuthToken() {
		return c.Status(http.StatusUnauthorized).JSON(responses.MemberResponse{Status: http.StatusUnauthorized, Message: "error", Data: &fiber.Map{"Reason": "Authentication failed"}})
	}

	if err := c.BodyParser(&no_team_participant); err != nil {
		return c.Status(http.StatusBadRequest).JSON(responses.MemberResponse{Status: http.StatusBadRequest, Message: "Empty Body"})
	}

	if validationErr := validateNoTeamParticipants.Struct(&no_team_participant); validationErr != nil {
		return c.Status(http.StatusBadRequest).JSON(responses.MemberResponse{Status: http.StatusBadRequest, Message: "Body is not compatible"})
	}
	if no_team_participant.FullName != "" {
		no_team_participant_map.FullName = no_team_participant.FullName
	}
	if *no_team_participant.HasTeam {
		no_team_participant_map.HasTeam = no_team_participant.HasTeam
	}
	if no_team_participant.TeamName != "" {
		no_team_participant_map.TeamName = no_team_participant.TeamName
	}
	if no_team_participant.Email != "" {
		no_team_participant_map.Email = no_team_participant.Email
	}
	if no_team_participant.University != "" {
		no_team_participant_map.University = no_team_participant.University
	}
	if no_team_participant.Age != 0 {
		no_team_participant_map.Age = no_team_participant.Age
	}
	if no_team_participant.Location != "" {
		no_team_participant_map.Location = no_team_participant.Location
	}
	if no_team_participant.ShirtSize != "" {
		no_team_participant_map.ShirtSize = no_team_participant.ShirtSize
	}

	update := bson.M{}
	v := reflect.ValueOf(no_team_participant_map)
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
	no_team_participant_key := c.Params("key", "key was not provided")
	bearer_token := c.Get("BEARER-TOKEN")
	defer cancel()

	if bearer_token != configs.ReturnAuthToken() {
		return c.Status(http.StatusUnauthorized).JSON(responses.MemberResponse{Status: http.StatusUnauthorized, Message: "error", Data: &fiber.Map{"Reason": "Authentication failed"}})
	}

	key_from_hex, _ := primitive.ObjectIDFromHex(no_team_participant_key)

	result, err := noTeamParticipantsCollection.DeleteOne(ctx, bson.M{"_id": key_from_hex})
	if err != nil {
		return c.Status(http.StatusInternalServerError).JSON(responses.MemberResponse{Status: http.StatusInternalServerError, Message: "Error", Data: &fiber.Map{"Reason": err.Error(), "Key": no_team_participant_key}})
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

	results, err := GetNumberOfNoTeamParticipants(ctx)

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
func GetNumberOfNoTeamParticipants(ctx context.Context) (int64, error) {
	results, err := noTeamParticipantsCollection.CountDocuments(ctx, bson.M{})
	return results, err
}

func BatchAddTeamMembersToNoParticipants(ctx context.Context, teamMembers []models.TeamMember) error {
	for i := 0; i < len(teamMembers); i++ {
		_, err := noTeamParticipantsCollection.InsertOne(ctx, teamMembers[i])
		if err != nil {
			return err
		}
	}
	return nil
}