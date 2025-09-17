// API-backed converter (Frankfurter).
// GET https://api.frankfurter.app/latest returns: { amount, base, date, rates: { ... } }

const API_URL = 'https://api.frankfurter.app/latest';

const amountEl = document.getElementById('amount');
const fromSel = document.getElementById('from');
const toSel = document.getElementById('to');
const buggyVal = document.getElementById('buggyVal');
const fixedVal = document.getElementById('fixedVal');
const apiBaseEl = document.getElementById('apiBase');
const tsEl = document.getElementById('ts');

let rates = {};
let apiBase = 'EUR';
let lastTs = '';

async function fetchRates(base = undefined) {
  const url = base ? `${API_URL}?base=${encodeURIComponent(base)}` : API_URL;
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Rates fetch failed: ${res.status}`);
  const data = await res.json();
  // Expected: { amount, base, date, rates: {...} }
  apiBase = data.base;
  rates = data.rates || {};
  rates[data.base] = 1; // ensure base is present with rate 1
  lastTs = data.date || new Date().toISOString().slice(0,10);
  apiBaseEl.textContent = apiBase;
  tsEl.textContent = lastTs;
  ensureCurrencyOptions();
  compute();
}

function ensureCurrencyOptions() {
  const codes = Object.keys(rates).sort();
  const fill = (sel) => {
    const prev = sel.value;
    sel.innerHTML = '';
    for (const c of codes) {
      const opt = document.createElement('option');
      opt.value = c; opt.textContent = c;
      sel.appendChild(opt);
    }
    if (codes.includes(prev)) sel.value = prev;
  };
  if (!fromSel.options.length || !toSel.options.length) {
    fill(fromSel);
    fill(toSel);
    fromSel.value = 'USD';
    toSel.value = 'INR';
  } else {
    fill(fromSel);
    fill(toSel);
  }
}

function toNum(v) {
  const n = Number.parseFloat(v);
  return Number.isFinite(n) ? n : NaN;
}

function fmt(x) {
  if (!Number.isFinite(x)) return 'Error';
  const d = Math.abs(x) >= 1 ? 2 : 4;
  return x.toFixed(d);
}

// BUGGY: assumes API base == from
function convertBuggy(amount, from, to) {
  if (!rates[to]) return NaN;
  return amount * rates[to];
}

// FIXED: cross-rate
function convertFixed(amount, from, to) {
  if (!rates[from] || !rates[to]) return NaN;
  if (from === to) return amount;
  return amount * (rates[to] / rates[from]);
}

function compute() {
  const a = toNum(amountEl.value);
  const f = fromSel.value;
  const t = toSel.value;
  if (!Number.isFinite(a) || a < 0) {
    buggyVal.textContent = 'Error';
    fixedVal.textContent = 'Error';
    return;
  }
  const b = convertBuggy(a, f, t);
  const x = convertFixed(a, f, t);
  buggyVal.textContent = fmt(b);
  fixedVal.textContent = fmt(x);
}

document.getElementById('swap').addEventListener('click', () => {
  const f = fromSel.value; fromSel.value = toSel.value; toSel.value = f; compute();
});
document.getElementById('refresh').addEventListener('click', () => fetchRates());

['input', 'change'].forEach(evt => {
  amountEl.addEventListener(evt, compute);
  fromSel.addEventListener(evt, compute);
  toSel.addEventListener(evt, compute);
});

amountEl.value = '10';
fetchRates().catch(err => {
  console.error(err);
  buggyVal.textContent = 'API error';
  fixedVal.textContent = 'API error';
});
