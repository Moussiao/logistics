import type { AuthToken } from '@/types/auth';
import api_axios from './axios';

export const createAccessToken = async (tma_init_data: string): Promise<AuthToken> => {
  const url = '/api/auth/access_token';
  const data = { tma_init_data: tma_init_data };

  return (await api_axios.post(url, data)).data.token as AuthToken;
};
