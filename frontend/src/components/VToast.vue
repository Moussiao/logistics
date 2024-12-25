<script lang="ts" setup>
  import { onMounted, onUnmounted } from 'vue';
  import { ExclamationCircleIcon } from 'vue-tabler-icons';

  export type ToastTypes = 'error';

  export interface Props {
    text: string;
    id: string;
    lifetime: number;
    type: ToastTypes;
  }

  const props = defineProps<Props>();

  const emit = defineEmits<{ delete: [id: string] }>();

  let timeout: ReturnType<typeof setTimeout>;

  onMounted(() => {
    timeout = setTimeout(() => {
      emit('delete', props.id);
    }, props.lifetime);
  });

  onUnmounted(() => {
    clearTimeout(timeout);
  });
</script>

<template>
  <div
    class="VToast flex flex-row gap-2 p-2 items-center rounded-8 cursor-pointer w-11/12 h-20 text-white"
    @click="emit('delete', id)">
    <div><ExclamationCircleIcon size="30" /></div>
    <div class="text-left">
      <div class="font-bold text-xl">Error!</div>
      <div class="font-medium">{{ text }}</div>
    </div>
  </div>
</template>

<style>
  .VToast {
    background: var(--errorColor);
  }
</style>
