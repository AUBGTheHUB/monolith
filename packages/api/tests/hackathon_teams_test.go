package tests

// TODO: Simulate an E2E registration workflow. Assert possible exceptions, such as 'full team', 'non-existing team', 'existing team' and etc.
// TODO: All req storing the API should use HTTP; responses should be Marshal; remove Nini's code, calling the API, which uses the package functions
// TODO: No usage of collections, they're set automatically
// TODO: Write only Team Endpoint tests in this file and each case should be in a different func; new files should be called x_test.go E2E_test.go

import (
	"bytes"
	"encoding/json"
	"hub-backend/app"
	"hub-backend/models"
	"net/http"
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
)

const url string = "http://127.0.0.1:8000/api/hackathon"

func SetHeaders(req *http.Request) {
	req.Header.Set("BEARER-TOKEN", "TEST_TOKEN")
	req.Header.Set("Content-Type", "application/json")
}

// TODO: Add another arg for num of members and make it return a slice
func GetMember(client http.Client, numberOfMembers int) string {
	var testBool bool = true
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

	json_data, _ := json.Marshal(dataMember)
	memberRequest, _ := http.NewRequest("POST", url+"/members", bytes.NewBuffer(json_data))

	SetHeaders(memberRequest)

	memberResponse, _ := client.Do(memberRequest)
	var memberResult map[string]interface{}
	json.NewDecoder(memberResponse.Body).Decode(&memberResult)

	memberResultID := memberResult["data"].(map[string]interface{})["data"].(map[string]interface{})["InsertedID"]

	return memberResultID.(string)
}

func GetTeamID(client http.Client, data models.Team) string {
	json_data, _ := json.Marshal(data)
	teamRequest, _ := http.NewRequest("POST", url+"/teams", bytes.NewBuffer(json_data))

	SetHeaders(teamRequest)

	teamResponse, _ := client.Do(teamRequest)
	var teamResult map[string]interface{}
	json.NewDecoder(teamResponse.Body).Decode(&teamResult)

	teamResultID := teamResult["data"].(map[string]interface{})["data"].(map[string]interface{})["InsertedID"]

	return teamResultID.(string)
}

// TODO: Fix return value of string, check if func works as intended
func CleanUp(client http.Client, data models.Team, res map[string]interface{}) (bool, string) {
	req, _ := http.NewRequest("DELETE", url+"/teams/"+GetTeamID(client, data), bytes.NewBufferString(""))

	SetHeaders(req)

	resp, err := client.Do(req)

	if err != nil {
		return false, err.Error()
	}

	json.NewDecoder(resp.Body).Decode(&res)
	if res["status"] == 200 {
		return true, ""
	}

	return false, ""
}

func TestPostTeamEndPoint(t *testing.T) {
	go app.StartApp()
	time.Sleep(5 * time.Second)

	var data models.Team
	client := &http.Client{}
	data.TeamName = "LookForTomAndYouWillFindJerrySuela2k23"
	data.TeamMembers = []string{GetMember(*client, 6)}
	json_data, _ := json.Marshal(data)
	// TODO: Check all cases => when empty, 1 or full
	req, _ := http.NewRequest("POST", url+"/teams", bytes.NewBuffer(json_data))

	SetHeaders(req)

	resp, err := client.Do(req)

	if err != nil {
		assert.FailNow(t, err.Error())
	}

	var res map[string]interface{}
	json.NewDecoder(resp.Body).Decode(&res)
	assert.Equal(t, float64(201), res["status"])
}
