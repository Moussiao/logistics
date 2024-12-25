import api_axios from './axios';
import type { EditableOrder, Order, Orders, OrdersFilters } from '@/types/orders';

export const getOrders = async (filters?: OrdersFilters): Promise<Orders> => {
  const url = '/api/delivery/orders';

  return (await api_axios.get(url, { params: filters })).data as Orders;
};

export const getOrder = async (orderId: string | number): Promise<Order> => {
  const url = `/api/delivery/orders/${orderId}`;

  return (await api_axios.get(url)).data as Order;
};

export const editOrder = async (orderId: string | number, payload: EditableOrder) => {
  const url = `/api/delivery/orders/${orderId}`;

  await api_axios.patch(url, payload);
};

export const takeOrderToJob = async (orderId: string | number) => {
  const url = `/api/delivery/orders/${orderId}/take-the-job`;

  await api_axios.post(url);
};

export const driveToCustomer = async (orderId: string | number) => {
  const url = `/api/delivery/orders/${orderId}/drive-to-customer`;

  await api_axios.post(url);
};

export const customerPaid = async (orderId: string | number) => {
  const url = `/api/delivery/orders/${orderId}/customer-paid`;

  await api_axios.post(url);
};

export const cancelOrder = async (orderId: string | number) => {
  const url = `/api/delivery/orders/${orderId}/cancel`;

  await api_axios.post(url);
};
