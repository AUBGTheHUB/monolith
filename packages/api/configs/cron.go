package configs

import (
	"time"

	"github.com/go-co-op/gocron"
)

func RunCronJobs() {
	schedule := gocron.NewScheduler(time.UTC)
	schedule.Every(5).Seconds().Do(func() {
		SetToken()
		//fmt.Println(token)
	})

	//This will block THIS Thread and allow other threads (the main thread) to continue work, right?
	schedule.StartAsync()

}
