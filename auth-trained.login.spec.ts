import { test, expect } from '@playwright/test';

test.describe('Login', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/login');
  });

  test('should login successfully', async ({ page }) => {
    await page.getByTestId('input-email').fill('test@example.com');
    await page.getByTestId('input-password').fill('password123');
    await page.getByTestId('button-login').click();
    await expect(page).toHaveURL('/dashboard');
  });
});
