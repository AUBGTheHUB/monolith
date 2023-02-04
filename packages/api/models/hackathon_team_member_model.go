package models

import "go.mongodb.org/mongo-driver/bson/primitive"

type TeamMember struct {
	ID                    primitive.ObjectID `json:"id" bson:"_id,omitempty"`
	FullName              string             `json:"fullname, omitempty" validate:"required"`
	TeamNoTeam            bool               `json:"teamnoteam, omitempty" validate:"required"`
	TeamName              string             `json:"teamname, omitempty" validate:"required"`
	Email                 string             `json:"email" validate:"required"`
	School                string             `json:"school, omitempty" validate:"required"`
	Age                   int                `json:"age, omitempty" validate:"required"`
	Location              string             `json:"location, omitempty" validate:"required"`
	HeardAboutUs          string             `json:"aboutus, omitempty" validate:"required"`
	PreviousParticipation bool               `json:"previouspart, omitempty" validate:"required"`
	PartDetails           string             `json:"partdetails" validate:"required"`
	Experience            bool               `json:"experience, omitempty" validate:"required"`
	ProgrammingLevel      string             `json:"level" validate:"required"`
	StrongSides           string             `json:"strength" validate:"required"`
	ShirtSize             string             `json:"size, omitempty" validate:"required"`
	Internship            bool               `json:"internship" validate:"required"`
	JobInterests          string             `json:"jobinterests" validate:"required"`
	SponsorShare          bool               `json:"sponsorshare, omitempty" validate:"required"`
	NewsLetter            bool               `json:"location, omitempty" validate:"required"`
}

type EditTeamMember struct {
	FullName   string `json:"fullname"`
	TeamNoTeam bool   `json: "teamnoteam"`
	TeamName   string `json:"teamname"`
	Email      string `json:"email"`
	School     string `json:"school"`
	Age        int    `json:"age"`
	Location   string `json:"location"`
	ShirtSize  string `json:"size"`
}
