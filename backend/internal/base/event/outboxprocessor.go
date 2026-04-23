package event

import (
	"context"
	"digital-contracting-service/internal/base/conf"
	"digital-contracting-service/internal/processauditandcompliance/ipfs"
	"fmt"
	"log"
	"time"

	"github.com/jmoiron/sqlx"
)

type OutboxProcessor struct {
	DB         *sqlx.DB
	Ctx        context.Context
	PubClient  *CloudEventPubClient
	IPFSClient *ipfs.APIClient
}

type OutboxEvent struct {
	ID        int64     `db:"id"         json:"id"`
	Component string    `db:"component"  json:"component"`
	EventType string    `db:"event_type" json:"event_type"`
	EventData []byte    `db:"event_data" json:"event_data"`
	DID       *string   `db:"did"        json:"did"`
	CreatedAt time.Time `db:"created_at" json:"created_at"`
}

type AuditLogEntry struct {
	ID        int64     `json:"id"`
	Component string    `json:"component"`
	EventType string    `json:"event_type"`
	EventData []byte    `json:"event_data"`
	DID       *string   `json:"did"`
	CreatedAt time.Time `json:"created_at"`
	PreCID    string    `json:"pre_cid"`
}

func (j OutboxProcessor) Start() {
	go startProcessingJob(j.DB, j.Ctx, j.PubClient, j.IPFSClient, conf.OutboxProcessorTimeOut())
}

func startProcessingJob(db *sqlx.DB, ctx context.Context, pubClient *CloudEventPubClient, ipfsClient *ipfs.APIClient, interval time.Duration) {
	if pubClient == nil {
		return
	}

	schedulerLogic := func() error {
		tx, err := db.BeginTxx(ctx, nil)
		if err != nil {
			return fmt.Errorf("could not start transaction: %w", err)
		}
		defer tx.Rollback()

		rows, err := tx.QueryxContext(ctx, `
			SELECT id, component, event_type, event_data, did, created_at
			FROM outbox_events
			WHERE processed = FALSE
			ORDER BY created_at ASC
			LIMIT 100
			FOR UPDATE SKIP LOCKED
		`)
		if err != nil {
			return fmt.Errorf("could not query outbox events: %w", err)
		}

		var events []OutboxEvent
		for rows.Next() {
			var event OutboxEvent
			if err := rows.StructScan(&event); err != nil {
				rows.Close()
				return fmt.Errorf("could not scan event: %w", err)
			}
			events = append(events, event)
		}
		rows.Close()

		if len(events) > 0 {
			log.Println("process ", len(events), " events")
		}

		var preCID string
		for _, event := range events {

			if err := pubClient.Publish(event.Component, event.EventType, event.EventData); err != nil {
				return fmt.Errorf("could not publish event %d: %w", event.ID, err)
			}

			auditLogEntry := AuditLogEntry{
				ID:        event.ID,
				Component: event.Component,
				EventType: event.EventType,
				EventData: event.EventData,
				DID:       event.DID,
				CreatedAt: event.CreatedAt,
				PreCID:    preCID,
			}

			result, err := ipfsClient.CreateFile(ctx, auditLogEntry)
			if err != nil {
				return fmt.Errorf("could not create IPFS file for event %d: %w", event.ID, err)
			}

			preCID = result.Identifier.Value

			if _, err := tx.ExecContext(ctx, `
				UPDATE outbox_events 
				SET processed = TRUE, processed_at = CURRENT_TIMESTAMP
				WHERE id = $1
			`, event.ID); err != nil {
				return fmt.Errorf("could not mark event %d as processed: %w", event.ID, err)
			}
		}

		return tx.Commit()
	}

	ticker := time.NewTicker(interval)
	for range ticker.C {
		if err := schedulerLogic(); err != nil {
			log.Printf("could not process outbox entries: %v", err)
		}
	}
}
