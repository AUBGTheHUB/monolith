package tests

import (
	"bytes"
	"encoding/json"
	"fmt"
	"hub-backend/app"
	"hub-backend/configs"
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

	client := &http.Client{}

	// * CREATE NEW MEMBER
	var falseBool bool = false

	dataMember := models.TeamMember{
		FullName:                       "Test",
		HasTeam:                        &falseBool,
		TeamName:                       "Integration Test",
		Email:                          configs.GenerateToken(10) + "@gmail.com",
		University:                     "Test School",
		Age:                            18,
		Location:                       "Test Location",
		HeardAboutUs:                   "Test",
		PreviousHackathonParticipation: &falseBool,
		PreviousHackAUBGParticipation:  &falseBool,
		HasExperience:                  &falseBool,
		ProgrammingLevel:               "Test",
		StrongSides:                    "Test",
		ShirtSize:                      "Test",
		WantInternship:                 &falseBool,
		JobInterests:                   "Test",
		ShareInfoWithSponsors:          &falseBool,
		WantJobOffers:                  &falseBool,
	}

	json_data, _ := json.Marshal(dataMember)
	req, _ := http.NewRequest("POST", "http://127.0.0.1:8000/api/hackathon/members", bytes.NewBuffer(json_data))
	SetHeaders(req)

	resp, err := client.Do(req)

	if err != nil {
		assert.FailNow(t, err.Error())
	}

	var res map[string]interface{}
	json.NewDecoder(resp.Body).Decode(&res)

	assert.Equal(t, float64(201), res["status"])
	memberId := res["data"].(map[string]interface{})["data"].(map[string]interface{})["InsertedID"]

	// * CREATE NEW TEAM
	var dataTeam models.Team
	dataTeam.TeamName = "INTEGRATION TEST TEAM"
	dataTeam.TeamMembers = []string{fmt.Sprint(memberId)}

	json_data, _ = json.Marshal(dataTeam)

	req, _ = http.NewRequest("POST", url, bytes.NewBuffer(json_data))
	SetHeaders(req)

	resp, err = client.Do(req)

	if err != nil {
		assert.FailNow(t, err.Error())
	}

	json.NewDecoder(resp.Body).Decode(&res)

	assert.Equal(t, float64(201), res["status"])

	iID := res["data"].(map[string]interface{})["data"].(map[string]interface{})["InsertedID"]

	// * VERIFY CREATE TEAM AND POPULATED MEMBER LIST
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

	assert.Equal(t, dataTeam.TeamName, uTD.TeamName)
	assert.Equal(t, dataTeam.TeamMembers, uTD.TeamMembers)

	// * CLEAN UP TEAM ENTRY
	req, _ = http.NewRequest("DELETE", url+"/"+fmt.Sprint(iID), bytes.NewBufferString(""))
	SetHeaders(req)

	resp, err = client.Do(req)

	if err != nil {
		assert.FailNow(t, err.Error())
	}

	json.NewDecoder(resp.Body).Decode(&res)

	assert.Equal(t, float64(200), res["status"])

	// * CLEAN UP MEMBER ENTRY
	req, _ = http.NewRequest("DELETE", "http://127.0.0.1:8000/api/hackathon/members"+"/"+fmt.Sprint(memberId), bytes.NewBufferString(""))
	SetHeaders(req)

	resp, err = client.Do(req)

	if err != nil {
		assert.FailNow(t, err.Error())
	}

	json.NewDecoder(resp.Body).Decode(&res)

	assert.Equal(t, float64(200), res["status"])
}
