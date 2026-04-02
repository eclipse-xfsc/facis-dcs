package event

import (
	"digital-contracting-service/internal/contractworkflowengine/datatype/eventtype"
	"time"
)

// RetrieveByIDEvent is emitted when contract data is retrieved.
type RetrieveByIDEvent struct {
	DID         string    `json:"did"`
	RetrievedBy string    `json:"retrieved_by"`
	OccurredAt  time.Time `json:"occurred_at"`
}

// EventType implements the Event interface.
func (e RetrieveByIDEvent) EventType() string {
	return eventtype.RetrieveByID.String()
}

// GetDID implements the Event interface.
func (e RetrieveByIDEvent) GetDID() string {
	return e.DID
}

// RetrieveAllEvent is emitted when contract data is retrieved.
type RetrieveAllEvent struct {
	RetrievedBy string    `json:"retrieved_by"`
	OccurredAt  time.Time `json:"occurred_at"`
}

// EventType implements the Event interface.
func (e RetrieveAllEvent) EventType() string {
	return eventtype.RetrieveAll.String()
}

// GetDID implements the Event interface.
func (e RetrieveAllEvent) GetDID() string {
	return "*"
}

// VerifyEvent is emitted when a template is verified.
type VerifyEvent struct {
	DID             string    `json:"did"`
	ContractVersion *int      `json:"contract_version,omitempty"`
	VerifiedBy      string    `json:"verified_by"`
	OccurredAt      time.Time `json:"occurred_at"`
}

// EventType implements the Event interface.
func (e VerifyEvent) EventType() string {
	return eventtype.Verify.String()
}

// GetDID implements the Event interface.
func (e VerifyEvent) GetDID() string {
	return e.DID
}

// AuditEvent is emitted when the contract is audited
type AuditEvent struct {
	DID             string    `json:"did"`
	ContractVersion *int      `json:"contract_version,omitempty"`
	AuditedBy       string    `json:"audited_by"`
	OccurredAt      time.Time `json:"occurred_at"`
}

// EventType implements the Event interface.
func (e AuditEvent) EventType() string {
	return eventtype.Audit.String()
}

// GetDID implements the Event interface.
func (e AuditEvent) GetDID() string {
	return e.DID
}
