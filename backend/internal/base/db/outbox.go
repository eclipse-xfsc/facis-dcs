package db

import (
	"context"
	"digital-contracting-service/internal/base/datatype/componenttype"
	"digital-contracting-service/internal/base/db/pq"

	"github.com/jmoiron/sqlx"
)

func PersistEvent(ctx context.Context, tx *sqlx.Tx, component componenttype.ComponentType, eventType string, eventJSON []byte, did string) error {
	return pq.PostgresPersistEvent(ctx, tx, component, eventType, eventJSON, did)
}

func UpdateOutboxEvent(ctx context.Context, tx *sqlx.Tx, id int64) error {
	return pq.PostgresUpdateOutboxEvent(ctx, tx, id)
}
