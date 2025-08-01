import 'jest-extended';
import { TextEncoder, TextDecoder } from 'util';

// Global test environment setup
Object.assign(global, { TextDecoder, TextEncoder });

// Mock environment variables
process.env.NODE_ENV = 'test';
process.env.DATABASE_URL = 'sqlite://memory';
process.env.REDIS_URL = 'redis://localhost:6379';

// Mock console methods in tests
global.console = {
  ...console,
  log: jest.fn(),
  debug: jest.fn(),
  info: jest.fn(),
  warn: jest.fn(),
  error: jest.fn(),
};

// Setup global test utilities
global.beforeEach(() => {
  jest.clearAllMocks();
});

// Mock external services
jest.mock('redis', () => ({
  createClient: jest.fn(() => ({
    connect: jest.fn(),
    disconnect: jest.fn(),
    get: jest.fn(),
    set: jest.fn(),
    del: jest.fn(),
  })),
}));

jest.mock('axios', () => ({
  default: {
    get: jest.fn(),
    post: jest.fn(),
    put: jest.fn(),
    delete: jest.fn(),
  },
  get: jest.fn(),
  post: jest.fn(),
  put: jest.fn(),
  delete: jest.fn(),
}));

// Increase test timeout for unit tests
jest.setTimeout(10000);
