import {
  CircleCheckIcon,
  Error404Icon,
  PackageExportIcon,
  PackageImportIcon,
  PackageOffIcon,
  TruckDeliveryIcon,
} from 'vue-tabler-icons';
import type { Dictionary } from './dictionary';
import type { Option } from '@/types/select';
import type { Order, OrdersItem } from '@/types/orders';

export const OrderStateVerboseByValue: Dictionary<string> = {
  new: 'Новый',
  processing: 'В обработке',
  delivery: 'В пути',
  paid: 'Оплачен',
  canceled: 'Отменен',
};

export const OrderStateOptions: Option[] = Object.entries(OrderStateVerboseByValue).map((entry) => {
  return { value: entry[0], name: entry[1] };
});

export const getOptionByOrderState = (state: string): Option => {
  const verbose = OrderStateVerboseByValue[state] || state;
  return { value: state, name: verbose };
};

export const getOrderStateVerbose = (order: Order | OrdersItem): string => {
  return OrderStateVerboseByValue[order.state] || order.state;
};

export const getIconByOrderState = (state: string): typeof CircleCheckIcon => {
  if (state === 'new') return PackageImportIcon;
  if (state === 'processing') return PackageExportIcon;
  if (state === 'delivery') return TruckDeliveryIcon;
  if (state === 'paid') return CircleCheckIcon;
  if (state === 'canceled') return PackageOffIcon;

  return Error404Icon;
};
