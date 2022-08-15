package models

import "go.mongodb.org/mongo-driver/bson/primitive"

type Job struct {
	ID          primitive.ObjectID `json:"id" bson:"_id,omitempty"`
	Position    string             `json:"position"`
	Company     string             `json:"company"`
	Description string             `json:"description"`
	Link        string             `json:"link"`
}
