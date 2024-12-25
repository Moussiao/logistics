import type { AxiosResponse } from 'axios';
import useToasts from '@/stores/toasts';

const handleRequestError = (response: AxiosResponse) => {
  if (response.status < 300) return;

  const toasts = useToasts();
  if (response.status == 401) {
    toasts.addMessage('Нет доступа', 'error');
  } else {
    toasts.addMessage('Не удалось выполнить запрос', 'error');
  }
};

export default handleRequestError;
