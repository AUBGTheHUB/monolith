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

var eventsCollection *mongo.Collection = configs.GetCollection(configs.DB, "events")

func EmptyStringBody(string_from_body string) bool {
	if string_from_body == "" {
		return true
	}
	return false
}

func isEmptyException(c *fiber.Ctx, data string) error {
	return c.Status(http.StatusInternalServerError).JSON(responses.MemberResponse{Status: http.StatusBadRequest, Message: data + " field is empty"})
}

func CreateEvent(c *fiber.Ctx) error {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)

	bearer_token := c.Get("BEARER_TOKEN")

	var event models.Event
	defer cancel()

	if bearer_token != configs.ReturnAuthToken() {
		return c.Status(http.StatusBadRequest).JSON(responses.MemberResponse{Status: http.StatusBadRequest, Message: "error", Data: &fiber.Map{"Reason": "Authentication failed"}})
	}

	if err := c.BodyParser(&event); err != nil {
		return c.Status(http.StatusBadRequest).JSON(responses.MemberResponse{Status: http.StatusBadRequest, Message: "error", Data: &fiber.Map{"data": err.Error()}})
	}

	if validationErr := validate.Struct(&event); validationErr != nil {
		return c.Status(http.StatusBadRequest).JSON(responses.MemberResponse{Status: http.StatusBadRequest, Message: "error", Data: &fiber.Map{"data": validationErr.Error()}})
	}

	newEvent := models.Event{
		Title:        event.Title,
		StartDate:    event.StartDate,
		EndDate:      event.EndDate,
		Description:  event.Description,
		Location:     event.Location,
		LocationLink: event.LocationLink,
		Banner:       event.Banner,
		FacebookLink: event.FacebookLink,
	}

	// this could be avoided with requiring validation in the model

	empty_body_check := EmptyStringBody(newEvent.Title)
	if empty_body_check {
		return isEmptyException(c, "title")
	}

	empty_body_check = EmptyStringBody(newEvent.Description)
	if empty_body_check {
		return isEmptyException(c, "description")
	}

	empty_body_check = EmptyStringBody(newEvent.Location)
	if empty_body_check {
		return isEmptyException(c, "location")
	}

	empty_body_check = EmptyStringBody(newEvent.LocationLink)
	if empty_body_check {
		return isEmptyException(c, "locationlink")
	}

	empty_body_check = EmptyStringBody(newEvent.Banner)
	if empty_body_check {
		return isEmptyException(c, "banner")
	}

	empty_body_check = EmptyStringBody(newEvent.FacebookLink)
	if empty_body_check {
		return isEmptyException(c, "facebooklink")
	}

	if newEvent.StartDate.IsZero() || newEvent.EndDate.IsZero() {
		return isEmptyException(c, "One or both of the DATE (ISO) ")
	}

	result, err := eventsCollection.InsertOne(ctx, newEvent)
	if err != nil {
		return c.Status(http.StatusInternalServerError).JSON(responses.MemberResponse{Status: http.StatusInternalServerError, Message: "error", Data: &fiber.Map{"data": err.Error()}})
	}

	return c.Status(http.StatusCreated).JSON(responses.MemberResponse{Status: http.StatusCreated, Message: "success", Data: &fiber.Map{"data": result}})
}

func GetEvent(c *fiber.Ctx) error {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	event_key := c.Params("key", "key was not provided") // change default key

	var event models.Event
	defer cancel()

	key_from_hex, _ := primitive.ObjectIDFromHex(event_key)

	err := eventsCollection.FindOne(ctx, bson.M{"_id": key_from_hex}).Decode(&event)
	if err != nil {
		return c.Status(http.StatusInternalServerError).JSON(responses.MemberResponse{Status: http.StatusInternalServerError, Message: "error", Data: &fiber.Map{"data": err.Error() + "key: " + event_key}})
	}

	return c.Status(http.StatusOK).JSON(responses.MemberResponse{Status: http.StatusOK, Message: "success", Data: &fiber.Map{"data": event}})

}

func GetAllEvents(c *fiber.Ctx) error {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	var events []models.Event
	defer cancel()

	results, err := eventsCollection.Find(ctx, bson.M{})

	if err != nil {
		return c.Status(http.StatusInternalServerError).JSON(responses.MemberResponse{Status: http.StatusInternalServerError, Message: "error", Data: &fiber.Map{"data": err.Error()}})
	}

	defer results.Close(ctx)
	for results.Next(ctx) {
		var event models.Event
		if err = results.Decode(&event); err != nil {
			return c.Status(http.StatusInternalServerError).JSON(responses.MemberResponse{Status: http.StatusInternalServerError, Message: "error", Data: &fiber.Map{"data": err.Error()}})
		}

		events = append(events, event)
	}

	return c.Status(http.StatusOK).JSON(
		responses.MemberResponse{Status: http.StatusOK, Message: "success", Data: &fiber.Map{"events": events}},
	)
}

func EditEvent(c *fiber.Ctx) error {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	eventid := c.Params("key", "key was not provided")
	var event models.Event

	bearer_token := c.Get("BEARER_TOKEN")

	defer cancel()
	if bearer_token != configs.ReturnAuthToken() {
		return c.Status(http.StatusBadRequest).JSON(responses.MemberResponse{Status: http.StatusBadRequest, Message: "error", Data: &fiber.Map{"Reason": "Authentication failed"}})
	}

	if err := c.BodyParser(&event); err != nil {
		return c.Status(http.StatusBadRequest).JSON(responses.MemberResponse{Status: http.StatusBadRequest, Message: "Empty Body"})
	}

	if validationErr := validate.Struct(&event); validationErr != nil {
		return c.Status(http.StatusBadRequest).JSON(responses.MemberResponse{Status: http.StatusBadRequest, Message: "Body is not compatible"})
	}

	event_map := make(map[string]interface{})

	// excuse me for this :)))
	if event.Title != "" {
		event_map["title"] = event.Title
	}
	if event.Description != "" {
		event_map["description"] = event.Description
	}
	if event.Location != "" {
		event_map["location"] = event.Location
	}
	if event.LocationLink != "" {
		event_map["locationlink"] = event.LocationLink
	}
	if event.Banner != "" {
		event_map["banner"] = event.Banner
	}

	if !event.StartDate.IsZero() {
		event_map["startdate"] = event.StartDate
	}

	if !event.EndDate.IsZero() {
		event_map["enddate"] = event.EndDate
	}

	if event.FacebookLink != "" {
		event_map["data"] = event.FacebookLink
	}

	update := bson.M{}
	for k, v := range event_map {
		update[k] = v
	}

	key_from_hex, _ := primitive.ObjectIDFromHex(eventid)

	result, err := eventsCollection.UpdateOne(ctx, bson.M{"_id": key_from_hex}, bson.M{"$set": update})

	if err != nil {
		return c.Status(http.StatusInternalServerError).JSON(responses.MemberResponse{Status: http.StatusInternalServerError, Message: err.Error()})
	}

	if result.MatchedCount != 1 {
		return c.Status(http.StatusInternalServerError).JSON(responses.MemberResponse{Status: http.StatusInternalServerError, Message: "Document not found"})
	}

	return c.Status(http.StatusOK).JSON(responses.MemberResponse{Status: http.StatusOK, Message: "Event was updated"})

}

func DeleteEvent(c *fiber.Ctx) error {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	event_key := c.Params("key", "key was not provided")
	bearer_token := c.Get("BEARER_TOKEN")
	defer cancel()

	if bearer_token != configs.ReturnAuthToken() {
		return c.Status(http.StatusBadRequest).JSON(responses.MemberResponse{Status: http.StatusBadRequest, Message: "error", Data: &fiber.Map{"Reason": "Authentication failed"}})
	}

	key_from_hex, _ := primitive.ObjectIDFromHex(event_key)

	result, err := eventsCollection.DeleteOne(ctx, bson.M{"_id": key_from_hex})
	if err != nil {
		return c.Status(http.StatusInternalServerError).JSON(responses.MemberResponse{Status: http.StatusInternalServerError, Message: "Error", Data: &fiber.Map{"Reason": err.Error(), "Key": event_key}})
	}

	if result.DeletedCount < 1 {
		return c.Status(http.StatusNotFound).JSON(
			responses.MemberResponse{Status: http.StatusNotFound, Message: "No such event"},
		)
	}

	return c.Status(http.StatusOK).JSON(
		responses.MemberResponse{Status: http.StatusOK, Message: "success", Data: &fiber.Map{"response": "Event has been deleted!"}},
	)

}
