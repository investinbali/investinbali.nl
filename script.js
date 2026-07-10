function formatCurrency(value) {
  return new Intl.NumberFormat("nl-NL", {
    style: "currency",
    currency: "EUR",
    maximumFractionDigits: 0,
  }).format(value);
}

const ANALYTICS_CONSENT_KEY = "investinbali_analytics_consent";

function getAnalyticsConsent() {
  try {
    return window.localStorage.getItem(ANALYTICS_CONSENT_KEY);
  } catch (_error) {
    return null;
  }
}

function setAnalyticsDisabled(disabled) {
  const measurementId = String(window.INVEST_IN_BALI_GA_ID || "").trim();
  if (measurementId) {
    window[`ga-disable-${measurementId}`] = disabled;
  }
}

function clearAnalyticsCookies() {
  const hostname = window.location.hostname;
  const domains = ["", hostname, `.${hostname}`, ".investinbali.nl"];
  document.cookie.split(";").forEach((cookie) => {
    const name = cookie.split("=")[0].trim();
    if (!/^_ga(?:_|$)|^_gid$|^_gat(?:_|$)/.test(name)) return;
    domains.forEach((domain) => {
      const domainPart = domain ? `; domain=${domain}` : "";
      document.cookie = `${name}=; Max-Age=0; path=/${domainPart}; SameSite=Lax`;
    });
  });
}

function setupGoogleAnalytics() {
  if (getAnalyticsConsent() !== "accepted") {
    return;
  }
  const configuredId =
    window.INVEST_IN_BALI_GA_ID ||
    document.querySelector("meta[name='google-analytics-id']")?.content ||
    "";
  const measurementId = configuredId.trim();
  setAnalyticsDisabled(false);

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

function setupCookieConsent(force = false) {
  if (!force && getAnalyticsConsent()) {
    return;
  }
  if (document.querySelector(".cookie-banner")) return;

  const banner = document.createElement("section");
  banner.className = "cookie-banner";
  banner.setAttribute("role", "dialog");
  banner.setAttribute("aria-modal", "false");
  banner.setAttribute("aria-labelledby", "cookie-consent-title");
  banner.innerHTML = `
    <div>
      <h2 id="cookie-consent-title">Jouw privacykeuze</h2>
      <p>We gebruiken alleen met jouw toestemming Google Analytics om de website te verbeteren. Noodzakelijke opslag voor je keuze staat altijd aan. Lees meer in ons <a href="/cookiebeleid/">cookiebeleid</a>.</p>
    </div>
    <div class="cookie-actions">
      <button class="button button-outline" type="button" data-cookie-choice="rejected">Weigeren</button>
      <button class="button button-gold" type="button" data-cookie-choice="accepted">Accepteren</button>
    </div>`;
  document.body.append(banner);

  banner.querySelectorAll("[data-cookie-choice]").forEach((button) => {
    button.addEventListener("click", () => {
      const choice = button.dataset.cookieChoice;
      try {
        window.localStorage.setItem(ANALYTICS_CONSENT_KEY, choice);
      } catch (_error) {
        // The choice remains effective for this page view if storage is unavailable.
      }
      banner.remove();
      if (choice === "accepted") {
        setAnalyticsDisabled(false);
        setupGoogleAnalytics();
      } else {
        setAnalyticsDisabled(true);
        clearAnalyticsCookies();
      }
    });
  });
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

function trackFunnelStep(step, properties = {}) {
  trackEvent("funnel_step_reached", {
    funnel_step: step,
    page_category: getPageCategory(),
    ...properties,
  });
}

function normaliseEventPart(value, fallback = "unknown") {
  const normalised = String(value || "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "_")
    .replace(/^_+|_+$/g, "");
  return normalised || fallback;
}

setupGoogleAnalytics();
setupCookieConsent();

document.addEventListener("click", (event) => {
  const control = event.target.closest("[data-cookie-preferences]");
  if (!control) return;
  event.preventDefault();
  setAnalyticsDisabled(true);
  clearAnalyticsCookies();
  try {
    window.localStorage.removeItem(ANALYTICS_CONSENT_KEY);
  } catch (_error) {
    // Reopening the banner still lets the visitor choose for this page view.
  }
  setupCookieConsent(true);
  document.querySelector(".cookie-banner button")?.focus();
});

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

function reportTrackingHealth() {
  const storageKey = `tracking_ready:${window.location.pathname}`;

  try {
    if (window.sessionStorage.getItem(storageKey)) {
      return;
    }
  } catch (_error) {
    // Ignore storage failures and fall through to best-effort tracking.
  }

  window.setTimeout(() => {
    trackEvent("tracking_ready", {
      page_category: getPageCategory(),
      has_ga_id: Boolean(window.INVEST_IN_BALI_GA_ID),
      has_gtag: typeof window.gtag === "function",
      has_vercel_analytics: typeof window.va === "function",
      page_title: document.title,
    });

    try {
      window.sessionStorage.setItem(storageKey, "1");
    } catch (_error) {
      // Ignore storage failures and avoid breaking user flows.
    }
  }, 1500);
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
    trackFunnelStep("engaged_read_30s");
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
reportTrackingHealth();

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

  const invalid = [];
  if (!Number.isFinite(investment) || investment <= 0) invalid.push("investering moet groter zijn dan 0");
  if (!Number.isFinite(dailyRate) || dailyRate < 0) invalid.push("dagprijs mag niet negatief zijn");
  if (!Number.isFinite(occupancy) || occupancy < 0 || occupancy > 1) invalid.push("bezetting moet tussen 0 en 100% liggen");
  if (!Number.isFinite(costs) || costs < 0 || costs > 1) invalid.push("kosten moeten tussen 0 en 100% liggen");

  summary.setAttribute("role", "status");
  summary.setAttribute("aria-live", "polite");
  if (invalid.length) {
    revenueValue.textContent = "-";
    netValue.textContent = "-";
    roiValue.textContent = "-";
    summary.textContent = `Controleer de invoer: ${invalid.join(", ")}.`;
    return false;
  }

  revenueValue.textContent = formatCurrency(revenue);
  netValue.textContent = formatCurrency(netRevenue);
  roiValue.textContent = `${roi.toFixed(1)}%`;
  summary.textContent = `Bij deze aannames kom je indicatief uit op ${formatCurrency(
    netRevenue
  )} netto-opbrengst per jaar en een netto rendement van ${roi.toFixed(1)}%.`;
  return true;
}

document.getElementById("calculateButton")?.addEventListener("click", () => {
  calculateRoi();
  trackEvent("roi_calculator_used", {
    page_category: getPageCategory(),
  });
  trackFunnelStep("micro_conversion", {
    micro_conversion_type: "roi_calculator_used",
  });
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
  if (!form.querySelector("input[name='website']")) {
    const honeypot = document.createElement("input");
    honeypot.type = "text";
    honeypot.name = "website";
    honeypot.tabIndex = -1;
    honeypot.autocomplete = "off";
    honeypot.className = "honeypot-field";
    honeypot.setAttribute("aria-hidden", "true");
    form.prepend(honeypot);
  }

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

    error.setAttribute("role", "alert");
    error.setAttribute("aria-live", "assertive");
    if (success) {
      success.setAttribute("role", "status");
      success.setAttribute("aria-live", "polite");
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
        const requestError = new Error(result.error || "Formulier kon niet worden verstuurd.");
        requestError.httpStatus = response.status;
        requestError.errorCode = result.code || "HTTP_ERROR";
        throw requestError;
      }

      trackEvent("form_submit_success", {
        lead_type: payload.lead_type || "unknown",
      });
      trackEvent("generate_lead", {
        lead_type: payload.lead_type || "unknown",
        form_name: form.dataset.formName || "unknown",
        page_category: getPageCategory(),
      });
      trackEvent("qualify_lead", {
        lead_type: payload.lead_type || "unknown",
        form_name: form.dataset.formName || "unknown",
        page_category: getPageCategory(),
      });
      trackEvent(`form_submit_success_${normaliseEventPart(payload.lead_type)}`, {
        lead_type: payload.lead_type || "unknown",
      });
      trackFunnelStep("generate_lead", {
        lead_type: payload.lead_type || "unknown",
        form_name: form.dataset.formName || "unknown",
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
        form_name: form.dataset.formName || "unknown",
        http_status: Number(err.httpStatus || 0),
        error_code: normaliseEventPart(err.errorCode || "client_or_network_error"),
      });
      trackEvent(`form_submit_error_${normaliseEventPart(formData.lead_type)}`, {
        lead_type: formData.lead_type || "unknown",
        form_name: form.dataset.formName || "unknown",
        http_status: Number(err.httpStatus || 0),
        error_code: normaliseEventPart(err.errorCode || "client_or_network_error"),
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
    const ctaTypeOverride = link.dataset.ctaType || "";
    const funnelStage = link.dataset.funnelStage || "";
    const intentRoute = link.dataset.intentRoute || "";
    const isInternalContentLink =
      href.startsWith("/") &&
      (link.classList.contains("article-link-card") ||
        link.classList.contains("text-link") ||
        link.classList.contains("section-cta"));
    const shouldTrack =
      Boolean(ctaTypeOverride) ||
      isInternalContentLink ||
      href.includes("/contact") ||
      href.includes("/gids") ||
      href.includes("/projecten") ||
      href.includes("calendar.app.google");

    if (!shouldTrack) {
      return;
    }

    let ctaType = ctaTypeOverride || "other";
    if (!ctaTypeOverride && href.includes("calendar.app.google")) {
      ctaType = "calendar";
    } else if (!ctaTypeOverride && href.includes("/contact")) {
      ctaType = "contact";
    } else if (!ctaTypeOverride && href.includes("/gids")) {
      ctaType = "gids";
    } else if (!ctaTypeOverride && href.includes("/projecten")) {
      ctaType = "projecten";
    } else if (!ctaTypeOverride && isInternalContentLink) {
      ctaType = "internal_content";
    }

    const label = link.textContent.trim().replace(/\s+/g, " ").slice(0, 80);

    trackEvent("cta_click", {
      href,
      label,
      cta_type: ctaType,
      funnel_stage: funnelStage || "unassigned",
      intent_route: intentRoute || "none",
      page_category: getPageCategory(),
    });
    trackEvent(`cta_${normaliseEventPart(ctaType)}_click`, {
      href,
      label,
    });

    if (intentRoute) {
      trackEvent("intent_route_selected", {
        href,
        label,
        intent_route: intentRoute,
        funnel_stage: funnelStage || "route_select",
        page_category: getPageCategory(),
      });
    }

    if (isInternalContentLink) {
      trackEvent("content_navigation_click", {
        href,
        label,
        page_category: getPageCategory(),
      });
    }

    if (funnelStage) {
      trackFunnelStep(funnelStage, {
        cta_type: ctaType,
        intent_route: intentRoute || "none",
        href,
      });
    }

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
      trackFunnelStep("micro_conversion", {
        micro_conversion_type: "download_gids_click",
        href,
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
