package models

import "go.mongodb.org/mongo-driver/bson/primitive"

type TeamMember struct {
	ID                    primitive.ObjectID `json:"id" bson:"_id,omitempty"`
	FullName              string             `json:"fullname, omitempty" validate:"required"`
	TeamNoTeam            bool               `json:"teamnoteam, omitempty"`
	TeamName              string             `json:"teamname, omitempty" validate:"required"`
	Email                 string             `json:"email" validate:"required"`
	School                string             `json:"school, omitempty"`
	Age                   int                `json:"age, omitempty"`
	Location              string             `json:"location, omitempty"`
	HeardAboutUs          string             `json:"aboutus, omitempty"`
	PreviousParticipation bool               `json:"previouspart, omitempty"`
	PartDetails           string             `json:"partdetails"`
	Experience            bool               `json:"experience, omitempty"`
	ProgrammingLevel      string             `json:"level"`
	StrongSides           string             `json:"strength"`
	ShirtSize             string             `json:"size, omitempty"`
	Internship            bool               `json:"internship"`
	JobInterests          string             `json:"jobinterests"`
	SponsorShare          bool               `json:"sponsorshare, omitempty"`
	NewsLetter            bool               `json:"location, omitempty"`
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
