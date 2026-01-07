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

    const response = await fetch("http://127.0.0.1:8000/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ data }),
    });

    const result = await response.json();

    const resultBox = document.getElementById("result");
    const bmiInfo = document.getElementById("bmi-info");
    const bmiValue = document.getElementById("bmi-value");
    const bmiCategory = document.getElementById("bmi-category");

    resultBox.style.display = "block";
    bmiInfo.style.display = "block";

    bmiValue.innerText = `BMI Value: ${result.bmi}`;
    bmiCategory.innerText = `BMI Category: ${result.bmi_category}`;

    if (result.prediction === 1) {
      resultBox.className = "result high";
      resultBox.innerHTML = `
        High Diabetes Risk<br>
        Estimated Probability: ${(result.probability * 100).toFixed(2)}%
      `;
    } else {
      resultBox.className = "result low";
      resultBox.innerHTML = `
        Low Diabetes Risk<br>
        Estimated Probability: ${(result.probability * 100).toFixed(2)}%
      `;
    }
  });
