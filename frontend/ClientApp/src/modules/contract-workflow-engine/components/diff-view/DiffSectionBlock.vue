<template>
  <p class="m-0 leading-6 font-semibold text-base-content" :class="sectionTextClass">
    {{ block.text }}
  </p>
</template>

<script setup lang="ts">
import type { ContractPlainTextSection } from '@/modules/contract-workflow-engine/composables/useContractPlainTextConverter'
import { computed } from 'vue'

const props = defineProps<{
  block: ContractPlainTextSection
}>()

const sectionTextClass = computed(() => {
  if (props.block.level <= 1) return 'text-lg'
  if (props.block.level === 2) return 'text-[17px]'
  return 'text-base'
})
</script>
