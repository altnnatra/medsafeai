async function checkDrug() {
  const drug = document.getElementById("drugInput").value;
  const responseDiv = document.getElementById("response");
  responseDiv.innerHTML = "Loading...";

  const res = await fetch("http://127.0.0.1:8000/check", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ drug }),
  });

  const data = await res.json();
  responseDiv.innerHTML = "";

  const sections = {
    "Contraindications": "contraindications",
    "How to use / Dosage guidelines": "usage",
    "Possible side effects": "side-effects",
    "Should not be combined with": "interactions",
  };

  for (const [title, key] of Object.entries(sections)) {
    const block = document.createElement("div");
    block.className = `response-card ${key}`;

    const heading = document.createElement("h3");
    heading.textContent = title;

    const content = document.createElement("ul");

    const items = data[key] && data[key] !== "No information available."
      ? data[key].split("\n").filter(line => line.trim().startsWith("-"))
      : ["No information available."];

    for (const item of items) {
      const li = document.createElement("li");
      li.textContent = item.replace(/^[-•]\s*/, "").trim();
      content.appendChild(li);
    }

    block.appendChild(heading);
    block.appendChild(content);
    responseDiv.appendChild(block);
  }
}
