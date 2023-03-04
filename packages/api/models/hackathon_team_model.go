package models

import "go.mongodb.org/mongo-driver/bson/primitive"

type Team struct {
	ID          primitive.ObjectID `json:"id" bson:"_id,omitempty"`
	TeamName    string             `json:"teamname" validate:"required"`
	TeamMembers []string           `json:"teammembers" validate:"required" `
}

type EditTeam struct {
	TeamName    string             `json:"teamname"`
	TeamMembers []string           `json:"teammembers"`
}
