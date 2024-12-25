<script lang="ts">
  import { MoodHappyIcon } from 'vue-tabler-icons';

  export type AllowedInputModes =
    | 'text'
    | 'search'
    | 'none'
    | 'tel'
    | 'url'
    | 'email'
    | 'numeric'
    | 'decimal'
    | undefined;

  export interface Props {
    type?: string;
    placeholder?: string;
    autocomplete?: string;
    title?: string;
    name?: string;
    inputmode?: AllowedInputModes;
    leftIcon?: typeof MoodHappyIcon;
    hasCleaner?: boolean;
  }
</script>

<script lang="ts" setup>
  import { XIcon } from 'vue-tabler-icons';

  withDefaults(defineProps<Props>(), {
    type: 'text',
    placeholder: '',
    inputmode: 'text',
    hasCleaner: true,
  });

  const modelValue = defineModel({ required: true });

  const emit = defineEmits<{
    'update:modelValue': [value: string | null];
  }>();

  const onUpdate = (e: Event) => {
    const target = e.target as HTMLInputElement;
    const value = target.value;

    emit('update:modelValue', value || '');
  };

  const onClear = () => {
    emit('update:modelValue', null);
  };
</script>

<template>
  <div>
    <span v-if="title" class="VTextInput__Title text-sm">{{ title }}</span>
    <div class="VTextInput flex items-center rounded-r rounded-bl w-full px-2">
      <component v-if="leftIcon" :is="leftIcon" />
      <input
        :type="type"
        :placeholder="placeholder"
        :name="name"
        :autocomplete="autocomplete"
        :inputmode="inputmode"
        :value="modelValue"
        class="p-2.5 w-full"
        @input="onUpdate" />
      <button
        v-if="hasCleaner && modelValue"
        type="button"
        title="Очистить"
        @click.stop.prevent="onClear">
        <XIcon />
      </button>
    </div>
  </div>
</template>

<style scoped>
  .VTextInput {
    background: var(--bg-color-64);
  }
  .VTextInput__Title {
    color: var(--hint-color);
  }

  input {
    border: none;
    outline: none;
    background: transparent;
  }
  input::placeholder {
    color: var(--hint-color);
  }

  button {
    background: transparent;
  }
</style>
