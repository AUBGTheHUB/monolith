package configs

import (
	"fmt"
	"time"

	"github.com/go-co-op/gocron"
)

func RunCronJobs() {
	schedule := gocron.NewScheduler(time.UTC)
	schedule.Every(5).Seconds().Do(func() {
		token = GenerateToken(32)
		//this is for test
		fmt.Println(token)
	})

	//This will block THIS Thread and allow other threads (the main thread) to continue work, right?
	schedule.StartBlocking()
}
