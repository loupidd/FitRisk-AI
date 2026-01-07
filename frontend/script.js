function predict() {
  fetch("http://localhost:8000/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      HighBP: 1,
      HighChol: 1,
      BMI: 30,
      Smoker: 0,
      Stroke: 0,
      HeartDiseaseorAttack: 0,
      PhysActivity: 1,
      Fruits: 1,
      Veggies: 1,
      HvyAlcoholConsump: 0,
      AnyHealthcare: 1,
      NoDocbcCost: 0,
      GenHlth: 3,
      MentHlth: 5,
      PhysHlth: 2,
      DiffWalk: 0,
      Sex: 1,
      Age: 9,
      Education: 4,
      Income: 6,
    }),
  })
    .then((res) => res.json())
    .then((data) => {
      document.getElementById("result").innerText =
        "Diabetes Risk: " + (data.diabetes_risk === 1 ? "YES" : "NO");
    });
}
