package tests

import (
	"context"
	"hub-backend/configs"
	"log"
	"os"
	"time"
)

func CheckEnv() {
	// exit test case if not in correct env
	if !configs.IsTestENV() {
		log.Fatalf("IS_TEST is missing or false!")
		os.Exit(1)
	}
}

func CleanUpCollection() {
	collections := configs.GetCollectionsStartingWith(configs.DB, "_tests")

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	for _, collection := range collections {
		collection.Drop(ctx)
	}
}
