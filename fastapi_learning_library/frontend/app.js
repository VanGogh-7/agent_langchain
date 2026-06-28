const tokenKey = "learningLibraryToken";
const apiBaseUrlKey = "learningLibraryApiBaseUrl";
const defaultApiBaseUrl = "http://127.0.0.1:8000/api";
const apiBaseUrlFromQuery = new URLSearchParams(window.location.search).get("api");

if (apiBaseUrlFromQuery) {
  localStorage.setItem(apiBaseUrlKey, apiBaseUrlFromQuery);
}

const API_BASE_URL = localStorage.getItem(apiBaseUrlKey) || defaultApiBaseUrl;

const registerForm = document.querySelector("#registerForm");
const loginForm = document.querySelector("#loginForm");
const resourceForm = document.querySelector("#resourceForm");
const filterForm = document.querySelector("#filterForm");
const resourceList = document.querySelector("#resourceList");
const currentUser = document.querySelector("#currentUser");
const message = document.querySelector("#message");
const logoutButton = document.querySelector("#logoutButton");

function getToken() {
  return localStorage.getItem(tokenKey);
}

function setMessage(text) {
  message.textContent = text;
}

function authHeaders() {
  const token = getToken();
  return token ? { Authorization: `Bearer ${token}` } : {};
}

function formDataToObject(form) {
  const data = Object.fromEntries(new FormData(form).entries());
  for (const key of Object.keys(data)) {
    if (data[key] === "") {
      data[key] = null;
    }
  }
  return data;
}

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...authHeaders(),
      ...options.headers,
    },
  });

  if (response.status === 204) {
    return null;
  }

  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.detail || "Request failed");
  }
  return data;
}

async function loadCurrentUser() {
  if (!getToken()) {
    currentUser.textContent = "Not logged in";
    return;
  }

  try {
    const user = await request("/auth/me");
    currentUser.textContent = `Logged in as ${user.username} (${user.email})`;
  } catch (error) {
    localStorage.removeItem(tokenKey);
    currentUser.textContent = "Not logged in";
  }
}

function renderResources(resources) {
  resourceList.innerHTML = "";

  if (resources.length === 0) {
    const emptyItem = document.createElement("li");
    emptyItem.textContent = "No resources found.";
    resourceList.appendChild(emptyItem);
    return;
  }

  for (const resource of resources) {
    const item = document.createElement("li");
    item.className = "resource-item";

    const header = document.createElement("header");
    const summary = document.createElement("div");
    const title = document.createElement("h3");
    const meta = document.createElement("p");
    const notes = document.createElement("p");
    const rating = document.createElement("p");
    const deleteButton = document.createElement("button");

    title.textContent = resource.title;
    meta.className = "meta";
    meta.textContent = `${resource.author || "Unknown author"} · ${resource.category || "No category"} · ${resource.status}`;
    notes.textContent = resource.notes || "";
    rating.className = "meta";
    rating.textContent = `Rating: ${resource.rating || "not rated"}`;
    deleteButton.className = "danger";
    deleteButton.type = "button";
    deleteButton.dataset.id = resource.id;
    deleteButton.textContent = "Delete";

    summary.append(title, meta);
    header.append(summary, deleteButton);
    item.append(header, notes, rating);
    resourceList.appendChild(item);
  }
}

async function loadResources() {
  if (!getToken()) {
    renderResources([]);
    return;
  }

  const filters = new FormData(filterForm);
  const params = new URLSearchParams();
  for (const [key, value] of filters.entries()) {
    if (value) {
      params.set(key, value);
    }
  }

  const resources = await request(`/resources?${params.toString()}`);
  renderResources(resources);
}

registerForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  try {
    await request("/auth/register", {
      method: "POST",
      body: JSON.stringify(formDataToObject(registerForm)),
    });
    setMessage("Registration complete. You can now log in.");
    registerForm.reset();
  } catch (error) {
    setMessage(error.message);
  }
});

loginForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  try {
    const token = await request("/auth/login", {
      method: "POST",
      body: JSON.stringify(formDataToObject(loginForm)),
    });
    localStorage.setItem(tokenKey, token.access_token);
    setMessage("Logged in.");
    loginForm.reset();
    await loadCurrentUser();
    await loadResources();
  } catch (error) {
    setMessage(error.message);
  }
});

resourceForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  try {
    const data = formDataToObject(resourceForm);
    if (data.rating !== null) {
      data.rating = Number(data.rating);
    }
    await request("/resources", {
      method: "POST",
      body: JSON.stringify(data),
    });
    resourceForm.reset();
    setMessage("Resource created.");
    await loadResources();
  } catch (error) {
    setMessage(error.message);
  }
});

filterForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  try {
    await loadResources();
  } catch (error) {
    setMessage(error.message);
  }
});

resourceList.addEventListener("click", async (event) => {
  if (!event.target.matches("button[data-id]")) {
    return;
  }

  try {
    await request(`/resources/${event.target.dataset.id}`, { method: "DELETE" });
    setMessage("Resource deleted.");
    await loadResources();
  } catch (error) {
    setMessage(error.message);
  }
});

logoutButton.addEventListener("click", async () => {
  localStorage.removeItem(tokenKey);
  currentUser.textContent = "Not logged in";
  renderResources([]);
  setMessage("Logged out.");
});

loadCurrentUser();
loadResources().catch((error) => setMessage(error.message));
