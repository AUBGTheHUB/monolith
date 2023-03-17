package tests

import (
	"context"
	"hub-backend/configs"
	"log"
	"os"
	"time"
)

func IsTestEnv() {
	if !configs.IsTestENV() {
		log.Fatalf("IS_TEST is missing or false!")
	}

	os.Exit(1)
}

func CleanUpCollection() {
	collections := configs.GetCollectionsStartingWith(configs.DB, "_tests")

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	for _, collection := range collections {
		collection.Drop(ctx)
	}
}
