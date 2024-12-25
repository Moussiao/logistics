import type { User } from '@/types/users';
import api_axios from './axios';

export const getMe = async (): Promise<User> => {
  const url = '/api/users/me';

  return (await api_axios.get(url)).data as User;
};
