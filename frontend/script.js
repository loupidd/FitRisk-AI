document
  .getElementById("riskForm")
  .addEventListener("submit", async function (e) {
    e.preventDefault();

    const heightCm = Number(document.getElementById("height").value);
    const weightKg = Number(document.getElementById("weight").value);

    const heightM = heightCm / 100;
    const BMI = weightKg / (heightM * heightM);

    const data = {
      HighBP: Number(document.getElementById("HighBP").value),
      HighChol: Number(document.getElementById("HighChol").value),
      CholCheck: 1,
      BMI: Number(BMI.toFixed(2)),
      Smoker: Number(document.getElementById("Smoker").value),
      Stroke: 0,
      HeartDiseaseorAttack: 0,
      PhysActivity: Number(document.getElementById("PhysActivity").value),
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
      Age: Number(document.getElementById("Age").value),
      Education: 4,
      Income: Number(document.getElementById("Income").value),
    };

    const loading = document.getElementById("loading");
    loading.style.display = "block";

    const response = await fetch("http://127.0.0.1:8000/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ data }),
    });

    loading.style.display = "none";

    const result = await response.json();

    const resultBox = document.getElementById("result");

    resultBox.style.display = "block";

    resultBox.innerHTML = `
  <b>${result.prediction === 1 ? "High" : "Low"} Diabetes Risk</b><br>
  Estimated Probability: ${(result.probability * 100).toFixed(2)}%
  <hr>
  <b>BMI</b><br>
  ${result.bmi} (${result.bmi_category})<br>
  <small>${result.bmi_description}</small>
  <hr>
  <b>Recommended Exercises</b>
  ${renderExercises(result.exercises)}
`;

    function renderExercises(exercises) {
      if (!exercises || exercises.length === 0) {
        return "<i>No exercise recommendations available.</i>";
      }

      return exercises
        .slice(0, 5)
        .map(
          (ex) => `
      <div style="margin-top:10px; padding:8px; border-left:4px solid #2563eb">
        <b>${ex.name}</b><br>
        Target: ${ex.target}<br>
        Equipment: ${ex.equipment}
      </div>
    `,
        )
        .join("");
    }
  });
