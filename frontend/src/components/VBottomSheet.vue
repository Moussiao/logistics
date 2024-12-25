<script lang="ts" setup>
  import { ref } from 'vue';
  import { onClickOutside } from '@vueuse/core';

  const target = ref<HTMLElement | null>(null);
  const visible = defineModel<boolean>({ required: true });

  onClickOutside(target, () => (visible.value = false));
</script>

<template>
  <Teleport to="body">
    <Transition name="bottom-sheet">
      <div
        v-if="visible"
        class="VBottomSheetWrapper flex items-end justify-center fixed left-0 top-0 h-full w-full">
        <div
          ref="target"
          class="VBottomSheet rounded-t w-full max-w-screen-sm overflow-y-auto grid gap-2">
          <div class="VBottomSheet__Header"><slot name="header" /></div>
          <div class="VBottomSheet__Body"><slot /></div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style>
  .VBottomSheetWrapper {
    background-color: rgba(0, 0, 0, 0.35);
  }

  .VBottomSheet {
    background-color: var(--section-bg-color);
    min-height: var(--bottom-sheet-min-width, 33%);
    max-height: var(--bottom-sheet-max-height, 66%);
  }

  .bottom-sheet-enter-active,
  .bottom-sheet-leave-active {
    transition: all 300ms ease;
  }

  .bottom-sheet-enter-from,
  .bottom-sheet-leave-to {
    opacity: 0;
  }
</style>
