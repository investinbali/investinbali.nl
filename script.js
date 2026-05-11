function formatCurrency(value) {
  return new Intl.NumberFormat("nl-NL", {
    style: "currency",
    currency: "EUR",
    maximumFractionDigits: 0,
  }).format(value);
}

function calculateRoi() {
  const investment = Number(document.getElementById("investment")?.value || 0);
  const dailyRate = Number(document.getElementById("dailyRate")?.value || 0);
  const occupancy = Number(document.getElementById("occupancy")?.value || 0) / 100;
  const costs = Number(document.getElementById("costs")?.value || 0) / 100;

  const revenue = dailyRate * 365 * occupancy;
  const netRevenue = revenue * (1 - costs);
  const roi = investment > 0 ? (netRevenue / investment) * 100 : 0;

  const revenueValue = document.getElementById("revenueValue");
  const netValue = document.getElementById("netValue");
  const roiValue = document.getElementById("roiValue");
  const summary = document.getElementById("calculatorSummary");

  if (!revenueValue || !netValue || !roiValue || !summary) {
    return;
  }

  revenueValue.textContent = formatCurrency(revenue);
  netValue.textContent = formatCurrency(netRevenue);
  roiValue.textContent = `${roi.toFixed(1)}%`;
  summary.textContent = `Bij deze aannames kom je indicatief uit op ${formatCurrency(
    netRevenue
  )} netto-opbrengst per jaar en een netto rendement van ${roi.toFixed(1)}%.`;
}

document.getElementById("calculateButton")?.addEventListener("click", calculateRoi);

if (document.getElementById("calculateButton")) {
  calculateRoi();
}

const FORM_ENDPOINT =
  window.INVEST_IN_BALI_FORM_ENDPOINT ||
  document.querySelector("meta[name='form-endpoint']")?.content ||
  "/api/contact";

const CALENDAR_URL =
  window.INVEST_IN_BALI_CALENDAR_URL ||
  document.querySelector("meta[name='calendar-url']")?.content ||
  "";

function getTrackingFields() {
  const params = new URLSearchParams(window.location.search);
  return {
    utm_source: params.get("utm_source") || "",
    utm_medium: params.get("utm_medium") || "",
    utm_campaign: params.get("utm_campaign") || "",
  };
}

document.querySelectorAll(".prepared-form").forEach((form) => {
  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    if (!form.reportValidity()) {
      return;
    }

    const button = form.querySelector("button[type='submit']");
    const success = form.querySelector(".form-success");
    const nextStep = form.querySelector(".form-next-step");
    let error = form.querySelector(".form-error");

    if (!error) {
      error = document.createElement("p");
      error.className = "form-error";
      error.hidden = true;
      form.append(error);
    }

    if (success) {
      success.hidden = true;
    }
    if (nextStep) {
      nextStep.hidden = true;
      nextStep.textContent = "";
    }
    error.hidden = true;

    const originalText = button?.textContent;
    if (button) {
      button.disabled = true;
      button.textContent = "Versturen...";
    }

    try {
      const payload = {
        ...Object.fromEntries(new FormData(form)),
        ...getTrackingFields(),
      };

      const response = await fetch(FORM_ENDPOINT, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const result = await response.json().catch(() => ({}));

      if (!response.ok) {
        throw new Error(result.error || "Formulier kon niet worden verstuurd.");
      }

      form.reset();
      if (success) {
        success.hidden = false;
      }

      const calendarUrl = result.calendar_url || CALENDAR_URL;
      if (nextStep && payload.lead_type === "call_aanvraag" && calendarUrl) {
        const link = document.createElement("a");
        link.href = calendarUrl;
        link.target = "_blank";
        link.rel = "noopener";
        link.textContent = "Plan je call in de agenda";
        nextStep.append(link);
        nextStep.hidden = false;
      }
    } catch (err) {
      error.textContent =
        err.message || "Er ging iets mis. Mail ons direct via info@investinbali.nl.";
      error.hidden = false;
    } finally {
      if (button) {
        button.disabled = false;
        button.textContent = originalText;
      }
    }
  });
});
