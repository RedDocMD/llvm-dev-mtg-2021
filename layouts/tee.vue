<script setup lang="ts">
const props = defineProps({
  class: {
    type: String,
  },
});
</script>

<template>
  <div class="slidev-layout two-columns w-full h-full flex flex-col">
    <div class="col-span-2" :class="props.class">
      <slot />
    </div>
    <div class="grid grid-cols-2 pt-5">
      <div class="col-left pr-3 content-start" :class="props.class">
        <slot name="left" />
      </div>
      <div class="col-right pl-3 content-start" :class="props.class">
        <slot name="right" />
      </div>
    </div>
  </div>
</template>