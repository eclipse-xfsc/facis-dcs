package service

import (
	"context"
	signaturemanagement "digital-contracting-service/gen/signature_management"
	"digital-contracting-service/internal/auth"
	cwedb "digital-contracting-service/internal/contractworkflowengine/db"

	"github.com/jmoiron/sqlx"
	"goa.design/clue/log"
)

type signatureManagementsrvc struct {
	DB    *sqlx.DB
	CRepo cwedb.ContractRepo
	auth.JWTAuthenticator
}

func NewSignatureManagement(db *sqlx.DB, jwtAuth auth.JWTAuthenticator, cRepo cwedb.ContractRepo) signaturemanagement.Service {

	return &signatureManagementsrvc{
		JWTAuthenticator: jwtAuth,
		DB:               db,
		CRepo:            cRepo,
	}
}

func (s *signatureManagementsrvc) Retrieve(ctx context.Context, req *signaturemanagement.SMContractRetrieveRequest) (res *signaturemanagement.SMContractRetrieveResponse, err error) {
	log.Printf(ctx, "signatureManagement.retrieve")
	return
}

func (s *signatureManagementsrvc) RetrieveByID(ctx context.Context, req *signaturemanagement.SMContractRetrieveByIDRequest) (res *signaturemanagement.SMContractRetrieveByIDResponse, err error) {
	log.Printf(ctx, "signatureManagement.retrieve")
	return
}

func (s *signatureManagementsrvc) Verify(ctx context.Context, req *signaturemanagement.SMContractVerifyRequest) (res *signaturemanagement.SMContractVerifyResponse, err error) {
	log.Printf(ctx, "signatureManagement.verify")
	return
}

func (s *signatureManagementsrvc) Apply(ctx context.Context, req *signaturemanagement.SMContractApplyRequest) (res *signaturemanagement.SMContractApplyResponse, err error) {
	log.Printf(ctx, "signatureManagement.apply")
	return
}

func (s *signatureManagementsrvc) Validate(ctx context.Context, req *signaturemanagement.SMContractValidateRequest) (res *signaturemanagement.SMContractValidateResponse, err error) {
	log.Printf(ctx, "signatureManagement.validate")
	return
}

func (s *signatureManagementsrvc) Revoke(ctx context.Context, request *signaturemanagement.SMContractRevokeRequest) (res *signaturemanagement.SMContractRevokeResponse, err error) {
	log.Printf(ctx, "signatureManagement.revoke")
	return
}

func (s *signatureManagementsrvc) Audit(ctx context.Context, req *signaturemanagement.SMContractAuditRequest) (res *signaturemanagement.SMContractAuditResponse, err error) {
	log.Printf(ctx, "signatureManagement.audit")
	return
}

func (s *signatureManagementsrvc) Compliance(ctx context.Context, req *signaturemanagement.SMContractComplianceRequest) (res *signaturemanagement.SMContractComplianceResponse, err error) {
	log.Printf(ctx, "signatureManagement.compliance")
	return
}
