import { defineStore } from 'pinia';
import { isEqual } from 'lodash-es';
import { getOrders } from '@/api/orders';
import type { OrdersItem, OrdersFilters } from '@/types/orders';

interface State {
  items: OrdersItem[];
  nextCursor: string | null;
  currentFilters: OrdersFilters | undefined;
}

const useOrders = defineStore('orders', {
  state: (): State => ({
    items: [],
    nextCursor: null,
    currentFilters: undefined,
  }),
  actions: {
    async getData(filters: OrdersFilters) {
      if (isEqual(filters, this.currentFilters) && this.items.length !== 0) return;
      try {
        const response = await getOrders(filters);
        this.items = response.items;
        this.nextCursor = response.nextCursor;
        this.currentFilters = filters;
      } catch {
        this.clean();
      }
    },
    async loadMore() {
      try {
        const filters = { ...this.currentFilters };
        filters.cursor = this.nextCursor;
        const response = await getOrders(filters);
        this.items.push(...response.items);
        this.nextCursor = response.nextCursor;
      } catch {
        this.nextCursor = null;
      }
    },
    clean() {
      this.items = [];
      this.nextCursor = null;
    },
  },
});

export default useOrders;
