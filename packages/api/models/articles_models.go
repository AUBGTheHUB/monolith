package models

import "go.mongodb.org/mongo-driver/bson/primitive"

type Article struct {
	ID         primitive.ObjectID `json:"id" bson:"_id,omitempty"`
	Title      string             `json:"title" validate:"required"`
	MediumLink string             `json:"mediumlink" validate:"required"`
	Author     string             `json:"author" validate:"required"`
	Banner     string             `json:"banner" validate:"required"`
}

type ArticleUpdate struct {
	Title      string `json:"title"`
	MediumLink string `json:"mediumlink"`
	Author     string `json:"author"`
	Banner     string `json:"banner"`
}
