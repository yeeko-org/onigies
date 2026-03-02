---
name: password-recovery
description: Implementing password recovery flows. Use this skill whenever the user needs to build or modify the forgot-password page, the recover-password page, token validation on page load, the confirm-new-password step, or the auto-login after reset. Also trigger when the user mentions password reset, recovery link, token expiry, `auth_onigies` cookie setup after recovery, or any of the `/api/password-recovery/` endpoints from the frontend side.
---

# password-recovery

Three-step flow split across two pages. Uses the project's `$api` plugin (axios) for all requests.

## Routing
```
/forgot-password          → Step 1: email form
/recover-password?token=  → Steps 2 + 3: validate token + new password form
```

Use Nuxt file-based routing (`pages/`). No auth middleware — these routes must be publicly accessible.

---

## Step 1 — Request reset email (`/forgot-password`)
```js
const { $api } = useNuxtApp()

async function requestReset(email) {
  await $api.post('/api/password-recovery/', { email })
  showGenericSuccess()  // "Si el correo existe, recibirás un enlace en breve."
  disableSubmitButton() // prevent spam
}
```

**UX rules:**
- Always HTTP 200 — never reveal whether the email is registered (anti-enumeration).
- Disable submit after first send.
- HTTP 400 only when `email` field is absent entirely → show field validation error.

---

## Step 2 — Validate token on page load (`/recover-password`)

The recovery link format is: `{FRONTEND_SITE_URL}/recover-password?token=<uuid>`
```js
const route = useRoute()
const token = route.query.token

async function validateToken() {
  try {
    const { data } = await $api.get(`/api/password-recovery/${token}/`)
    // data = { email, full_name, valid: true }
    userEmail.value = data.email  // optional UX pre-fill
  } catch (err) {
    if (err.response?.status === 400 || err.response?.status === 404) {
      showExpiredTokenError()     // "Enlace inválido o expirado"
      showRequestNewLinkButton()
    }
  }
}
```

| Status | Meaning |
|---|---|
| `200` | Valid — render password form |
| `400` | Expired or already used |
| `404` | UUID not found |

Do **not** render the password form until token is confirmed valid.

---

## Step 3 — Confirm new password + auto-login
```js
async function confirmPassword(password, passwordConfirm) {
  try {
    const { data } = await $api.post(
      `/api/password-recovery/${token}/confirm/`,
      { password, password_confirm: passwordConfirm }
    )
    // Response is identical to POST /api/login/
    const authStore = useAuthStore()
    authStore.user_onigies = data
    authStore.is_logged = true
    const cookie = useCookie('auth_onigies')
    cookie.value = data.token
    navigateTo('/dashboard')
  } catch (err) {
    handleValidationErrors(err.response?.data?.errors)
  }
}
```

**API validation errors (HTTP 400):**

| Field | Message |
|---|---|
| `password` | `"La contraseña debe tener al menos 8 caracteres."` |
| `password_confirm` | `"Las contraseñas no coinciden."` |

HTTP 400 also fires if the token expired between Step 2 and Step 3 (race condition) — show expired token UI again.

---

## Auth store (`store/auth.js`)
```js
// Expected shape
user_onigies   // full user object from API
is_logged      // boolean
// Getters: is_staff, is_full_editor, is_mini_editor
```

After Step 3, set both `user_onigies` and `is_logged = true`. The `$api` plugin auto-attaches `auth_onigies` cookie on all subsequent requests — no extra headers needed. Store the token in the cookie, never in `localStorage`.

---

## Form validation (`composables/useRules.js`)
```js
const { required, minLength } = useRules()

const rules = {
  password: [required, minLength(8)],
  passwordConfirm: [required, (v) => v === password.value || 'Las contraseñas no coinciden']
}
```

Always validate `password_confirm` client-side before submitting.

---

## Security checklist

- [ ] Never reveal email existence in Step 1
- [ ] Disable submit after first send
- [ ] Validate token before rendering password form
- [ ] Show expired-link UI with "request new link" CTA
- [ ] Match `password_confirm` client-side before submit
- [ ] Handle token-expired race condition in Step 3
- [ ] Store session token in `auth_onigies` cookie, not `localStorage`
- [ ] Redirect to `/dashboard` after auto-login, not `/login`

---

## Out of scope

- `/api/login/` endpoint (use the main auth skill)
- Email template customization (backend concern)
- MFA or OAuth login