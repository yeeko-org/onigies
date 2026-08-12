---
type: task
id: task-118
title: Borrar sectors_legacy cuando nada lo consuma
state: open
date: 2026-08-12
owner: ai
parent: "[[task-41]]"
source: ["[[2026-08-12-sesion-orquestada-a-b-captura-correcta]]"]
related: ["[[task-112]]", "[[adr-0012]]"]
---

# Borrar sectors_legacy cuando nada lo consuma

Al degradar `Survey.sectors` a propiedad derivada ([[task-112]]), el M2M se renombró a `sectors_legacy` en vez de borrarse, porque [[adr-0012]] mandaba conservarlo mientras hubiera código que lo consumiera. Ricardo lo aceptó **«con miras a borrarlo en el futuro muy pronto, para que no haya dos fuentes de verdad y se confunda»**. Tras la revisión crítica ya quedó fuera del API (excluido del serializer); sobreviven el campo, su tabla intermedia, el `prefetch_related('sectors_legacy')` del ViewSet y el `filter_horizontal` del admin.

Cuándo: después de [[task-117]] y de que el deploy del viernes se asiente. El borrado es una operación más de migración (o la primera de una `0010` si la `0009` ya se deployó), más el barrido de esos tres residuos.

## Criterios de aceptación

- [ ] El campo `sectors_legacy` y su tabla intermedia no existen
- [ ] Ningún residuo en ViewSet, admin ni serializers
- [ ] La propiedad derivada `sectors` sigue siendo la única fuente de verdad
