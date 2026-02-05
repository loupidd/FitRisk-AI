<template>
  <div class="min-h-screen bg-linear-to-br from-gray-50 via-white to-indigo-50">
    <!-- Header -->
    <header
      class="bg-white/80 backdrop-blur-md shadow-sm border-b border-gray-200 sticky top-0 z-50"
    >
      <div class="max-w-7xl mx-auto px-4 py-5">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-3">
            <div
              class="w-12 h-12 bg-linear-to-br from-indigo-600 to-indigo-700 rounded-xl flex items-center justify-center shadow-lg shadow-indigo-200"
            >
              <svg
                class="w-7 h-7 text-white"
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
              <h1 class="text-xl font-bold text-gray-900">FitRisk-AI</h1>
              <p class="text-xs text-gray-500">
                Powered by KNN Machine Learning
              </p>
            </div>
          </div>

          <div class="relative">
            <!-- Background shape for CDC badge -->
            <div
              class="absolute inset-0 bg-linear-to-r from-indigo-100 to-blue-100 rounded-lg opacity-50 blur-sm"
            ></div>
            <div
              class="relative px-4 py-2 bg-linear-to-r from-indigo-50 to-blue-50 text-indigo-700 rounded-lg text-sm font-semibold border border-indigo-200 shadow-sm"
            >
              CDC BRFSS 2015
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 py-8">
      <div class="grid lg:grid-cols-2 gap-6">
        <!-- Form Section -->
        <div class="bg-white rounded-2xl shadow-lg p-8 border border-gray-200">
          <div class="flex items-center gap-3 mb-6">
            <div
              class="w-10 h-10 bg-linear-to-br from-indigo-100 to-indigo-200 rounded-xl flex items-center justify-center"
            >
              <svg
                class="w-6 h-6 text-indigo-600"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                />
              </svg>
            </div>
            <div>
              <h3 class="text-lg font-bold text-gray-900">Health Assessment</h3>
              <p class="text-xs text-gray-500">
                Complete the form for AI-powered risk analysis
              </p>
            </div>
          </div>
          <RiskForm :loading="loading" @submit="handleSubmit" />
        </div>

        <!-- Results Section -->
        <div>
          <ResultCard v-if="result" :result="result" />

          <!-- Placeholder when no results -->
          <div
            v-else
            class="bg-white rounded-2xl shadow-lg p-10 text-center border border-gray-200 relative overflow-hidden"
          >
            <!-- Background pattern -->
            <div class="absolute inset-0 opacity-5">
              <svg
                class="w-full h-full"
                viewBox="0 0 100 100"
                preserveAspectRatio="none"
              >
                <defs>
                  <pattern
                    id="placeholder-grid"
                    width="10"
                    height="10"
                    patternUnits="userSpaceOnUse"
                  >
                    <circle
                      cx="5"
                      cy="5"
                      r="1"
                      fill="currentColor"
                      class="text-indigo-600"
                    />
                  </pattern>
                </defs>
                <rect width="100" height="100" fill="url(#placeholder-grid)" />
              </svg>
            </div>

            <div class="relative">
              <div
                class="w-20 h-20 bg-linear-to-br from-indigo-100 to-indigo-200 rounded-2xl flex items-center justify-center mx-auto mb-5 shadow-sm"
              >
                <svg
                  class="w-10 h-10 text-indigo-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
                  />
                </svg>
              </div>
              <h4 class="text-xl font-bold text-gray-900 mb-2">
                Ready to Analyze
              </h4>
              <p class="text-gray-600 text-sm max-w-sm mx-auto leading-relaxed">
                Fill out the health assessment form to receive your personalized
                diabetes risk prediction powered by advanced KNN machine
                learning.
              </p>

              <!-- Feature highlights -->
              <div class="grid grid-cols-3 gap-4 mt-8">
                <div class="text-center">
                  <div
                    class="w-12 h-12 bg-indigo-50 rounded-lg flex items-center justify-center mx-auto mb-2"
                  >
                    <svg
                      class="w-6 h-6 text-indigo-600"
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
                  <p class="text-xs font-medium text-gray-600">
                    Instant Results
                  </p>
                </div>
                <div class="text-center">
                  <div
                    class="w-12 h-12 bg-indigo-50 rounded-lg flex items-center justify-center mx-auto mb-2"
                  >
                    <svg
                      class="w-6 h-6 text-indigo-600"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"
                      />
                    </svg>
                  </div>
                  <p class="text-xs font-medium text-gray-600">AI-Powered</p>
                </div>
                <div class="text-center">
                  <div
                    class="w-12 h-12 bg-indigo-50 rounded-lg flex items-center justify-center mx-auto mb-2"
                  >
                    <svg
                      class="w-6 h-6 text-indigo-600"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M14 10l-2 1m0 0l-2-1m2 1v2.5M20 7l-2 1m2-1l-2-1m2 1v2.5M14 4l-2-1-2 1M4 7l2-1M4 7l2 1M4 7v2.5M12 21l-2-1m2 1l2-1m-2 1v-2.5M6 18l-2-1v-2.5M18 18l2-1v-2.5"
                      />
                    </svg>
                  </div>
                  <p class="text-xs font-medium text-gray-600">Personalized</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from "vue";
import RiskForm from "./components/RiskForm.vue";
import ResultCard from "./components/ResultCard.vue";

const loading = ref(false);
const result = ref(null);

async function handleSubmit(form) {
  loading.value = true;
  result.value = null;

  try {
    const heightM = form.height / 100;
    const BMI = form.weight / (heightM * heightM);

    // Let the backend calculate intelligent defaults
    const payload = {
      height_cm: form.height,
      weight_kg: form.weight,
      BMI: Number(BMI.toFixed(2)),
      HighBP: form.HighBP,
      HighChol: form.HighChol,
      Smoker: form.Smoker,
      PhysActivity: form.PhysActivity,
      Age: form.Age,
      Income: form.Income,
    };

    console.log("Sending payload:", payload);

    const API_BASE = import.meta.env.VITE_API_BASE_URL;

    const res = await fetch(`${API_BASE}/predict`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ data: payload }),
    });

    if (!res.ok) {
      throw new Error(`HTTP error! status: ${res.status}`);
    }

    result.value = await res.json();
    console.log("Received result:", result.value);
  } catch (error) {
    console.error("Prediction error:", error);
    alert("Error processing your request. Please try again.");
  } finally {
    loading.value = false;
  }
}
</script>
