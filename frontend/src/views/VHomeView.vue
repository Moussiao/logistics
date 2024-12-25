<script lang="ts" setup>
  import VHeading from '@/components/VHeading.vue';
  import VCard from '@/components/VCard.vue';
</script>

<template>
  <div class="grid gap-4">
    <VHeading tag="h1">Домашняя страница</VHeading>
    <RouterLink class="link" :to="{ name: 'orders' }">
      <VCard class="VHome__Card">
        <VHeading tag="h2" class="text-center">Заказы</VHeading>
      </VCard>
    </RouterLink>
  </div>
</template>

<style>
  .VHome__Card:hover {
    opacity: 0.8;
  }
</style>
