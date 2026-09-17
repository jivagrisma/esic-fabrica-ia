// Escenario 2 — UI del validador de documentos (vanilla JS, sin librerías).

function escapeHtml(v) {
  return String(v ?? "")
    .replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;").replaceAll("'", "&#39;");
}

function _archivoElegido() {
  const a = document.getElementById("doc-file");
  const b = document.getElementById("doc-file-cam");
  if (a.files.length) return a.files[0];
  if (b.files.length) return b.files[0];
  return null;
}

async function sendDoc(event) {
  event.preventDefault();
  const file = _archivoElegido();
  const out = document.getElementById("docs-result");
  if (!file) {
    out.innerHTML = '<p><span class="badge warn">Primero adjunta un documento</span></p>';
    return false;
  }
  if (file.size > 10 * 1024 * 1024) {
    out.innerHTML = '<p><span class="badge warn">El archivo supera 10 MB</span></p>';
    return false;
  }

  const fd = new FormData();
  fd.append("file", file);
  fd.append("doc_type", document.getElementById("doc-type").value);
  fd.append("applicant_name", document.getElementById("applicant-name").value);
  fd.append("solicitud_id", "SOL-" + String(Math.floor(1000 + Math.random() * 9000)));

  const btn = document.getElementById("docs-submit");
  btn.disabled = true;
  btn.innerHTML = '<span class="spinner"></span>Analizando documento…';
  out.innerHTML = "";

  try {
    const res = await fetch("/api/documents", { method: "POST", body: fd });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || ("HTTP " + res.status));
    }
    renderDocResult(await res.json());
  } catch (e) {
    out.innerHTML = '<p><span class="badge err">No pudimos validar el documento</span><br>' +
      '<span class="hint">' + escapeHtml(e.message) + '</span></p>';
  } finally {
    btn.disabled = false;
    btn.textContent = "Validar documento";
  }
  return false;
}

function renderDocResult(d) {
  const cls = d.verdict === "valido" ? "ok" : (d.verdict === "alerta" ? "warn" : "err");
  const labels = {
    valido: "✓ DOCUMENTO VÁLIDO",
    alerta: "⚠ REVISAR — CON ALERTAS",
    rechazado: "✕ DOCUMENTO RECHAZADO",
  };

  let html = '<span class="badge ' + cls + '">' + escapeHtml(labels[d.verdict] || d.verdict) +
    "</span> &nbsp;<span class='hint'>Confianza de lectura: " +
    escapeHtml(Math.round((d.confidence || 0) * 100) + "%") +
    " · Reporte " + escapeHtml(d.report_id) + "</span>";

  const campos = d.campos_extraidos || {};
  const claves = Object.keys(campos);
  if (claves.length) {
    html += "<h4>Datos leídos del documento</h4><div class='campos'>";
    for (const k of claves) {
      const v = campos[k];
      html += "<div class='campo'><b>" + escapeHtml(k) + "</b>" +
        (v === null || v === undefined || v === "" ? "—" : escapeHtml(v)) + "</div>";
    }
    html += "</div>";
  }

  if (d.alertas && d.alertas.length) {
    html += "<h4 style='color:var(--rojo)'>⚠ Alertas para revisar</h4><ul class='alertas'>";
    for (const a of d.alertas) html += "<li>" + escapeHtml(a) + "</li>";
    html += "</ul>";
  } else if (d.verdict === "valido") {
    html += "<h4 style='color:var(--verde)'>Sin alertas: documento completo y consistente.</h4>";
  }

  const sia = d.entrega_sia || {};
  html += "<h4>Entrega al sistema académico</h4><div class='nota-sim'>" +
    (sia.omitido
      ? "No se entregó: " + escapeHtml(sia.omitido) + "."
      : "✓ Registrada en la solicitud (modo de prueba) · Comprobante: <b>" +
        escapeHtml(sia.recibo || "?") + "</b>") + "</div>";

  html += "<details class='tecnico'><summary>Ver detalle técnico completo</summary>" +
    "<pre class='json'>" + escapeHtml(JSON.stringify(d, null, 2)) + "</pre></details>";

  document.getElementById("docs-result").innerHTML = html;
}
