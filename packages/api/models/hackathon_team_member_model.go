package models

import "go.mongodb.org/mongo-driver/bson/primitive"

type TeamMember struct {
	ID                             primitive.ObjectID `json:"id" bson:"_id,omitempty"`
	FullName                       string             `json:"fullname" validate:"required"`
	HasTeam                        *bool              `json:"hasteam" validate:"required"`
	TeamName                       string             `json:"teamname"`
	Email                          string             `json:"email" validate:"required"`
	University                     string             `json:"university" validate:"required"`
	Age                            int                `json:"age" validate:"required"`
	Location                       string             `json:"location" validate:"required"`
	HeardAboutUs                   string             `json:"heardaboutus" validate:"required"`
	PreviousHackathonParticipation *bool              `json:"prevhackathonparticipation" validate:"required"`
	PreviousHackAUBGParticipation  *bool              `json:"prevhackaubgparticipation" validate:"required"`
	HasExperience                  *bool              `json:"hasexperience" validate:"required"`
	ProgrammingLevel               string             `json:"programminglevel" validate:"required"`
	StrongSides                    string             `json:"strongsides" validate:"required"`
	ShirtSize                      string             `json:"shirtsize" validate:"required"`
	WantInternship                 *bool              `json:"wantinternship" validate:"required"`
	JobInterests                   string             `json:"jobinterests" validate:"required"`
	ShareInfoWithSponsors          *bool              `json:"shareinfowithsponsors" validate:"required"`
	WantJobOffers                  *bool              `json:"wantjoboffers" validate:"required"`
}

type EditTeamMember struct {
	FullName                       string `json:"fullname"`
	HasTeam                        *bool  `json:"hasteam"`
	TeamName                       string `json:"teamname"`
	Email                          string `json:"email"`
	University                     string `json:"university"`
	Age                            int    `json:"age"`
	Location                       string `json:"location"`
	HeardAboutUs                   string `json:"heardaboutus"`
	PreviousHackathonParticipation *bool  `json:"prevhackathonparticipation"`
	PreviousHackAUBGParticipation  *bool  `json:"prevhackaubgparticipation"`
	HasExperience                  *bool  `json:"hasexperience"`
	ProgrammingLevel               string `json:"programminglevel"`
	StrongSides                    string `json:"strongsides"`
	ShirtSize                      string `json:"shirtsize"`
	WantInternship                 *bool  `json:"wantinternship"`
	JobInterests                   string `json:"jobinterests"`
	ShareInfoWithSponsors          *bool  `json:"shareinfowithsponsors"`
	WantJobOffers                  *bool  `json:"wantjoboffers"`
}
