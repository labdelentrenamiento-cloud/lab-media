# Lab del Entrenamiento — Runbook de automatización

Repositorio público: `labdelentrenamiento-cloud/lab-media` (rama `main`).
- `videos/` — MP4 finales (vNNN_Tema_LAB.mp4). URL pública: `https://raw.githubusercontent.com/labdelentrenamiento-cloud/lab-media/main/videos/<archivo>`
- `queue.json` — cola: título, caption, fuentes, hashtags, slot y estado por red (pending | scheduled | published | failed), `synced_to_pc`.
- `motor/` — motor de video (engine.py, engine_ext.py, audio.py, vo.py, render_*.py, script_*.json, LEEME.txt).
- `stats/` — informes semanales de estadísticas y horarios (`stats/AAAA-MM-DD.md`).

Git en las tareas programadas: el repo YA viene clonado en /home/claude/lab-media (HEAD suelto). NO llames add_repo. Antes de trabajar: `cd /home/claude/lab-media && git fetch origin main && git checkout -B main origin/main` (si la carpeta no existe: `git clone --depth 1 https://github.com/labdelentrenamiento-cloud/lab-media /home/claude/lab-media`). Para guardar: `git add -A && git commit -m "..." && git fetch origin main && git rebase origin/main && git push origin HEAD:main`. Commits con user.name "Lab del Entrenamiento", user.email "labdelentrenamiento@gmail.com". Si el push falla, NO publiques nada que dependa de ese cambio y avisa a Michelle.

Regla de seguridad: queue.json es la única fuente de verdad. Solo se publican videos con `file_ready: true`. Guarda el estado (push) inmediatamente después de cada publicación, antes de pasar a la siguiente.

## Reglas de contenido (Michelle)
- Estilo = video n.º 3 (Huesos): holograma LAB, HUD, datos con fuente en pantalla, subtítulos palabra por palabra. No cambiar las ideas/temas del canal (ciencia del entrenamiento: fuerza, músculo, huesos, cerebro, salud, rendimiento).
- Michelle NO aparece ni se presenta como profe en los videos.
- Evidencia: cada dato con fuente verificable y vigente. Buscar en varias fuentes (PubMed, revistas, OMS, ACSM, NIH, web actualizada). Si hay evidencia más nueva que contradice un dato, corregirlo. Nunca inventar cifras.
- Monetización (política de YouTube de contenido genérico/repetitivo): variar formatos (mito vs. realidad, "qué pasa si…", comparaciones, récords del cuerpo, "si quisieras X harías esto"), paletas/escenas por serie, ganchos y títulos distintos. Nada sensacionalista ni de miedo.
- Etiqueta IA: YouTube NO (voz genérica + animación). Instagram SÍ (voz en off realista con IA). TikTok SÍ (`isAiGenerated: true`).
- TikTok (decidido por Michelle): público, comentarios sí, música confirmada, etiqueta IA.

## Producción
Antes de elegir temas, leer el informe más reciente en `stats/` (sección "Para producción") y seguir sus recomendaciones de temas, formatos y ganchos.

## Publicación (orden por slot: YouTube H → Instagram H+1 → TikTok H+2)
Slots actuales (America/Santiago): ver `queue.json` → `slots`. Se ajustan con las estadísticas semanales.

### YouTube (Chrome de Michelle, extensión Claude in Chrome)
La subida de archivos con la herramienta file_upload está bloqueada; usar este método en la página:
1. Abrir `https://studio.youtube.com/channel/UC-FvbgKGTDuGtCBt5SLRZgA/videos/upload?d=ud`.
2. javascript_tool: `const b=await (await fetch(RAW_URL)).blob(); const f=new File([b],NOMBRE,{type:'video/mp4'}); const dt=new DataTransfer(); dt.items.add(f); const i=document.querySelector('input[type=file]'); i.files=dt.files; i.dispatchEvent(new Event('change',{bubbles:true}));`
3. Título y descripción: foco en `ytcp-uploads-dialog #title-textarea #textbox` y `#description-textarea #textbox`, `document.execCommand('selectAll')` + `document.execCommand('insertText',false,TEXTO)`. Descripción = caption + "Fuentes:" (lista) + "Lab del Entrenamiento: ciencia del entrenamiento en menos de 1 minuto. Sígueme para más." + hashtags.
4. "No es contenido para niños": click en `tp-yt-paper-radio-button[name="VIDEO_MADE_FOR_KIDS_NOT_MFK"]`.
5. `#next-button` x3 → Visibilidad → expandir "Programar" → fecha/hora del slot (campo hora: triple click, escribir "h:mm p.m.", Enter) → "Programar". Si el slot ya pasó: Público → Publicar.
6. Leer el enlace del diálogo final y guardarlo en queue.json.

### Instagram (Chrome, a la hora H+1 — la web no permite programar)
1. `https://www.instagram.com/labdelentrenamiento/` → Crear → Publicación.
2. En el diálogo, inyectar el MP4 igual que en YouTube en el `input[type=file]` del diálogo.
3. Recortar: elegir **Original** (NO 1:1). Siguiente → portada = primer cuadro, sonido activado → Siguiente.
4. Caption (contenteditable del diálogo): caption + "📚 Fuentes:" + fuentes + "Sígueme para más ciencia del entrenamiento 🔬" + hashtags. Activar la etiqueta de IA en "Configuración avanzada" si aparece. Compartir y esperar "Se compartió tu reel".

### TikTok (vidIQ, en la nube; no necesita el computador)
`vidiq_video_upload` con RAW_URL → `vidiq_social_post_draft_create` (destino TIKTOK, platformAccountId `_000GSl62CkrNcegWeVPUh6LPcRlcItlafJk`, ajustes de `tiktok_settings`, `publishAt` = H+2 con zona -03:00) → `vidiq_social_post_publish`.

### Si el computador/Chrome no responde
Publicar en TikTok igual (vidIQ) y dejar YouTube/Instagram en `pending`; el siguiente run los recupera antes de tomar videos nuevos. Nunca publicar el mismo video dos veces en la misma red.

## Copia en el computador
Carpeta: `C:\Users\usuario\Videos\Lab del Entrenamiento\1_por_subir\`. Con las herramientas mcp__remote-devices__ (si responden): descargar el MP4 desde RAW_URL a /mnt/user-data/outputs/ y `device_commit_files`. Marcar `synced_to_pc: true`. Si el computador está apagado, dejar `false` y reintentar en el siguiente run.

## Panel
Artefacto "panel" (slug en la tarea programada): registrar cada video y cada publicación en el log del panel.
