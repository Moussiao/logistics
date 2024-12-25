<script lang="ts" setup>
  import { ref, watch, onMounted, onBeforeUnmount } from 'vue';
  import { useRouter } from 'vue-router';
  import VOrdersFilters from '@/components/Orders/VOrdersFilters.vue';
  import VOrdersListItems from '@/components/Orders/VOrdersListItems.vue';
  import VOrdersListLoader from '@/components/Orders/VOrdersListLoader.vue';
  import useOrders from '@/stores/orders';
  import useTelegram from '@/stores/telegram';
  import type { OrdersFilters } from '@/types/orders';

  const router = useRouter();
  const orders = useOrders();
  const telegram = useTelegram();

  const isLoadingOrders = ref<boolean>(orders.items.length ? false : true);
  const ordersFilters = ref<OrdersFilters>({ ...orders.currentFilters });
  const isLoadingMoreOrders = ref<boolean>(false);

  const loadMore = async () => {
    isLoadingMoreOrders.value = true;
    await orders.loadMore();
    isLoadingMoreOrders.value = false;
  };

  watch(ordersFilters, async (filters: OrdersFilters) => {
    isLoadingOrders.value = true;
    await orders.getData(filters);
    isLoadingOrders.value = false;
  });

  onMounted(() => {
    telegram.showBackButton(() => {
      void router.push({ name: 'home' });
    });
  });

  onBeforeUnmount(() => {
    telegram.hideBackButton();
  });
</script>

<template>
  <div class="flex flex-col h-full gap-2">
    <VOrdersFilters v-model="ordersFilters" :disabled="isLoadingOrders" class="py-2 px-2" />
    <VOrdersListItems
      v-if="!isLoadingOrders"
      :orders="orders.items"
      :can-load-more="Boolean(orders.nextCursor) && !isLoadingMoreOrders"
      @load-more="loadMore"
      class="px-2 pb-2" />
    <VOrdersListLoader v-else class="px-2" />
  </div>
</template>
