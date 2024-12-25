<script lang="ts" setup>
  export interface Props {
    tag?: string;
  }

  withDefaults(defineProps<Props>(), { tag: 'div' });
</script>

<template>
  <component :is="tag" class="VCard overflow-hidden rounded p-3">
    <slot />
  </component>
</template>

<style>
  .VCard {
    background: var(--section-bg-color);
  }
</style>
