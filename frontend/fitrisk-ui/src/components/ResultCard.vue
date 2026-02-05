<template>
  <div
    class="bg-white rounded-2xl shadow-lg border border-gray-200 overflow-hidden"
  >
    <!-- Risk Status Header with gradient -->
    <div
      :class="[
        'p-8 relative overflow-hidden',
        result.prediction === 1
          ? 'bg-linear-to-br from-red-500 to-red-600'
          : 'bg-linear-to-br from-indigo-600 to-indigo-700',
      ]"
    >
      <!-- Background pattern -->
      <div class="absolute inset-0 opacity-10">
        <svg
          class="w-full h-full"
          viewBox="0 0 100 100"
          preserveAspectRatio="none"
        >
          <defs>
            <pattern
              id="grid"
              width="10"
              height="10"
              patternUnits="userSpaceOnUse"
            >
              <circle cx="5" cy="5" r="1" fill="white" />
            </pattern>
          </defs>
          <rect width="100" height="100" fill="url(#grid)" />
        </svg>
      </div>

      <div class="relative">
        <div class="flex items-start justify-between">
          <div class="flex-1">
            <div class="flex items-center gap-2 mb-3">
              <div
                class="w-10 h-10 bg-white/20 backdrop-blur-sm rounded-lg flex items-center justify-center"
              >
                <svg
                  class="w-6 h-6 text-white"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    v-if="result.prediction === 1"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                  />
                  <path
                    v-else
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
              </div>
              <span class="text-white/90 text-sm font-medium"
                >Risk Assessment Result</span
              >
            </div>

            <h3 class="text-3xl font-bold text-white mb-2">
              {{
                result.prediction === 1
                  ? "High Diabetes Risk"
                  : "Low Diabetes Risk"
              }}
            </h3>

            <p class="text-white/90 text-sm">
              {{
                result.prediction === 1
                  ? "Immediate lifestyle changes recommended"
                  : "Continue maintaining a healthy lifestyle"
              }}
            </p>
          </div>

          <!-- Probability Badge -->
          <div
            class="bg-white/20 backdrop-blur-sm rounded-2xl px-5 py-4 text-center border border-white/30"
          >
            <div class="text-4xl font-bold text-white mb-1">
              {{ displayProbability }}
            </div>
            <div
              class="text-white/80 text-xs font-medium uppercase tracking-wide"
            >
              Risk Level
            </div>
          </div>
        </div>

        <!-- Progress bar -->
        <div class="mt-6">
          <div
            class="bg-white/20 rounded-full h-2 overflow-hidden backdrop-blur-sm"
          >
            <div
              class="h-full bg-white rounded-full transition-all duration-1000 ease-out"
              :style="{ width: progressWidth + '%' }"
            ></div>
          </div>
          <div
            class="flex justify-between mt-2 text-xs text-white/70 font-medium"
          >
            <span>Low Risk</span>
            <span>Moderate</span>
            <span>High Risk</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Content Section -->
    <div class="p-8 space-y-6">
      <!-- BMI Section -->
      <div
        class="bg-linear-to-br from-gray-50 to-gray-100 rounded-xl p-6 border border-gray-200"
      >
        <div class="flex items-center gap-3 mb-4">
          <div
            class="w-10 h-10 bg-indigo-100 rounded-lg flex items-center justify-center"
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
                d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
              />
            </svg>
          </div>
          <div>
            <h4 class="font-semibold text-gray-900">Body Mass Index</h4>
            <p class="text-xs text-gray-500">BMI Calculator Result</p>
          </div>
        </div>

        <div class="flex items-baseline gap-3 mb-3">
          <span class="text-4xl font-bold text-gray-900">{{ result.bmi }}</span>
          <span
            class="text-lg font-semibold px-3 py-1 rounded-lg"
            :class="getBMIColorClasses(result.bmi_category)"
          >
            {{ result.bmi_category }}
          </span>
        </div>

        <p class="text-sm text-gray-600 leading-relaxed mb-4">
          {{ result.bmi_description }}
        </p>

        <!-- BMI Scale -->
        <div class="space-y-2">
          <div class="flex gap-1 h-3 rounded-full overflow-hidden">
            <div class="flex-1 bg-blue-400"></div>
            <div class="flex-1 bg-green-400"></div>
            <div class="flex-1 bg-yellow-400"></div>
            <div class="flex-1 bg-orange-400"></div>
            <div class="flex-1 bg-red-400"></div>
          </div>
          <div class="flex justify-between text-xs text-gray-500 font-medium">
            <span>&lt;18.5</span>
            <span>18.5-25</span>
            <span>25-30</span>
            <span>30-35</span>
            <span>35+</span>
          </div>
        </div>
      </div>

      <div
        class="h-px bg-linear-to-r from-transparent via-gray-300 to-transparent"
      ></div>

      <!-- Exercise Recommendations -->
      <ExerciseList :exercises="result.exercises" />

      <!-- Health Disclaimer -->
      <div
        class="bg-linear-to-br from-amber-50 to-yellow-50 border border-amber-200 rounded-xl p-5"
      >
        <div class="flex gap-3">
          <div class="shrink-0">
            <div
              class="w-10 h-10 bg-white rounded-lg shadow-sm flex items-center justify-center"
            >
              <svg
                class="w-5 h-5 text-amber-600"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                />
              </svg>
            </div>
          </div>
          <div class="flex-1">
            <p class="text-sm font-semibold text-amber-900 mb-2">
              Important Medical Disclaimer
            </p>
            <p class="text-xs text-amber-800 leading-relaxed">
              This assessment is powered by AI and machine learning for
              informational purposes only. It should not replace professional
              medical advice, diagnosis, or treatment. Please consult with a
              qualified healthcare provider for proper medical evaluation and
              guidance.
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";
import ExerciseList from "./ExerciseList.vue";

const props = defineProps({
  result: Object,
});

const displayProbability = computed(() => {
  const prob = props.result.probability;
  if (prob === null || prob === undefined || isNaN(prob)) {
    return "N/A";
  }
  return (prob * 100).toFixed(0) + "%";
});

const progressWidth = computed(() => {
  const prob = props.result.probability;
  if (prob === null || prob === undefined || isNaN(prob)) {
    return 0;
  }
  return Math.min(100, Math.max(0, prob * 100));
});

function getBMIColorClasses(category) {
  if (!category) return "bg-gray-100 text-gray-700";

  const categoryLower = category.toLowerCase();

  if (categoryLower.includes("underweight")) {
    return "bg-blue-100 text-blue-700";
  } else if (categoryLower.includes("normal")) {
    return "bg-green-100 text-green-700";
  } else if (categoryLower.includes("overweight")) {
    return "bg-yellow-100 text-yellow-700";
  } else if (categoryLower.includes("obese")) {
    return "bg-red-100 text-red-700";
  }

  return "bg-gray-100 text-gray-700";
}
</script>
