<script lang="ts" setup>
  import { computed } from 'vue';
  import { EditIcon } from 'vue-tabler-icons';
  import VOrderDetailBlock from '@/components/Order/VOrderDetailBlock.vue';
  import VOrderDetailBlockField from '@/components/Order/VOrderDetailBlockField.vue';
  import type { Order } from '@/types/orders';

  export interface Props {
    order: Order;
  }

  const props = defineProps<Props>();
  defineEmits(['onClickEditOrder']);

  const orderDeliveryCity = computed((): string => {
    if (!props.order.customerAddress) return '-';

    const address = props.order.customerAddress;
    const addressValues: string[] = [];
    if (address.postcode) addressValues.push(address.postcode);
    if (address.regionName) addressValues.push(address.regionName);
    if (address.cityName) addressValues.push(address.cityName);

    return addressValues.join(', ') || '-';
  });

  const orderDeliveryStreet = computed((): string => {
    if (!(props.order.customerAddress && props.order.customerAddress.street)) return '-';

    const address = props.order.customerAddress;
    return `${address.street} д. ${address.houseNumber} кв. ${address.flatNumber}`;
  });
</script>

<template>
  <div class="VOrderDetail rounded flex flex-col gap-2">
    <VOrderDetailBlock name="Детали заказа">
      <template v-slot:right-header>
        <button
          type="button"
          title="Изменить"
          @click.stop.prevent="$emit('onClickEditOrder')"
          class="VOrderDetail__Edit">
          <EditIcon />
        </button>
      </template>
      <VOrderDetailBlockField name="Имя заказчика" :value="order.customer?.name || '-'" />
      <VOrderDetailBlockField name="Телефон заказчика" :value="order.customer?.phone || '-'" />
      <VOrderDetailBlockField name="Комментарий" :value="order.comment || '-'" />
    </VOrderDetailBlock>
    <VOrderDetailBlock name="Адрес доставки">
      <VOrderDetailBlockField name="Населенный пункт" :value="orderDeliveryCity" />
      <VOrderDetailBlockField name="Улица" :value="orderDeliveryStreet" />
      <VOrderDetailBlockField
        name="Комментарий к доставке"
        :value="order.customerAddress?.comment || '-'" />
    </VOrderDetailBlock>
    <VOrderDetailBlock name="Товары">
      <div class="flex flex-col gap-1">
        <div v-for="orderProduct in order.products" :key="orderProduct.productId" class="flex">
          <div class="flex flex-col flex-auto">
            <span>{{ orderProduct.productName }}</span>
            <span class="VOrderDetail__Hint">{{ orderProduct.quantity }} шт</span>
          </div>
          <div class="flex flex-col text-right">
            <span>{{ +orderProduct.totalPrice }}</span>
            <span class="VOrderDetail__Hint">
              {{ +(orderProduct.totalPrice / (orderProduct.quantity || 1)).toFixed(2) }}/шт
            </span>
          </div>
        </div>
      </div>
      <div class="flex items-center">
        <span class="font-bold text-xl flex-auto">Итого</span>
        <span class="font-bold text-xl">{{ +order.totalPrice }}</span>
      </div>
    </VOrderDetailBlock>
  </div>
</template>

<style>
  .VOrderDetail__Edit {
    color: var(--link-color);
  }
  .VOrderDetail__Hint {
    color: var(--hint-color);
  }
</style>
