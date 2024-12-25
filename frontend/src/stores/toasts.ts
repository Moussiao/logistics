import { defineStore } from 'pinia';
import { uuid } from '@/utils/uuid';

type VToastType = 'error';

export class VToastMessage {
  text: string;
  id: string;
  lifetime: number;
  type: VToastType;

  constructor(text: string, type: VToastType, lifetime = 5000) {
    this.text = text;
    this.type = type;
    this.id = uuid();
    this.lifetime = lifetime;
  }
}

interface State {
  messages: VToastMessage[];
  disabled: boolean;
}

const useToasts = defineStore('toasts', {
  state: (): State => {
    return {
      messages: [],
      disabled: false,
    };
  },
  actions: {
    addMessage(text: string, type: VToastType) {
      if (this.disabled) return;
      this.messages = [...this.messages, new VToastMessage(text, type)];
    },
    removeMessage(id: string) {
      this.messages = this.messages.filter((message) => message.id !== id);
    },
    disable() {
      this.messages = [];
      this.disabled = true;
    },
    enable() {
      this.disabled = false;
    },
  },
});

export default useToasts;
