
// ✅ troque isso se estiver online (ex.: "https://api.hortinbox.com")
const API_URL = "http://127.0.0.1:5000";

async function login(e) {
  e.preventDefault();
  const id = document.getElementById("guest_id").value;
  const res = await fetch(`${API_URL}/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify({ guest_id: Number(id) })
  });
  if (res.ok) {
    window.location.href = `${API_URL}/`;
  } else {
    alert("Convidado não encontrado.");
  }
}

async function carregarPresentes() {
  const res = await fetch(`${API_URL}/gifts`, { credentials: "include" });
  const gifts = await res.json();
  const list = document.getElementById("gift-list");
  list.innerHTML = "";

  gifts.forEach(p => {
    const div = document.createElement("div");
    div.className = "gift" + (p.catched ? " catched" : "");
    div.innerHTML = `
      <img src="${p.source_img || ''}">
      <h3>${p.description}</h3>
      <a href="${p.url || '#'}" target="_blank">Ver anúncio</a>
      ${
        p.catched
          ? `<button disabled>Já foi pego</button>`
          : `<button onclick="pegar(${p.gift_id})">Pegar Presente</button>`
      }
    `;
    list.appendChild(div);
  });
}

// ✅ Mude aqui caso vá hospedar a API em outro domínio

async function carregarPresentes() {
  const res = await fetch(`${API_URL}/gifts`, { credentials: "include" });
  const gifts = await res.json();

  const list = document.getElementById("gift-list");
  list.innerHTML = "";

  gifts.forEach(p => {
    const div = document.createElement("div");
    div.className = "gift" + (p.catched ? " catched" : "");
    div.innerHTML = `
      <img src="${p.source_img || ''}" alt="${p.description}">
      <h3>${p.description}</h3>
      <a href="${p.url || '#'}" target="_blank">Ver anúncio</a>
      ${
        p.catched
          ? `<button disabled>Já foi pego</button>`
          : `<button onclick="pegar(${p.gift_id})">Pegar Presente</button>`
      }
    `;
    list.appendChild(div);
  });
}

async function pegar(id) {
  const res = await fetch(`${API_URL}/getGift/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify({ catched: true })
  });

  if (res.ok) {
    carregarPresentes();
  } else if (res.status === 409) {
    alert("Este presente já foi pego!");
  } else {
    alert("Erro ao pegar presente.");
  }
}

async function logout() {
  await fetch(`${API_URL}/logout`, { credentials: "include" });
  window.location.href = "/login"; // volta para login do mesmo site
}

// Inicialização
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("loginForm");
  const logoutBtn = document.getElementById("logoutBtn");
  const list = document.getElementById("gift-list");

  if (form) form.addEventListener("submit", login);
  if (logoutBtn) logoutBtn.addEventListener("click", logout);
  if (list) carregarPresentes();
});

