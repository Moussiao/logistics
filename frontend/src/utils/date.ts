import dayjs from 'dayjs';
import 'dayjs/locale/ru';

dayjs.locale('ru');

export const formatDate = (date: dayjs.ConfigType, format: string): string => {
  return dayjs(date).format(format);
};
