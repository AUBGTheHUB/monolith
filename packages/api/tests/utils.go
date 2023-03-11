package tests

import (
	"context"
	"hub-backend/configs"
	"time"
)

func CleanUpCollection() {
	collections := configs.GetCollectionsStartingWith(configs.DB, "_tests")
	
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	for _, collection := range collections {
		collection.Drop(ctx)	
	}
}
