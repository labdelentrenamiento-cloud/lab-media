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

## Portada (obligatoria en cada video)
Estilo de portada = el mismo del video (fondo azul noche con grilla, holograma nítido, neón cian/verde/ámbar): `--estilo video` (por defecto). Instagram y TikTok usan el PRIMER cuadro del video como portada, y la grilla del perfil de Instagram recorta al centro 3:4. Por eso cada video lleva una portada propia como primeros 0,2 s:
`python3 motor/cover.py videos/vNNN_X_LAB.mp4 "LÍNEA 1|LÍNEA *CLAVE*|LÍNEA 3" videos/vNNN_X_LAB.mp4 --png portadas/vNNN_portada.png`
- Texto centrado en la zona que muestra Instagram (feed 4:5 y grilla 3:4).
- 2–3 líneas cortas en MAYÚSCULAS con el gancho (pregunta o promesa), 1–2 palabras clave entre *asteriscos* (van en ámbar). Nada de spoilers del resultado en el texto.
- Revisa la PNG antes de guardar: texto completo, sin superposiciones, legible en miniatura, colores cálidos (no todo azul).
- En queue.json: `cover` (texto), `cover_png` y `cover_in_video: true`. No publiques un video sin `cover_in_video: true`.
- YouTube: si la API/Studio lo permite, usar portadas/vNNN_portada.png como miniatura.

## Encuadre e interacción (pedido de Michelle)
- Centrado: Instagram muestra los Reels recortados a 4:5 en el feed (se pierden ~285 px arriba y abajo). El motor ya baja todo el contenido 90 px (`SHIFT_Y` en engine_ext.py) y pone los subtítulos en y=1490. Al revisar la hoja de contacto, todo lo importante (títulos, datos, fuentes) debe quedar entre y≈300 y y≈1620, y nada importante en los 140 px de la derecha (botones de Instagram/TikTok).
- Compartir: el motor dibuja en la escena final "COMPÁRTELO CON QUIEN LO NECESITE" y "GUÁRDALO PARA DESPUÉS". La última frase del guion es: "Compártelo con alguien que lo necesite y sígueme para más ciencia del entrenamiento."
- Caption (Instagram y TikTok) y descripción (YouTube), en este orden: gancho + resumen breve → una PREGUNTA para comentar relacionada con el tema (p. ej. "¿Cuánto descansas tú entre series? 👇") → "📤 Envíaselo a alguien que lo necesite y 🔖 guárdalo para tu próximo entrenamiento" → "📚 Fuentes:" → "Sígueme para más ciencia del entrenamiento 🔬" → hashtags.

## Publicación (orden por slot: YouTube H → Instagram H+1 → TikTok H+2)
Slots actuales (America/Santiago): ver `queue.json` → `slots`. Se ajustan con las estadísticas semanales.

Desde el 2026-11-11 TODO se publica con vidIQ, en la nube (Michelle decidió no depender del computador). Cuentas conectadas en vidIQ (`vidiq_social_account_list`):
- YouTube: platformAccountId `UC-FvbgKGTDuGtCBt5SLRZgA` (@labdelentrenamiento)
- Instagram: platformAccountId `29194008733571171` (labdelentrenamiento)
- TikTok: platformAccountId `_000GSl62CkrNcegWeVPUh6LPcRlcItlafJk`
Si una cuenta aparece con canPublish false o la conexión expiró, NO publiques en esa red: deja `pending` y avisa a Michelle con el enlace de reconexión (`vidiq_social_account_connect` para Instagram/TikTok, `vidiq_connect_youtube_channel` para YouTube).

### YouTube (vidIQ)
1. `vidiq_video_upload` con RAW_URL → uploadId.
2. `vidiq_social_post_draft_create`: media `[{type:"video", id:uploadId}]`, destino YOUTUBE con title (con #shorts), text = descripción (caption + "Fuentes:" (lista) + "Lab del Entrenamiento: ciencia del entrenamiento en menos de 1 minuto. Sígueme para más." + hashtags), privacyStatus `public`, categoryId 27, tags (5–6 palabras clave) y `publishAt` = H con -03:00 (queda privado y YouTube lo hace público a esa hora). Si el slot ya pasó: sin publishAt (público inmediato).
3. `vidiq_social_post_publish` con postId y revision → `vidiq_social_post_status` hasta tener postUrl. Guardar `vidiq_post` y url (status "scheduled" si tiene publishAt, "published" si salió).
4. Duplicados: antes de subir, si el video ya tiene `vidiq_post`, consulta su estado en vez de crear otro; `vidiq_channel_videos` (Shorts, 5 créditos) muestra lo ya publicado.

### YouTube (método antiguo con Chrome — solo respaldo)
La subida de archivos con la herramienta file_upload está bloqueada; usar este método en la página:
1. Abrir `https://studio.youtube.com/channel/UC-FvbgKGTDuGtCBt5SLRZgA/videos/upload?d=ud`.
2. javascript_tool: `const b=await (await fetch(RAW_URL)).blob(); const f=new File([b],NOMBRE,{type:'video/mp4'}); const dt=new DataTransfer(); dt.items.add(f); const i=document.querySelector('input[type=file]'); i.files=dt.files; i.dispatchEvent(new Event('change',{bubbles:true}));`
3. Título y descripción: foco en `ytcp-uploads-dialog #title-textarea #textbox` y `#description-textarea #textbox`, `document.execCommand('selectAll')` + `document.execCommand('insertText',false,TEXTO)`. Descripción = caption + "Fuentes:" (lista) + "Lab del Entrenamiento: ciencia del entrenamiento en menos de 1 minuto. Sígueme para más." + hashtags.
4. "No es contenido para niños": click en `tp-yt-paper-radio-button[name="VIDEO_MADE_FOR_KIDS_NOT_MFK"]`.
5. `#next-button` x3 → Visibilidad → expandir "Programar" → fecha/hora del slot (campo hora: triple click, escribir "h:mm p.m.", Enter) → "Programar". Si el slot ya pasó: Público → Publicar.
6. Leer el enlace del diálogo final y guardarlo en queue.json.

### Instagram (vidIQ, a la hora H+1)
1. Duplicados: `vidiq_instagram_owner_insights` (platformAccountId de arriba, mode `media`, metrics `["views"]`, gratis) lista los reels publicados; si el del video ya está, solo guarda su permalink.
2. `vidiq_video_upload` con RAW_URL → videoUrl (firmado de vidIQ).
3. `vidiq_instagram_publish_reel` con platformAccountId, videoUrl, caption = caption + "📚 Fuentes:" + fuentes + "Sígueme para más ciencia del entrenamiento 🔬" + hashtags, e `isAiGenerated: true` (etiqueta IA, regla de Michelle). Devuelve containerId con IN_PROGRESS: espera ~15 s y vuelve a llamar solo con platformAccountId + containerId hasta PUBLISHED. Nunca crees otro contenedor para el mismo video; si da error, déjalo `pending` y anota el error.
4. Guarda el permalink como `https://www.instagram.com/labdelentrenamiento/reel/<shortcode>/` (status "published") y haz push.

### Instagram (método antiguo con Chrome — solo respaldo)
1. `https://www.instagram.com/labdelentrenamiento/` → Crear → Publicación.
2. En el diálogo, inyectar el MP4 igual que en YouTube en el `input[type=file]` del diálogo.
3. Recortar: elegir **Original** (NO 1:1). Siguiente → portada = primer cuadro, sonido activado → Siguiente.
4. Caption (contenteditable del diálogo): caption + "📚 Fuentes:" + fuentes + "Sígueme para más ciencia del entrenamiento 🔬" + hashtags. Activar la etiqueta de IA en "Configuración avanzada" si aparece. Compartir y esperar "Se compartió tu reel".

### TikTok (vidIQ, en la nube; no necesita el computador)
`vidiq_video_upload` con RAW_URL → `vidiq_social_post_draft_create` (destino TIKTOK, platformAccountId `_000GSl62CkrNcegWeVPUh6LPcRlcItlafJk`, ajustes de `tiktok_settings`, `publishAt` = H+2 con zona -03:00) → `vidiq_social_post_publish`.

### Si vidIQ falla en una red
Publicar en las demás redes igual y dejar la que falló en `pending`; el siguiente run la recupera antes de tomar videos nuevos. Nunca publicar el mismo video dos veces en la misma red.

## Copia en el computador
Carpeta: `C:\Users\usuario\Videos\Lab del Entrenamiento\1_por_subir\`. Con las herramientas mcp__remote-devices__ (si responden): descargar el MP4 desde RAW_URL a /mnt/user-data/outputs/ y `device_commit_files`. Marcar `synced_to_pc: true`. Si el computador está apagado, dejar `false` y reintentar en el siguiente run.

## Panel
Artefacto "panel" (slug en la tarea programada): registrar cada video y cada publicación en el log del panel.
