import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './agent_tests/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  reporter: 'list',
  use: {
    baseURL: 'http://localhost:3737',
    trace: 'on-first-retry',
  },
  webServer: {
    command: 'python3 -m http.server 3737 --directory app',
    url: 'http://localhost:3737',
    reuseExistingServer: !process.env.CI,
  },
});
