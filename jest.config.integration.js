module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  displayName: 'Integration Tests',
  testMatch: ['**/tests/integration/**/*.test.(ts|js)'],
  setupFilesAfterEnv: ['<rootDir>/tests/setup/integration.setup.ts'],
  testTimeout: 30000,
  maxWorkers: 2, // Limited parallelism for integration tests
  verbose: true,
  collectCoverage: false, // Coverage handled separately
  globalSetup: '<rootDir>/tests/setup/global.setup.ts',
  globalTeardown: '<rootDir>/tests/setup/global.teardown.ts',
};
