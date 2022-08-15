package models

import "go.mongodb.org/mongo-driver/bson/primitive"

type Member struct {
	ID             primitive.ObjectID `json:"id" bson:"_id,omitempty"`
	Firstname      string             `json:"firstname, omitempty" validate:"required"`
	Lastname       string             `json:"lastname, omitempty" validate:"required"`
	Department     string             `json:"department, omitempty" validate:"required"`
	Position       string             `json:"position, omitempty" validate:"required"`
	SocialLink     string             `json:"sociallink, omitempty"`
	ProfilePicture string             `json:"profilepicture, omitempty" validate:"required"`
}

type EditMember struct {
	Firstname      string `json:"firstname"`
	Lastname       string `json:"lastname"`
	Department     string `json:"department"`
	Position       string `json:"position"`
	SocialLink     string `json:"sociallink"`
	ProfilePicture string `json:"profilepicture"`
}
