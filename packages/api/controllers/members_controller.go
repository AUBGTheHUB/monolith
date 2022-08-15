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
	"go.mongodb.org/mongo-driver/bson/primitive"
	"go.mongodb.org/mongo-driver/mongo"
)

var membersCollection *mongo.Collection = configs.GetCollection(configs.DB, "members")

var validate = validator.New()

func CreateMember(c *fiber.Ctx) error {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)

	bearer_token := c.Get("BEARER_TOKEN")

	var member models.Member
	defer cancel()
	if bearer_token != configs.ReturnAuthToken() {
		return c.Status(http.StatusUnauthorized).JSON(responses.MemberResponse{Status: http.StatusUnauthorized, Message: "error", Data: &fiber.Map{"Reason": "Authentication failed"}})
	}

	// validate request body
	if err := c.BodyParser(&member); err != nil {
		return c.Status(http.StatusBadRequest).JSON(responses.MemberResponse{Status: http.StatusBadRequest, Message: "error", Data: &fiber.Map{"data": err.Error()}})
	}

	if validationErr := validate.Struct(&member); validationErr != nil {
		return c.Status(http.StatusBadRequest).JSON(responses.MemberResponse{Status: http.StatusBadRequest, Message: "error", Data: &fiber.Map{"data": validationErr.Error()}})
	}

	newMember := models.Member{
		// ID:             member.ID,
		Firstname:      member.Firstname,
		Lastname:       member.Lastname,
		Department:     member.Department,
		Position:       member.Position,
		SocialLink:     member.SocialLink,
		ProfilePicture: member.ProfilePicture,
	}

	// fmt.Println(newMember.ProfilePicture)

	result, err := membersCollection.InsertOne(ctx, newMember)
	if err != nil {
		return c.Status(http.StatusInternalServerError).JSON(responses.MemberResponse{Status: http.StatusInternalServerError, Message: "error", Data: &fiber.Map{"data": err.Error()}})
	}

	return c.Status(http.StatusCreated).JSON(responses.MemberResponse{Status: http.StatusCreated, Message: "success", Data: &fiber.Map{"data": result}})
}

func GetAllMembers(c *fiber.Ctx) error {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	var members []models.Member
	defer cancel()

	results, err := membersCollection.Find(ctx, bson.M{})

	if err != nil {
		return c.Status(http.StatusInternalServerError).JSON(responses.MemberResponse{Status: http.StatusInternalServerError, Message: "error", Data: &fiber.Map{"data": err.Error()}})
	}

	defer results.Close(ctx)
	for results.Next(ctx) {
		var singleMember models.Member
		if err = results.Decode(&singleMember); err != nil {
			return c.Status(http.StatusInternalServerError).JSON(responses.MemberResponse{Status: http.StatusInternalServerError, Message: "error", Data: &fiber.Map{"data": err.Error()}})
		}

		members = append(members, singleMember)
	}

	return c.Status(http.StatusOK).JSON(
		responses.MemberResponse{Status: http.StatusOK, Message: "success", Data: &fiber.Map{"data": members}},
	)
}

func GetMember(c *fiber.Ctx) error {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	member_key := c.Params("key", "key was not provided")

	var member models.Member
	defer cancel()

	key_from_hex, _ := primitive.ObjectIDFromHex(member_key)
	err := membersCollection.FindOne(ctx, bson.M{"_id": key_from_hex}).Decode(&member)
	if err != nil {
		return c.Status(http.StatusInternalServerError).JSON(responses.MemberResponse{Status: http.StatusInternalServerError, Message: "error", Data: &fiber.Map{"data": err.Error() + "key: " + member_key}})
	}

	return c.Status(http.StatusOK).JSON(responses.MemberResponse{Status: http.StatusOK, Message: "success", Data: &fiber.Map{"data": member}})
}

func EditMember(c *fiber.Ctx) error {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	member_key := c.Params("key", "key was not provided")
	var member models.EditMember

	bearer_token := c.Get("BEARER_TOKEN")

	defer cancel()
	if bearer_token != configs.ReturnAuthToken() {
		return c.Status(http.StatusUnauthorized).JSON(responses.MemberResponse{Status: http.StatusUnauthorized, Message: "error", Data: &fiber.Map{"Reason": "Authentication failed"}})
	}

	if err := c.BodyParser(&member); err != nil {
		return c.Status(http.StatusBadRequest).JSON(responses.MemberResponse{Status: http.StatusBadRequest, Message: "Empty Body"})
	}

	if validationErr := validate.Struct(&member); validationErr != nil {
		return c.Status(http.StatusBadRequest).JSON(responses.MemberResponse{Status: http.StatusBadRequest, Message: "Body is not compatible"})
	}

	member_map := make(map[string]string)

	// the commented code stops admins from modifying member id key
	// if member.MemberID != "" {
	// 	member_map["memberid"] = member.MemberID
	// }

	// excuse me for this :)))
	if member.Firstname != "" {
		member_map["firstname"] = member.Firstname
	}
	if member.Lastname != "" {
		member_map["lastname"] = member.Lastname
	}
	if member.Department != "" {
		member_map["department"] = member.Department
	}
	if member.Position != "" {
		member_map["position"] = member.Position
	}
	if member.SocialLink != "" {
		member_map["sociallink"] = member.SocialLink
	}
	if member.ProfilePicture != "" {
		member_map["profilepicture"] = member.ProfilePicture
	}

	update := bson.M{}
	for k, v := range member_map {
		update[k] = v
	}

	key_from_hex, _ := primitive.ObjectIDFromHex(member_key)

	result, err := membersCollection.UpdateOne(ctx, bson.M{"_id": key_from_hex}, bson.M{"$set": update})

	if err != nil {
		return c.Status(http.StatusInternalServerError).JSON(responses.MemberResponse{Status: http.StatusInternalServerError, Message: err.Error()})
	}

	if result.MatchedCount != 1 {
		return c.Status(http.StatusInternalServerError).JSON(responses.MemberResponse{Status: http.StatusInternalServerError, Message: "Document not found"})
	}

	return c.Status(http.StatusOK).JSON(responses.MemberResponse{Status: http.StatusOK, Message: "User was updated"})
}

func DeleteMember(c *fiber.Ctx) error {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	member_key := c.Params("key", "key was not provided")
	bearer_token := c.Get("BEARER_TOKEN")
	defer cancel()

	if bearer_token != configs.ReturnAuthToken() {
		return c.Status(http.StatusUnauthorized).JSON(responses.MemberResponse{Status: http.StatusUnauthorized, Message: "error", Data: &fiber.Map{"Reason": "Authentication failed"}})
	}

	key_from_hex, _ := primitive.ObjectIDFromHex(member_key)

	result, err := membersCollection.DeleteOne(ctx, bson.M{"_id": key_from_hex})
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
