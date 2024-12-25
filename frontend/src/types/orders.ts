export type OrdersItem = {
  id: number;
  state: string;
  totalPrice: number;
  deliveryDate: string;
  expectedDeliveryDate: string;
};

export type Orders = {
  items: OrdersItem[];
  nextCursor: string | null;
};

export type OrdersFilters = {
  cursor?: string | null;
  ids?: number[];
  states?: string;
};

export type Customer = {
  id: number;
  name: string;
  email: string;
  phone: string;
  gender: string;
};

export type CustomerAddress = {
  id: number;
  countryName: string;
  regionName: string;
  cityName: string;
  postcode: string;
  street: string;
  houseNumber: string;
  flatNumber: string;
  comment: string;
};

export type OrderProduct = {
  productId: number;
  productName: string;
  totalPrice: number;
  quantity: number;
};

export type Order = {
  id: number;
  externalId: number;
  externalVerbose: string;
  state: string;
  stateChangedAt: string;
  deliveryDate: string;
  expectedDeliveryDate: string;
  totalPrice: number;
  createdAt: string;
  updatedAt: string;
  comment: string;
  customer: Customer | undefined;
  customerAddress: CustomerAddress | undefined;
  products: OrderProduct[];
};

export type EditableOrder = {
  comment?: string;
};
