---
name: snackbar
description: >
  [nuxt] Global toast notification after async operations (success, error,
  warning). Trigger when showing user feedback after create, update, delete,
  copy, or any action that needs a confirmation message.
---

# snackbar

Store: `store/dash.js` — `useDashboardStore().showSnackbar(message?, action?)`

```js
const dashStore = useDashboardStore()

dashStore.showSnackbar()                           // default: 'Cambios guardados'
dashStore.showSnackbar('Invitación creada')
dashStore.showSnackbar('URL copiada al portapapeles')
```

`action = { label, handler }` turns the toast into an **offer**: an outlined
button that closes the snackbar and runs `handler`, and a 12 s timeout instead
of 4 s so it can be read and reached. Use it to propose the next step without
taking it (cp capture offers «Marcar como completado» to the observable once
its groups allow it); a confirmation needs no action.

## Recommended messages

| Action | Message |
|--------|---------|
| Create | `'<Resource> creado'` |
| Update | `'Cambios guardados'` |
| Delete | `'<Resource> eliminado'` |
| Copy to clipboard | `'URL copiada al portapapeles'` |

## Notes

- Call **inside `try`**, after the operation succeeds — not in `catch`
- Only use from Vue components/pages, not plain composables