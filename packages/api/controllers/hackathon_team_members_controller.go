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

var teamMembersCollection *mongo.Collection = configs.GetCollection(configs.DB, "hackathonMembers")

// var teamMembersCollection

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
		FullName:                       member.FullName,
		HasTeam:                        member.HasTeam,
		TeamName:                       member.TeamName,
		Email:                          member.Email,
		University:                     member.University,
		Age:                            member.Age,
		Location:                       member.Location,
		HeardAboutUs:                   member.HeardAboutUs,
		PreviousHackathonParticipation: member.PreviousHackathonParticipation,
		PreviousHackAUBGParticipation:  member.PreviousHackAUBGParticipation,
		HasExperience:                  member.HasExperience,
		ProgrammingLevel:               member.ProgrammingLevel,
		StrongSides:                    member.StrongSides,
		ShirtSize:                      member.ShirtSize,
		WantInternship:                 member.WantInternship,
		JobInterests:                   member.JobInterests,
		ShareInfoWithSponsors:          member.ShareInfoWithSponsors,
		WantJobOffers:                  member.WantJobOffers}

	if CheckIfTeamMemberExists(newHackathonTeamMember) {
		return c.Status(http.StatusBadRequest).JSON(responses.MemberResponse{Status: http.StatusBadRequest, Message: "This email is already present in the DB", Data: &fiber.Map{"data": newHackathonTeamMember.Email}})
	}

	result, err := CreateNewHackathonParticipant(ctx, newHackathonTeamMember)

	if err != nil {
		return c.Status(http.StatusInternalServerError).JSON(responses.MemberResponse{Status: http.StatusInternalServerError, Message: "error", Data: &fiber.Map{"data": err.Error()}})
	}

	return c.Status(http.StatusCreated).JSON(responses.MemberResponse{Status: http.StatusCreated, Message: "success", Data: &fiber.Map{"data": result}})

}

func GetHackathonMember(c *fiber.Ctx) error {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	member_key := c.Params("key", "key was not provided")

	bearer_token := c.Get("BEARER-TOKEN")

	var member models.TeamMember
	defer cancel()

	if bearer_token != configs.ReturnAuthToken() {
		return c.Status(http.StatusUnauthorized).JSON(responses.MemberResponse{Status: http.StatusUnauthorized, Message: "error", Data: &fiber.Map{"Reason": "Authentication failed"}})
	}

	key_from_hex, _ := primitive.ObjectIDFromHex(member_key)
	err := teamMembersCollection.FindOne(ctx, bson.M{"_id": key_from_hex}).Decode(&member)
	if err != nil {
		return c.Status(http.StatusInternalServerError).JSON(responses.MemberResponse{Status: http.StatusInternalServerError, Message: "error", Data: &fiber.Map{"data": err.Error() + "key: " + member_key}})
	}
	return c.Status(http.StatusOK).JSON(responses.MemberResponse{Status: http.StatusOK, Message: "success", Data: &fiber.Map{"data": member}})
}

func EditHackathonMember(c *fiber.Ctx) error {

	//TODO: Maybe change message if body is only of non-existings fields
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	member_key := c.Params("key", "key was not provided")
	var member models.EditTeamMember
	defer cancel()
	var member_map models.EditTeamMember
	key_from_hex, _ := primitive.ObjectIDFromHex(member_key)
	err1 := teamMembersCollection.FindOne(ctx, bson.M{"_id": key_from_hex}).Decode(&member_map)

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

	if validationErr := validateTeamMembers.Struct(&member); validationErr != nil {
		return c.Status(http.StatusBadRequest).JSON(responses.MemberResponse{Status: http.StatusBadRequest, Message: "Body is not compatible"})
	}

	if member.FullName != "" {
		member_map.FullName = member.FullName
	}
	if *member.HasTeam {
		member_map.HasTeam = member.HasTeam
	}
	if member.TeamName != "" {
		member_map.TeamName = member.TeamName
	}
	if member.Email != "" {
		member_map.Email = member.Email
	}
	if member.University != "" {
		member_map.University = member.University
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

	result, err := teamMembersCollection.UpdateOne(ctx, bson.M{"_id": key_from_hex}, bson.M{"$set": update})

	if err != nil {
		return c.Status(http.StatusInternalServerError).JSON(responses.MemberResponse{Status: http.StatusInternalServerError, Message: err.Error()})
	}

	if result.MatchedCount != 1 {
		return c.Status(http.StatusNotFound).JSON(responses.MemberResponse{Status: http.StatusNotFound, Message: "Document not found"})
	}

	return c.Status(http.StatusOK).JSON(responses.MemberResponse{Status: http.StatusOK, Message: "User was updated"})

}

func DeleteHackathonMember(c *fiber.Ctx, key ...string) error {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	var member_key string

	if len(key) > 0 {
		member_key = key[0]
	} else {
		member_key = c.Params("key", "key was not provided")
	}

	bearer_token := c.Get("BEARER-TOKEN")
	defer cancel()

	if bearer_token != configs.ReturnAuthToken() {
		return c.Status(http.StatusUnauthorized).JSON(responses.MemberResponse{Status: http.StatusUnauthorized, Message: "error", Data: &fiber.Map{"Reason": "Authentication failed"}})
	}

	key_from_hex, _ := primitive.ObjectIDFromHex(member_key)

	var member models.TeamMember

	err := teamMembersCollection.FindOne(ctx, bson.M{"_id": key_from_hex}).Decode(&member)

	if err != nil {
		return c.Status(http.StatusInternalServerError).JSON(responses.MemberResponse{Status: http.StatusNotFound, Message: "error", Data: &fiber.Map{"data": err.Error() + "key: " + member_key}})
	}

	if *(member.HasTeam) {

	results, _ := hackathonTeamCollection.Find(ctx, bson.M{})

	for results.Next(ctx) {
		var team models.Team
		results.Decode(&team)
		if CompareTeamNames(team.TeamName, member.TeamName) {
			_, err := hackathonTeamCollection.UpdateOne(ctx, bson.M{"_id": team.ID}, bson.M{"$pull": bson.M{"teammembers": member_key}})
			
			if err != nil {
				return c.Status(http.StatusInternalServerError).JSON(responses.MemberResponse{Status: http.StatusInternalServerError, Message: "Error", Data: &fiber.Map{"Reason": err.Error()}})
			}
		}
	}

	}

	result, err := teamMembersCollection.DeleteOne(ctx, bson.M{"_id": key_from_hex})
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

func GetHackathonMembersCount(c *fiber.Ctx) error {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	var countOfMembers int = 0
	bearer_token := c.Get("BEARER-TOKEN")

	defer cancel()

	if bearer_token != configs.ReturnAuthToken() {
		return c.Status(http.StatusUnauthorized).JSON(responses.MemberResponse{Status: http.StatusUnauthorized, Message: "error", Data: &fiber.Map{"Reason": "Authentication failed"}})
	}

	results, err := GetNumberOfHackathonParticipants(ctx)

	if err != nil {
		return c.Status(http.StatusInternalServerError).JSON(responses.MemberResponse{Status: http.StatusInternalServerError, Message: "error", Data: &fiber.Map{"data": err.Error()}})
	}

	countOfMembers = int(results)

	return c.Status(http.StatusOK).JSON(
		responses.MemberResponse{Status: http.StatusOK, Message: "success", Data: &fiber.Map{"count_of_members": countOfMembers}},
	)

}

func GetNumberOfHackathonParticipants(ctx context.Context) (int64, error) {
	results, err := teamMembersCollection.CountDocuments(ctx, bson.M{})
	return results, err
}

func CheckIfTeamMemberExists(newHackathonTeamMember models.TeamMember) bool {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()
	cursor, _ := teamMembersCollection.Find(
		ctx,
		bson.D{{"email", newHackathonTeamMember.Email}},
	)
	var results []models.TeamMember

	_ = cursor.All(ctx, &results)

	return len(results) > 0
}

func CreateNewHackathonParticipant(ctx context.Context, newHackathonTeamMember models.TeamMember) (*mongo.InsertOneResult, error) {
	result, err := teamMembersCollection.InsertOne(ctx, newHackathonTeamMember)
	return result, err
}

func BatchDeleteTeamMembers(ctx context.Context, keys []string) (*mongo.DeleteResult, error) {
	var keys_from_hex []primitive.ObjectID
	for _, key := range keys {
		key_from_hex, _ := primitive.ObjectIDFromHex(key)
		keys_from_hex = append(keys_from_hex, key_from_hex)
	}
	result, err := teamMembersCollection.DeleteMany(ctx, bson.M{"_id": bson.M{"$in": keys_from_hex}})
	return result, err
}
