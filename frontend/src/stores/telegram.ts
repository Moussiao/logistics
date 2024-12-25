import { defineStore } from 'pinia';
import { initBackButton, initMainButton, initPopup } from '@telegram-apps/sdk';
import type { BackButton, MainButton, Popup, OpenPopupOptionsButton } from '@telegram-apps/sdk';

interface State {
  popup: Popup;
  backButton: BackButton;
  mainButton: MainButton;
  onClickBackButtonListener?: () => void;
  onClickMainButtonListener?: () => void;
}

export interface OpenPopupOptions {
  title?: string;
  message: string;
  onActionButtonClick?: () => void;
}

const useTelegram = defineStore('telegram', {
  state: (): State => {
    const popup = initPopup();
    const [backButton] = initBackButton();
    const [mainButton] = initMainButton();
    return {
      popup: popup,
      backButton: backButton,
      mainButton: mainButton,
    };
  },
  actions: {
    openPopup(options: OpenPopupOptions): void {
      const buttons: OpenPopupOptionsButton[] = [
        { type: 'destructive', text: 'Нет' },
        { id: 'action', type: 'default', text: 'Да' },
      ];

      this.popup
        .open({ title: options.title, message: options.message, buttons: buttons })
        .then((buttonId) => {
          if (buttonId === 'action' && options.onActionButtonClick) {
            options.onActionButtonClick();
          }
        });
    },
    showBackButton(callback: () => void): void {
      this.offBackButtonClickListener();
      this.backButton.on('click', callback);
      this.onClickBackButtonListener = callback;

      this.backButton.show();
    },
    hideBackButton(): void {
      this.offBackButtonClickListener();
      this.backButton.hide();
    },
    offBackButtonClickListener(): void {
      if (this.onClickBackButtonListener) {
        this.backButton.off('click', this.onClickBackButtonListener);
        this.onClickBackButtonListener = undefined;
      }
    },
    showMainButton(text: string, callback: () => void): void {
      this.offMainButtonClickListener();
      this.mainButton.on('click', callback);
      this.onClickMainButtonListener = callback;

      if (!this.mainButton.isLoaderVisible) this.mainButton.enable();
      this.mainButton.setText(text);
      this.mainButton.show();
    },
    hideMainButton(): void {
      if (this.onClickMainButtonListener) {
        this.mainButton.off('click', this.onClickMainButtonListener);
        this.onClickMainButtonListener = undefined;
      }
      this.mainButton.disable();
      this.mainButton.hide();
    },
    offMainButtonClickListener(): void {
      if (this.onClickMainButtonListener) {
        this.mainButton.off('click', this.onClickMainButtonListener);
        this.onClickMainButtonListener = undefined;
      }
    },
    showMainButtonLoader(): void {
      this.mainButton.showLoader();
      this.mainButton.disable();
    },
    hideMainButtonLoader(): void {
      this.mainButton.hideLoader();
      this.mainButton.enable();
    },
  },
});

export default useTelegram;
