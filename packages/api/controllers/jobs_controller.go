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

var jobsCollection *mongo.Collection = configs.GetCollection(configs.DB, "jobs")

func CreateJob(c *fiber.Ctx) error {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)

	bearer_token := c.Get("BEARER_TOKEN")

	var job models.Job
	defer cancel()

	if bearer_token != configs.ReturnAuthToken() {
		return c.Status(http.StatusUnauthorized).JSON(responses.MemberResponse{Status: http.StatusUnauthorized, Message: "error", Data: &fiber.Map{"data": "Unauthorized"}})
	}

	if err := c.BodyParser(&job); err != nil {
		return c.Status(http.StatusBadRequest).JSON(responses.MemberResponse{Status: http.StatusBadRequest, Message: "error", Data: &fiber.Map{"data": err.Error()}})
	}

	if validationErr := validate.Struct(&job); validationErr != nil {
		return c.Status(http.StatusBadRequest).JSON(responses.MemberResponse{Status: http.StatusBadRequest, Message: "error", Data: &fiber.Map{"data": validationErr.Error()}})
	}

	newJob := models.Job{
		Logo:        job.Logo,
		Position:    job.Position,
		Company:     job.Company,
		Description: job.Description,
		Link:        job.Link,
	}

	// empty_body_check := EmptyStringBody(newJob.JobID)

	v := reflect.ValueOf(newJob)
	type_of_v := v.Type()

	// this will only work if all struct fields are string

	for i := 0; i < v.NumField(); i++ {
		if v.Field(i).Kind() == 17 {
			// We check the type of the field, if it is a string, we check if it is empty
			// But code breaks if we have a field that is not a string
			// In the model we have a primitive.ObjectID field
			// So we need to break the loop when we reach the ObjectID field
			// Do not ask me why it is 17, I don't know either

			break
		}

		empty_body_check := EmptyStringBody(v.Field(i).Interface().(string))
		if empty_body_check {
			return isEmptyException(c, type_of_v.Field(i).Name)
		}
	}

	result, err := jobsCollection.InsertOne(ctx, newJob)

	if err != nil {
		return c.Status(http.StatusInternalServerError).JSON(responses.MemberResponse{Status: http.StatusInternalServerError, Message: "error", Data: &fiber.Map{"data": err.Error()}})
	}

	return c.Status(http.StatusCreated).JSON(responses.MemberResponse{Status: http.StatusCreated, Message: "success", Data: &fiber.Map{"data": result}})
}

func GetJob(c *fiber.Ctx) error {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	job_key := c.Params("key", "key was not provided")
	var job models.Job
	defer cancel()

	key_from_hex, _ := primitive.ObjectIDFromHex(job_key)

	err := jobsCollection.FindOne(ctx, bson.M{"_id": key_from_hex}).Decode(&job)
	if err != nil {
		return c.Status(http.StatusInternalServerError).JSON(responses.MemberResponse{Status: http.StatusInternalServerError, Message: "error", Data: &fiber.Map{"data": err.Error() + "key: " + job_key}})
	}

	return c.Status(http.StatusOK).JSON(responses.MemberResponse{Status: http.StatusOK, Message: "success", Data: &fiber.Map{"data": job}})

}

func GetAllJobs(c *fiber.Ctx) error {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	var jobs []models.Job
	defer cancel()

	results, err := jobsCollection.Find(ctx, bson.M{})

	if err != nil {
		return c.Status(http.StatusInternalServerError).JSON(responses.MemberResponse{Status: http.StatusInternalServerError, Message: "error", Data: &fiber.Map{"data": err.Error()}})
	}

	defer results.Close(ctx)
	for results.Next(ctx) {
		var job models.Job
		err := results.Decode(&job)
		if err != nil {
			return c.Status(http.StatusInternalServerError).JSON(responses.MemberResponse{Status: http.StatusInternalServerError, Message: "error", Data: &fiber.Map{"data": err.Error()}})
		}
		jobs = append(jobs, job)
	}

	return c.Status(http.StatusOK).JSON(responses.MemberResponse{Status: http.StatusOK, Message: "success", Data: &fiber.Map{"data": jobs}})
}

func EditJob(c *fiber.Ctx) error {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	job_key := c.Params("key", "key was not provided")
	var job models.Job

	bearer_token := c.Get("BEARER_TOKEN")
	defer cancel()

	if bearer_token != configs.ReturnAuthToken() {
		return c.Status(http.StatusUnauthorized).JSON(responses.MemberResponse{Status: http.StatusUnauthorized, Message: "error", Data: &fiber.Map{"data": "Unauthorized"}})
	}

	if err := c.BodyParser(&job); err != nil {
		return c.Status(http.StatusBadRequest).JSON(responses.MemberResponse{Status: http.StatusBadRequest, Message: "error", Data: &fiber.Map{"data": err.Error()}})
	}

	if validationErr := validate.Struct(&job); validationErr != nil {
		return c.Status(http.StatusBadRequest).JSON(responses.MemberResponse{Status: http.StatusBadRequest, Message: "error", Data: &fiber.Map{"data": validationErr.Error()}})
	}

	job_map := make(map[string]string)

	if job.Position != "" {
		job_map["position"] = job.Position
	}

	if job.Company != "" {
		job_map["company"] = job.Company
	}

	if job.Logo != "" {
		job_map["logo"] = job.Logo
	}

	if job.Description != "" {
		job_map["description"] = job.Description
	}

	if job.Link != "" {
		job_map["link"] = job.Link
	}

	update := bson.M{}
	for key, value := range job_map {
		update[key] = value
	}

	key_from_hex, _ := primitive.ObjectIDFromHex(job_key)

	result, err := jobsCollection.UpdateOne(ctx, bson.M{"_id": key_from_hex}, bson.M{"$set": update})

	if err != nil {
		return c.Status(http.StatusInternalServerError).JSON(responses.MemberResponse{Status: http.StatusInternalServerError, Message: "error", Data: &fiber.Map{"data": err.Error()}})
	}

	if result.MatchedCount != 1 {
		return c.Status(http.StatusNotFound).JSON(responses.MemberResponse{Status: http.StatusNotFound, Message: "error", Data: &fiber.Map{"data": "Job not found"}})
	}

	return c.Status(http.StatusOK).JSON(responses.MemberResponse{Status: http.StatusOK, Message: "Job was updated"})

}

func DeleteJob(c *fiber.Ctx) error {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	job_key := c.Params("key", "key was not provided")
	bearer_token := c.Get("BEARER_TOKEN")
	defer cancel()

	if bearer_token != configs.ReturnAuthToken() {
		return c.Status(http.StatusUnauthorized).JSON(responses.MemberResponse{Status: http.StatusUnauthorized, Message: "error", Data: &fiber.Map{"data": "Unauthorized"}})
	}

	key_from_hex, _ := primitive.ObjectIDFromHex(job_key)
	result, err := jobsCollection.DeleteOne(ctx, bson.M{"_id": key_from_hex})

	if err != nil {
		return c.Status(http.StatusInternalServerError).JSON(responses.MemberResponse{Status: http.StatusInternalServerError, Message: "error", Data: &fiber.Map{"data": err.Error()}})
	}

	return c.Status(http.StatusOK).JSON(responses.MemberResponse{Status: http.StatusOK, Message: "success", Data: &fiber.Map{"data": result}})
}
