// Mobile nav, reveal-on-scroll, and the contact form (which opens a pre-filled email).

const toggle = document.querySelector("[data-nav-toggle]");
const nav = document.querySelector("[data-nav]");
if (toggle && nav) {
  toggle.addEventListener("click", () => {
    const open = toggle.getAttribute("aria-expanded") !== "true";
    toggle.setAttribute("aria-expanded", String(open));
    nav.classList.toggle("open", open);
  });
  nav.addEventListener("click", (e) => {
    if (e.target.closest("a")) {
      toggle.setAttribute("aria-expanded", "false");
      nav.classList.remove("open");
    }
  });
}

// Only hide elements once JS is running, so nothing is invisible without it.
const revealables = document.querySelectorAll("[data-reveal]");
if ("IntersectionObserver" in window && !matchMedia("(prefers-reduced-motion: reduce)").matches) {
  const io = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      if (entry.isIntersecting) {
        entry.target.classList.add("in");
        io.unobserve(entry.target);
      }
    }
  }, { rootMargin: "0px 0px -8% 0px" });
  revealables.forEach((el, i) => {
    el.classList.add("reveal");
    el.style.transitionDelay = `${(i % 4) * 70}ms`;
    io.observe(el);
  });
}

// Contact form: pre-select a topic from ?about=..., then compose an email on submit.
// Swap this for a form service (Formspree, Cloudflare Pages Function) when going live.
const form = document.querySelector("[data-contact]");
if (form) {
  const about = new URLSearchParams(location.search).get("about");
  if (about) {
    const chip = form.querySelector(`input[name="topic"][value="${CSS.escape(about)}"]`);
    if (chip) chip.checked = true;
  }
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const data = new FormData(form);
    const topics = data.getAll("topic");
    const details = [
      `Name: ${data.get("name")}`,
      `Email: ${data.get("email")}`,
      data.get("team") && `League / team: ${data.get("team")}`,
      data.get("where") && `Location: ${data.get("where")}`,
      data.get("when") && `Timeframe: ${data.get("when")}`,
      topics.length && `Interested in: ${topics.join(", ")}`,
    ].filter(Boolean);
    const lines = [...details, "", data.get("message")];
    const subject = `Coaching inquiry${topics.length ? `: ${topics[0]}` : ""} from ${data.get("name")}`;
    location.href = `mailto:missteamaven@gmail.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(lines.join("\n"))}`;
    form.querySelector(".form-status")?.classList.add("show");
  });
}
