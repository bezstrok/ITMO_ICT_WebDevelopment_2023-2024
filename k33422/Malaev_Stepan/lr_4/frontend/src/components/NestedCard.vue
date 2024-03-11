<template>
  <v-card class="my-3" outlined>
    <v-card-title>{{ title }}</v-card-title>
    <v-card-text>
      <v-row>
        <template v-for="(value, key) in obj" :key="`nested-${key}`">
          <v-col cols="12" md="6">
            <div v-if="isNestedObject(value)">
              <NestedCard :obj="value" :title="formatTitle(key)"/>
            </div>
            <div v-else class="d-flex justify-start align-center">
              <v-icon class="mr-2">mdi-chevron-right</v-icon>
              <div>
                <div class="text-subtitle-2">{{ formatTitle(key) }}</div>
                <div class="text-caption">{{ formatValue(value) }}</div>
              </div>
            </div>
          </v-col>
        </template>
      </v-row>
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

<style scoped>
.d-flex {
  display: flex;
}

.justify-start {
  justify-content: flex-start;
}

.align-center {
  align-items: center;
}

.mr-2 {
  margin-right: 8px;
}
</style>
