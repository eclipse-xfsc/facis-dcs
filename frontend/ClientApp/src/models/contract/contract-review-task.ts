import type { ReviewTaskState } from "@/types/review-task-state";

export interface ContractReviewTask {
  type: 'contract'
  did: string;
  contract_version?: string;
  state: ReviewTaskState;
  reviewer: string;
  created_at: string;
}
