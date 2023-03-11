// @ts-check
import { test, expect } from '@playwright/test'

test('account creation', async ({ page }) => {
  await page.goto('http://localhost:8000/')
  // wait 5 seconds for the page to load
  await page.waitForTimeout(1000)
  await expect(page).toHaveTitle('JamCo')

  await page.evaluate(
    // @ts-ignore
    // eslint-disable-next-line no-return-await
    async () => await window.signIn({ credential: 'test', client_id: 'test' }),
  )

  // check that the first name field is filled
  await expect(page.locator('#first_name')).toHaveValue('John')
  // check that the last name field is filled
  await expect(page.locator('#last_name')).toHaveValue('Doe')

  await page.fill('#country', 'Canada')
  await page.fill('#region', 'Ontario')
  await page.fill('#city', 'Toronto')

  await page.fill('#field_of_work', 'Software Engineer')
  await page.locator('#sign_up_button').click()
  // check that dialog is closed
  await expect(page.locator('#signin_dialog')).toBeHidden()
})
