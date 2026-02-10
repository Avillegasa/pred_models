/**
 * Test Data
 * Sample data for testing each prediction model
 */

// Phishing Test Cases
export const phishingTestCases = [
  {
    name: 'Ataque de Phishing Obvio',
    data: {
      sender: 'urgent-verify@suspicious-bank.com',
      receiver: 'user@company.com',
      subject: 'URGENTE: Verifique su cuenta AHORA!!!',
      body: 'Su cuenta sera suspendida en 24 horas. Haga clic aqui inmediatamente para verificar: http://fake-bank-verify.com/login',
      urls: 1
    },
    expectedPrediction: 1,
    description: 'Email de phishing clasico con urgencia, dominio sospechoso y enlace malicioso'
  },
  {
    name: 'Email Empresarial Legitimo',
    data: {
      sender: 'rrhh@company.com',
      receiver: 'empleado@company.com',
      subject: 'Reunion de Equipo - Viernes 2PM',
      body: 'Hola equipo, recordatorio sobre nuestra reunion semanal este viernes a las 2PM en la Sala de Conferencias B. Por favor revisen la agenda adjunta.',
      urls: 0
    },
    expectedPrediction: 0,
    description: 'Comunicacion empresarial interna normal'
  },
  {
    name: 'Estafa del Principe Nigeriano',
    data: {
      sender: 'prince@nigeria.ng',
      receiver: 'victima@example.com',
      subject: 'Propuesta de Negocio Urgente',
      body: 'Estimado/a, Soy Principe de Nigeria y necesito su ayuda para transferir $10 millones. Recibira 20% de comision. Contacteme urgentemente.',
      urls: 0
    },
    expectedPrediction: 1,
    description: 'Email clasico de estafa de pago anticipado'
  }
];

// Network Attack Test Cases
export const networkAttackTestCases = [
  {
    name: 'Ataque de Escaneo de Puertos',
    data: {
      sourceIp: '203.0.113.5',
      port: 8888,
      protocol: 'TCP',
      packetCount: 2500,
      timestamp: new Date().toISOString().slice(0, 16),
      payload: ''
    },
    expectedPrediction: 1,
    description: 'Alto conteo de paquetes a puerto poco comun indica escaneo de puertos'
  },
  {
    name: 'Trafico HTTPS Normal',
    data: {
      sourceIp: '192.168.1.50',
      port: 443,
      protocol: 'HTTPS',
      packetCount: 150,
      timestamp: new Date().toISOString().slice(0, 16),
      payload: ''
    },
    expectedPrediction: 0,
    description: 'Trafico normal de navegacion web'
  },
  {
    name: 'Ataque de Inundacion ICMP',
    data: {
      sourceIp: '198.51.100.100',
      port: 0,
      protocol: 'ICMP',
      packetCount: 5000,
      timestamp: new Date().toISOString().slice(0, 16),
      payload: ''
    },
    expectedPrediction: 1,
    description: 'Alto conteo de paquetes ICMP indica ataque de inundacion'
  },
  {
    name: 'Conexion SSH',
    data: {
      sourceIp: '192.168.1.100',
      port: 22,
      protocol: 'TCP',
      packetCount: 50,
      timestamp: new Date().toISOString().slice(0, 16),
      payload: ''
    },
    expectedPrediction: 0,
    description: 'Intento de conexion SSH normal'
  }
];

// Brute Force Test Cases
export const bruteForceTestCases = [
  {
    name: 'Ataque de Fuerza Bruta Obvio',
    data: {
      username: 'root',
      sourceIp: '198.51.100.23',
      failedAttempts: 45,
      timeWindow: 3,
      loginMethod: 'SSH',
      lastSuccessful: ''
    },
    expectedPrediction: 1,
    description: 'Fuerza bruta SSH de alta velocidad en cuenta root'
  },
  {
    name: 'Fallo de Login Normal',
    data: {
      username: 'juan.perez',
      sourceIp: '192.168.1.100',
      failedAttempts: 2,
      timeWindow: 120,
      loginMethod: 'HTTP',
      lastSuccessful: new Date(Date.now() - 86400000).toISOString().slice(0, 16)
    },
    expectedPrediction: 0,
    description: 'Error de tipeo del usuario - actividad normal'
  },
  {
    name: 'Fuerza Bruta FTP',
    data: {
      username: 'admin',
      sourceIp: '203.0.113.77',
      failedAttempts: 25,
      timeWindow: 5,
      loginMethod: 'FTP',
      lastSuccessful: ''
    },
    expectedPrediction: 1,
    description: 'Intentos rapidos de login FTP en cuenta admin'
  },
  {
    name: 'Contrasena Olvidada',
    data: {
      username: 'maria.garcia',
      sourceIp: '192.168.1.55',
      failedAttempts: 5,
      timeWindow: 30,
      loginMethod: 'HTTP',
      lastSuccessful: new Date(Date.now() - 172800000).toISOString().slice(0, 16)
    },
    expectedPrediction: 0,
    description: 'Usuario intentando recordar contrasena - bajo riesgo'
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
