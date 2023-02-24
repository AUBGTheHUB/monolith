package controllers

import (
	"context"
	"encoding/json"
	"fmt"
	"hub-backend/models"
	"hub-backend/responses"
	"net/http"
	"time"

	"github.com/gofiber/fiber/v2"
	"go.mongodb.org/mongo-driver/bson"
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

	if newHackathonTeamMember.TeamNoTeam {
		cursor, _ := teamMembersCollection.Find(
			ctx, bson.D{{"teamname", newHackathonTeamMember.TeamName}},
		)
		var results []models.TeamMember

		_ = cursor.All(ctx, &results)

		if len(results) > 0 {
			AddHackathonMemberToTeam(newHackathonTeamMember.TeamName)
		}else {
			//TODO: Add new team and add current hackathon member to that team
		}
	}else{
		//TODO: Add current hackathon memberto a list of members without teams
	}
	return c.Status(http.StatusCreated).JSON(responses.MemberResponse{Status: http.StatusCreated, Message: "success"})
}

func AddHackathonMemberToTeam(teamName string) {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	var results []models.Team
	// team_map := models.EditTeam{}

	cursor, _ := hackathonTeamCollection.Find(
		ctx,
		bson.D{{"teamname", teamName}},
	)
	_ = cursor.All(ctx, &results)
	if len(results) > 0 {
		for _, result := range results {
			res, _ := json.Marshal(result)
			fmt.Println(string(res))
			// TODO: Get only ObjectID in order to make a PUT request to add the hackathon member to the array of teammembers for the current team
		}
	}
}
