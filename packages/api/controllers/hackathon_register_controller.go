package controllers

import (
	"context"
	"fmt"
	"hub-backend/models"
	"hub-backend/responses"
	"net/http"
	"strings"
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

	hasTeam := newHackathonTeamMember.TeamNoTeam
	var actualTeamID string = ""

	if *hasTeam {
		results, _ := hackathonTeamCollection.Find(ctx, bson.M{})
		var nubmerOfTeams int = 0
		var team models.Team
		for results.Next(ctx){
			nubmerOfTeams++
			var res models.Team
			results.Decode(&res)
			if CompareTeamNames(res.TeamName, member.TeamName) {
				team = res
				actualTeamID = team.ID.Hex()
			}
		}
		
		if actualTeamID != "" {
			if len(team.TeamMembers) < 6  {
				team.TeamMembers = append(team.TeamMembers, newHackathonTeamMember.TeamName)
			}else{
				return c.Status(http.StatusBadRequest).JSON(responses.MemberResponse{Status: http.StatusBadRequest, Message: "Team's max capacity is reached"})
			}
		} else{
			if nubmerOfTeams < 15 {
			// actual team name = passed team name
			// create new team and assign member by id
			
			} else{
				return c.Status(http.StatusBadRequest).JSON(responses.MemberResponse{Status: http.StatusBadRequest, Message: "Max number of teams is reached"})
			}
		}
	} else {
		// assign member to list of no team participants
	}

	// create new member document
	
	return c.Status(http.StatusCreated).JSON(responses.MemberResponse{Status: http.StatusCreated, Message: "success"})
}

// func AddHackathonMemberToTeam(teamName string, fullname string) {
// 	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
// 	defer cancel()
// 	// var id string
// 	var results []models.Team
// 	// team_map := models.EditTeam{}

// 	cursor, _ := hackathonTeamCollection.Find(
// 		ctx,
// 		bson.D{},
// 	)

// 	_ = cursor.All(ctx, &results)

// 	fmt.Println("HERE", results)
// 	var teamID string = ""
// 	if len(results) > 0 {
// 		for _, result := range results {
// 			if CompareTeamNames(teamName, result.TeamName) {
// 				teamID = result.ID.String()
// 			}
// 		}

// 		fmt.Println(teamID)

// 		if teamID == "" {
// 			fmt.Println("No team found")
// 			// TODO: create new team
// 		}
// 	}

// }

func FormatTeamName(teamName string) string {
	return strings.ToLower(strings.ReplaceAll(teamName, " ", ""))
}

func CompareTeamNames(passedTeamName string, storedTeamName string) bool {
	return FormatTeamName(passedTeamName) == FormatTeamName(storedTeamName)
}
