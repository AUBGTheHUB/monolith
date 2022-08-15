package models

import "go.mongodb.org/mongo-driver/bson/primitive"

type Jury struct {
	ID             primitive.ObjectID `json:"id" bson:"_id,omitempty"`
	Firstname      string             `json:"firstname" validate:"required"`
	Lastname       string             `json:"lastname" validate:"required"`
	Company        string             `json:"company" validate:"required"`
	Position       string             `json:"position" validate:"required"`
	SocialLink     string             `json:"sociallink" validate:"required"`
	ProfilePicture string             `json:"profilepicture" validate:"required"`
}
