package tests

import (
	"bytes"
	"encoding/json"
	"fmt"
	"hub-backend/app"
	"hub-backend/models"
	"net/http"
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
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
	var data models.Team
	data.TeamName = "TEST TEAM"
	data.TeamMembers = []string{"memberOne", "memberTwo"}

	json_data, _ := json.Marshal(data)

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

	teamData, _ := json.Marshal(res["data"].(map[string]interface{})["data"])
	var uTD models.Team
	json.NewDecoder(bytes.NewBuffer(teamData)).Decode(&uTD)

	assert.Equal(t, data.TeamName, uTD.TeamName)
	assert.Equal(t, data.TeamMembers, uTD.TeamMembers)

	// Clean Up
	req, _ = http.NewRequest("DELETE", url+"/"+fmt.Sprint(iID), bytes.NewBufferString(""))

	SetHeaders(req)

	resp, err = client.Do(req)

	if err != nil {
		assert.FailNow(t, err.Error())
	}

	json.NewDecoder(resp.Body).Decode(&res)

	assert.Equal(t, float64(200), res["status"])

}
