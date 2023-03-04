package controllers

import (
	"bytes"
	"context"
	"fmt"
	"hub-backend/models"
	"hub-backend/responses"
	"io"
	"net/http"
	"os"
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
		FullName:              member.FullName,
		TeamNoTeam:            member.TeamNoTeam,
		TeamName:              member.TeamName,
		Email:                 member.Email,
		School:                member.School,
		Age:                   member.Age,
		Location:              member.Location,
		HeardAboutUs:          member.HeardAboutUs,
		PreviousParticipation: member.PreviousParticipation,
		Experience:            member.Experience,
		ProgrammingLevel:      member.ProgrammingLevel,
		StrongSides:           member.StrongSides,
		ShirtSize:             member.ShirtSize,
		Internship:            member.Internship,
		JobInterests:          member.JobInterests,
		SponsorShare:          member.SponsorShare,
		NewsLetter:            member.NewsLetter}

	numberOfMembers, _ := GetNumberOfHackathonParticipants(ctx)
	numberOfTeams, _ := GetNumberOfHackathonTeams(ctx)

	if numberOfMembers >= 90 {
		return c.Status(http.StatusConflict).JSON(responses.MemberResponse{Status: http.StatusConflict, Message: "Max Hackathon participants is reached"})
	}

	if CheckIfTeamMemberExists(newHackathonTeamMember) {
		return c.Status(http.StatusBadRequest).JSON(responses.MemberResponse{Status: http.StatusBadRequest, Message: "This email is already present in the DB", Data: &fiber.Map{"data": newHackathonTeamMember.Email}})
	}

	hasTeam := newHackathonTeamMember.TeamNoTeam

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

					go SendEmailToNewParticipant(newHackathonTeamMember.FullName, newHackathonTeamMember.Email)

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
			go SendEmailToNewParticipant(newHackathonTeamMember.FullName, newHackathonTeamMember.Email)

			return c.Status(http.StatusCreated).JSON(responses.MemberResponse{Status: http.StatusCreated, Message: "New team created", Data: &fiber.Map{"data": result}})
		}
	}

	if CheckIfNoTeamParticipantExists(newHackathonTeamMember) {
		return c.Status(http.StatusBadRequest).JSON(responses.MemberResponse{Status: http.StatusBadRequest, Message: "This email is already present in the DB", Data: &fiber.Map{"data": newHackathonTeamMember.Email}})
	}

	// Add participant to collection of participants without team
	_, err := noTeamParticipantsCollection.InsertOne(ctx, newHackathonTeamMember)

	if err != nil {
		return c.Status(http.StatusInternalServerError).JSON(responses.MemberResponse{Status: http.StatusInternalServerError, Message: "error", Data: &fiber.Map{"data": err.Error()}})
	}

	// return success code participant added to no team list and created
	return c.Status(http.StatusCreated).JSON(responses.MemberResponse{Status: http.StatusCreated, Message: "Partcipant added to particapnts without team collection"})

}

func FormatTeamName(teamName string) string {
	return strings.ToLower(strings.ReplaceAll(teamName, " ", ""))
}

func CompareTeamNames(passedTeamName string, storedTeamName string) bool {
	return FormatTeamName(passedTeamName) == FormatTeamName(storedTeamName)
}

func SendEmailToNewParticipant(fullName string, email string) {
	requestURL := "https://europe-west3-cloudservices-378314.cloudfunctions.net/mailer"

	emailBody := fmt.Sprintf(`{
		"html": "<h1>Hello %s, This is the body of the email</h1>",
		"subject": "Welcome to HackAUBG", 
		"receiver": %s}`, fullName, email)
	//TODO: Fix parsing. When hardcoded email is passed func works, when it is with %s string it doesn't
	jsonBody := []byte(emailBody)
	bodyReader := bytes.NewReader(jsonBody)

	client := &http.Client{}

	req, err := http.NewRequest(http.MethodPost, requestURL, bodyReader)

	if err != nil {
		fmt.Println("could not create request to mailing service: ")
		fmt.Print(err.Error())
	}

	mailingToken := os.Getenv("MAILING_TOKEN")
	req.Header.Set("Authorization", mailingToken)
	req.Header.Set("Content-Type", "application/json")

	resp, err := client.Do(req)

	if err != nil {
		fmt.Println("error making http request to mailing service: ")
		fmt.Print(err.Error())
	}

	fmt.Println("email was sent to parcipant: ")
	defer resp.Body.Close()
	body, err := io.ReadAll(resp.Body)
	fmt.Println(string(body))
}
