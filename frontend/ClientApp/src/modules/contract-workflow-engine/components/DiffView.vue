<template>
  <div class="space-y-3">
    <!-- toolbar -->
    <div class="flex items-center justify-between rounded-md border border-base-300 bg-base-100 px-3 py-2">
      <div class="flex items-center gap-3">
        <label
          for="line-number-toggle"
          class="text-sm text-base-content/80"
        >
          Line numbers
        </label>
        <input
          id="line-number-toggle"
          v-model="showLineNumbers"
          type="checkbox"
          class="toggle toggle-sm"
        />
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-4 min-h-[32rem]">
      <DiffPane
        title="Prior Version"
        :blocks="priorBlocks"
        :show-no-prior-version="!hasPriorContractData"
        :show-line-numbers="showLineNumbers"
      />
      <DiffPane
        title="Current Version"
        :blocks="currentBlocks"
        :show-line-numbers="showLineNumbers"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import type { ContractData } from '@/models/contract-data'
import {
  type ContractPlainTextBlock,
  useContractPlainTextConverter
} from '@/modules/contract-workflow-engine/composables/useContractPlainTextConverter'
import DiffPane from '@/modules/contract-workflow-engine/components/diff-view/DiffPane.vue'
import { computed, ref } from 'vue'

const props = defineProps<{
  priorContractData?: ContractData
  currentContractData?: ContractData
}>()

const { convertContractToPlainTextBlocks } = useContractPlainTextConverter()
const showLineNumbers = ref(true)

const hasPriorContractData = computed(() => !!props.priorContractData)

const priorBlocks = computed<ContractPlainTextBlock[]>(() => {
  if (!props.priorContractData) return []
  return convertContractToPlainTextBlocks(props.priorContractData)
})

const currentBlocks = computed<ContractPlainTextBlock[]>(() => {
  if (!props.currentContractData) return []
  return convertContractToPlainTextBlocks(props.currentContractData)
})

</script>