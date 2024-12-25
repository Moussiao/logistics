<script lang="ts" setup>
  export interface Props {
    name: string | number;
    value: string;
  }

  defineProps<Props>();
</script>

<template>
  <div class="VOrderDetailBlockField flex flex-col">
    <div class="flex flex-col">
      <span class="VOrderDetailBlockField__Name text-sm">{{ name }}</span>
      <span>{{ value }}</span>
    </div>
  </div>
</template>

<style>
  .VOrderDetailBlockField__Name {
    color: var(--hint-color);
  }
</style>
