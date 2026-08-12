import {test,expect} from '@playwright/test';
test('missing share link is safe',async({page})=>{await page.goto('/share/not-real'); await expect(page.getByRole('alert')).toBeVisible()});
