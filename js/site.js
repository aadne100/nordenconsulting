/* Navigation and forms have native fallbacks. Full movies load only after a click. */
(() => {
  "use strict";
  const $ = (q, r = document) => r.querySelector(q),
    $$ = (q, r = document) => [...r.querySelectorAll(q)];
  const reduced = matchMedia("(prefers-reduced-motion: reduce)"),
    pointer = matchMedia("(hover: hover) and (pointer: fine)");
  const supportsDialog =
    typeof HTMLDialogElement !== "undefined" &&
    "showModal" in HTMLDialogElement.prototype;
  const openers = new WeakMap(),
    states = new WeakMap(),
    cards = $$("[data-preview-card]");
  let active = null;
  function pause(card) {
    if (!card) return;
    const v = $("video", card),
      b = $(".preview-toggle", card);
    v.pause();
    v.classList.remove("is-playing");
    b.textContent = "▷";
    b.setAttribute("aria-pressed", "false");
    b.setAttribute(
      "aria-label",
      `Spill stille forhåndsvisning av ${$("[data-film]", card).dataset.title}`,
    );
    if (active === card) active = null;
  }
  function pauseAll() {
    cards.forEach(pause);
  }
  async function play(card, manual = false) {
    const state = states.get(card);
    if (
      reduced.matches ||
      document.hidden ||
      !state.visible ||
      $("dialog[open]") ||
      (!manual && (state.stopped || navigator.connection?.saveData))
    )
      return;
    if (active && active !== card) pause(active);
    const v = $("video", card),
      b = $(".preview-toggle", card);
    if (!v.getAttribute("src")) v.src = v.dataset.preview;
    v.muted = true;
    active = card;
    try {
      await v.play();
      if (
        !state.visible ||
        document.hidden ||
        reduced.matches ||
        active !== card
      ) {
        pause(card);
        return;
      }
      v.classList.add("is-playing");
      b.textContent = "Ⅱ";
      b.setAttribute("aria-pressed", "true");
      b.setAttribute(
        "aria-label",
        `Pause forhåndsvisning av ${$("[data-film]", card).dataset.title}`,
      );
    } catch {
      pause(card);
    }
  }
  if ("IntersectionObserver" in window) {
    const observer = new IntersectionObserver(
      (entries) =>
        entries.forEach((entry) => {
          states.get(entry.target).visible = entry.isIntersecting;
          if (!entry.isIntersecting) pause(entry.target);
          else if (!pointer.matches) play(entry.target);
        }),
      { rootMargin: "-18% 0px -18% 0px", threshold: 0.25 },
    );
    cards.forEach((card) => {
      const state = { visible: false, stopped: false };
      states.set(card, state);
      const b = $(".preview-toggle", card);
      b.hidden = reduced.matches;
      card.addEventListener("mouseenter", () => {
        if (pointer.matches) play(card);
      });
      card.addEventListener("mouseleave", () => {
        if (pointer.matches) pause(card);
      });
      b.addEventListener("click", () => {
        if (!$("video", card).paused) {
          state.stopped = true;
          pause(card);
        } else {
          state.stopped = false;
          play(card, true);
        }
      });
      $("video", card).addEventListener("error", () => pause(card));
      observer.observe(card);
    });
  }
  document.addEventListener("visibilitychange", pauseAll);
  reduced.addEventListener("change", () => {
    pauseAll();
    cards.forEach((c) => ($(".preview-toggle", c).hidden = reduced.matches));
  });
  function open(dialog, opener) {
    pauseAll();
    openers.set(dialog, opener);
    dialog.showModal();
    document.body.classList.add("dialog-open");
    $(".modal-close", dialog)?.focus();
  }
  if (supportsDialog) {
    $$("dialog").forEach((dialog) => {
      $("[data-close]", dialog)?.addEventListener("click", () =>
        dialog.close(),
      );
      dialog.addEventListener("click", (event) => {
        const r = dialog.getBoundingClientRect();
        if (
          event.target === dialog &&
          (event.clientX < r.left ||
            event.clientX > r.right ||
            event.clientY < r.top ||
            event.clientY > r.bottom)
        )
          dialog.close();
      });
      dialog.addEventListener("close", () => {
        if (dialog.open) return;
        if (!$("dialog[open]")) document.body.classList.remove("dialog-open");
        openers.get(dialog)?.focus({ preventScroll: true });
      });
    });
    const contact = $("#contact-dialog"),
      card = $("#contact-card");
    if (contact && card) {
      $$("[data-contact]").forEach((link) =>
        link.addEventListener("click", (event) => {
          if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey)
            return;
          event.preventDefault();
          $("#contact-modal-content").append(card);
          $("[data-modal-details]", card).hidden = false;
          open(contact, link);
        }),
      );
      contact.addEventListener("close", () => {
        if (contact.open) return;
        $("#contact-home").append(card);
        $("[data-modal-details]", card).hidden = true;
      });
    }
    const dialog = $("#video-dialog"),
      video = $("#full-video");
    $$("[data-film]").forEach((link) =>
      link.addEventListener("click", (event) => {
        if (
          event.metaKey ||
          event.ctrlKey ||
          event.shiftKey ||
          event.altKey ||
          !dialog
        )
          return;
        event.preventDefault();
        video.pause();
        video.replaceChildren();
        video.removeAttribute("src");
        $("#video-title").textContent = link.dataset.title;
        $("#video-description").textContent = link.dataset.description;
        $("#video-fallback").href = link.href;
        $("#video-error").hidden = true;
        video.poster = `/assets/video/${link.dataset.film}/poster.webp`;
        for (const format of ["webm", "mp4"]) {
          const s = document.createElement("source");
          s.src = `/assets/video/${link.dataset.film}/full.${format}`;
          s.type = `video/${format}`;
          video.append(s);
        }
        open(dialog, link);
        video.load();
        video.play().catch(() => {});
      }),
    );
    video?.addEventListener("error", () => {
      $("#video-error").hidden = false;
    });
    dialog?.addEventListener("close", () => {
      if (dialog.open) return;
      video.pause();
      video.replaceChildren();
      video.removeAttribute("src");
      video.load();
    });
    const photoDialog = $("#photo-dialog");
    $$("[data-photo]").forEach((link) =>
      link.addEventListener("click", (event) => {
        if (
          event.metaKey ||
          event.ctrlKey ||
          event.shiftKey ||
          event.altKey ||
          !photoDialog
        )
          return;
        event.preventDefault();
        const thumb = $("img", link),
          photo = $("#photo-full");
        photo.src = link.href;
        photo.alt = thumb.alt;
        photo.width = thumb.getAttribute("width");
        photo.height = thumb.getAttribute("height");
        $("#photo-caption").textContent = thumb.alt;
        open(photoDialog, link);
      }),
    );
    photoDialog?.addEventListener("close", () => {
      if (!photoDialog.open) $("#photo-full").removeAttribute("src");
    });
  }
  const filters = $(".filters"),
    portfolio = $(".portfolio");
  if (filters && portfolio) {
    filters.hidden = false;
    $$("[data-filter]", filters).forEach((button) =>
      button.addEventListener("click", () => {
        pauseAll();
        let count = 0;
        const filter = button.dataset.filter;
        $$("[data-filter]", filters).forEach((b) =>
          b.setAttribute("aria-pressed", String(b === button)),
        );
        $$(".project", portfolio).forEach((p) => {
          p.hidden = !(
            filter === "all" || p.dataset.category.split(" ").includes(filter)
          );
          if (!p.hidden) count++;
        });
        portfolio.classList.toggle("filtered", filter !== "all");
        $("#filter-status").textContent = `${count} prosjekter vises.`;
      }),
    );
  }
  function openCollection() {
    let id;
    try {
      id = decodeURIComponent(location.hash.slice(1));
    } catch {
      return;
    }
    const target = document.getElementById(id);
    if (target?.matches("details.collection")) {
      target.open = true;
      requestAnimationFrame(() =>
        target.scrollIntoView({ block: "start", behavior: "instant" }),
      );
    }
  }
  window.addEventListener("hashchange", openCollection);
  openCollection();
  const form = $("#contact-form");
  if (form && window.fetch) {
    const submit = $("#send-button"),
      status = $("#form-status"),
      fallback = $("#native-submit");
    let sending = false;
    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      if (sending || !form.reportValidity()) return;
      sending = true;
      submit.disabled = true;
      form.setAttribute("aria-busy", "true");
      status.className = "form-status";
      status.textContent = "Sender meldingen …";
      fallback.hidden = true;
      const body = new FormData(form);
      body.set("email", String(body.get("epost") || "").trim());
      const controller = new AbortController(),
        timeout = setTimeout(() => controller.abort(), 20000);
      try {
        const response = await fetch(form.action, {
          method: "POST",
          body,
          headers: { Accept: "application/json" },
          signal: controller.signal,
        });
        const data = await response.json();
        if (!response.ok || data.ok !== true) throw new Error("submission");
        status.className = "form-status success";
        status.textContent =
          "Takk! Meldingen er sendt. Jeg tar kontakt på e-post.";
        form.reset();
      } catch (error) {
        status.className = "form-status error";
        status.textContent =
          error.name === "AbortError"
            ? "Bekreftelsen tok for lang tid. Meldingen kan ha blitt sendt. Kontakt meg på e-post hvis du er usikker."
            : "Jeg kunne ikke bekrefte at meldingen ble sendt. Prøv hos Formspree, eller bruk e-postlenken.";
        fallback.hidden = false;
      } finally {
        clearTimeout(timeout);
        sending = false;
        submit.disabled = false;
        form.removeAttribute("aria-busy");
      }
    });
    fallback.addEventListener("click", () => {
      if (form.reportValidity()) HTMLFormElement.prototype.submit.call(form);
    });
  }
})();
