<script lang="ts" setup>
  import { ref } from 'vue';
  import { useInfiniteScroll } from '@vueuse/core';
  import VOrdersItem from '@/components/Orders/VOrdersItem.vue';
  import type { OrdersItem } from '@/types/orders';

  export interface Props {
    orders: OrdersItem[];
    canLoadMore: boolean;
  }

  const props = defineProps<Props>();
  const emit = defineEmits(['loadMore']);

  const el = ref<HTMLElement | null>(null);

  useInfiniteScroll(el, () => emit('loadMore'), {
    distance: 200,
    canLoadMore: () => props.canLoadMore,
  });
</script>

<template>
  <div v-if="orders.length" ref="el" class="flex flex-col overflow-y-auto min-h-0 gap-2">
    <VOrdersItem v-for="order in orders" :key="order.id" :order="order" class="h-28" />
  </div>
  <div
    v-else
    class="flex h-128 flex-grow items-center justify-center rounded border border-dashed text-center">
    Нет заказов
  </div>
</template>
