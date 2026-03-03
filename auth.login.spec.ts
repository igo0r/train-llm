import { test, expect } from '@playwright/test';

test.describe('Login Page', () => {
    test('should log in successfully and navigate to dashboard', async ({ page }) => {
        // Navigate to the login page
        await page.goto('/login');

        // Fill email input with "test@example.com"
        await page.fill('[data-testid="input-email"]', 'test@example.com');

        // Fill password input with "password123"
        await page.fill('[data-testid="input-password"]', 'password123');

        // Click login button
        await page.click('[data-testid="button-login"]');

        // Assert URL changes to "/dashboard"
        await expect(page).toHaveURL('/dashboard');
    });
});
