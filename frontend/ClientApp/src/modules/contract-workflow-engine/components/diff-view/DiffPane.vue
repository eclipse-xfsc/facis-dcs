<template>
  <div class="card bg-base-100 border border-base-300 shadow-sm h-full min-h-0">
    <div class="card-body p-4 min-h-0">
      <div class="font-semibold text-sm text-base-content/70 mb-2">
        {{ title }}
      </div>
      <div class="overflow-y-auto min-h-0 flex-1">
        <div
          v-if="showNoPriorVersion"
          class="h-full flex items-center justify-center text-base-content/50"
        >
          no prior version
        </div>
        <template v-else>
          <div
            v-for="(block, index) in blocks"
            :key="`${block.type}-${index}`"
            class="flex items-start"
          >
            <div
              v-if="showLineNumbers"
              class="w-10 shrink-0 pr-2 mr-3 pt-0 text-right text-base leading-6 text-base-content/40 border-r border-base-300/60 select-none"
            >
              {{ index + 1 }}
            </div>
            <div class="min-w-0 flex-1">
              <DiffSectionBlock
                v-if="isSectionPlainTextBlock(block)"
                :block="block"
              />
              <DiffTextBlock
                v-else
                :block="block"
              />
            </div>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {
  isSectionPlainTextBlock,
  type ContractPlainTextBlock
} from '@/modules/contract-workflow-engine/composables/useContractPlainTextConverter'
import DiffSectionBlock from './DiffSectionBlock.vue'
import DiffTextBlock from './DiffTextBlock.vue'

withDefaults(defineProps<{
  title: string
  blocks: ContractPlainTextBlock[]
  showNoPriorVersion?: boolean
  showLineNumbers?: boolean
}>(), {
  showNoPriorVersion: false,
  showLineNumbers: true
})
</script>
