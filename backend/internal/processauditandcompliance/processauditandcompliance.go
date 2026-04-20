package processauditandcompliance

import (
	"crypto/sha256"
	event2 "digital-contracting-service/internal/base/event"
	"encoding/base64"
	"log"
	"strings"

	"github.com/cloudevents/sdk-go/v2/event"
)

type AuditLogEntry struct {
	LogEntry LogEntry `json:"log_entry"`
	Checksum [32]byte `json:"hash"`
}

type LogEntry struct {
	ID           string   `json:"id"`
	Source       string   `json:"source"`
	EventType    string   `json:"event_type"`
	Payload      string   `json:"payload"`
	PredChecksum [32]byte `json:"pred_checksum"`
}

type PACSubscriber struct {
	SubClient *event2.CloudEventSubClient
}

func (j PACSubscriber) Start() {
	go func() {
		var previousChecksum [32]byte
		j.SubClient.Subscribe(func(evt event.Event) {

			raw := string(evt.Data())

			raw = strings.Trim(raw, `"`)

			payload, err := base64.StdEncoding.DecodeString(raw)
			if err != nil {
				log.Println(err)
			}

			entry := LogEntry{
				ID:           evt.ID(),
				Source:       evt.Source(),
				EventType:    evt.Type(),
				Payload:      string(payload),
				PredChecksum: previousChecksum,
			}
			checksum := sha256.Sum256(payload)
			auditLogEntry := AuditLogEntry{
				LogEntry: entry,
				Checksum: checksum,
			}
			log.Println(auditLogEntry)

			previousChecksum = checksum
		})
	}()
}

func (j PACSubscriber) Stop() {
	j.SubClient.Cancel()
}
