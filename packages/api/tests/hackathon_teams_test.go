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

	type Member struct {
		FullName                       string `json:"fullname" validate:"required"`
		HasTeam                        bool   `json:"hasteam" validate:"required"`
		TeamName                       string `json:"teamname" validate:"required"`
		Email                          string `json:"email" validate:"required"`
		University                     string `json:"university" validate:"required"`
		Age                            int    `json:"age" validate:"required"`
		Location                       string `json:"location" validate:"required"`
		HeardAboutUs                   string `json:"heardaboutus" validate:"required"`
		PreviousHackathonParticipation bool   `json:"prevhackathonparticipation" validate:"required"`
		PreviousHackAUBGParticipation  bool   `json:"prevhackaubgparticipation" validate:"required"`
		HasExperience                  bool   `json:"hasexperience" validate:"required"`
		ProgrammingLevel               string `json:"programminglevel" validate:"required"`
		StrongSides                    string `json:"strongsides" validate:"required"`
		ShirtSize                      string `json:"shirtsize" validate:"required"`
		WantInternship                 bool   `json:"wantinternship" validate:"required"`
		JobInterests                   string `json:"jobinterests" validate:"required"`
		ShareInfoWithSponsors          bool   `json:"shareinfowithsponsors" validate:"required"`
		WantJobOffers                  bool   `json:"wantjoboffers" validate:"required"`
	}

	dataMember := Member{
		FullName:                       "Test",
		HasTeam:                        true,
		TeamName:                       "Integration Test",
		Email:                          "integration_test@gmail.com",
		University:                     "Test School",
		Age:                            18,
		Location:                       "Test Location",
		HeardAboutUs:                   "Test",
		PreviousHackathonParticipation: true,
		PreviousHackAUBGParticipation:  true,
		HasExperience:                  true,
		ProgrammingLevel:               "Test",
		StrongSides:                    "Test",
		ShirtSize:                      "Test",
		WantInternship:                 true,
		JobInterests:                   "Test",
		ShareInfoWithSponsors:          true,
		WantJobOffers:                  true,
	}

	fmt.Println(dataMember)

	client := &http.Client{}

	// * CREATE NEW MEMBER
	json_data, _ := json.Marshal(dataMember)
	req, _ := http.NewRequest("POST", "http://127.0.0.1:8000/api/hackathon/members", bytes.NewBuffer(json_data))
	SetHeaders(req)

	resp, err := client.Do(req)

	if err != nil {
		assert.FailNow(t, err.Error())
	}

	var res map[string]interface{}
	json.NewDecoder(resp.Body).Decode(&res)

	fmt.Println(res)

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
