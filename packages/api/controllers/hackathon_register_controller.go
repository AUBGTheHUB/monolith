package controllers

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"hub-backend/models"
	"hub-backend/responses"
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

	isEligeble, getNubmerErr := IsTotalNumberOfParticipantsEligeble(c)

	if getNubmerErr != nil {
		return c.Status(http.StatusInternalServerError).JSON(responses.MemberResponse{Status: http.StatusInternalServerError, Message: "error", Data: &fiber.Map{"data": "Couldn't get number of participants, please contact TheHubAUBG"}})
	}

	if !isEligeble {
		return c.Status(http.StatusConflict).JSON(responses.MemberResponse{Status: http.StatusConflict, Message: "Max number of Hackathon participants is reached"})
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
	_, err := noTeamParticipantsCollection.InsertOne(ctx, newHackathonTeamMember)

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

func IsTotalNumberOfParticipantsEligeble(c *fiber.Ctx) (bool, error) {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	numberOfParticipantsWithTeam, err := GetNumberOfHackathonParticipants(ctx)
	if err != nil {
		return false, err
	}

	numberOfParticipantsWithoutTeam, err := GetNumberOfNoTeamParticipants(ctx)
	if err != nil {
		return false, err
	}

	result := numberOfParticipantsWithTeam + numberOfParticipantsWithoutTeam

	if result >= 90 {
		return false, nil
	}
	return true, nil
}

func CheckRegistrationAvailability(c *fiber.Ctx) error {

	isEligeble, getNubmerErr := IsTotalNumberOfParticipantsEligeble(c)

	if getNubmerErr != nil {
		return c.Status(http.StatusInternalServerError).JSON(responses.MemberResponse{Status: http.StatusInternalServerError, Message: "error", Data: &fiber.Map{"data": "Couldn't get number of participants, please contact TheHubAUBG"}})
	}

	if !isEligeble {
		return c.Status(http.StatusConflict).JSON(responses.MemberResponse{Status: http.StatusConflict, Message: "Max number of Hackathon participants is reached"})
	}

	return c.Status(http.StatusOK).JSON(responses.MemberResponse{Status: http.StatusOK, Message: "Registration avaliable"})
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

	//TODO: bruh Please somebody fix this html :D, Also maybe we should make a separeate issue for it.
	html := fmt.Sprintf(`<div class="container"
		style="max-width: 700px;  background-color: #fcfcff; padding-left: 30px; padding-right: 90px;">
		<br /><br />
		<h4><b> You registered for HackAUBG 5.0! <br /></b></h4>
		<br />
		Welcome on board, %s! <b>Text from Marketing.
		<br/>
		<br />

		Each team that takes part in HackAUBG 5.0 will have assigned a <b>facilitator</b> from The Hub. This will be the person to answer all your questions and help you out whenever you need assistance.
			We'll send you a follow-up email to introduce you to your facilitator and let you know what follows!
		<br />

		<br />
		We can't wait to meet you!

		<br />
		<br />
		<b>- The Hub AUBG</b>
		<br />
		<br />
		<a href="https://www.facebook.com/TheHubAUBG/" target="_blank" title="TheHubAUBG"><i class="fa fa-facebook" style="font-size: 25px; padding-right: 10px;"></i></a>
		<a href="https://www.instagram.com/thehubaubg/" target="_blank" title="TheHubAUBG"><i class="fa fa-instagram" style="font-size: 25px; padding-right: 10px;"></i></a>
		<a href="https://www.linkedin.com/company/the-hub-aubg" target="_blank" title="TheHubAUBG" style="padding-left:8px;"><i class="fa fa-linkedin" style="font-size: 25px; padding-right: 10px;"></i></a>
		<a href="https://www.youtube.com/channel/UChdtBZBvaK9XZurP3GjPDug" target="_blank" title="TheHubAUBG" style="padding-left:8px;"><i class="fa fa-youtube" style="font-size: 25px; padding-right: 10px;"></i></a>

		<br />
		<br />
	</div>

	<div class="container" style="max-width: 700px; background-color: #fcfcff; padding-right:0; margin-top: -100px; z-index: -1;">
		<img src="https://i.ibb.co/5Mw9Dzr/Robot.png" width="250"
				height="auto" alt="TheHubAUBG"
				style="display:block; border: none; max-width:230px; margin: 0 auto; margin-bottom: 0; margin-right:0;" />
	</div>

	<div class="container" style="max-height: 72px; height: 72px; background: linear-gradient(90deg, rgba(0,87,146,1) 0%, rgba(0,187,240,1) 100%); -webkit-border-bottom-right-radius: 72px;
	-moz-border-radius-bottomleft: 90px;
	border-bottom-right-radius: 72px;
	max-width: 700px;">
		<h5 class="text-center" style="vertical-align: middle;
	line-height: 72px; color: white; ">Learn &nbsp;•&nbsp; Innovate &nbsp;•&nbsp; Inspire</h5>
	</div>
	</div>
	<div class="container" style="margin-top: 15px; margin-bottom: 15px; max-width: 700px; font-size: 12px;
					line-height: 15px;
					text-align: center;
					color: black;
					max-width: 820px">
		<div class="text-center">Hub International &copy;, <br />2022</div>
	</div>`, firstName)

	reqBody.Html = html
	reqBody.Receiver = email
	reqBody.Subject = "Welcome to HackAUBG 5.0"

	json_data, _ := json.Marshal(reqBody)

	client := &http.Client{}

	req, err := http.NewRequest(http.MethodPost, requestURL, bytes.NewBuffer(json_data))

	if err != nil {
		fmt.Println("could not create request to mailing service: ")
		fmt.Print(err.Error())
		return
	}

	req.Header.Set("Authorization", mailingToken)
	req.Header.Set("Content-Type", "application/json")

	resp, err := client.Do(req)

	if err != nil {
		fmt.Println("error making http request to mailing service: ")
		fmt.Print(err.Error())
		return
	}

	var res map[string]interface{}

	json.NewDecoder(resp.Body).Decode(&res)

	fmt.Println(res["message"])

}
