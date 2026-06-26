import { chromium } from 'playwright'

const TOKEN = process.env.QA_TOKEN
const BASE = 'https://localhost:3018'

const logs = []
const errors = []

const browser = await chromium.launch({ headless: true })
const context = await browser.newContext({ ignoreHTTPSErrors: true })

await context.addCookies([{
  name: 'auth_onigies', value: TOKEN, domain: 'localhost',
  path: '/', httpOnly: false, secure: true, sameSite: 'Lax',
}])

const page = await context.newPage()

page.on('console', (msg) => {
  logs.push(`[${msg.type()}] ${msg.text()}`)
})
page.on('pageerror', (err) => {
  errors.push(`PAGEERROR: ${err.message}\n${err.stack || ''}`)
})
page.on('requestfailed', (req) => {
  const f = req.failure()
  if (f && !/favicon/.test(req.url()))
    logs.push(`[reqfailed] ${req.method()} ${req.url()} :: ${f.errorText}`)
})

console.log('--- 1. Navegando al dashboard de good_practice_package ---')
await page.goto(`${BASE}/dashboard/good_practice_package`, {
  waitUntil: 'networkidle', timeout: 30000,
}).catch((e) => console.log('goto warn:', e.message))

await page.waitForTimeout(2500)
console.log('URL actual:', page.url())
console.log('Título h1/h2:', await page.locator('h1,h2').allTextContents().catch(() => []))

// Cuántas filas/items de lista hay
const rowCount = await page.locator('.v-list-item, tbody tr, [class*="row"]').count().catch(() => 0)
console.log('Posibles filas en lista:', rowCount)

// Buscar el texto TEST5-2025
console.log('\n--- 2. Buscando panel/registro "TEST5-2025" ---')
const test5 = page.getByText('TEST5-2025', { exact: false }).first()
const test5Visible = await test5.count()
console.log('Coincidencias TEST5-2025:', test5Visible)

if (test5Visible > 0) {
  await test5.scrollIntoViewIfNeeded().catch(() => {})
  console.log('Click en TEST5-2025 para abrir detalle...')
  await test5.click().catch((e) => console.log('click warn:', e.message))
  await page.waitForTimeout(2500)
  console.log('URL tras click:', page.url())
}

// Snapshot de paneles expansibles
console.log('\n--- 3. Expansion panels presentes ---')
const panels = page.locator('.v-expansion-panel-title, .v-expansion-panel')
const pCount = await panels.count()
console.log('Expansion panels:', pCount)
const titles = await page.locator('.v-expansion-panel-title').allTextContents().catch(() => [])
titles.slice(0, 30).forEach((t, i) => console.log(`  panel[${i}]: ${t.trim().slice(0, 80)}`))

console.log('\n--- 4. Errores ANTES de expandir ---')
console.log('pageerrors:', errors.length)

// Expandir cada panel uno por uno y registrar errores nuevos
console.log('\n--- 5. Expandiendo paneles ---')
const titleLocator = page.locator('.v-expansion-panel-title')
const n = await titleLocator.count()
for (let i = 0; i < n; i++) {
  const before = errors.length
  const t = (await titleLocator.nth(i).textContent().catch(() => '')) || ''
  await titleLocator.nth(i).scrollIntoViewIfNeeded().catch(() => {})
  await titleLocator.nth(i).click().catch((e) => console.log(`click panel ${i} warn:`, e.message))
  await page.waitForTimeout(1500)
  const after = errors.length
  console.log(`panel[${i}] "${t.trim().slice(0, 50)}" -> nuevos errores: ${after - before}`)
}

await page.waitForTimeout(1000)

console.log('\n================ CONSOLE LOGS ================')
logs.forEach((l) => console.log(l))

console.log('\n================ PAGE ERRORS ================')
errors.forEach((e) => console.log(e + '\n'))

await page.screenshot({ path: '/tmp/claude-1000/-home-rick-dev-unam-onigies/69345763-0ce5-4db9-8124-4bebc87a3890/scratchpad/gpp.png', fullPage: true }).catch(() => {})

await browser.close()
console.log('\nDONE. errores totales:', errors.length)
