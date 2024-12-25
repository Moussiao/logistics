import type { AuthToken, AuthTokenPayload } from '@/types/auth';

export const isAccessTokenExpired = (token: AuthToken): boolean => {
  const payloadBase64 = token.split('.')[1];
  const payload = JSON.parse(atob(payloadBase64)) as AuthTokenPayload;

  const now = Math.floor(new Date().getTime() / 1000);
  return now >= payload.exp;
};
