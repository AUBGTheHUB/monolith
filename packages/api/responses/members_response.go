package responses

import (
	"github.com/gofiber/fiber/v2"
)

type MemberResponse struct { // should be renamed as it is used for all types of respponses
	Status  int        `json:"status"`
	Message string     `json:"message"`
	Data    *fiber.Map `json:"data"`
}
