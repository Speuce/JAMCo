// @ts-check
import { test, expect } from '@playwright/test'

async function setup(page) {
  await page.goto('http://localhost:8000/')
  // wait 5 seconds for the page to load
  await page.waitForTimeout(1000)
  await expect(page).toHaveTitle('JamCo')

  await page.evaluate(
    // @ts-ignore
    // eslint-disable-next-line no-return-await
    async () => await window.signIn({ credential: 'test', client_id: 'test' }),
  )
  await page.fill('#country', 'Canada')
  await page.fill('#field_of_work', 'Software Engineer')
  await page.locator('#sign_up_button').click()
  await page.waitForTimeout(500)
}

test('Basic Job Creation', async ({ page }) => {
  await setup(page)

  await page.locator('#add-job-button').click()

  // ensure the job modal is open
  await expect(page.locator('#job-detail-modal-card')).toBeVisible()

  // fill out the job modal
  await page.fill('#job-title', 'Software Engineer')
  await page.fill('#job-type', 'Frontend')
  await page.fill('#job-company', 'Google')
  await page.fill('#job-description', 'This is a job description')
  await page.fill('#job-cover-letter', 'This is a cover letter')
  await page.fill('#job-notes', 'This is a note')

  // submit the job
  await page.locator('#job-save-button').click()

  // ensure the job modal is closed
  await expect(page.locator('#job-detail-modal-card')).toBeHidden()

  // ensure the job is in the list
  await expect(page.locator('div.job-card')).toHaveCount(1)
})

test('Job Creation with no title', async ({ page }) => {
  await setup(page)

  await page.locator('#add-job-button').click()

  // ensure the job modal is open
  await expect(page.locator('#job-detail-modal-card')).toBeVisible()

  // fill out the job modal
  await page.fill('#job-type', 'Frontend')
  await page.fill('#job-company', 'Google')
  await page.fill('#job-description', 'This is a job description')
  await page.fill('#job-cover-letter', 'This is a cover letter')
  await page.fill('#job-notes', 'This is a note')

  // submit the job
  await page.locator('#job-save-button').click()

  // ensure the job modal is still open
  await expect(page.locator('#job-detail-modal-card')).toBeVisible()

  // ensure the job is not in the list
  await expect(page.locator('div.job-card')).toHaveCount(0)
})
