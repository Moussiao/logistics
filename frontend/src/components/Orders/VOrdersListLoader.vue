<template>
  <div class="flex flex-col gap-2">
    <div
      v-for="index in 5"
      :key="index"
      class="VOrdersListLoader__Item rounded h-28 animate-pulse"></div>
  </div>
</template>

<style>
  .VOrdersListLoader__Item {
    background: var(--section-bg-color);
  }
</style>
