// Chat del Scenario 1 — ESIC Assistant (JS vanilla, sin dependencias)

const CHAT = {};

function escapeHtml(s) {
  return String(s)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function appendMsg(text, who, metaHtml = null) {
  const log = document.getElementById("chat-log");
  const div = document.createElement("div");
  div.className = "msg " + who;
  div.textContent = text;
  if (metaHtml !== null) {
    const meta = document.createElement("span");
    meta.className = "meta";
    meta.innerHTML = metaHtml;
    div.appendChild(meta);
  }
  log.appendChild(div);
  log.scrollTop = log.scrollHeight;
  return div;
}

function seedChat() {
  CHAT.sessionId = "ses-" + Math.random().toString(36).slice(2, 10);
  CHAT.history = [];
  appendMsg(
    "¡Hola! Soy ESIC Assistant 👋 Pregúntame por programas, financiamiento u oportunidades laborales.",
    "bot"
  );
}

async function sendChat(event) {
  event.preventDefault();
  const input = document.getElementById("chat-input");
  const message = input.value.trim();
  if (!message) return false;

  appendMsg(message, "user");
  CHAT.history.push({ role: "user", text: message });
  input.value = "";

  const waiting = appendMsg("…", "bot");
  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: message, session_id: CHAT.sessionId }),
    });
    if (!res.ok) throw new Error("HTTP " + res.status);
    const data = await res.json();
    waiting.remove();

    let meta = null;
    if (data.escalated) {
      const tid = data.ticket && data.ticket.ticket_id ? data.ticket.ticket_id : "—";
      meta = '<span class="meta ticket">🎟️ Derivado a agente humano · Ticket ' + escapeHtml(tid) + "</span>";
    }
    appendMsg(data.reply, "bot", meta);
    CHAT.history.push({ role: "bot", text: data.reply, escalated: data.escalated });
  } catch (err) {
    waiting.remove();
    appendMsg(
      "Lo siento, hubo un problema de conexión con el servicio. Intenta de nuevo en unos momentos.",
      "bot"
    );
  }
  return false;
}
