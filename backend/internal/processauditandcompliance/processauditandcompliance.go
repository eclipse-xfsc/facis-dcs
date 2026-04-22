package processauditandcompliance

import (
	"context"
	"crypto/sha256"
	event2 "digital-contracting-service/internal/base/event"
	"digital-contracting-service/internal/processauditandcompliance/ipfs"
	"encoding/base64"
	"log"
	"strings"

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
	SubClient  *event2.CloudEventSubClient
	IPFSClient *ipfs.APIClient
}

func (s PACSubscriber) Start() {
	go func() {
		var preCID string
		err := s.SubClient.Subscribe(func(evt event.Event) {

			raw := string(evt.Data())
			raw = strings.Trim(raw, `"`)

			payload, err := base64.StdEncoding.DecodeString(raw)
			if err != nil {
				log.Println(err)
				return
			}

			logEntry := LogEntry{
				EventID:   evt.ID(),
				Source:    evt.Source(),
				EventType: evt.Type(),
				Payload:   string(payload),
				PreCID:    preCID,
			}
			checksum := sha256.Sum256(payload)
			auditLogEntry := AuditLogEntry{
				LogEntry: logEntry,
				Checksum: checksum,
			}

			result, err := s.IPFSClient.CreateFile(context.Background(), auditLogEntry)
			if err != nil {
				log.Println(err)
				return
			}

			preCID = result.Identifier.Value
		})
		if err != nil {
			log.Fatalf("failed to subscribe to events: %s", err)
		}
	}()
}

func (s PACSubscriber) Stop() {
	s.SubClient.Cancel()
}
