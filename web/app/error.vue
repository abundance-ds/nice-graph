<script setup lang="ts">
defineProps({
  error: Object as () => { statusCode: number; message: string },
});

const handleError = () => clearError({ redirect: "/" });
</script>

<template>
  <div
    class="min-h-screen bg-white font-sans text-stone-600 flex items-center justify-center"
  >
    <div class="text-center px-6">
      <p class="text-7xl font-serif font-semibold text-stone-100">
        {{ error?.statusCode }}
      </p>
      <h1
        class="mt-4 text-xl font-serif font-semibold text-stone-900 tracking-tight"
      >
        Page not found
      </h1>
      <p class="mt-2 text-sm text-stone-400">
        The page you requested does not exist.
      </p>
      <button
        @click="handleError"
        class="mt-8 text-sm text-stone-500 hover:text-stone-900 transition-colors"
      >
        &larr; Home
      </button>
    </div>
  </div>
</template>
