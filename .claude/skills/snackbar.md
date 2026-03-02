---
name: snackbar
description: Show global snackbar notifications after user actions. Use when a CRUD operation, clipboard copy, or UI event needs visual feedback. Trigger on "snackbar", "toast", "notification", "success message", or "user feedback".
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