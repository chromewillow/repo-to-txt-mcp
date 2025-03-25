#!/usr/bin/env node

const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

// Parse config
let config = {};
if (process.argv.length > 2) {
  try {
    const configArg = process.argv.find(arg => arg.startsWith('--config='));
    if (configArg) {
      const configStr = configArg.split('=')[1];
      config = JSON.parse(configStr);
    }
  } catch (error) {
    console.error('Error parsing config:', error);
  }
}

// Default port
const port = config.port || process.env.PORT || 8000;

// Find the Python executable
function findPythonExecutable() {
  const possibleExecutables = ['python3', 'python', 'py'];
  
  for (const executable of possibleExecutables) {
    try {
      const result = spawn(executable, ['-c', 'print("Python found")']);
      return executable;
    } catch (error) {
      // Continue to the next possible executable
    }
  }
  
  throw new Error('Python executable not found. Make sure Python is installed and available in PATH.');
}

// Start the Python server
function startPythonServer() {
  const pythonExecutable = findPythonExecutable();
  const serverPath = path.join(__dirname, 'server.py');
  
  // Check if server.py exists
  if (!fs.existsSync(serverPath)) {
    console.error(`server.py not found at ${serverPath}`);
    process.exit(1);
  }
  
  console.log(`Starting repo-to-txt MCP server on port ${port}...`);
  
  // Set environment variables for Python process
  const env = { ...process.env, PORT: port.toString() };
  
  const pythonProcess = spawn(pythonExecutable, [serverPath], { env });
  
  pythonProcess.stdout.on('data', (data) => {
    console.log(`[Python] ${data.toString().trim()}`);
  });
  
  pythonProcess.stderr.on('data', (data) => {
    console.error(`[Python Error] ${data.toString().trim()}`);
  });
  
  pythonProcess.on('close', (code) => {
    console.log(`Python process exited with code ${code}`);
    process.exit(code);
  });
  
  // Handle Node.js process termination
  process.on('SIGINT', () => {
    console.log('Received SIGINT. Shutting down Python server...');
    pythonProcess.kill('SIGINT');
  });
  
  process.on('SIGTERM', () => {
    console.log('Received SIGTERM. Shutting down Python server...');
    pythonProcess.kill('SIGTERM');
  });
}

// Start the server
startPythonServer();