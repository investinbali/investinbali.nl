function formatCurrency(value) {
  return new Intl.NumberFormat("nl-NL", {
    style: "currency",
    currency: "EUR",
    maximumFractionDigits: 0,
  }).format(value);
}

function setupGoogleAnalytics() {
  const configuredId =
    window.INVEST_IN_BALI_GA_ID ||
    document.querySelector("meta[name='google-analytics-id']")?.content ||
    "";
  const measurementId = configuredId.trim();

  if (!/^G-[A-Z0-9]+$/i.test(measurementId) || typeof window.gtag === "function") {
    return;
  }

  window.dataLayer = window.dataLayer || [];
  window.gtag = function gtag() {
    window.dataLayer.push(arguments);
  };
  window.gtag("js", new Date());
  window.gtag("config", measurementId);

  const script = document.createElement("script");
  script.async = true;
  script.src = `https://www.googletagmanager.com/gtag/js?id=${encodeURIComponent(measurementId)}`;
  document.head.append(script);
}

function trackEvent(name, properties = {}) {
  if (typeof window.va === "function") {
    window.va("event", {
      name,
      data: {
        page: window.location.pathname,
        ...properties,
      },
    });
  }

  if (typeof window.gtag === "function") {
    window.gtag("event", name, {
      page_path: window.location.pathname,
      ...properties,
    });
  }
}

function normaliseEventPart(value, fallback = "unknown") {
  const normalised = String(value || "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "_")
    .replace(/^_+|_+$/g, "");
  return normalised || fallback;
}

setupGoogleAnalytics();

const scrollMilestones = [25, 50, 75, 90];
const reachedScrollMilestones = new Set();
let engagedReaderTracked = false;
let engagedReaderTimer = null;

function getPageCategory() {
  const path = window.location.pathname;

  if (path === "/") {
    return "home";
  }
  if (path.startsWith("/projecten/")) {
    return path === "/projecten/" ? "projecten_hub" : "project_detail";
  }
  if (path.startsWith("/kenniscentrum/")) {
    return path === "/kenniscentrum/" ? "kenniscentrum_hub" : "kenniscentrum_article";
  }

  return path.replace(/^\/|\/$/g, "") || "other";
}

function trackScrollDepth() {
  const root = document.documentElement;
  const scrollRange = root.scrollHeight - window.innerHeight;

  if (scrollRange <= 0) {
    return;
  }

  const progress = Math.round((window.scrollY / scrollRange) * 100);

  scrollMilestones.forEach((milestone) => {
    if (progress >= milestone && !reachedScrollMilestones.has(milestone)) {
      reachedScrollMilestones.add(milestone);
      trackEvent("scroll_depth", {
        percent_scrolled: milestone,
        page_category: getPageCategory(),
      });
    }
  });
}

function resetEngagedReaderTimer() {
  if (engagedReaderTracked || document.hidden) {
    return;
  }

  window.clearTimeout(engagedReaderTimer);
  engagedReaderTimer = window.setTimeout(() => {
    if (document.hidden || engagedReaderTracked) {
      return;
    }

    engagedReaderTracked = true;
    trackEvent("engaged_read_30s", {
      page_category: getPageCategory(),
    });
  }, 30000);
}

window.addEventListener("scroll", trackScrollDepth, { passive: true });
window.addEventListener("load", trackScrollDepth);
window.addEventListener("focus", resetEngagedReaderTimer);
document.addEventListener("visibilitychange", () => {
  if (document.hidden) {
    window.clearTimeout(engagedReaderTimer);
    return;
  }

  resetEngagedReaderTimer();
});
resetEngagedReaderTimer();

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

document.getElementById("calculateButton")?.addEventListener("click", () => {
  calculateRoi();
  trackEvent("roi_calculator_used");
});

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

      trackEvent("form_submit_success", {
        lead_type: payload.lead_type || "unknown",
      });
      trackEvent("generate_lead", {
        lead_type: payload.lead_type || "unknown",
        form_name: form.dataset.formName || "unknown",
        page_category: getPageCategory(),
      });
      trackEvent(`form_submit_success_${normaliseEventPart(payload.lead_type)}`, {
        lead_type: payload.lead_type || "unknown",
      });

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
        trackEvent("schedule_call_prompt_shown", {
          lead_type: payload.lead_type || "unknown",
        });
      }
    } catch (err) {
      const formData = Object.fromEntries(new FormData(form));
      trackEvent("form_submit_error", {
        lead_type: formData.lead_type || "unknown",
      });
      trackEvent(`form_submit_error_${normaliseEventPart(formData.lead_type)}`, {
        lead_type: formData.lead_type || "unknown",
      });

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

document.querySelectorAll("a[href]").forEach((link) => {
  link.addEventListener("click", () => {
    const href = link.getAttribute("href") || "";
    const shouldTrack =
      href.includes("/contact") ||
      href.includes("/gids") ||
      href.includes("/projecten") ||
      href.includes("calendar.app.google");

    if (!shouldTrack) {
      return;
    }

    let ctaType = "other";
    if (href.includes("calendar.app.google")) {
      ctaType = "calendar";
    } else if (href.includes("/contact")) {
      ctaType = "contact";
    } else if (href.includes("/gids")) {
      ctaType = "gids";
    } else if (href.includes("/projecten")) {
      ctaType = "projecten";
    }

    const label = link.textContent.trim().replace(/\s+/g, " ").slice(0, 80);

    trackEvent("cta_click", {
      href,
      label,
      cta_type: ctaType,
      page_category: getPageCategory(),
    });
    trackEvent(`cta_${normaliseEventPart(ctaType)}_click`, {
      href,
      label,
    });

    if (href.includes("/projecten/") && href !== "/projecten/") {
      trackEvent("project_interest_click", {
        href,
        label,
      });
    }

    if (href.includes("/gids")) {
      trackEvent("download_gids_click", {
        href,
        label,
      });
    }

    if (href.includes("calendar.app.google") || label.toLowerCase().includes("plan")) {
      trackEvent("schedule_call_click", {
        href,
        label,
      });
    }
  });
});
