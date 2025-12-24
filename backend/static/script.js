function submitForm() {
  const payload = {
    age: parseInt(document.getElementById("age").value, 10),
    state: document.getElementById("state").value.trim(),
    scenario: document.getElementById("scenario").value.trim()
  };

  fetch("/analyze", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  })
    .then(res => res.json())
    .then(data => {
      // -------------------------------
      // ADVICE PANEL
      // -------------------------------
      const adviceEl = document.getElementById("advice-text");
      adviceEl.innerText =
        data.advice || "Please reach out to one of the trusted helplines below.";

      // -------------------------------
      // HELPLINES
      // -------------------------------
      const container = document.getElementById("helplines-container");
      container.innerHTML = "";

      if (!data.helplines || data.helplines.length === 0) {
        container.innerHTML = `
          <div class="helpline">
            <div class="helpline-desc">
              No specific helplines were found for this situation.
              Please contact local emergency services if needed.
            </div>
          </div>
        `;
        return;
      }

      data.helplines.forEach(h => {
        const helplineCard = document.createElement("div");
        helplineCard.className = "helpline";

        helplineCard.onclick = () => {
          navigator.clipboard.writeText(h.phone_number);
          helplineCard.classList.add("copied");
          setTimeout(() => helplineCard.classList.remove("copied"), 1200);
        };

        helplineCard.innerHTML = `
          <div class="helpline-number">${h.phone_number}</div>
          <div class="helpline-name">${h.helpline_name}</div>
          ${
            h.description
              ? `<div class="helpline-desc">${h.description}</div>`
              : ""
          }
        `;

        container.appendChild(helplineCard);
      });
    })
    .catch(err => {
      console.error("Fetch error:", err);
      document.getElementById("advice-text").innerText =
        "Something went wrong. Please try again in a moment.";
    });
}
