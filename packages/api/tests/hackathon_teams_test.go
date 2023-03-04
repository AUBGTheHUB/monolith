package tests

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"hub-backend/app"
	"hub-backend/configs"
	"hub-backend/models"
	"net/http"
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
	"go.mongodb.org/mongo-driver/mongo"
)

const url string = "http://127.0.0.1:8000/api/hackathon/teams"

func SetHeaders(req *http.Request) {
	req.Header.Set("BEARER-TOKEN", "TEST_TOKEN")
	req.Header.Set("Content-Type", "application/json")
}

func TestTeamEndpoint(t *testing.T) {
	// Set up
	go app.StartApp()

	time.Sleep(5 * time.Second)

	// Test Create Team endpoint
	var teamMembersCollection *mongo.Collection = configs.GetCollection(configs.DB, "hackathonMembers")
	var hackathonTeamCollection *mongo.Collection = configs.GetCollection(configs.DB, "hackathonTeam")

	var testBool bool = true

	var dataTeam models.Team
	dataMember := &models.TeamMember{
		FullName:              "Test",
		TeamNoTeam:            &testBool,
		TeamName:              "Integration Test",
		Email:                 "integration_test@gmail.com",
		School:                "Test School",
		Age:                   18,
		Location:              "Test Location",
		HeardAboutUs:          "Test",
		PreviousParticipation: &testBool,
		PartDetails:           "Test",
		Experience:            &testBool,
		ProgrammingLevel:      "Test",
		StrongSides:           "Test",
		ShirtSize:             "Test",
		Internship:            &testBool,
		JobInterests:          "Test",
		SponsorShare:          &testBool,
		NewsLetter:            &testBool,
	}

	memberResult, err := teamMembersCollection.InsertOne(context.TODO(), dataMember)

	dataTeam.TeamName = "INTEGRATION TEST"
	dataTeam.TeamMembers = []string{memberResult.InsertedID.(primitive.ObjectID).Hex()}

	json_data, _ := json.Marshal(dataTeam)

	client := &http.Client{}

	req, _ := http.NewRequest("POST", url, bytes.NewBuffer(json_data))

	SetHeaders(req)

	resp, err := client.Do(req)

	if err != nil {
		assert.FailNow(t, err.Error())
	}

	var res map[string]interface{}

	json.NewDecoder(resp.Body).Decode(&res)

	assert.Equal(t, float64(201), res["status"])

	iID := res["data"].(map[string]interface{})["data"].(map[string]interface{})["InsertedID"]

	// Verify
	req, _ = http.NewRequest("GET", url+"/"+fmt.Sprint(iID), bytes.NewBufferString(""))

	SetHeaders(req)

	resp, err = client.Do(req)

	if err != nil {
		assert.FailNow(t, err.Error())
	}

	json.NewDecoder(resp.Body).Decode(&res)

	var uTD models.Team
	key_from_hex, _ := primitive.ObjectIDFromHex(iID.(string))
	err = hackathonTeamCollection.FindOne(context.TODO(), bson.M{"_id": key_from_hex}).Decode(&uTD)

	assert.Equal(t, dataTeam.TeamName, uTD.TeamName)
	
	assert.Equal(t, dataTeam.TeamMembers, uTD.TeamMembers)

	// Clean Up
	teamMembersCollection.DeleteOne(context.TODO(), bson.M{"_id": dataTeam.TeamMembers[0]})
	req, _ = http.NewRequest("DELETE", url+"/"+fmt.Sprint(iID), bytes.NewBufferString(""))

	SetHeaders(req)

	resp, err = client.Do(req)

	if err != nil {
		assert.FailNow(t, err.Error())
	}

	json.NewDecoder(resp.Body).Decode(&res)

	assert.Equal(t, float64(200), res["status"])

}
