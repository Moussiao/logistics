<script lang="ts" setup>
  import Multiselect from 'vue-multiselect';
  import type { Option } from '@/types/select';

  export interface Props {
    options: Option[];
    placeholder?: string;
  }

  withDefaults(defineProps<Props>(), {
    placeholder: '',
  });

  const modelValue = defineModel({ required: true });
</script>

<template>
  <multiselect
    v-model="modelValue"
    label="name"
    :options="options"
    :searchable="false"
    :placeholder="placeholder"
    class="rounded p-2.5 w-full" />
</template>

<style>
  .multiselect {
    background: var(--bg-color-64);
  }
  .multiselect__placeholder {
    color: var(--hint-color);
  }

  .multiselect {
    position: relative;
  }

  .multiselect--active .multiselect__select {
    transform: rotateZ(180deg);
  }

  .multiselect__input,
  .multiselect__single {
    display: inline-block;
    width: calc(100%);
  }

  .multiselect__tags {
    min-height: 40px;
    border: 1px solid #e8e8e8;
    background: transparent;
  }

  .multiselect__select {
    position: absolute;
    height: 38px;
    right: 1px;
    top: 1px;
  }

  .multiselect__select::before {
    position: relative;
    top: 65%;
    border-width: 5px 5px 0 5px;
    border-color: #999 transparent transparent transparent;
    content: '';
  }

  .multiselect__content {
    min-width: 100%;
  }

  .multiselect__option {
    display: block;
    min-height: 40px;
    position: relative;
  }
</style>
