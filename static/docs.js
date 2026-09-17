// Escenario 2 — UI del validador de documentos (vanilla JS, sin librerías).

function escapeHtml(v) {
  return String(v ?? "")
    .replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;").replaceAll("'", "&#39;");
}

async function sendDoc(event) {
  event.preventDefault();
  const fileInput = document.getElementById("doc-file");
  if (!fileInput.files.length) {
    document.getElementById("docs-result").innerHTML =
      '<p class="badge err">Selecciona un archivo para validar.</p>';
    return false;
  }
  const fd = new FormData();
  fd.append("file", fileInput.files[0]);
  fd.append("doc_type", document.getElementById("doc-type").value);
  fd.append("applicant_name", document.getElementById("applicant-name").value);
  fd.append("solicitud_id", "SOL-" + String(Math.floor(1000 + Math.random() * 9000)));
  const out = document.getElementById("docs-result");
  out.innerHTML = "<p>Analizando documento…</p>";
  try {
    const res = await fetch("/api/documents", { method: "POST", body: fd });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || ("HTTP " + res.status));
    }
    renderDocResult(await res.json());
  } catch (e) {
    out.innerHTML = '<p class="badge err">Error al validar el documento: ' +
      escapeHtml(e.message) + "</p>";
  }
  return false;
}

function renderDocResult(d) {
  const cls = d.verdict === "valido" ? "ok" : (d.verdict === "alerta" ? "warn" : "err");
  const labels = { valido: "VÁLIDO", alerta: "ALERTA", rechazado: "RECHAZADO" };

  let html = '<span class="badge ' + cls + '">' + escapeHtml(labels[d.verdict] || d.verdict) +
    "</span> <span>Confianza OCR: " + escapeHtml(Math.round((d.confidence || 0) * 100) + "%") +
    " · Reporte " + escapeHtml(d.report_id) + "</span>";

  html += "<h4>Campos extraídos</h4><ul>";
  const campos = d.campos_extraidos || {};
  const claves = Object.keys(campos);
  if (!claves.length) {
    html += "<li>—</li>";
  } else {
    for (const k of claves) {
      html += "<li><b>" + escapeHtml(k) + ":</b> " +
        (campos[k] === null || campos[k] === undefined || campos[k] === ""
          ? "—" : escapeHtml(campos[k])) + "</li>";
    }
  }
  html += "</ul>";

  if (d.alertas && d.alertas.length) {
    html += '<h4 style="color:#a00">Alertas</h4><ul style="color:#a00">';
    for (const a of d.alertas) html += "<li>" + escapeHtml(a) + "</li>";
    html += "</ul>";
  }

  const sia = d.entrega_sia || {};
  html += '<div class="sim"><b>Entrega al sistema académico (SIMULADA)</b><br>' +
    (sia.omitido
      ? "Omitida: " + escapeHtml(sia.omitido)
      : "Estado: " + escapeHtml(sia.solicitud_estado || "?") +
        " · Recibo: " + escapeHtml(sia.recibo || "?")) + "</div>";

  const teams = d.notificacion_teams || {};
  html += '<div class="sim"><b>Notificación Teams (SIMULADA)</b><br>' +
    (teams.omitido
      ? "Omitida: " + escapeHtml(teams.omitido)
      : escapeHtml(teams.mensaje_publicado || teams.mensaje || "")) + "</div>";

  html += '<pre class="json">' + escapeHtml(JSON.stringify(d, null, 2)) + "</pre>";

  document.getElementById("docs-result").innerHTML = html;
}
