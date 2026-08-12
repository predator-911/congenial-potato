import {test,expect} from '@playwright/test';
test('home redirects to login',async({page})=>{await page.goto('/'); await expect(page.getByText('Log in')).toBeVisible()});
