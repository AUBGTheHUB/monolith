package models

import "go.mongodb.org/mongo-driver/bson/primitive"

type TeamMember struct {
	ID                            primitive.ObjectID `json:"id" bson:"_id,omitempty"`
	FullName                      string             `json:"fullname" validate:"required"`
	TeamNoTeam                    *bool              `json:"hasteam" validate:"required"`
	TeamName                      string             `json:"teamname"`
	Email                         string             `json:"email" validate:"required"`
	School                        string             `json:"university" validate:"required"`
	Age                           int                `json:"age" validate:"required"`
	Location                      string             `json:"location" validate:"required"`
	HeardAboutUs                  string             `json:"heardaboutus" validate:"required"`
	PreviousParticipation         *bool              `json:"prevhackathonparticipation" validate:"required"`
	PreviousHackAUBGParticipation *bool              `json:"prevhackaubgparticipation" validate:"required"`
	Experience                    *bool              `json:"hasexperience" validate:"required"`
	ProgrammingLevel              string             `json:"programminglevel" validate:"required"`
	StrongSides                   string             `json:"strongsides" validate:"required"`
	ShirtSize                     string             `json:"shirtsize" validate:"required"`
	Internship                    *bool              `json:"wantinternship" validate:"required"`
	JobInterests                  string             `json:"jobinterests" validate:"required"`
	SponsorShare                  *bool              `json:"shareinfowithsponsors" validate:"required"`
	NewsLetter                    *bool              `json:"wantjoboffers" validate:"required"`
}

type EditTeamMember struct {
	FullName              string `json:"fullname"`
	TeamNoTeam            bool   `json:"teamnoteam"`
	TeamName              string `json:"teamname"`
	Email                 string `json:"email"`
	School                string `json:"school"`
	Age                   int    `json:"age"`
	Location              string `json:"location"`
	HeardAboutUs          string `json:"aboutus"`
	PreviousParticipation *bool  `json:"previouspart"`
	PartDetails           string `json:"partdetails"`
	Experience            *bool  `json:"experience"`
	ProgrammingLevel      string `json:"level"`
	StrongSides           string `json:"strength"`
	ShirtSize             string `json:"size"`
	Internship            *bool  `json:"internship"`
	JobInterests          string `json:"jobinterests"`
	SponsorShare          *bool  `json:"sponsorshare"`
	NewsLetter            *bool  `json:"newsletter"`
}
