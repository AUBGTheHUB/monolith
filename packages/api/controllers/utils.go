package controllers

import (
	"hub-backend/responses"
	"net/http"

	"github.com/gofiber/fiber/v2"
)

func EmptyStringBody(string_from_body string) bool {
	if string_from_body == "" {
		return true
	}
	return false
}

func isEmptyException(c *fiber.Ctx, data string) error {
	return c.Status(http.StatusInternalServerError).JSON(responses.MemberResponse{Status: http.StatusBadRequest, Message: data + " field is empty"})
}
