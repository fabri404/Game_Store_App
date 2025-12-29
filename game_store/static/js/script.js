document.addEventListener("DOMContentLoaded", () => {
  function setBadge(id, value) {
    const el = document.getElementById(id);
    if (!el) return;

    const n = Number(value || 0);
    el.textContent = String(n);

    if (n <= 0) el.classList.add("d-none");
    else el.classList.remove("d-none");
  }

  async function postFormNoReload(form) {
    const url = form.action;
    const formData = new FormData(form);

    const csrf = form.querySelector('input[name="csrfmiddlewaretoken"]')?.value;

    let resp;
    try {
      resp = await fetch(url, {
        method: "POST",
        headers: {
          "X-Requested-With": "XMLHttpRequest",
          ...(csrf ? { "X-CSRFToken": csrf } : {}),
        },
        body: formData,
      });
    } catch (err) {
      console.error("Fetch error:", err);
      return;
    }

    // Si no está logueado, Django redirige al login -> navegamos ahí
    if (resp.redirected) {
      window.location.href = resp.url;
      return;
    }

    if (!resp.ok) {
      console.error("HTTP error:", resp.status);
      return;
    }

    // Si backend responde JSON con contadores, actualizamos badges
    const ct = resp.headers.get("content-type") || "";
    if (ct.includes("application/json")) {
      const data = await resp.json();

      if (typeof data.carrito_total_items !== "undefined") {
        setBadge("carrito-badge", data.carrito_total_items);
      }
      if (typeof data.favoritos_total_items !== "undefined") {
        setBadge("favoritos-badge", data.favoritos_total_items);
      }
    }
  }

  // ---- FAVORITOS ----
  document.querySelectorAll(".js-fav-form").forEach((form) => {
    // Clave: cortar bubbling para que no dispare un click en la card
    // NO usamos preventDefault acá
    form.addEventListener("click", (e) => e.stopPropagation());

    form.addEventListener("submit", (e) => {
      e.preventDefault();
      e.stopPropagation();
      postFormNoReload(form);
    });
  });

  // ---- CARRITO ----
  document.querySelectorAll(".js-cart-form").forEach((form) => {
    form.addEventListener("click", (e) => e.stopPropagation());

    form.addEventListener("submit", (e) => {
      e.preventDefault();
      e.stopPropagation();
      postFormNoReload(form);
    });
  });
});
