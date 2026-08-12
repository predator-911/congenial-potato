import {test,expect} from '@playwright/test';
test('register page is available',async({page})=>{await page.goto('/register'); await expect(page.getByText('Register')).toBeVisible()});
