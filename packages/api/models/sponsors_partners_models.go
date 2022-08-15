package models

import "go.mongodb.org/mongo-driver/bson/primitive"

type Sponsors struct {
	ID             primitive.ObjectID `json:"id" bson:"_id,omitempty"`
	Company        string             `json:"company" validate:"required"`
	SocialLink     string             `json:"sociallink" validate:"required"`
	ProfilePicture string             `json:"profilepicture" validate:"required"`
}
