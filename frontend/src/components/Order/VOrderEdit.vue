<script lang="ts" setup>
  import { ref, watch, onMounted } from 'vue';
  import VTextInput from '@/components/VTextInput.vue';
  import useOrder from '@/stores/order';
  import useTelegram from '@/stores/telegram';

  const emit = defineEmits(['orderUpdated']);

  const order = useOrder();
  const telegram = useTelegram();

  const isChanged = ref<boolean>(false);
  const comment = ref<string | undefined>(undefined);

  watch(comment, () => {
    if (isChanged.value) return;
    if (comment.value !== order.comment) {
      telegram.showMainButton('Сохранить', async () => {
        telegram.showMainButtonLoader();
        await order.setData({ comment: comment.value || '' });
        telegram.hideMainButtonLoader();
        emit('orderUpdated');
      });
      isChanged.value = true;
    }
  });

  onMounted(() => {
    comment.value = order.comment;
  });
</script>

<template>
  <div class="flex flex-col gap-2 px-2 pb-2">
    <VTextInput v-model="comment" title="Комментарий" placeholder="Введите комментарий к заказу" />
  </div>
</template>
