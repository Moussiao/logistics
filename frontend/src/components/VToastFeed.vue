<script lang="ts" setup>
  import { storeToRefs } from 'pinia';
  import VToast from '@/components/VToast.vue';
  import useToasts from '@/stores/toasts';

  const toasts = useToasts();
  const { messages } = storeToRefs(toasts);

  const handleDelete = (id: string) => {
    toasts.removeMessage(id);
  };
</script>

<template>
  <div class="fixed right-0 top-4 left-0 flex flex-col items-center gap-4">
    <TransitionGroup name="toast">
      <VToast
        v-for="message in messages"
        v-bind="message"
        :key="message.id"
        @delete="handleDelete" />
    </TransitionGroup>
  </div>
</template>

<style>
  .toast-enter-active,
  .toast-leave-active {
    transition: all 300ms ease;
  }

  .toast-enter-from,
  .toast-leave-to {
    opacity: 0;
    transform: translateX(100%);
  }
</style>
