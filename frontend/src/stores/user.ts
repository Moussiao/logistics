import { defineStore } from 'pinia';
import { getMe } from '@/api/users';
import type { User } from '@/types/users';

const useUser = defineStore('user', {
  state: (): User => {
    return {
      id: -1,
      role: '',
    };
  },
  actions: {
    async getData() {
      try {
        const user = await getMe();
        const { id, role } = user;

        this.id = id;
        this.role = role;
      } catch {}
    },
    isLoaded() {
      return this.id !== -1;
    },
  },
});

export default useUser;
