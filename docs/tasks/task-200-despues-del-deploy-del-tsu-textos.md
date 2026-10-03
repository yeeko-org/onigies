---
type: task
id: task-200
title: "Después del deploy del TSU: textos de las preguntas de planes, aviso a Rubén y smoke manual"
state: open
date: 2026-10-03
owner: ricardo
parent: "[[task-2]]"
source: ["[[2026-10-03-deploy-del-nivel-tecnico-superior-y-la-valvula-de-admin]]"]
related: ["[[task-192]]", "[[task-163]]", "[[task-186]]"]
---

# Después del deploy del TSU: textos de las preguntas de planes, aviso a Rubén y smoke manual

Lo que el deploy de [[task-192]] dejó en manos de Ricardo, fuera de la plataforma o del dashboard.

- **Textos vivos de las cuatro preguntas de planes del 1.12.** `add_tsu_sector` creó `technical_plans` con el texto del comando y dejó las otras tres como estaban; el dashboard es la única fuente del instrumento ([[adr-0015]]), así que los textos con «técnico superior» los edita Rubén o Ricardo ahí.
- **Aviso a Rubén.** El TSU ya está vivo: en Generales (grupo de planes y población) y en el alcance del 1.16; las 3 IES con TSU quedaron en «No» (lo resolvió Ricardo el 2026-10-02 en task-192). También la válvula de admin ya está en el dashboard. Si el aviso cp de [[task-163]] sigue pendiente, van juntos.
- **Smoke manual en navegador** tras el deploy: login, `/respuestas`, un paquete de BP; como revisora, la válvula de admin en un timeline; como IES de prueba, el 1.12 con la pregunta de planes TSU.

## Criterios de aceptación

- [ ] Textos de las cuatro preguntas de planes editados en el dashboard con «técnico superior»
- [ ] Rubén avisado del TSU y de la válvula de admin
- [ ] Smoke manual en navegador en verde
