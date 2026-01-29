/**
 * Test Data
 * Sample data for testing each prediction model
 */

// Phishing Test Cases
export const phishingTestCases = [
  {
    name: 'Obvious Phishing Attack',
    data: {
      sender: 'urgent-verify@suspicious-bank.com',
      receiver: 'user@company.com',
      subject: 'URGENT: Verify your account NOW!!!',
      body: 'Your account will be suspended in 24 hours. Click here immediately to verify: http://fake-bank-verify.com/login',
      urls: 1
    },
    expectedPrediction: 1,
    description: 'Classic phishing email with urgency, suspicious domain, and malicious link'
  },
  {
    name: 'Legitimate Business Email',
    data: {
      sender: 'hr@company.com',
      receiver: 'employee@company.com',
      subject: 'Team Meeting - Friday 2PM',
      body: 'Hi team, reminder about our weekly sync meeting this Friday at 2PM in Conference Room B. Please review the attached agenda.',
      urls: 0
    },
    expectedPrediction: 0,
    description: 'Normal internal business communication'
  },
  {
    name: 'Nigerian Prince Scam',
    data: {
      sender: 'prince@nigeria.ng',
      receiver: 'victim@example.com',
      subject: 'Urgent Business Proposal',
      body: 'Dear Sir/Madam, I am Prince of Nigeria and I need your help to transfer $10 million. You will receive 20% commission. Contact me urgently.',
      urls: 0
    },
    expectedPrediction: 1,
    description: 'Classic advance-fee scam email'
  }
];

// Network Attack Test Cases
export const networkAttackTestCases = [
  {
    name: 'Port Scanning Attack',
    data: {
      sourceIp: '203.0.113.5',
      port: 8888,
      protocol: 'TCP',
      packetCount: 2500,
      timestamp: new Date().toISOString().slice(0, 16),
      payload: ''
    },
    expectedPrediction: 1,
    description: 'High packet count to uncommon port indicates port scanning'
  },
  {
    name: 'Normal HTTPS Traffic',
    data: {
      sourceIp: '192.168.1.50',
      port: 443,
      protocol: 'HTTPS',
      packetCount: 150,
      timestamp: new Date().toISOString().slice(0, 16),
      payload: ''
    },
    expectedPrediction: 0,
    description: 'Normal web browsing traffic'
  },
  {
    name: 'ICMP Flood Attack',
    data: {
      sourceIp: '198.51.100.100',
      port: 0,
      protocol: 'ICMP',
      packetCount: 5000,
      timestamp: new Date().toISOString().slice(0, 16),
      payload: ''
    },
    expectedPrediction: 1,
    description: 'High ICMP packet count indicates flood attack'
  },
  {
    name: 'SSH Connection',
    data: {
      sourceIp: '192.168.1.100',
      port: 22,
      protocol: 'TCP',
      packetCount: 50,
      timestamp: new Date().toISOString().slice(0, 16),
      payload: ''
    },
    expectedPrediction: 0,
    description: 'Normal SSH connection attempt'
  }
];

// Brute Force Test Cases
export const bruteForceTestCases = [
  {
    name: 'Obvious Brute Force Attack',
    data: {
      username: 'root',
      sourceIp: '198.51.100.23',
      failedAttempts: 45,
      timeWindow: 3,
      loginMethod: 'SSH',
      lastSuccessful: ''
    },
    expectedPrediction: 1,
    description: 'High velocity SSH brute force on root account'
  },
  {
    name: 'Normal Failed Login',
    data: {
      username: 'john.doe',
      sourceIp: '192.168.1.100',
      failedAttempts: 2,
      timeWindow: 120,
      loginMethod: 'HTTP',
      lastSuccessful: new Date(Date.now() - 86400000).toISOString().slice(0, 16)
    },
    expectedPrediction: 0,
    description: 'User typo - normal activity'
  },
  {
    name: 'FTP Brute Force',
    data: {
      username: 'admin',
      sourceIp: '203.0.113.77',
      failedAttempts: 25,
      timeWindow: 5,
      loginMethod: 'FTP',
      lastSuccessful: ''
    },
    expectedPrediction: 1,
    description: 'Rapid FTP login attempts on admin account'
  },
  {
    name: 'Forgotten Password',
    data: {
      username: 'alice.smith',
      sourceIp: '192.168.1.55',
      failedAttempts: 5,
      timeWindow: 30,
      loginMethod: 'HTTP',
      lastSuccessful: new Date(Date.now() - 172800000).toISOString().slice(0, 16)
    },
    expectedPrediction: 0,
    description: 'User trying to remember password - low risk'
  }
];

// Helper function to get test cases by model type
export const getTestCasesByModel = (modelType) => {
  const testCases = {
    phishing: phishingTestCases,
    ataques_sospechosos: networkAttackTestCases,
    fuerza_bruta: bruteForceTestCases
  };

  return testCases[modelType] || [];
};

// Helper function to get all test cases
export const getAllTestCases = () => {
  return {
    phishing: phishingTestCases,
    ataques_sospechosos: networkAttackTestCases,
    fuerza_bruta: bruteForceTestCases
  };
};

export default {
  phishingTestCases,
  networkAttackTestCases,
  bruteForceTestCases,
  getTestCasesByModel,
  getAllTestCases
};
