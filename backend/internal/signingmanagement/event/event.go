package event

import (
	"digital-contracting-service/internal/signingmanagement/datatype/eventtype"
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

// ValidateEvent is emitted when a signature is validated.
type ValidateEvent struct {
	DID             string    `json:"did"`
	ContractVersion *int      `json:"contract_version,omitempty"`
	ValidatedBy     string    `json:"validated_by"`
	OccurredAt      time.Time `json:"occurred_at"`
}

// EventType implements the Event interface.
func (e ValidateEvent) EventType() string {
	return eventtype.Validate.String()
}

// GetDID implements the Event interface.
func (e ValidateEvent) GetDID() string {
	return e.DID
}

// RetrieveAuditLogEvent is emitted when the audit log is retrieved
type RetrieveAuditLogEvent struct {
	DID             string    `json:"did"`
	ContractVersion *int      `json:"contract_version,omitempty"`
	RetrievedBy     string    `json:"retrieved_by"`
	OccurredAt      time.Time `json:"occurred_at"`
}

// EventType implements the Event interface.
func (e RetrieveAuditLogEvent) EventType() string {
	return eventtype.RetrieveAuditLog.String()
}

// GetDID implements the Event interface.
func (e RetrieveAuditLogEvent) GetDID() string {
	return e.DID
}

// AuditEvent is emitted when a signature is revoked
type RevokeEvent struct {
	DID             string    `json:"did"`
	ContractVersion *int      `json:"contract_version,omitempty"`
	RevokedBy       string    `json:"revoked_by"`
	OccurredAt      time.Time `json:"occurred_at"`
}

// EventType implements the Event interface.
func (e RevokeEvent) EventType() string {
	return eventtype.Revoke.String()
}

// GetDID implements the Event interface.
func (e RevokeEvent) GetDID() string {
	return e.DID
}

// ComplianceValidation is emitted when compliance check ist started
type ComplianceValidationEvent struct {
	DID             string    `json:"did"`
	ContractVersion *int      `json:"contract_version,omitempty"`
	ValidatedBy     string    `json:"validated_by"`
	OccurredAt      time.Time `json:"occurred_at"`
}

// EventType implements the Event interface.
func (e ComplianceValidationEvent) EventType() string {
	return eventtype.ComplianceValidation.String()
}

// GetDID implements the Event interface.
func (e ComplianceValidationEvent) GetDID() string {
	return e.DID
}
