<script lang="ts" setup>
  export interface Props {
    name: string;
  }

  defineProps<Props>();
</script>

<template>
  <div class="VOrderDetailBlock flex flex-col gap-2 rounded px-2 py-2">
    <div class="flex items-center">
      <span class="font-bold text-lg flex-auto">{{ name }}</span>
      <slot name="right-header" />
    </div>
    <div class="flex flex-col gap-2">
      <slot />
    </div>
  </div>
</template>

<style>
  .VOrderDetailBlock {
    background: var(--section-bg-color);
  }
</style>
