import { defineConfig, devices } from '@playwright/test'

const PORT = 3019
const BASE_URL = `https://localhost:${PORT}`

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [
    ['list'],
    ['html', { open: 'never' }],
  ],
  use: {
    baseURL: BASE_URL,
    ignoreHTTPSErrors: true,
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
  webServer: {
    command: 'pnpm dev:test',
    url: BASE_URL,
    reuseExistingServer: !process.env.CI,
    timeout: 180_000,
    ignoreHTTPSErrors: true,
    // Forzamos env vars aquí por si `nuxi --dotenv` no se aplica como
    // esperamos — garantiza que el backend URL apunte al :8019 fake.
    env: {
      NUXT_API_URL: 'http://localhost:8019/api',
      NUXT_ADMIN_URL: 'http://localhost:8019/admin',
    },
    stdout: 'pipe',
    stderr: 'pipe',
  },
})