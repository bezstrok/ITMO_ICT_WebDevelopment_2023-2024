<template>
  <v-card outlined class="my-3">
    <v-card-title>{{ title }}</v-card-title>
    <v-card-text>
      <template v-for="(value, key) in obj" :key="`nested-${key}`">
        <div v-if="isNestedObject(value)">
          <NestedCard :obj="value" :title="formatTitle(key)"/>
        </div>
        <v-list v-else two-line dense>
          <v-list-item>
            <v-list-item-title>{{ formatTitle(key) }}</v-list-item-title>
            <v-list-item-subtitle>{{ formatValue(value) }}</v-list-item-subtitle>
          </v-list-item>
        </v-list>
      </template>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: 'NestedCard',
  props: {
    obj: Object,
    title: String,
  },
  methods: {
    formatTitle(key) {
      return key.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
    },
    formatValue(value) {
      if (typeof value === 'object' && value !== null) {
        return JSON.stringify(value, null, 2); // Fallback for non-nested objects
      }
      return value.toString();
    },
    isNestedObject(value) {
      return typeof value === 'object' && value !== null && !Array.isArray(value);
    },
  },
};
</script>
