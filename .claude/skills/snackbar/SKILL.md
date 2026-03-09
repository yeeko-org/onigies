---
name: snackbar
description: >
  [nuxt] Global toast notification after async operations (success, error,
  warning). Trigger when showing user feedback after create, update, delete,
  copy, or any action that needs a confirmation message.
---

# snackbar

Store: `store/dash.js` — `useDashboardStore().showSnackbar(message?)`

```js
const dashStore = useDashboardStore()

dashStore.showSnackbar()                           // default: 'Cambios guardados'
dashStore.showSnackbar('Invitación creada')
dashStore.showSnackbar('URL copiada al portapapeles')
```

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