package tests

import (
	"context"
	"hub-backend/configs"
	"time"
)

func CleanUpCollection() {
	collection := configs.GetCollection(configs.DB, "_tests")
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	collection.Drop(ctx)
}
