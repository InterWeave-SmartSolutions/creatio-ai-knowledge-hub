import { test, expect } from '@playwright/test';

test.describe('Knowledge Hub Search', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to the search page
    await page.goto('/');
    await page.waitForLoadState('networkidle');
  });

  test('should display search form on homepage', async ({ page }) => {
    // Check if search form is visible
    await expect(page.locator('[data-test="search-form"]')).toBeVisible();
    await expect(page.locator('[data-test="search-input"]')).toBeVisible();
    await expect(page.locator('[data-test="search-button"]')).toBeVisible();
  });

  test('should search for videos and display results', async ({ page }) => {
    // Enter search term
    await page.fill('[data-test="search-input"]', 'creatio development');
    await page.click('[data-test="search-button"]');

    // Wait for results to load
    await page.waitForSelector('[data-test="search-results"]');

    // Verify results are displayed
    await expect(page.locator('[data-test="search-results"]')).toBeVisible();
    await expect(page.locator('[data-test="result-item"]')).toHaveCount({ min: 1 });

    // Check if video results contain expected elements
    const firstResult = page.locator('[data-test="result-item"]').first();
    await expect(firstResult.locator('[data-test="result-title"]')).toBeVisible();
    await expect(firstResult.locator('[data-test="result-summary"]')).toBeVisible();
    await expect(firstResult.locator('[data-test="result-topics"]')).toBeVisible();
  });

  test('should filter results by content type', async ({ page }) => {
    // Search for content
    await page.fill('[data-test="search-input"]', 'creatio');
    await page.click('[data-test="search-button"]');
    await page.waitForSelector('[data-test="search-results"]');

    // Apply video filter
    await page.click('[data-test="filter-videos"]');
    await page.waitForLoadState('networkidle');

    // Verify only video results are shown
    const results = page.locator('[data-test="result-item"]');
    await expect(results).toHaveCount({ min: 1 });
    
    for (let i = 0; i < await results.count(); i++) {
      await expect(results.nth(i).locator('[data-test="result-type"]')).toContainText('Video');
    }
  });

  test('should display no results message for invalid search', async ({ page }) => {
    // Search for non-existent content
    await page.fill('[data-test="search-input"]', 'xyznonexistentquery123');
    await page.click('[data-test="search-button"]');

    // Wait for no results message
    await page.waitForSelector('[data-test="no-results"]');
    await expect(page.locator('[data-test="no-results"]')).toBeVisible();
    await expect(page.locator('[data-test="no-results"]')).toContainText('No results found');
  });

  test('should handle search with special characters', async ({ page }) => {
    // Search with special characters
    await page.fill('[data-test="search-input"]', 'C# .NET "development"');
    await page.click('[data-test="search-button"]');

    // Should either show results or no results message (not error)
    await page.waitForSelector('[data-test="search-results"], [data-test="no-results"]');
    
    // Verify no error messages are displayed
    await expect(page.locator('[data-test="error-message"]')).not.toBeVisible();
  });

  test('should navigate to video details page', async ({ page }) => {
    // Search and get results
    await page.fill('[data-test="search-input"]', 'creatio');
    await page.click('[data-test="search-button"]');
    await page.waitForSelector('[data-test="search-results"]');

    // Click on first result
    const firstResult = page.locator('[data-test="result-item"]').first();
    await firstResult.click();

    // Verify navigation to details page
    await page.waitForURL(/\/videos\/.+/);
    await expect(page.locator('[data-test="video-title"]')).toBeVisible();
    await expect(page.locator('[data-test="video-transcript"]')).toBeVisible();
  });

  test('should maintain search state on back navigation', async ({ page }) => {
    const searchTerm = 'creatio development';
    
    // Perform search
    await page.fill('[data-test="search-input"]', searchTerm);
    await page.click('[data-test="search-button"]');
    await page.waitForSelector('[data-test="search-results"]');

    // Navigate to a result
    await page.locator('[data-test="result-item"]').first().click();
    await page.waitForLoadState('networkidle');

    // Go back
    await page.goBack();
    await page.waitForSelector('[data-test="search-results"]');

    // Verify search term is still in input
    await expect(page.locator('[data-test="search-input"]')).toHaveValue(searchTerm);
    await expect(page.locator('[data-test="search-results"]')).toBeVisible();
  });
});
