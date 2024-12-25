<script lang="ts" setup>
  import { ref, computed, watch, onMounted, onBeforeUnmount } from 'vue';
  import { watchImmediate } from '@vueuse/core';
  import { useRoute, useRouter } from 'vue-router';
  import { takeOrderToJob, driveToCustomer, customerPaid } from '@/api/orders';
  import VOrderDetail from '@/components/Order/VOrderDetail.vue';
  import VOrderHeader from '@/components/Order/VOrderHeader.vue';
  import VOrderEdit from '@/components/Order/VOrderEdit.vue';
  import VOrdersListLoader from '@/components/Orders/VOrdersListLoader.vue';
  import VBottomSheet from '@/components/VBottomSheet.vue';
  import useOrder from '@/stores/order';
  import useOrders from '@/stores/orders';
  import useTelegram from '@/stores/telegram';
  import useUser from '@/stores/user';

  const route = useRoute();
  const router = useRouter();

  const user = useUser();
  const order = useOrder();
  const orders = useOrders();
  const telegram = useTelegram();

  const isLoading = ref<boolean>(true);
  const isVisibleEditOrderSheet = ref<boolean>(false);
  const orderId = computed((): string => String(route.params.id));

  const showOrderChangeStateButton = () => {
    if (user.role !== 'partner') return;

    const telegram = useTelegram();
    if (order.state === 'new') {
      telegram.showMainButton('Взять в работу', () => {
        telegram.openPopup({
          title: 'Взять заказ в работу',
          message: 'Вы точно хотите взять заказ в работу?',
          onActionButtonClick: async () => {
            telegram.showMainButtonLoader();
            await takeOrderToJob(order.id);
            await onOrderUpdated();
            telegram.hideMainButtonLoader();
          },
        });
      });
    }
    if (order.state === 'processing') {
      telegram.showMainButton('Отправиться к заказчику', () => {
        telegram.openPopup({
          title: 'Отправиться к заказчику',
          message: 'Вы подтверждаете, что отправляетесь к заказчику?',
          onActionButtonClick: async () => {
            telegram.showMainButtonLoader();
            await driveToCustomer(order.id);
            await onOrderUpdated();
            telegram.hideMainButtonLoader();
          },
        });
      });
    }
    if (order.state === 'delivery') {
      telegram.showMainButton('Заказ оплачен', () => {
        telegram.openPopup({
          title: 'Заказ оплачен',
          message: 'Вы подтверждаете, что заказ оплачен?',
          onActionButtonClick: async () => {
            telegram.showMainButtonLoader();
            await customerPaid(order.id);
            await onOrderUpdated();
            telegram.hideMainButtonLoader();
          },
        });
      });
    }
  };

  const onOrderUpdated = async () => {
    isLoading.value = true;
    isVisibleEditOrderSheet.value = false;
    // Очищаем закешированные данные о заказах
    orders.clean();
    await order.getData(orderId.value);
    isLoading.value = false;
  };

  watchImmediate(orderId, async (id: string) => {
    isLoading.value = true;
    await order.getData(id);
    isLoading.value = false;
  });

  watch(isLoading, () => {
    if (isLoading.value) {
      telegram.hideMainButton();
    } else {
      showOrderChangeStateButton();
    }
  });

  watch(isVisibleEditOrderSheet, (isVisible: boolean) => {
    if (isVisible) {
      telegram.showMainButton('Закрыть', () => (isVisibleEditOrderSheet.value = false));
    } else if (!isLoading.value) {
      telegram.hideMainButton();
      showOrderChangeStateButton();
    }
  });

  onMounted(() => {
    telegram.showBackButton(() => {
      void router.push({ name: 'orders' });
    });
  });

  onBeforeUnmount(() => {
    telegram.hideBackButton();
    telegram.hideMainButton();
  });
</script>

<template>
  <div class="flex flex-col h-full">
    <div v-if="!isLoading" class="flex flex-col overflow-y-auto min-h-0 gap-2">
      <VOrderHeader :order="order" />
      <VOrderDetail :order="order" @on-click-edit-order="isVisibleEditOrderSheet = true" />
    </div>
    <VOrdersListLoader v-else class="px-2" />
  </div>
  <VBottomSheet v-model="isVisibleEditOrderSheet">
    <VOrderEdit @order-updated="onOrderUpdated" />
  </VBottomSheet>
</template>
