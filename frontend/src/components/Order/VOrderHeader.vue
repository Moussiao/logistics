<script lang="ts" setup>
  import { computed } from 'vue';
  import { formatDate } from '@/utils/date';
  import { getOrderStateVerbose, getIconByOrderState } from '@/utils/orders';
  import type { Order } from '@/types/orders';

  export interface Props {
    order: Order;
  }

  const props = defineProps<Props>();

  const orderStateVerbose = computed((): string => {
    return getOrderStateVerbose(props.order);
  });

  const orderStateChanged = computed((): string => {
    return formatDate(props.order.stateChangedAt, 'D MMM HH:mm');
  });

  const orderStateIcon = computed(() => {
    return getIconByOrderState(props.order.state);
  });
</script>

<template>
  <div class="VOrderHeader rounded px-2 py-2">
    <div class="flex items-center">
      <span class="font-bold text-2xl flex-auto">{{ orderStateVerbose }}</span>
      <orderStateIcon />
    </div>
    <div>
      <span class="font-bold">{{ orderStateChanged }}</span>
    </div>
  </div>
</template>

<style>
  .VOrderHeader {
    background: var(--section-bg-color);
  }
</style>
