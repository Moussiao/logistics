import type { AxiosError, InternalAxiosRequestConfig } from 'axios';

import useAuth from '@/stores/auth';
import handleRequestError from '@/utils/handleRequestError';
import api_axios from './index';
import responseCaseMiddleware from './responseCaseMiddleware';

const onResponseRejected = async (error: AxiosError, enableCaseMiddleware: boolean) => {
  const auth = useAuth();

  if (!error.response) return Promise.reject(error);

  if (error.response.status === 401) {
    if (auth.isTokenExpired() && error.config) {
      await auth.updateToken();
      // Делаем повторный запрос с уже обновленным токеном
      return new Promise((resolve) => {
        const config = error.config as InternalAxiosRequestConfig;
        resolve(api_axios(config));
      });
    }

    auth.resetAuth();
    window.location.href = window.origin;
  }

  if (error.response.data) {
    error.response.data = responseCaseMiddleware(error.response.data as any, enableCaseMiddleware);
  }

  handleRequestError(error.response);
  return Promise.reject(error);
};

export default onResponseRejected;
