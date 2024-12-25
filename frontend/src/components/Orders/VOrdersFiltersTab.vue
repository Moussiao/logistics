<script lang="ts" setup>
  import { MoodHappyIcon } from 'vue-tabler-icons';
  export interface Props {
    name: string;
    isActive?: boolean;
    disabled?: boolean;
    leftIcon?: typeof MoodHappyIcon;
  }

  withDefaults(defineProps<Props>(), { isActive: false });
</script>

<template>
  <div
    v-if="!disabled"
    class="VFiltersTab flex items-center rounded px-2 py-1 w-full"
    :class="{ active: isActive }">
    <component v-if="leftIcon" :is="leftIcon" class="VFiltersTab__Icon mr-1" />
    {{ name }}
  </div>
</template>

<style scoped>
  .icon-tabler {
    color: var(--hint-color);
  }

  .VFiltersTab {
    background: var(--bg-color-64);
  }

  .VFiltersTab.active {
    background: var(--accent-bg-color);
  }

  .VFiltersTab.active .VFiltersTab__Icon {
    color: var(--text-color);
  }
</style>
