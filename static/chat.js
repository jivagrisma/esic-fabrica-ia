// Chat del Escenario 1 — ESIC Assistant (JS vanilla, sin dependencias)

const CHAT = {};

function escapeHtml(s) {
  return String(s)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function _hora() {
  return new Date().toLocaleTimeString("es-CO", { hour: "2-digit", minute: "2-digit" });
}

// Mini-markdown seguro: se escapa TODO el HTML primero y solo entonces se
// aplican nuestras propias etiquetas (negrita/cursiva) sobre el texto escapado.
function fmt(text) {
  return escapeHtml(text)
    .replace(/\*\*(.+?)\*\*/g, "<b>$1</b>")
    .replace(/(^|[^*])\*([^*\n]+)\*/g, "$1<i>$2</i>");
}

function appendMsg(text, who, metaHtml = null) {
  const log = document.getElementById("chat-log");
  const div = document.createElement("div");
  div.className = "msg " + who;
  div.innerHTML = fmt(text);

  const meta = document.createElement("span");
  meta.className = "meta";
  meta.innerHTML = '<time>' + _hora() + "</time>" + (metaHtml !== null ? " · " + metaHtml : "");
  div.appendChild(meta);

  log.appendChild(div);
  log.scrollTop = log.scrollHeight;
  return div;
}

// Indicador de escritura (tres puntos animados) mientras responde el asistente
function showTyping() {
  const log = document.getElementById("chat-log");
  const div = document.createElement("div");
  div.className = "msg bot typing";
  div.id = "typing-indicator";
  div.innerHTML = "<span></span><span></span><span></span>";
  log.appendChild(div);
  log.scrollTop = log.scrollHeight;
}

function hideTyping() {
  const el = document.getElementById("typing-indicator");
  if (el) el.remove();
}

// Chips de sugerencia: arrancan la conversación sin exigir redactar
const SUGERENCIAS = ["🎓 Programas y precios", "💰 Formas de pago", "💼 Oportunidades laborales"];

function addChips() {
  removeChips();
  const log = document.getElementById("chat-log");
  const wrap = document.createElement("div");
  wrap.className = "chips";
  wrap.id = "chips";
  for (const s of SUGERENCIAS) {
    const b = document.createElement("button");
    b.type = "button";
    b.textContent = s;
    b.onclick = () => {
      removeChips();
      document.getElementById("chat-input").value = s.replace(/^[^\s]+\s/, "");
      document.getElementById("chat-form").requestSubmit();
    };
    wrap.appendChild(b);
  }
  log.appendChild(wrap);
  log.scrollTop = log.scrollHeight;
}

function removeChips() {
  const el = document.getElementById("chips");
  if (el) el.remove();
}

function seedChat() {
  CHAT.sessionId = "ses-" + Math.random().toString(36).slice(2, 10);
  CHAT.history = [];
  document.getElementById("chat-log").innerHTML = "";
  appendMsg(
    "¡Hola! Soy ESIC Assistant 👋 Pregúntame por programas, financiamiento u oportunidades laborales.",
    "bot"
  );
  addChips();
}

// Nueva consulta: limpia la conversación y arranca una sesión fresca
// (la conversación anterior queda registrada en el historial del servidor).
function newChat() {
  seedChat();
  document.getElementById("chat-input").focus();
}

async function sendChat(event) {
  event.preventDefault();
  const input = document.getElementById("chat-input");
  const message = input.value.trim();
  if (!message) return false;

  removeChips();
  appendMsg(message, "user");
  CHAT.history.push({ role: "user", text: message });
  input.value = "";

  showTyping();
  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: message, session_id: CHAT.sessionId }),
    });
    if (!res.ok) throw new Error("HTTP " + res.status);
    const data = await res.json();
    hideTyping();

    let meta = null;
    if (data.escalated) {
      const tid = data.ticket && data.ticket.ticket_id ? data.ticket.ticket_id : "—";
      meta = '<span class="ticket">🎟️ Un asesor continuará tu caso · Ticket ' + escapeHtml(tid) + "</span>";
    }
    appendMsg(data.reply, "bot", meta);
    CHAT.history.push({ role: "bot", text: data.reply, escalated: data.escalated });
    addChips();
  } catch (err) {
    hideTyping();
    appendMsg(
      "Lo siento, hubo un problema de conexión. Intenta de nuevo en unos momentos.",
      "bot"
    );
  }
  return false;
}
