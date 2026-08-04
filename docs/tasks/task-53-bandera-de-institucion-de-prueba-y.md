---
type: task
id: task-53
title: Bandera de institución de prueba y secciones publicadas o internas
state: open
date: 2026-08-03
owner: ricardo
source: ["[[2026-07-28-reunion-flujo-bp-e-informacion-base]]"]
---

# Bandera de institución de prueba y secciones publicadas o internas

Para poder probar internamente cada sección antes de abrirla a las IES, y para que Rubí pueda demostrarla en la sesión informativa del 14 de agosto con un usuario de prueba. `[26:22]` «no sé si ya existe como tal, como esa marca o esa bandera o ese flag, como que para distinguir a las universidades que son test de las universidades que no son test. Creo que podríamos como que darle como atributos a los test, por ejemplo... que podamos internamente con la plataforma probar como las secciones que vayamos desarrollando antes de que sean públicas, como ahorita están como congeladas, están inhabilitadas, solo le puedes picar a buenas prácticas y no le puedes picar a los demás. Creo que lo ideal sería que los test puedan picar todo sin restricción, pero como en algún lugar decir esto sólo se va... o sea, esto ya es público, ya es para las universidades».

Son dos mecanismos distintos que se combinan:

1. **Institución de prueba** — una marca en la institución (o en el usuario) que levanta las restricciones de sección.
2. **Sección publicada o interna** — un interruptor por sección que decide si está abierta a las IES reales.

Estado actual: no existe ninguno de los dos. Una búsqueda de `is_test`, `es_test`, `test_institution` y `sandbox` sobre `api/` no devuelve nada; hoy el congelamiento de secciones vive en el frontend.

**Esta task registra el qué, no el cómo.** El modelo de datos —dónde vive cada bandera, si la sección es un catálogo o una constante, cómo se relaciona con `Period`— toca esquema y se decide en su propia sesión con Ricardo antes de escribir código o migraciones.

## Criterios de aceptación

- [ ] Existe una definición escrita del modelo de datos, aprobada por Ricardo
- [ ] Un usuario de institución de prueba puede entrar a todas las secciones
- [ ] Una institución real solo ve las secciones marcadas como publicadas
