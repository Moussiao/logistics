<script lang="ts">
  import { SettingsIcon, PackageIcon, TruckIcon } from 'vue-tabler-icons';
  import { isEqual, isEmpty } from 'lodash-es';
  import type { OrdersFilters } from '@/types/orders';
  import type { Tab } from '@/types/tabs';
  import type { Option } from '@/types/select';

  export interface Props {
    disabled: boolean;
  }

  interface OrdersFiltersByTabId {
    [key: number]: OrdersFilters;
  }

  const activeTab: Tab = {
    id: 1,
    name: 'Активные',
    leftIcon: TruckIcon,
  };
  const newTab: Tab = {
    id: 2,
    name: 'Новые',
    leftIcon: PackageIcon,
  };
  const customTab: Tab = {
    id: 3,
    name: 'Пользовательские',
    leftIcon: SettingsIcon,
    disabled: true,
  };
  const filtersTabs: Tab[] = [activeTab, newTab, customTab];

  const ordersFiltersByTabId: OrdersFiltersByTabId = {};
  ordersFiltersByTabId[activeTab.id] = { states: 'processing,delivery' };
  ordersFiltersByTabId[newTab.id] = { states: 'new' };
  ordersFiltersByTabId[customTab.id] = {};

  const getSelectedTabId = (filters: OrdersFilters): number => {
    if (isEmpty(filters)) return activeTab.id;
    if (isEqual(filters, ordersFiltersByTabId[activeTab.id])) return activeTab.id;
    if (isEqual(filters, ordersFiltersByTabId[newTab.id])) return newTab.id;

    return customTab.id;
  };
</script>

<script lang="ts" setup>
  import { ref, computed, watch, onMounted, onBeforeUnmount } from 'vue';
  import { ChevronDownIcon, ChevronUpIcon } from 'vue-tabler-icons';
  import VOrdersFiltersTabs from './VOrdersFiltersTabs.vue';
  import VMultiselect from '@/components/VMultiselect.vue';
  import useTelegram from '@/stores/telegram';
  import { OrderStateOptions, getOptionByOrderState } from '@/utils/orders';

  const props = defineProps<Props>();
  const ordersFilters = defineModel<OrdersFilters>({ required: true });

  const telegram = useTelegram();

  const selectedTabId = ref<number>(0);
  const isVisibleUserFilters = ref<boolean>(false);
  const ordersState = ref<Option | undefined>(undefined);

  const ordersFiltersCount = computed(() => Object.keys(ordersFilters.value).length);

  const onApplyFilters = () => {
    if (props.disabled) return;

    const newOrdersFilters: OrdersFilters = {};
    if (ordersState.value) {
      newOrdersFilters['states'] = ordersState.value.value;
    }

    ordersFilters.value = newOrdersFilters;
    selectedTabId.value = customTab.id;
    isVisibleUserFilters.value = false;
    telegram.hideMainButton();
  };

  const openUserFilters = () => {
    if (props.disabled) return;

    isVisibleUserFilters.value = !isVisibleUserFilters.value;
    if (isVisibleUserFilters.value) {
      telegram.showMainButton('Применить', onApplyFilters);
    } else {
      telegram.hideMainButton();
    }
  };

  const onTabClick = (tabId: number) => {
    if (!props.disabled) {
      selectedTabId.value = tabId;
      ordersFilters.value = ordersFiltersByTabId[tabId];
    }
  };

  watch(ordersFilters, (filters: OrdersFilters) => {
    if (filters.states) {
      ordersState.value = getOptionByOrderState(filters.states);
    } else {
      ordersState.value = undefined;
    }
  });

  onMounted(() => {
    selectedTabId.value = getSelectedTabId(ordersFilters.value);
    if (selectedTabId.value !== customTab.id) {
      ordersFilters.value = ordersFiltersByTabId[selectedTabId.value];
    }

    if (ordersFilters.value.states) {
      ordersState.value = getOptionByOrderState(ordersFilters.value.states);
    }
  });

  onBeforeUnmount(() => {
    // Пытаемся скрыть кнопку, даже если она не открыта,
    // так как она сама не скрывается при переходе на другую старницу.
    telegram.hideMainButton();
  });
</script>

<template>
  <div class="VOrdersFilters flex flex-col gap-4">
    <div class="flex flex-col gap-1">
      <div class="flex items-center w-min">
        <button
          type="button"
          title="Дополнительные фильтры"
          class="VOrdersFilters__FiltersButton flex items-center rounded px-2 py-1"
          @click.stop.prevent="openUserFilters">
          <span class="VOrdersFilters__FiltersCount rounded-full text-center size-6 mr-2">
            {{ ordersFiltersCount }}
          </span>
          Фильтры
          <ChevronDownIcon v-if="!isVisibleUserFilters" />
          <ChevronUpIcon v-else />
        </button>
      </div>
      <div v-if="isVisibleUserFilters">
        <VMultiselect
          v-model="ordersState"
          placeholder="Выберите статус заказа"
          :searchable="false"
          :options="OrderStateOptions"
          class="rounded" />
      </div>
    </div>
    <VOrdersFiltersTabs :tabs="filtersTabs" :activeTab="selectedTabId" @on-tab-click="onTabClick" />
  </div>
</template>

<style>
  .VOrdersFilters {
    background: var(--section-bg-color);
  }

  .VOrdersFilters__Tab,
  .VOrdersFilters__FiltersButton {
    background: var(--bg-color-64);
  }

  .VOrdersFilters__FiltersCount {
    background: var(--accent-bg-color);
  }

  .VOrdersFilters__TabIcon {
    color: var(--hint-color);
  }
</style>
