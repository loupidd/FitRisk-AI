import RiskForm from "./components/RiskForm.js";
import ResultCard from "./components/ResultCard.vue";

const { createApp } = Vue;

createApp({
  components: { RiskForm, ResultCard },

  data() {
    return {
      loading: false,
      result: null,
    };
  },

  methods: {
    async handleSubmit(form) {
      this.loading = true;
      this.result = null;

      const heightM = form.height / 100;
      const BMI = form.weight / (heightM * heightM);

      const payload = {
        HighBP: form.HighBP,
        HighChol: form.HighChol,
        CholCheck: 1,
        BMI: Number(BMI.toFixed(2)),
        Smoker: form.Smoker,
        Stroke: 0,
        HeartDiseaseorAttack: 0,
        PhysActivity: form.PhysActivity,
        Fruits: 1,
        Veggies: 1,
        HvyAlcoholConsump: 0,
        AnyHealthcare: 1,
        NoDocbcCost: 0,
        GenHlth: 3,
        MentHlth: 0,
        PhysHlth: 0,
        DiffWalk: 0,
        Sex: 1,
        Age: form.Age,
        Education: 4,
        Income: form.Income,
      };

      const res = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ data: payload }),
      });

      this.result = await res.json();
      this.loading = false;
    },
  },

  template: `
  <div class="max-w-2xl mx-auto bg-white p-8 rounded-xl shadow-lg">
    <h1 class="text-3xl font-bold text-center mb-2">FitRisk-AI</h1>
    <p class="text-center text-gray-500 text-sm mb-6">
      Diabetes risk prediction using ML
    </p>

    <RiskForm :loading="loading" @submit="handleSubmit" />
    <ResultCard v-if="result" :result="result" />
  </div>
  `,
}).mount("#app");
