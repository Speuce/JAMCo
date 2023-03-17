// @ts-check
import { test, expect } from '@playwright/test'
async function openSite(page) {
  await page.goto('http://localhost:8000/')
  // wait 1 second for the page to load
  await page.waitForTimeout(1000)
  await expect(page).toHaveTitle('JamCo')
}

/**
 * Logs in as john doe and sets up the account
 */
async function setupAccount1(page, initial = false) {
  await page.evaluate(
    // @ts-ignore
    // eslint-disable-next-line no-return-await
    async () => await window.signIn({ credential: 'test', client_id: 'test' }),
  )
  if (initial) {
    await page.fill('#country', 'Canada')
    await page.fill('#field_of_work', 'Software Engineer')
    await page.locator('#sign_up_button').click()
    await page.waitForTimeout(500)
  }
}

/**
 * Logs in as jane doe and sets up the account
 */
async function setupAccount2(page, initial = false) {
  await page.evaluate(async () => {
    // @ts-ignore
    await window.signIn({ credential: 'test2', client_id: 'test2' })
  })
  if (initial) {
    await page.fill('#country', 'USA')
    await page.fill('#field_of_work', 'Data Engineer')
    await page.locator('#sign_up_button').click()
    await page.waitForTimeout(500)
  }
}

/**
 * Logs out the current user
 */
async function logout(page) {
  await page.locator('#user_info_modal_button').click()
  await page.locator('#logout_button').click()
  await page.waitForTimeout(500)
}

test('Adding Friends', async ({ page }) => {
  // setup two users
  await openSite(page)
  await setupAccount1(page, true)
  await logout(page)
  await setupAccount2(page, true)

  // from janes account, add john as a friend
  await page.locator('#friends_modal_button').click()
  await expect(page.locator('#friend_modal')).toBeVisible()
  await page.locator('#add_friends_button').click()
  await expect(page.locator('#search_friends_modal')).toBeVisible()
  await page.fill('#search_friends_search_field', 'John')
  await page.locator('#search_friends_search_button').click()
  // check that john is in the list
  await expect(page.locator('div.friend_card')).toHaveCount(1)
  await expect(page.locator('div.friend_card')).toHaveText('John Doe, Canada')
  // send the request
  await page.locator('#send_friend_request_button').click()
  await expect(page.locator('#friend_request_sent_button')).toBeVisible()

  await page.locator('#close_search_friends_modal_button').click()
  await page.locator('#friend_modal_close_button').click()
  await logout(page)

  // login from johns account and accept the request
  await setupAccount1(page)
  await page.locator('#friends_modal_button').click()
  await expect(page.locator('#friend_modal')).toBeVisible()
  await expect(page.locator('div.request_card')).toHaveCount(1)
  await expect(page.locator('div.request_card')).toContainText('Jane Doe')
  await expect(page.locator('div.request_card')).toContainText('USA')
  await page.locator('#accept_friend_request_button').click()
  await expect(page.locator('div.request_card')).toHaveCount(0)
  await expect(page.locator('div.friend_card')).toHaveCount(1)
  await expect(page.locator('div.friend_card')).toHaveText('Jane Doe, USA')
  await expect(page.locator('#view_kanban_button')).toBeVisible()
  await page.locator('#friend_modal_close_button').click()

  await logout(page)

  // login from janes account and check that the request is gone
  await setupAccount2(page)
  await page.locator('#friends_modal_button').click()
  await expect(page.locator('#friend_modal')).toBeVisible()
  await expect(page.locator('div.friend_card')).toHaveCount(1)
  await expect(page.locator('div.friend_card')).toHaveText('John Doe, Canada')
  await expect(page.locator('#view_kanban_button')).toBeVisible()
})
