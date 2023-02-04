package models

import "go.mongodb.org/mongo-driver/bson/primitive"

type Team struct{
	ID         		primitive.ObjectID 		`json:"id" bson:"_id,omitempty"`
	teamName 		string  				`json:"teamname"`
	teamMembers 	TeamMember[]			`json:"teammember"`
}

type EditTeam{
	ID         		primitive.ObjectID 		`json:"id" bson:"_id,omitempty"`
	teamName 		string  				`json:"teamname"`
	teamMembers 	TeamMember[]			`json:"teammember"`
}


