package configs

import (
	"context"
	"log"
	"strings"
	"time"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

func ConnectDB() *mongo.Client {
	client, err := mongo.NewClient(options.Client().ApplyURI(EnvMongoURI()))

	if err != nil {
		log.Fatal(err)
	}

	ctx, _ := context.WithTimeout(context.Background(), 10*time.Second)
	err = client.Connect(ctx)

	if err != nil {
		log.Fatal("Context timeout")
	}

	err = client.Ping(ctx, nil)
	if err != nil {
		log.Fatal(err)
	}

	return client
}

var DB *mongo.Client = ConnectDB()

func GetCollection(client *mongo.Client, collectionName string) *mongo.Collection {
	if IsTestENV() {
		collectionName = "_tests_"+collectionName
	}

	collection := client.Database("TheHubDB").Collection(collectionName)
	return collection
}

func GetCollectionsStartingWith(client *mongo.Client, prefix string) []*mongo.Collection {
	var collections []*mongo.Collection

	result, err := client.Database("TheHubDB").ListCollectionNames(context.Background(), bson.M{})

	if err != nil {
		log.Fatal(err)
	}

	for _, coll := range result {
		if strings.HasPrefix(coll, prefix) {
			collection := client.Database("TheHubDB").Collection(coll)
			collections = append(collections, collection)
		}
	}

	return collections
}
