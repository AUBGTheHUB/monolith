package controllers

import (
	"context"
	"fmt"
	"hub-backend/configs"
	"hub-backend/models"
	"hub-backend/responses"
	"net/http"
	"time"

	"github.com/gofiber/fiber/v2"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"golang.org/x/crypto/bcrypt"
)

var adminCollection *mongo.Collection = configs.GetCollection(configs.DB, "admins")

func LoginAdmin(c *fiber.Ctx) error {
	var incomming_admin models.Admin

	if err := c.BodyParser(&incomming_admin); err != nil {
		return err
	}

	var user models.Admin

	ctx, _ := context.WithTimeout(context.Background(), 10*time.Second)
	err := adminCollection.FindOne(ctx, bson.M{"username": incomming_admin.Username}).Decode(&user)

	if err != nil {
		return c.Status(http.StatusInternalServerError).JSON(responses.MemberResponse{Status: http.StatusInternalServerError, Message: "error", Data: &fiber.Map{"Reason": err.Error()}})
	}

	if err := bcrypt.CompareHashAndPassword([]byte(user.Password), []byte(incomming_admin.Password)); err != nil {
		return c.Status(http.StatusInternalServerError).JSON(responses.MemberResponse{Status: http.StatusInternalServerError, Message: "error", Data: &fiber.Map{"Reason": err.Error()}})
	}

	auth_token := configs.ReturnAuthToken()
	fmt.Println(auth_token)
	if auth_token == "" {
		return c.Status(http.StatusInternalServerError).JSON(responses.MemberResponse{Status: http.StatusInternalServerError, Message: "error", Data: &fiber.Map{"Reason": "Authentication failed"}})
	}

	return c.Status(http.StatusOK).JSON(
		responses.MemberResponse{Status: http.StatusOK, Message: "success", Data: &fiber.Map{"auth_token": auth_token}},
	)
}

func ValidateAuth(c *fiber.Ctx) error {
	bearer_token := c.Get("BEARER_TOKEN")
	if bearer_token != configs.ReturnAuthToken() {
		return c.Status(http.StatusBadRequest).JSON(responses.MemberResponse{Status: http.StatusBadRequest, Message: "error", Data: &fiber.Map{"Reason": "Authentication failed"}})
	}

	return c.Status(http.StatusOK).JSON(responses.MemberResponse{Status: http.StatusOK, Message: "Authentication success", Data: &fiber.Map{"User persmission": true}})

}
