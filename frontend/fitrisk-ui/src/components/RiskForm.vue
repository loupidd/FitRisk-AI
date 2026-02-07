<template>
  <form @submit.prevent="onSubmit" class="space-y-6">
    <!-- Physical Metrics -->
    <div class="space-y-4">
      <h4 class="font-semibold text-gray-900 flex items-center gap-2">
        <span
          class="w-7 h-7 bg-linear-to-br from-indigo-600 to-indigo-700 text-white rounded-lg flex items-center justify-center text-xs font-bold shadow-sm"
          >1</span
        >
        Physical Metrics
      </h4>

      <div class="grid md:grid-cols-2 gap-4">
        <!-- Height with Spinner -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Height (cm)
          </label>
          <div class="flex items-center gap-2">
            <button
              type="button"
              class="w-10 h-10 rounded-lg bg-indigo-50 hover:bg-indigo-100 text-indigo-600 transition-all flex items-center justify-center font-semibold text-lg hover:shadow-md"
              @click="decrementHeight"
            >
              −
            </button>
            <input
              v-model="form.height"
              type="number"
              class="input text-center flex-1"
              placeholder="170"
              min="50"
              max="250"
              step="0.1"
              @blur="validateHeight"
            />

            <button
              type="button"
              class="w-10 h-10 rounded-lg bg-indigo-50 hover:bg-indigo-100 text-indigo-600 transition-all flex items-center justify-center font-semibold text-lg hover:shadow-md"
              @click="incrementHeight"
            >
              +
            </button>
          </div>
          <p class="text-xs text-gray-500 mt-1">Range: 50-250 cm</p>
          <p v-if="heightError" class="text-xs text-red-600 mt-1">
            {{ heightError }}
          </p>
        </div>

        <!-- Weight with Spinner -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Weight (kg)
          </label>
          <div class="flex items-center gap-2">
            <button
              type="button"
              class="w-10 h-10 rounded-lg bg-indigo-50 hover:bg-indigo-100 text-indigo-600 transition-all flex items-center justify-center font-semibold text-lg hover:shadow-md"
              @click="decrementWeight"
            >
              −
            </button>
            <input
              v-model="form.weight"
              type="number"
              class="input text-center flex-1"
              placeholder="70"
              min="20"
              max="300"
              step="0.1"
              @blur="validateWeight"
            />

            <button
              type="button"
              class="w-10 h-10 rounded-lg bg-indigo-50 hover:bg-indigo-100 text-indigo-600 transition-all flex items-center justify-center font-semibold text-lg hover:shadow-md"
              @click="incrementWeight"
            >
              +
            </button>
          </div>
          <p class="text-xs text-gray-500 mt-1">Range: 20-300 kg</p>
          <p v-if="weightError" class="text-xs text-red-600 mt-1">
            {{ weightError }}
          </p>
        </div>
      </div>

      <!-- BMI Preview -->
      <div
        v-if="form.height && form.weight && !heightError && !weightError"
        class="p-4 bg-linear-to-br from-indigo-50 to-blue-50 rounded-xl border border-indigo-200 shadow-sm"
      >
        <div class="flex items-center justify-between">
          <span class="text-sm font-semibold text-indigo-900"
            >Calculated BMI:</span
          >
          <span class="text-2xl font-bold text-indigo-600">{{
            calculatedBMI
          }}</span>
        </div>
        <div class="text-xs text-indigo-700 mt-1 font-medium">
          {{ bmiCategory }}
        </div>
      </div>
    </div>

    <!-- Demographics -->
    <div class="space-y-4">
      <h4 class="font-semibold text-gray-900 flex items-center gap-2">
        <span
          class="w-7 h-7 bg-linear-to-br from-indigo-600 to-indigo-700 text-white rounded-lg flex items-center justify-center text-xs font-bold shadow-sm"
          >2</span
        >
        Demographics
      </h4>

      <div class="grid md:grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Age Range
          </label>
          <select v-model.number="form.Age" class="input">
            <option v-for="(label, val) in ageOptions" :key="val" :value="val">
              {{ label }}
            </option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Annual Income
          </label>
          <select v-model.number="form.Income" class="input">
            <option
              v-for="(label, val) in incomeOptions"
              :key="val"
              :value="val"
            >
              {{ label }}
            </option>
          </select>
        </div>
      </div>
    </div>

    <!-- Health Conditions -->
    <div class="space-y-4">
      <h4 class="font-semibold text-gray-900 flex items-center gap-2">
        <span
          class="w-7 h-7 bg-linear-to-br from-indigo-600 to-indigo-700 text-white rounded-lg flex items-center justify-center text-xs font-bold shadow-sm"
          >3</span
        >
        Health Conditions
      </h4>

      <div class="grid md:grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            High Blood Pressure
          </label>
          <div class="grid grid-cols-2 gap-2">
            <button
              type="button"
              @click="form.HighBP = 0"
              :class="[
                'py-3 px-4 rounded-xl font-medium transition-all duration-200',
                form.HighBP === 0
                  ? 'bg-linear-to-br from-indigo-600 to-indigo-700 text-white shadow-md shadow-indigo-200'
                  : 'bg-gray-50 text-gray-700 hover:bg-gray-100 border border-gray-200',
              ]"
            >
              No
            </button>
            <button
              type="button"
              @click="form.HighBP = 1"
              :class="[
                'py-3 px-4 rounded-xl font-medium transition-all duration-200',
                form.HighBP === 1
                  ? 'bg-linear-to-br from-indigo-600 to-indigo-700 text-white shadow-md shadow-indigo-200'
                  : 'bg-gray-50 text-gray-700 hover:bg-gray-100 border border-gray-200',
              ]"
            >
              Yes
            </button>
          </div>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            High Cholesterol
          </label>
          <div class="grid grid-cols-2 gap-2">
            <button
              type="button"
              @click="form.HighChol = 0"
              :class="[
                'py-3 px-4 rounded-xl font-medium transition-all duration-200',
                form.HighChol === 0
                  ? 'bg-linear-to-br from-indigo-600 to-indigo-700 text-white shadow-md shadow-indigo-200'
                  : 'bg-gray-50 text-gray-700 hover:bg-gray-100 border border-gray-200',
              ]"
            >
              No
            </button>
            <button
              type="button"
              @click="form.HighChol = 1"
              :class="[
                'py-3 px-4 rounded-xl font-medium transition-all duration-200',
                form.HighChol === 1
                  ? 'bg-linear-to-br from-indigo-600 to-indigo-700 text-white shadow-md shadow-indigo-200'
                  : 'bg-gray-50 text-gray-700 hover:bg-gray-100 border border-gray-200',
              ]"
            >
              Yes
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Lifestyle -->
    <div class="space-y-4">
      <h4 class="font-semibold text-gray-900 flex items-center gap-2">
        <span
          class="w-7 h-7 bg-linear-to-br from-indigo-600 to-indigo-700 text-white rounded-lg flex items-center justify-center text-xs font-bold shadow-sm"
          >4</span
        >
        Lifestyle
      </h4>

      <div class="grid md:grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Smoking Status
          </label>
          <div class="grid grid-cols-2 gap-2">
            <button
              type="button"
              @click="form.Smoker = 0"
              :class="[
                'py-3 px-4 rounded-xl font-medium transition-all duration-200',
                form.Smoker === 0
                  ? 'bg-linear-to-br from-indigo-600 to-indigo-700 text-white shadow-md shadow-indigo-200'
                  : 'bg-gray-50 text-gray-700 hover:bg-gray-100 border border-gray-200',
              ]"
            >
              Non-Smoker
            </button>
            <button
              type="button"
              @click="form.Smoker = 1"
              :class="[
                'py-3 px-4 rounded-xl font-medium transition-all duration-200',
                form.Smoker === 1
                  ? 'bg-linear-to-br from-indigo-600 to-indigo-700 text-white shadow-md shadow-indigo-200'
                  : 'bg-gray-50 text-gray-700 hover:bg-gray-100 border border-gray-200',
              ]"
            >
              Smoker
            </button>
          </div>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Physical Activity
          </label>
          <div class="grid grid-cols-2 gap-2">
            <button
              type="button"
              @click="form.PhysActivity = 0"
              :class="[
                'py-3 px-4 rounded-xl font-medium transition-all duration-200',
                form.PhysActivity === 0
                  ? 'bg-linear-to-br from-indigo-600 to-indigo-700 text-white shadow-md shadow-indigo-200'
                  : 'bg-gray-50 text-gray-700 hover:bg-gray-100 border border-gray-200',
              ]"
            >
              Inactive
            </button>
            <button
              type="button"
              @click="form.PhysActivity = 1"
              :class="[
                'py-3 px-4 rounded-xl font-medium transition-all duration-200',
                form.PhysActivity === 1
                  ? 'bg-linear-to-br from-indigo-600 to-indigo-700 text-white shadow-md shadow-indigo-200'
                  : 'bg-gray-50 text-gray-700 hover:bg-gray-100 border border-gray-200',
              ]"
            >
              Active
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Submit Button -->
    <button
      type="submit"
      :disabled="loading || !isFormValid"
      class="w-full bg-linear-to-r from-indigo-600 to-indigo-700 text-white py-4 rounded-xl font-semibold hover:from-indigo-700 hover:to-indigo-800 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 shadow-lg shadow-indigo-200 hover:shadow-xl hover:shadow-indigo-300"
    >
      <svg
        v-if="!loading"
        class="w-5 h-5"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"
        />
      </svg>

      <svg v-else class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
        <circle
          class="opacity-25"
          cx="12"
          cy="12"
          r="10"
          stroke="currentColor"
          stroke-width="4"
        ></circle>
        <path
          class="opacity-75"
          fill="currentColor"
          d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
        ></path>
      </svg>

      <span>{{
        loading ? "Analyzing Your Health..." : "Generate Risk Assessment"
      }}</span>
    </button>

    <p
      v-if="loading"
      class="text-sm text-center text-indigo-600 font-medium animate-pulse"
    >
      Processing with KNN Machine Learning algorithm...
    </p>
  </form>
</template>

<script setup>
import { reactive, computed, ref } from "vue";

defineProps({ loading: Boolean });
const emit = defineEmits(["submit"]);

const heightError = ref("");
const weightError = ref("");

const form = reactive({
  height: null,
  weight: null,
  HighBP: 0,
  HighChol: 0,
  Smoker: 0,
  PhysActivity: 0, // Default to Inactive
  Age: 1,
  Income: 1, // Default to "Less than Rp 150 juta"
});

const ageOptions = {
  1: "18–24 years",
  2: "25–29 years",
  3: "30–34 years",
  4: "35–39 years",
  5: "40–44 years",
  6: "45–49 years",
  7: "50–54 years",
  8: "55–59 years",
  9: "60–64 years",
  10: "65–69 years",
  11: "70–74 years",
  12: "75–79 years",
  13: "80+ years",
};

const incomeOptions = {
  1: "Less than Rp 150 juta",
  2: "Rp 150 juta - Rp 225 juta",
  3: "Rp 225 juta - Rp 300 juta",
  4: "Rp 300 juta - Rp 375 juta",
  5: "Rp 375 juta - Rp 525 juta",
  6: "Rp 525 juta - Rp 750 juta",
  7: "Rp 750 juta - Rp 1.1 miliar",
  8: "Rp 1.1 miliar or more",
};

const calculatedBMI = computed(() => {
  if (!form.height || !form.weight || heightError.value || weightError.value)
    return null;
  const heightM = form.height / 100;
  const bmi = form.weight / (heightM * heightM);
  return bmi.toFixed(1);
});

const bmiCategory = computed(() => {
  const bmi = parseFloat(calculatedBMI.value);
  if (!bmi) return "";
  if (bmi < 18.5) return "Underweight";
  if (bmi < 25) return "Normal weight";
  if (bmi < 30) return "Overweight";
  return "Obese";
});

const isFormValid = computed(() => {
  const h = Number(form.height);
  const w = Number(form.weight);

  return (
    !isNaN(h) &&
    !isNaN(w) &&
    h >= 50 &&
    h <= 250 &&
    w >= 20 &&
    w <= 300 &&
    !heightError.value &&
    !weightError.value
  );
});

// Spinner button functions
function incrementHeight() {
  const current = Number(form.height) || 0;
  form.height = Math.min(current + 1, 250);
  validateHeight();
}

function decrementHeight() {
  const current = Number(form.height) || 0;
  form.height = Math.max(current - 1, 0);
  validateHeight();
}

function incrementWeight() {
  const current = Number(form.weight) || 0;
  form.weight = Math.min(current + 1, 300);
  validateWeight();
}

function decrementWeight() {
  const current = Number(form.weight) || 0;
  form.weight = Math.max(current - 1, 0);
  validateWeight();
}

// Validation functions
function validateHeight() {
  if (form.height === null || form.height === "") {
    heightError.value = "";
    return;
  }

  const value = Number(form.height);

  if (isNaN(value)) {
    heightError.value = "Invalid height";
    return;
  }

  if (value < 50) {
    heightError.value = "Height must be at least 50 cm";
  } else if (value > 250) {
    heightError.value = "Height cannot exceed 250 cm";
  } else {
    heightError.value = "";
  }
}

function validateWeight() {
  if (form.weight === null || form.weight === "") {
    weightError.value = "";
    return;
  }

  const value = Number(form.weight);

  if (isNaN(value)) {
    weightError.value = "Invalid weight";
    return;
  }

  if (value < 20) {
    weightError.value = "Weight must be at least 20 kg";
  } else if (value > 300) {
    weightError.value = "Weight cannot exceed 300 kg";
  } else {
    weightError.value = "";
  }
}

function onSubmit() {
  validateHeight();
  validateWeight();

  if (!isFormValid.value) {
    alert("Please enter valid height (50–250 cm) and weight (20–300 kg)");
    return;
  }

  emit("submit", {
    ...form,
    height: Number(form.height),
    weight: Number(form.weight),
  });
}
</script>
