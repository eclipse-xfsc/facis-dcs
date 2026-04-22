<template>
  <p class="m-0 leading-6 whitespace-pre-wrap text-base-content/90">
    {{ block.text }}
  </p>
</template>

<script setup lang="ts">
import type { ContractPlainTextLine } from '@/modules/contract-workflow-engine/composables/useContractPlainTextConverter'

defineProps<{
  block: ContractPlainTextLine
}>()
</script>
