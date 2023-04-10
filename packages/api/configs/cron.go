package configs

import (
	"time"

	"github.com/go-co-op/gocron"
)

// Sets a new random value of the BEARER TOKEN every 24 hours
func RunCronJobs() {
	schedule := gocron.NewScheduler(time.UTC)
	schedule.Every(1).Day().At("7:00").Do(func() {
		token = SetToken()
	})

	schedule.StartAsync()
}
