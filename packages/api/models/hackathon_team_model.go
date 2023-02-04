package models

import "go.mongodb.org/mongo-driver/bson/primitive"

type Team struct {
	ID          primitive.ObjectID `json:"id" bson:"_id,omitempty"`
	TeamName    string             `json:"teamname" validate:"required"`
	TeamMembers []string           `json:"teammember" validate:"required" `
}

type EditTeam struct {
	ID          primitive.ObjectID `json:"id" bson:"_id,omitempty"`
	TeamName    string             `json:"teamname" validate:"required`
	TeamMembers []TeamMember       `json:"teammember" validate:"required`
}
