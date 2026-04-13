<template>
  <div
    class="flex items-start gap-3 p-3 rounded-lg border border-base-300 bg-base-200/30 group hover:shadow-sm transition-all"
  >
    <div class="flex-1 min-w-0">
      <div class="font-semibold text-sm text-base-content">
        {{ condition.conditionName }}
        <span class="font-normal text-base-content/60 ml-1">
          (used in {{ usedInClauseCount }} clause{{ usedInClauseCount === 1 ? '' : 's' }})
        </span>
      </div>
      <div class="flex flex-wrap gap-2 mt-2">
        <div
          v-for="(p, i) in condition.parameters"
          :key="i"
          class="badge badge-ghost badge-sm gap-1"
        >
          <span>{{ p.parameterName }}</span>
          <span class="opacity-70">({{ p.type }}, {{ p.isRequired ? 'required' : 'optional' }})</span>
        </div>
      </div>
    </div>
    <button
      v-if="isEditable"
      type="button"
      class="btn btn-ghost btn-xs text-base-content/70 opacity-0 group-hover:opacity-100 transition-opacity shrink-0"
      aria-label="Edit rule"
      @click="$emit('edit-rule', condition.conditionId)"
    >
      Edit
    </button>
    <button
      v-if="isEditable"
      type="button"
      class="btn btn-ghost btn-xs text-error opacity-0 group-hover:opacity-100 transition-opacity shrink-0"
      aria-label="Delete rule"
      @click="$emit('delete-rule', condition.conditionId)"
    >
      ✕
    </button>
  </div>
</template>

<script setup lang="ts">
import type { SemanticCondition } from '@template-repository/models/contract-templace'

const props = defineProps<{
  condition: SemanticCondition
  usedInClauseCount: number
  isEditable: boolean
}>()

defineEmits<{
  'edit-rule': [conditionId: string]
  'delete-rule': [conditionId: string]
}>()
</script>