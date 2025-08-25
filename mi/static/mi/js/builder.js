import { runPython } from './py_engine.js';

const state = {
  schema: [],
  sample: [],
  // Use this to hold the DataFrame rows returned from Python (if any)
  transformed: null,
  roles: { x: null, y: null, color: null, size: null },
  vizId: window.MI_BOOT.vizId,
  datasourceId: window.MI_BOOT.datasourceId,
};

function $(q) { return document.querySelector(q); }
function el(tag, attrs = {}, text = "") {
  const n = document.createElement(tag);
  Object.entries(attrs).forEach(([k, v]) => n.setAttribute(k, v));
  if (text) n.textContent = text;
  return n;
}

// Prefer Python output if available, else fall back to the original sample
function getActiveRows() {
  return (state.transformed && state.transformed.length) ? state.transformed : state.sample;
}

// Heuristics for inferring roles from rows
function isFiniteNumber(v) {
  if (v === null || v === undefined) return false;
  const n = Number(v);
  return Number.isFinite(n);
}
function columnIsNumeric(rows, key, sampleN = 50) {
  const n = Math.min(rows.length, sampleN);
  let seen = 0, numeric = 0;
  for (let i = 0; i < n; i++) {
    const val = rows[i][key];
    if (val !== null && val !== undefined && val !== "") {
      seen++;
      if (isFiniteNumber(val)) numeric++;
    }
  }
  // numeric if most seen values are numeric
  return seen > 0 && numeric / seen >= 0.7;
}
function inferRolesFromRows(rows) {
  if (!rows || !rows.length) return null;
  const keys = Object.keys(rows[0] || {});
  if (!keys.length) return null;
  const numericCols = keys.filter(k => columnIsNumeric(rows, k));
  const nonNumericCols = keys.filter(k => !numericCols.includes(k));
  const y = numericCols[0] || null;
  // Prefer a non-numeric column for X; else use row index sentinel
  const x = nonNumericCols[0] || '__index__';
  if (!y) return { x: null, y: null };
  return { x, y };
}

async function fetchSchema() {
  if (!state.datasourceId) return;
  const res = await fetch(`/mi/api/dataset/${state.datasourceId}/schema/`);
  const json = await res.json();
  if (json.error) throw new Error(json.error);
  state.schema = json.schema;
  state.sample = json.sample;
  state.transformed = null; // reset when dataset changes
  renderFields();
}

function renderFields() {
  const fields = $("#fields");
  if (!fields) return;
  fields.innerHTML = "";
  state.schema.forEach(c => {
    const item = el("div", { class: "field", draggable: "true", "data-col": c.name }, c.name);
    item.addEventListener("dragstart", e => {
      e.dataTransfer.setData("text/col", c.name);
    });
    fields.appendChild(item);
  });
}

function setupDrops() {
  document.querySelectorAll(".drop").forEach(box => {
    box.addEventListener("dragover", e => e.preventDefault());
    box.addEventListener("drop", e => {
      e.preventDefault();
      const col = e.dataTransfer.getData("text/col");
      const role = box.getAttribute("data-role");
      state.roles[role] = col;
      box.textContent = role + ": " + col;
      // Re-render using Python output if available
      renderPlotFromRoles(getActiveRows());
    });
  });
}

function renderPlotFromRoles(rows) {
  if (!rows || !rows.length) {
    Plotly.newPlot('chart', [], { title: 'No rows to plot' });
    return;
  }
  const type = $("#chartType") ? $("#chartType").value : "auto";
  const keys = Object.keys(rows[0] || {});
  // Validate roles against current rows; infer if missing/invalid
  let x = state.roles.x;
  let y = state.roles.y;
  if (!x || (x !== '__index__' && !keys.includes(x)) || !y || !keys.includes(y)) {
    const inferred = inferRolesFromRows(rows);
    if (inferred) {
      if (!x || (x !== '__index__' && !keys.includes(x))) state.roles.x = inferred.x;
      if (!y || !keys.includes(y)) state.roles.y = inferred.y;
      x = state.roles.x; y = state.roles.y;
      // Reflect inferred roles in the UI
      const boxX = document.querySelector(`.drop[data-role="x"]`);
      const boxY = document.querySelector(`.drop[data-role="y"]`);
      if (boxX) boxX.textContent = "x: " + (x === '__index__' ? 'row_index' : x);
      if (boxY) boxY.textContent = "y: " + y;
    }
  }
  if (!x || !y) {
    Plotly.newPlot('chart', [], { title: 'Assign at least X and Y' });
    return;
  }
  const xVals = (x === '__index__') ? rows.map((_, i) => i) : rows.map(r => r[x]);
  const yVals = rows.map(r => r[y]).map(v => Number(v));
  const trace = {
    type: type === "auto" ? "bar" : type,
    x: xVals,
    y: yVals,
  };
  const color = state.roles.color;
  if (color && keys.includes(color)) {
    trace.marker = { color: rows.map(r => r[color]) };
  }
  Plotly.newPlot('chart', [trace], { margin: { t: 30 } }, { responsive: true });
}

async function runUserCode() {
  const outEl = $("#pyOut");
  if (outEl) outEl.textContent = ""; // clear console
  const code = $("#editor").value;
  const res = await runPython(code, state.sample);

  // Console output
  if (outEl) {
    const parts = [];
    if (res.stdout) parts.push(res.stdout);
    if (res.stderr) parts.push(res.stderr);
    outEl.textContent = parts.join("\n");
  }

  if (res.error) {
    $("#status").textContent = "Error: " + res.error;
    return;
  }
  $("#status").textContent = "";

  if (res.kind === "plotly") {
    // Accept either a full figure dict {data, layout} or a list of traces
    state.transformed = null;
    const fig = res.data;
    const data = Array.isArray(fig) ? fig : (fig?.data || []);
    const layout = Array.isArray(fig) ? {} : (fig?.layout || {});
    Plotly.newPlot('chart', data, layout, { responsive: true });
  } else if (res.kind === "frame") {
    // Use Python-transformed rows and auto-infer roles if needed
    state.transformed = res.data;
    renderPlotFromRoles(getActiveRows());
  } else {
    Plotly.purge('chart');
  }
}

async function saveViz() {
  const payload = {
    id: state.vizId,
    name: $("#vizName").value || "Untitled",
    datasource_id: state.datasourceId,
    chart_type: $("#chartType").value || "auto",
    drag_drop_config: state.roles,
    python_code: $("#editor").value || "",
  };
  const res = await fetch('/mi/api/viz/save/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  const json = await res.json();
  if (json.id) {
    state.vizId = json.id;
    $("#status").textContent = "Saved #" + json.id;
  } else {
    $("#status").textContent = "Save failed";
  }
}

function wireUpload() {
  const btn = $("#uploadBtn");
  if (!btn) return;
  btn.addEventListener("click", async () => {
    const name = $("#dsName").value.trim();
    const fmt = $("#dsFormat").value;
    const file = $("#dsFile").files[0];
    const status = $("#uploadStatus");
    if (!name || !file) {
      status.textContent = "Name and file are required.";
      return;
    }
    const fd = new FormData();
    fd.append('name', name);
    if (fmt) fd.append('format', fmt);
    fd.append('file', file);
    status.textContent = "Uploading...";
    try {
      const res = await fetch('/mi/api/datasource/create/', { method: 'POST', body: fd });
      const json = await res.json();
      if (!res.ok) throw new Error(json?.error || 'Upload failed');
      status.textContent = "Uploaded. Redirecting...";
      window.location.href = `/mi/builder/${json.id}/`;
    } catch (e) {
      status.textContent = "Error: " + (e.message || e.toString());
    }
  });
}

function wireEvents() {
  const renderBtn = $("#renderBtn");
  const runBtn = $("#runBtn");
  const saveBtn = $("#saveBtn");
  if (renderBtn) renderBtn.addEventListener("click", () => renderPlotFromRoles(getActiveRows()));
  if (runBtn) runBtn.addEventListener("click", runUserCode);
  if (saveBtn) saveBtn.addEventListener("click", saveViz);
}

(async function init() {
  wireUpload();
  setupDrops();
  wireEvents();
  await fetchSchema();
  await loadVizIfAny();
})();

async function loadVizIfAny() {
  if (!state.vizId) return;
  const res = await fetch(`/mi/api/viz/${state.vizId}/`);
  const v = await res.json();
  const nameEl = $("#vizName");
  const chartTypeEl = $("#chartType");
  const editorEl = $("#editor");
  if (nameEl) nameEl.value = v.name || "";
  if (chartTypeEl) chartTypeEl.value = v.chart_type || "auto";
  if (editorEl) editorEl.value = v.python_code || (editorEl ? editorEl.value : "");
  state.roles = Object.assign(state.roles, v.drag_drop_config || {});
  for (const role of Object.keys(state.roles)) {
    if (state.roles[role]) {
      const box = document.querySelector(`.drop[data-role="${role}"]`);
      if (box) box.textContent = role + ": " + state.roles[role];
    }
  }
}
