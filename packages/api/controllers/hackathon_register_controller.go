package controllers

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"hub-backend/models"
	"hub-backend/responses"
	"io/ioutil"
	"net/http"
	"os"
	"path"
	"path/filepath"
	"runtime"
	"strings"
	"time"

	"github.com/gofiber/fiber/v2"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
)

func RegisterTeamMember(c *fiber.Ctx) error {

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	var member models.TeamMember
	defer cancel()

	// validate request body
	if err := c.BodyParser(&member); err != nil {
		return c.Status(http.StatusBadRequest).JSON(responses.MemberResponse{Status: http.StatusBadRequest, Message: "error", Data: &fiber.Map{"data": err.Error()}})
	}

	if validationErr := validateTeamMembers.Struct(&member); validationErr != nil {
		return c.Status(http.StatusBadRequest).JSON(responses.MemberResponse{Status: http.StatusBadRequest, Message: "error", Data: &fiber.Map{"data": validationErr.Error()}})
	}

	newHackathonTeamMember := models.TeamMember{
		FullName:                       member.FullName,
		HasTeam:                        member.HasTeam,
		TeamName:                       member.TeamName,
		Email:                          member.Email,
		University:                     member.University,
		Age:                            member.Age,
		Location:                       member.Location,
		HeardAboutUs:                   member.HeardAboutUs,
		PreviousHackathonParticipation: member.PreviousHackathonParticipation,
		PreviousHackAUBGParticipation:  member.PreviousHackAUBGParticipation,
		HasExperience:                  member.HasExperience,
		ProgrammingLevel:               member.ProgrammingLevel,
		StrongSides:                    member.StrongSides,
		ShirtSize:                      member.ShirtSize,
		WantInternship:                 member.WantInternship,
		JobInterests:                   member.JobInterests,
		ShareInfoWithSponsors:          member.ShareInfoWithSponsors,
		WantJobOffers:                  member.WantJobOffers}

	numberOfTeams, _ := GetNumberOfHackathonTeams(ctx)

	err := IsRegistrationAvailable(c)

	if err != nil {
		return err
	}

	if CheckIfTeamMemberExists(newHackathonTeamMember) {
		return c.Status(http.StatusBadRequest).JSON(responses.MemberResponse{Status: http.StatusBadRequest, Message: "This email is already present in the DB", Data: &fiber.Map{"data": newHackathonTeamMember.Email}})
	}

	if CheckIfNoTeamParticipantExists(newHackathonTeamMember) {
		return c.Status(http.StatusBadRequest).JSON(responses.MemberResponse{Status: http.StatusBadRequest, Message: "This email is already present in the DB", Data: &fiber.Map{"data": newHackathonTeamMember.Email}})
	}

	hasTeam := newHackathonTeamMember.HasTeam

	if *hasTeam {

		results, _ := hackathonTeamCollection.Find(ctx, bson.M{})

		for results.Next(ctx) {

			var team models.Team
			results.Decode(&team)

			//Finds if a team exists in the DB by comparing passed teamName from particapnt to teamNames in DB
			if CompareTeamNames(team.TeamName, member.TeamName) {

				if len(team.TeamMembers) < 6 {

					//Sets the correct teamName for particiapnt (the one in the DB)
					member.TeamName = team.TeamName
					actualTeamID, _ := primitive.ObjectIDFromHex(team.ID.Hex())

					//Creates new participant in the DB
					resultFromInsertingTeamMemberToDB, createErr := CreateNewHackathonParticipant(ctx, newHackathonTeamMember)
					memberID := resultFromInsertingTeamMemberToDB.InsertedID.(primitive.ObjectID).Hex()

					if createErr != nil {
						return c.Status(http.StatusInternalServerError).JSON(responses.MemberResponse{Status: http.StatusInternalServerError, Message: "error", Data: &fiber.Map{"data": createErr.Error()}})
					}

					//Add new participant to rescpective team in the DB
					_, updateErr := hackathonTeamCollection.UpdateOne(ctx, bson.M{"_id": actualTeamID}, bson.M{"$push": bson.M{"teammembers": memberID}})

					if updateErr != nil {
						return c.Status(http.StatusInternalServerError).JSON(responses.MemberResponse{Status: http.StatusInternalServerError, Message: "error", Data: &fiber.Map{"data": updateErr.Error()}})
					}

					go SendEmailToNewParticipant(newHackathonTeamMember.FullName, newHackathonTeamMember.Email, c.Query("string"))

					return c.Status(http.StatusCreated).JSON(responses.MemberResponse{Status: http.StatusCreated, Message: "Partcipant added to existing team"})
				}

				return c.Status(http.StatusConflict).JSON(responses.MemberResponse{Status: http.StatusConflict, Message: "Team's max capacity is reached"})
			}
		}

		if numberOfTeams < 15 {

			//Creates new participant in the DB
			resultFromInsertingTeamMemberToDB, createErr := CreateNewHackathonParticipant(ctx, newHackathonTeamMember)

			if createErr != nil {
				return c.Status(http.StatusInternalServerError).JSON(responses.MemberResponse{Status: http.StatusInternalServerError, Message: "error", Data: &fiber.Map{"data": createErr.Error()}})
			}

			//Creates new Team in the DB with first member the new participant
			var newTeam models.Team
			memberID := resultFromInsertingTeamMemberToDB.InsertedID.(primitive.ObjectID).Hex()
			newTeam.TeamName = newHackathonTeamMember.TeamName

			newTeam.TeamMembers = append(newTeam.TeamMembers, memberID)
			result, err := hackathonTeamCollection.InsertOne(ctx, newTeam)

			if err != nil {
				err := DeleteHackathonMember(c, memberID)
				if err != nil {
					return c.Status(http.StatusInternalServerError).JSON(responses.MemberResponse{Status: http.StatusInternalServerError, Message: "error", Data: &fiber.Map{"data": "Failed deleting member when create team has failed"}})
				}
				return c.Status(http.StatusInternalServerError).JSON(responses.MemberResponse{Status: http.StatusInternalServerError, Message: "error", Data: &fiber.Map{"data": "Couldn't create team"}})
			}
			go SendEmailToNewParticipant(newHackathonTeamMember.FullName, newHackathonTeamMember.Email, c.Query("testing"))

			return c.Status(http.StatusCreated).JSON(responses.MemberResponse{Status: http.StatusCreated, Message: "New team created", Data: &fiber.Map{"data": result}})
		}

		return c.Status(http.StatusConflict).JSON(responses.MemberResponse{Status: http.StatusConflict, Message: "Max number of teams in the hackathon is reached"})
	}

	// Add participant to collection of participants without team
	_, err = noTeamParticipantsCollection.InsertOne(ctx, newHackathonTeamMember)

	if err != nil {
		return c.Status(http.StatusInternalServerError).JSON(responses.MemberResponse{Status: http.StatusInternalServerError, Message: "error", Data: &fiber.Map{"data": err.Error()}})
	}

	go SendEmailToNewParticipant(newHackathonTeamMember.FullName, newHackathonTeamMember.Email, c.Query("testing"))

	// return success code participant added to no team list and created
	return c.Status(http.StatusCreated).JSON(responses.MemberResponse{Status: http.StatusCreated, Message: "Partcipant added to particapnts without team collection"})

}

func FormatTeamName(teamName string) string {
	return strings.ToLower(strings.ReplaceAll(teamName, " ", ""))
}

func CompareTeamNames(passedTeamName string, storedTeamName string) bool {
	return FormatTeamName(passedTeamName) == FormatTeamName(storedTeamName)
}

func IsRegistrationAvailable(c *fiber.Ctx) error {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	var regErr responses.MemberResponse

	numberOfParticipantsWithTeam, err := GetNumberOfHackathonParticipants(ctx)
	if err != nil {
		var err fiber.Error
		err.Code = 503

		regErr.Message = "Couldn't get number of participants with a team, please contact TheHubAUBG"
		regErr.Status = 503

		message, _ := json.Marshal(regErr)
		err.Message = string(message)

		return &err
	}

	numberOfParticipantsWithoutTeam, err := GetNumberOfNoTeamParticipants(ctx)

	if err != nil {
		var err fiber.Error
		err.Code = 503

		regErr.Message = "Couldn't get number of participants without a team, please contact TheHubAUBG"
		regErr.Status = 503

		message, _ := json.Marshal(regErr)
		err.Message = string(message)

		return &err
	}

	if numberOfParticipantsWithTeam+numberOfParticipantsWithoutTeam >= 90 {
		var err fiber.Error
		err.Code = 503

		regErr.Message = "Max capacity of participans is reached"
		regErr.Status = 503

		message, _ := json.Marshal(regErr)
		err.Message = string(message)

		return &err
	}

	return c.SendStatus(http.StatusOK)

}

func SendEmailToNewParticipant(fullName string, email string, testing string) {

	if testing == "true" {
		return
	}

	requestURL := os.Getenv("MAILING_URL")
	mailingToken := os.Getenv("MAILING_TOKEN")

	type Mailer struct {
		Receiver string `json:"receiver"`
		Html     string `json:"html"`
		Subject  string `json:"subject"`
	}

	var reqBody Mailer

	firstName := strings.Split(fullName, " ")[0]
	_, base, _, _ := runtime.Caller(0)
	root := filepath.Join(filepath.Dir(base), "..")
	html_file := path.Join(root, "email_template.html")
	html_bytes, err := ioutil.ReadFile(html_file)

	if err != nil {
		fmt.Println("Error loading html")
		fmt.Println(err)
		return
	}
	html_string := string(html_bytes)

	html := fmt.Sprintf(html_string, firstName)

	reqBody.Html = html
	reqBody.Receiver = email
	reqBody.Subject = "Welcome to HackAUBG 5.0"

	json_data, _ := json.Marshal(reqBody)

	client := &http.Client{}

	req, err := http.NewRequest(http.MethodPost, requestURL, bytes.NewBuffer(json_data))

	if err != nil {
		fmt.Println("Could not build mailing request")
		fmt.Print(err)
		return
	}

	req.Header.Set("Authorization", mailingToken)
	req.Header.Set("Content-Type", "application/json")

	resp, err := client.Do(req)

	if err != nil {
		fmt.Println("Failed making mailing request")
		fmt.Print(err)
		return
	}

	var res map[string]interface{}

	json.NewDecoder(resp.Body).Decode(&res)

	fmt.Println(res["message"])

}
