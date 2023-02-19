package controllers

import (
	"context"
	"hub-backend/configs"
	"hub-backend/models"
	"hub-backend/responses"
	"net/http"
	"time"

	"github.com/gofiber/fiber/v2"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
	"go.mongodb.org/mongo-driver/mongo"
)

var partnersCollection *mongo.Collection = configs.GetCollection(configs.DB, "partners")

// Mentors use the same model as Jury

func CreatePartner(c *fiber.Ctx) error {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)

	bearer_token := c.Get("BEARER-TOKEN")

	var sponsor models.Sponsors
	defer cancel()
	if bearer_token != configs.ReturnAuthToken() {
		return c.Status(http.StatusUnauthorized).JSON(responses.MemberResponse{Status: http.StatusUnauthorized, Message: "error", Data: &fiber.Map{"Reason": "Authentication failed"}})
	}

	if err := c.BodyParser(&sponsor); err != nil {
		return c.Status(http.StatusBadRequest).JSON(responses.MemberResponse{Status: http.StatusBadRequest, Message: "error", Data: &fiber.Map{"data": err.Error()}})
	}

	if validationErr := validate.Struct(&sponsor); validationErr != nil {
		return c.Status(http.StatusBadRequest).JSON(responses.MemberResponse{Status: http.StatusBadRequest, Message: "error", Data: &fiber.Map{"data": validationErr.Error()}})
	}

	result, err := partnersCollection.InsertOne(ctx, sponsor)
	if err != nil {
		return c.Status(http.StatusInternalServerError).JSON(responses.MemberResponse{Status: http.StatusInternalServerError, Message: "error", Data: &fiber.Map{"data": err.Error()}})
	}

	return c.Status(http.StatusCreated).JSON(responses.MemberResponse{Status: http.StatusCreated, Message: "success", Data: &fiber.Map{"data": result}})

}

func EditPartner(c *fiber.Ctx) error {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	key := c.Params("key", "key was not provided")
	var sponsor models.Sponsors

	bearer_token := c.Get("BEARER-TOKEN")

	defer cancel()
	if bearer_token != configs.ReturnAuthToken() {
		return c.Status(http.StatusUnauthorized).JSON(responses.MemberResponse{Status: http.StatusUnauthorized, Message: "error", Data: &fiber.Map{"Reason": "Authentication failed"}})
	}

	if err := c.BodyParser(&sponsor); err != nil {
		return c.Status(http.StatusBadRequest).JSON(responses.MemberResponse{Status: http.StatusBadRequest, Message: "Empty Body"})
	}

	newSponsor := models.Sponsors{
		Company:        sponsor.Company,
		SocialLink:     sponsor.SocialLink,
		ProfilePicture: sponsor.ProfilePicture,
		Category:       sponsor.Category,
	}

	jury_map := make(map[string]string)
	flag := false

	if newSponsor.Company != "" {
		jury_map["company"] = newSponsor.Company
		flag = true
	}
	if newSponsor.SocialLink != "" {
		jury_map["sociallink"] = newSponsor.SocialLink
		flag = true
	}
	if newSponsor.ProfilePicture != "" {
		jury_map["profilepicture"] = newSponsor.ProfilePicture
		flag = true
	}

	if newSponsor.Category != "" {
		jury_map["category"] = newSponsor.Category
		flag = true
	}

	if !flag {
		return c.Status(http.StatusBadRequest).JSON(responses.MemberResponse{Status: http.StatusBadRequest, Message: "error", Data: &fiber.Map{"data": "No matching fields"}})
	}

	update := bson.M{}
	for k, v := range jury_map {
		update[k] = v
	}

	key_from_hex, _ := primitive.ObjectIDFromHex(key)

	result, err := partnersCollection.UpdateOne(ctx, bson.M{"_id": key_from_hex}, bson.M{"$set": update})

	if err != nil {
		return c.Status(http.StatusInternalServerError).JSON(responses.MemberResponse{Status: http.StatusInternalServerError, Message: err.Error()})
	}

	if result.MatchedCount != 1 {
		return c.Status(http.StatusInternalServerError).JSON(responses.MemberResponse{Status: http.StatusInternalServerError, Message: "Document not found"})
	}

	return c.Status(http.StatusOK).JSON(responses.MemberResponse{Status: http.StatusOK, Message: "Partner was updated"})
}

func DeletePartner(c *fiber.Ctx) error {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	member_key := c.Params("key", "key was not provided")
	bearer_token := c.Get("BEARER-TOKEN")
	defer cancel()

	if bearer_token != configs.ReturnAuthToken() {
		return c.Status(http.StatusUnauthorized).JSON(responses.MemberResponse{Status: http.StatusUnauthorized, Message: "error", Data: &fiber.Map{"Reason": "Authentication failed"}})
	}

	key_from_hex, _ := primitive.ObjectIDFromHex(member_key)

	result, err := partnersCollection.DeleteOne(ctx, bson.M{"_id": key_from_hex})
	if err != nil {
		return c.Status(http.StatusInternalServerError).JSON(responses.MemberResponse{Status: http.StatusInternalServerError, Message: "Error", Data: &fiber.Map{"Reason": err.Error(), "Key": member_key}})
	}

	if result.DeletedCount < 1 {
		return c.Status(http.StatusNotFound).JSON(
			responses.MemberResponse{Status: http.StatusNotFound, Message: "error", Data: &fiber.Map{"data": "Partner with specified ID not found!"}},
		)
	}

	return c.Status(http.StatusOK).JSON(
		responses.MemberResponse{Status: http.StatusOK, Message: "success", Data: &fiber.Map{"data": "Partner successfully deleted!"}},
	)
}

func GetPartner(c *fiber.Ctx) error {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	member_key := c.Params("key", "key was not provided")

	var member models.Sponsors
	defer cancel()

	key_from_hex, _ := primitive.ObjectIDFromHex(member_key)
	err := partnersCollection.FindOne(ctx, bson.M{"_id": key_from_hex}).Decode(&member)
	if err != nil {
		return c.Status(http.StatusInternalServerError).JSON(responses.MemberResponse{Status: http.StatusInternalServerError, Message: "error", Data: &fiber.Map{"data": err.Error() + "key: " + member_key}})
	}

	return c.Status(http.StatusOK).JSON(responses.MemberResponse{Status: http.StatusOK, Message: "success", Data: &fiber.Map{"data": member}})
}

func GetAllPartners(c *fiber.Ctx) error {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	var members []models.Sponsors
	defer cancel()

	results, err := partnersCollection.Find(ctx, bson.M{})

	if err != nil {
		return c.Status(http.StatusInternalServerError).JSON(responses.MemberResponse{Status: http.StatusInternalServerError, Message: "error", Data: &fiber.Map{"data": err.Error()}})
	}

	defer results.Close(ctx)
	for results.Next(ctx) {
		var singleMember models.Sponsors
		if err = results.Decode(&singleMember); err != nil {
			return c.Status(http.StatusInternalServerError).JSON(responses.MemberResponse{Status: http.StatusInternalServerError, Message: "error", Data: &fiber.Map{"data": err.Error()}})
		}

		members = append(members, singleMember)
	}

	return c.Status(http.StatusOK).JSON(
		responses.MemberResponse{Status: http.StatusOK, Message: "success", Data: &fiber.Map{"data": members}},
	)
}
