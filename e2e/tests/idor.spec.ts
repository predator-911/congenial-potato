import {test,expect} from '@playwright/test';
test('login required before files are visible',async({page})=>{await page.goto('/'); await expect(page).toHaveURL(/login/)});
