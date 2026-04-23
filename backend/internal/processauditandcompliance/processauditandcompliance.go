package processauditandcompliance

import (
	event2 "digital-contracting-service/internal/base/event"
	"log"

	"github.com/cloudevents/sdk-go/v2/event"
)

type AuditLogEntry struct {
	LogEntry LogEntry `json:"log_entry"`
	Checksum [32]byte `json:"checksum"`
}

type LogEntry struct {
	EventID   string `json:"event_id"`
	Source    string `json:"source"`
	EventType string `json:"event_type"`
	Payload   string `json:"payload"`
	PreCID    string `json:"pre_cid"`
}

type PACSubscriber struct {
	SubClient *event2.CloudEventSubClient
}

func (s PACSubscriber) Start() {
	go func() {

		err := s.SubClient.Subscribe(func(evt event.Event) {
			/*
				raw := string(evt.Data())
				raw = strings.Trim(raw, `"`)

				payload, err := base64.StdEncoding.DecodeString(raw)
				if err != nil {
					log.Println(err)
					return
				}
			*/
		})
		if err != nil {
			log.Fatalf("failed to subscribe to events: %s", err)
		}
	}()
}

func (s PACSubscriber) Stop() {
	s.SubClient.Cancel()
}
