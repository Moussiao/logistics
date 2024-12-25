import { defineStore } from 'pinia';
import { retrieveLaunchParams } from '@telegram-apps/sdk';

import { createAccessToken } from '@/api/auth';
import type { AuthToken } from '@/types/auth';
import { isAccessTokenExpired } from '@/utils/auth';

type AuthStoreState = {
  token: AuthToken | undefined;
};

const useAuth = defineStore('auth', {
  state: (): AuthStoreState => {
    return {
      token: undefined,
    };
  },
  actions: {
    async createToken() {
      try {
        const telegramInitData = retrieveLaunchParams().initDataRaw;
        if (telegramInitData) {
          const token = await createAccessToken(telegramInitData);
          this.token = token;
        }
      } catch {}
    },
    async updateToken() {
      this.resetAuth();
      await this.createToken();
    },
    isTokenExpired() {
      if (!this.token) {
        return false;
      }

      try {
        return isAccessTokenExpired(this.token);
      } catch {
        return false;
      }
    },
    resetAuth() {
      this.token = undefined;
    },
  },
  persist: true,
});

export default useAuth;
