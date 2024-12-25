import type { InternalAxiosRequestConfig } from 'axios';
import { cloneDeep } from 'lodash-es';

import useAuth from '@/stores/auth';
import requestCaseMiddleware from './requestCaseMiddleware';

const onRequestFulfilled = async (
  request: InternalAxiosRequestConfig,
  enableCaseMiddleware = true,
) => {
  const auth = useAuth();

  request = cloneDeep(request);

  request.headers = request.headers || {};

  if (auth.isTokenExpired()) {
    await auth.updateToken();
  }

  if (auth.token) {
    request.headers.Authorization = `Bearer ${auth.token}`;
  }

  if (!(request.data instanceof FormData)) {
    request.data = requestCaseMiddleware(request.data, enableCaseMiddleware);
  }

  return request;
};

export default onRequestFulfilled;
