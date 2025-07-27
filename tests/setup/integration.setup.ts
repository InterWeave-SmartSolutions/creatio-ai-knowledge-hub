import { TestClient } from '@fastapi/testclient';
import { spawn, ChildProcess } from 'child_process';
import path from 'path';
import fs from 'fs/promises';

// Global test environment setup for integration tests
process.env.NODE_ENV = 'test';
process.env.DATABASE_URL = process.env.TEST_DATABASE_URL || 'sqlite:///test_integration.db';
process.env.REDIS_URL = process.env.TEST_REDIS_URL || 'redis://localhost:6379/1';

let testServer: ChildProcess | null = null;

// Setup test database
export async function setupTestDatabase(): Promise<void> {
  const dbPath = path.resolve(__dirname, '../../test_integration.db');
  
  try {
    await fs.unlink(dbPath);
  } catch (error) {
    // Database doesn't exist, continue
  }
  
  // Run database migrations
  const migrationProcess = spawn('python', ['-m', 'alembic', 'upgrade', 'head'], {
    env: { ...process.env, DATABASE_URL: process.env.DATABASE_URL },
    stdio: 'inherit',
  });
  
  await new Promise((resolve, reject) => {
    migrationProcess.on('close', (code) => {
      if (code === 0) {
        resolve(void 0);
      } else {
        reject(new Error(`Migration failed with code ${code}`));
      }
    });
  });
}

// Start test server
export async function startTestServer(): Promise<void> {
  testServer = spawn('python', ['-m', 'uvicorn', 'ai_knowledge_hub.enhanced_mcp_server:app', '--port', '8001'], {
    env: process.env,
    stdio: 'pipe',
  });
  
  // Wait for server to start
  await new Promise((resolve) => {
    setTimeout(resolve, 3000);
  });
}

// Stop test server
export async function stopTestServer(): Promise<void> {
  if (testServer) {
    testServer.kill('SIGTERM');
    testServer = null;
  }
}

// Global setup
beforeAll(async () => {
  await setupTestDatabase();
  await startTestServer();
}, 30000);

// Global teardown
afterAll(async () => {
  await stopTestServer();
}, 10000);

// Increase timeout for integration tests
jest.setTimeout(30000);
