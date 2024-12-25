import { MoodHappyIcon } from 'vue-tabler-icons';

export type Tab = {
  id: number;
  name: string;
  disabled?: boolean;
  leftIcon?: typeof MoodHappyIcon;
};
