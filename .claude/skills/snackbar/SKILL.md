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

`dashStore.showError(message)` is the error variant: same toast, `error` color, no action. Use it for a failure the component detects itself without an API error to parse (e.g. a `{errors}` result whose message the helper did not already show); API errors still go through `notifyApiError`.

## Recommended messages

| Action | Message |
|--------|---------|
| Create | `'<Resource> creado'` |
| Update | `'Cambios guardados'` |
| Delete | `'<Resource> eliminado'` |
| Copy to clipboard | `'URL copiada al portapapeles'` |

## Notes

- Success toasts go **inside `try`**, after the operation succeeds.
- Errors go through `notifyApiError` (`useApiError`) or the `error_msg` of `fail` (`utils/api.js`, used by the save helpers), never a raw `showSnackbar` in a `catch`: they extract the API message consistently.
- The composables that own the operation (`useFlowActions`, `useApiError`) do call `showSnackbar` themselves; don't repeat the toast in the component that uses them.