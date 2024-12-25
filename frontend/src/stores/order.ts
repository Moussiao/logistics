import { defineStore } from 'pinia';
import { isEmpty } from 'lodash-es';
import { getOrder, editOrder } from '@/api/orders';
import type { EditableOrder, Order } from '@/types/orders';
import { filterDictionary, type Dictionary } from '@/utils/dictionary';

const useOrder = defineStore('order', {
  state: (): Order => {
    return {
      id: -1,
      externalId: -1,
      externalVerbose: '',
      state: '',
      stateChangedAt: '',
      deliveryDate: '',
      expectedDeliveryDate: '',
      totalPrice: 0,
      createdAt: '',
      updatedAt: '',
      comment: '',
      customer: undefined,
      customerAddress: undefined,
      products: [],
    };
  },
  actions: {
    async getData(orderId: string | number) {
      try {
        const order = await getOrder(orderId);
        const {
          id,
          externalId,
          externalVerbose,
          state,
          stateChangedAt,
          deliveryDate,
          expectedDeliveryDate,
          totalPrice,
          createdAt,
          updatedAt,
          comment,
          customer,
          customerAddress,
          products,
        } = order;

        this.id = id;
        this.externalId = externalId;
        this.externalVerbose = externalVerbose;
        this.state = state;
        this.stateChangedAt = stateChangedAt;
        this.deliveryDate = deliveryDate;
        this.expectedDeliveryDate = expectedDeliveryDate;
        this.totalPrice = totalPrice;
        this.createdAt = createdAt;
        this.updatedAt = updatedAt;
        this.comment = comment;
        this.customer = customer;
        this.customerAddress = customerAddress;
        this.products = products;
      } catch {}
    },
    async setData(updates: EditableOrder) {
      const data = filterDictionary(updates, (value, key) => {
        return (this as Dictionary<any>)[key] !== value;
      });
      if (isEmpty(data)) return;

      try {
        await editOrder(this.id, data);
      } catch {}
    },
  },
});

export default useOrder;
