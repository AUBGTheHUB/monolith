package controllers

import (
	"context"
	"hub-backend/models"
	"hub-backend/responses"
	"net/http"
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
		PartDetails:           member.PartDetails,
		Experience:            member.Experience,
		ProgrammingLevel:      member.ProgrammingLevel,
		StrongSides:           member.StrongSides,
		ShirtSize:             member.ShirtSize,
		Internship:            member.Internship,
		JobInterests:          member.JobInterests,
		SponsorShare:          member.SponsorShare,
		NewsLetter:            member.NewsLetter}

	hasTeam := newHackathonTeamMember.TeamNoTeam
	var actualTeamID string = ""

	if CheckIfTeamMemberExists(newHackathonTeamMember) {
		return c.Status(http.StatusBadRequest).JSON(responses.MemberResponse{Status: http.StatusBadRequest, Message: "This email is already present in the DB", Data: &fiber.Map{"data": newHackathonTeamMember.Email}})
	}
	resultFromInsertingTeamMemberToDB, err := teamMembersCollection.InsertOne(ctx, newHackathonTeamMember)

	if err != nil {
		return c.Status(http.StatusInternalServerError).JSON(responses.MemberResponse{Status: http.StatusInternalServerError, Message: "error", Data: &fiber.Map{"data": err.Error()}})
	}

	if *hasTeam {
		results, _ := hackathonTeamCollection.Find(ctx, bson.M{})
		var nubmerOfTeams int = 0
		var team models.Team
		for results.Next(ctx) {
			nubmerOfTeams++
			var res models.Team
			results.Decode(&res)
			if CompareTeamNames(res.TeamName, member.TeamName) {
				team = res
				actualTeamID = team.ID.Hex()
			}
		}

		if actualTeamID != "" {
			if len(team.TeamMembers) < 6 {
				key_from_hex, _ := primitive.ObjectIDFromHex(actualTeamID)
				hackathonTeamCollection.UpdateOne(ctx, bson.M{"_id": key_from_hex}, bson.M{"$push": bson.M{"teammembers": resultFromInsertingTeamMemberToDB.InsertedID.(primitive.ObjectID).Hex()}})
				return c.Status(http.StatusCreated).JSON(responses.MemberResponse{Status: http.StatusCreated, Message: "Partcipant added to existing team"})
			} else {
				return c.Status(http.StatusBadRequest).JSON(responses.MemberResponse{Status: http.StatusBadRequest, Message: "Team's max capacity is reached"})
			}
		} else {
			if nubmerOfTeams < 15 {
				//Creates new Team in the DB with first member the new participant
				var newTeam models.Team
				newTeam.TeamName = newHackathonTeamMember.TeamName
				newTeam.TeamMembers = append(newTeam.TeamMembers, resultFromInsertingTeamMemberToDB.InsertedID.(primitive.ObjectID).Hex())
				result, _ := hackathonTeamCollection.InsertOne(ctx, newTeam)

				return c.Status(http.StatusCreated).JSON(responses.MemberResponse{Status: http.StatusCreated, Message: "New team created", Data: &fiber.Map{"data": result}})

			} else {
				return c.Status(http.StatusBadRequest).JSON(responses.MemberResponse{Status: http.StatusBadRequest, Message: "Max number of teams is reached"})
			}
		}
	} else {
		// assign member to list of no team participants
	}

	// create new member document

	return c.Status(http.StatusCreated).JSON(responses.MemberResponse{Status: http.StatusCreated, Message: "success"})
}

func FormatTeamName(teamName string) string {
	return strings.ToLower(strings.ReplaceAll(teamName, " ", ""))
}

func CompareTeamNames(passedTeamName string, storedTeamName string) bool {
	return FormatTeamName(passedTeamName) == FormatTeamName(storedTeamName)
}
