---
type: feedback
id: fb-1
title: "El campo order nunca se edita en un formulario del dashboard: para eso existe el switch Reordenar"
state: pending
date: 2026-09-10
created: "2026-09-10T18:59:24-06:00"
scope: local
kind: new
author:
  role: coordinator
mode: requested
session: d5ef9c1e-a1fa-4557-975b-341682832e18
target: .claude/skills/dashboard-collections/SKILL.md
from-repo: onigies
---

# El campo order nunca se edita en un formulario del dashboard: para eso existe el switch Reordenar

## Qué pasó

Al revisar el editor nuevo de tipos de pregunta y el de observable, Ricardo: «El campo "Orden del bloque" no va nunca en Edit, eso se cambia desde otro lugar (Esto es un FB o algo a modificar del skill de dashboard-collections)» y después «El orden tampoco va dentro de un observable» y «La regla del campo "order" aplica al marco genérico, es algo que se edita fuera, para eso existe el switch de "Reordenar" arriba de las listas». Ninguna regla lo decía; el marco genérico EditCommonFields lo pintaba editable desde siempre.

## Propuesta

Ya escrito en dashboard-collections (§ Edit vs EditSimple) y aplicado al marco genérico y a los editores de la sesión; queda task-147 para barrer los demás editores.

## Outcome
