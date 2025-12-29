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


function ajaxifyForms(selector, onDone) {
  document.querySelectorAll(selector).forEach(form => {
    form.addEventListener("submit", function (e) {
      e.preventDefault();

      fetch(form.action, {
        method: "POST",
        body: new FormData(form),
        headers: {
          "X-Requested-With": "XMLHttpRequest"
        }
      })
        .then(r => r.json())
        .then(onDone)
        .catch(console.error);
    });
  });
}

function updateHeaderCounters(data) {
  const favBadge = document.querySelector("#fav-count");
  const cartBadge = document.querySelector("#cart-count");

  if (favBadge) favBadge.textContent = data.favoritos;
  if (cartBadge) cartBadge.textContent = data.carrito;

  // Mostrar / ocultar si es 0
  if (favBadge) favBadge.parentElement.classList.toggle("d-none", data.favoritos === 0);
  if (cartBadge) cartBadge.parentElement.classList.toggle("d-none", data.carrito === 0);
}

ajaxifyForms(".js-cart-form", updateHeaderCounters);
ajaxifyForms(".js-fav-form", updateHeaderCounters);
