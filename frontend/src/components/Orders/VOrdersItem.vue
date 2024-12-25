<script lang="ts" setup>
  import { computed } from 'vue';
  import { getOrderStateVerbose, getIconByOrderState } from '@/utils/orders';
  import type { OrdersItem } from '@/types/orders';

  export interface Props {
    order: OrdersItem;
  }

  const props = defineProps<Props>();

  const orderStateVerbose = computed(() => {
    return getOrderStateVerbose(props.order);
  });

  const rightIcon = computed(() => {
    return getIconByOrderState(props.order.state);
  });
</script>

<template>
  <div class="VOrdersItem rounded p-3">
    <RouterLink class="link" :to="{ name: 'order', params: { id: order.id } }">
      <div>
        <div class="VOrdersItem__State flex items-center">
          <span class="flex-auto text-sm">{{ orderStateVerbose }}</span>
          <rightIcon />
        </div>
        <div class="VOrdersItem__Id">
          <span class="font-bold">№ {{ order.id }}</span>
        </div>
        <div class="VOrdersItem__Body text-sm flex flex-col">
          <span>Стоимость: {{ order.totalPrice }}</span>
          <span>Ожидаемая дата доставки: {{ order.expectedDeliveryDate }}</span>
        </div>
      </div>
    </RouterLink>
  </div>
</template>

<style>
  .VOrdersItem {
    background: var(--section-bg-color);
  }

  .VOrdersItem__Body,
  .VOrdersItem__State {
    color: var(--subtitle-text-color);
  }

  .VOrdersItem__Id {
    color: var(--text-color);
  }
</style>
