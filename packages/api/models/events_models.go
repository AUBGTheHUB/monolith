package models

import (
	"time"

	"go.mongodb.org/mongo-driver/bson/primitive"
)

type Event struct {
	ID           primitive.ObjectID `json:"id" bson:"_id,omitempty"`
	Title        string             `json:"title"`
	StartDate    time.Time          `json:"startdate"`    // should be converted to ISO in frontend
	EndDate      time.Time          `json:"enddate"`      // --||--
	Description  string             `json:"description"`  // long string
	Location     string             `json:"location"`     // location in text
	LocationLink string             `json:"locationlink"` // location google maps link
	Banner       string             `json:"banner"`       // banner image google drive link
	FacebookLink string             `json:"facebooklink"`
}
