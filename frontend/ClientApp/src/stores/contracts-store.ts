import type { Contract } from '@/models/contract/contract'
import type { ContractApprovalTask } from '@/models/contract/contract-approval-task'
import type { ContractReviewTask } from '@/models/contract/contract-review-task'
import { defineStore } from 'pinia'
import { computed, ref, type Ref } from 'vue'
import { useDataRouteStore } from './data-route-store'
import { ROUTES } from '@/router/router'
import { contractWorkflowService } from '@/services/contract-workflow-service'

export const useContractsStore = defineStore('contracts', () => {
  const contracts: Ref<Contract[]> = ref([])
  const reviewTasks: Ref<ContractReviewTask[]> = ref([])
  const approvalTasks: Ref<ContractApprovalTask[]> = ref([])

  const loading = ref(false)
  const error = ref<string | null>(null)

  const dataRouteStore = useDataRouteStore()

  const hasContracts = computed(() => contracts.value.length > 0)

  async function loadContracts() {
    loading.value = true
    error.value = null
    try {
      const data = await contractWorkflowService.retrieve()
      contracts.value = data.contracts
      reviewTasks.value = data.review_tasks
      approvalTasks.value = data.approval_tasks
      if (reviewTasks.value.length > 0) {
        dataRouteStore.addDataRouteLoaded(ROUTES.TASKS.REVIEWS)
      }
      if (approvalTasks.value.length > 0) {
        dataRouteStore.addDataRouteLoaded(ROUTES.TASKS.APPROVALS)
      }
    } catch (err: any) {
      error.value = err.message || 'Error loading the contracts'
    } finally {
      loading.value = false
    }
  }

  return { contracts, reviewTasks, approvalTasks, hasContracts, loadContracts, loading, error }
})
