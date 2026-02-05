<template>
  <div>
    <div class="flex items-center justify-between mb-4">
      <h4 class="font-semibold text-gray-900">Recommended Exercises</h4>
      <span class="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded-full"
        >{{ exercises?.length || 0 }} exercises</span
      >
    </div>

    <div v-if="exercises?.length" class="space-y-3">
      <div
        v-for="(ex, index) in exercises.slice(0, 5)"
        :key="ex.id || ex.name"
        class="group relative bg-white border border-gray-200 rounded-xl p-5 hover:border-indigo-300 hover:shadow-md transition-all duration-300 overflow-hidden"
      >
        <!-- Gradient accent line -->
        <div
          class="absolute top-0 left-0 w-1 h-full bg-linear-to-b from-indigo-500 to-indigo-600"
        ></div>

        <!-- Number badge -->
        <div
          class="absolute top-4 right-4 w-8 h-8 bg-indigo-50 text-indigo-600 rounded-lg flex items-center justify-center text-sm font-bold group-hover:bg-indigo-100 transition-colors"
        >
          {{ index + 1 }}
        </div>

        <div class="pr-12">
          <!-- Exercise name -->
          <h5
            class="font-semibold text-gray-900 text-base mb-3 capitalize group-hover:text-indigo-600 transition-colors"
          >
            {{ ex.name }}
          </h5>

          <!-- Details grid with Equipment and Difficulty side by side -->
          <div class="grid grid-cols-2 gap-3 mb-3">
            <!-- Target -->
            <div class="col-span-2 flex items-start gap-2">
              <div
                class="w-5 h-5 bg-indigo-50 rounded flex items-center justify-center shrink-0 mt-0.5"
              >
                <svg
                  class="w-3 h-3 text-indigo-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M13 10V3L4 14h7v7l9-11h-7z"
                  />
                </svg>
              </div>
              <div>
                <p class="text-xs text-gray-500 font-medium">Target</p>
                <p class="text-sm text-gray-700 capitalize">{{ ex.target }}</p>
              </div>
            </div>

            <!-- Equipment -->
            <div class="flex items-start gap-2">
              <div
                class="w-5 h-5 bg-indigo-50 rounded flex items-center justify-center shrink-0 mt-0.5"
              >
                <svg
                  class="w-3 h-3 text-indigo-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"
                  />
                </svg>
              </div>
              <div>
                <p class="text-xs text-gray-500 font-medium">Equipment</p>
                <p class="text-sm text-gray-700 capitalize">
                  {{ ex.equipment }}
                </p>
              </div>
            </div>

            <!-- Difficulty -->
            <div class="flex items-start gap-2">
              <div
                class="w-5 h-5 bg-indigo-50 rounded flex items-center justify-center shrink-0 mt-0.5"
              >
                <svg
                  class="w-3 h-3 text-indigo-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
                  />
                </svg>
              </div>
              <div>
                <p class="text-xs text-gray-500 font-medium">Difficulty</p>
                <span
                  class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium"
                  :class="getDifficultyColor(ex.difficulty)"
                >
                  {{ capitalizeFirst(ex.difficulty || "beginner") }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- Hover overlay effect -->
        <div
          class="absolute inset-0 bg-linear-to-r from-indigo-50/0 to-indigo-50/0 group-hover:from-indigo-50/20 group-hover:to-indigo-50/0 pointer-events-none transition-all duration-300"
        ></div>
      </div>

      <!-- Exercise tips -->
      <div
        class="mt-5 bg-linear-to-br from-indigo-50 to-blue-50 border border-indigo-100 rounded-xl p-5"
      >
        <div class="flex gap-3">
          <div class="shrink-0">
            <div
              class="w-10 h-10 bg-white rounded-lg shadow-sm flex items-center justify-center"
            >
              <svg
                class="w-5 h-5 text-indigo-600"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"
                />
              </svg>
            </div>
          </div>
          <div class="flex-1">
            <p class="text-sm font-semibold text-indigo-900 mb-2">
              Exercise Guidelines
            </p>
            <ul class="space-y-1.5 text-xs text-indigo-800">
              <li class="flex items-start gap-2">
                <svg
                  class="w-4 h-4 text-indigo-500 shrink-0 mt-0.5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M5 13l4 4L19 7"
                  />
                </svg>
                <span>Start with 3 sets of 10-12 repetitions per exercise</span>
              </li>
              <li class="flex items-start gap-2">
                <svg
                  class="w-4 h-4 text-indigo-500 shrink-0 mt-0.5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M5 13l4 4L19 7"
                  />
                </svg>
                <span
                  >Rest 60-90 seconds between sets for optimal recovery</span
                >
              </li>
              <li class="flex items-start gap-2">
                <svg
                  class="w-4 h-4 text-indigo-500 shrink-0 mt-0.5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M5 13l4 4L19 7"
                  />
                </svg>
                <span
                  >Maintain proper form to prevent injury and maximize
                  results</span
                >
              </li>
              <li class="flex items-start gap-2">
                <svg
                  class="w-4 h-4 text-indigo-500 shrink-0 mt-0.5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M5 13l4 4L19 7"
                  />
                </svg>
                <span
                  >Consult a fitness professional if you're new to
                  training</span
                >
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <div
      v-else
      class="text-center py-12 bg-linear-to-br from-gray-50 to-gray-100 rounded-xl border-2 border-dashed border-gray-300"
    >
      <div
        class="w-16 h-16 bg-white rounded-full flex items-center justify-center mx-auto mb-3 shadow-sm"
      >
        <svg
          class="w-8 h-8 text-gray-400"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>
      </div>
      <p class="text-gray-600 font-medium mb-1">
        No exercise recommendations available
      </p>
      <p class="text-sm text-gray-500">
        Exercise data may be temporarily unavailable
      </p>
    </div>
  </div>
</template>

<script setup>
defineProps({
  exercises: Array,
});

function capitalizeFirst(str) {
  if (!str) return "";
  return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
}

function getDifficultyColor(difficulty) {
  if (!difficulty) return "bg-green-100 text-green-700";

  const diff = difficulty.toLowerCase();

  if (diff === "beginner") {
    return "bg-green-100 text-green-700";
  } else if (diff === "intermediate") {
    return "bg-yellow-100 text-yellow-700";
  } else if (diff === "advanced" || diff === "expert") {
    return "bg-red-100 text-red-700";
  }

  return "bg-gray-100 text-gray-700";
}
</script>
