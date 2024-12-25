<script lang="ts" setup>
  import VFiltersTab from '@/components/Orders/VOrdersFiltersTab.vue';
  import type { Tab } from '@/types/tabs';

  export interface Props {
    tabs: Tab[];
    activeTab: number;
  }

  const props = defineProps<Props>();

  const emit = defineEmits(['onTabClick']);

  const changeTab = (tabId: number) => {
    if (tabId !== props.activeTab) {
      emit('onTabClick', tabId);
    }
  };
</script>

<template>
  <div class="flex items-center gap-2 overflow-x-auto">
    <VFiltersTab
      v-for="tab in tabs"
      :key="tab.id"
      :name="tab.name"
      :isActive="tab.id === activeTab"
      :leftIcon="tab.leftIcon"
      :disabled="tab.disabled && tab.id !== activeTab"
      @click="changeTab(tab.id)" />
  </div>
</template>
