<script lang="ts" setup>
  export type AllowedTags = 'h1' | 'h2' | 'h3' | 'div';

  export interface Props {
    tag?: AllowedTags;
  }

  withDefaults(defineProps<Props>(), {
    tag: 'h2',
  });
</script>

<template>
  <component
    :is="tag"
    class="font-display font-bold"
    :class="{
      'text-4xl': tag === 'h1',
      'text-2xl': tag === 'h2',
      'text-xl': tag === 'h3',
    }">
    <slot />
  </component>
</template>
