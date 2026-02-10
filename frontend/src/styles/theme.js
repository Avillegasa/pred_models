/**
 * Cybersecurity Dashboard - Design Tokens
 * Identity: BCP Bolivia Corporate Theme (Light)
 *
 * Primary: #004B8E (BCP Blue)
 * Accent: #F26E29 (BCP Orange)
 * Navy: #32335C (Dark text)
 * Backgrounds: White and light grays
 * Text: Dark grays for readability
 */

// =============================================================================
// PRIMITIVE TOKENS (Raw palette - never use directly in components)
// =============================================================================
const primitives = {
  // Brand - BCP Bolivia Corporate
  blue: {
    700: '#32335C',  // Navy (BCP Bolivia)
    600: '#004B8E',  // Primary BCP Blue
    500: '#005BA8',  // Hover state
    400: '#0073C4',  // Light blue
    100: 'rgba(0, 75, 142, 0.08)',  // Subtle background
  },

  orange: {
    600: '#E56A00',  // Pressed state
    500: '#F26E29',  // Accent BCP Orange (BCP Bolivia)
    400: '#ef7a1d',  // Hover state (BCP Bolivia)
    100: 'rgba(242, 110, 41, 0.08)',  // Subtle background
  },

  // Neutrals - Light Theme
  gray: {
    900: '#1A1A1A',  // Darkest text
    800: '#333333',  // Primary text
    700: '#4D4D4D',  // Secondary text
    600: '#666666',  // Muted text
    500: '#808080',  // Placeholder
    400: '#ababab',  // Disabled (BCP Bolivia)
    300: '#B3B3B3',  // Borders
    200: '#DFE1E7',  // Light borders (BCP Bolivia)
    100: '#F0F0F0',  // Subtle backgrounds
    50: '#F8F9FA',   // Card backgrounds
  },

  // Semantic colors
  red: {
    600: '#C53030',  // Pressed
    500: '#E53E3E',  // Error/Danger
    400: '#FC8181',  // Light
    100: 'rgba(229, 62, 62, 0.08)',
  },
  green: {
    600: '#276749',  // Pressed
    500: '#38A169',  // Success
    400: '#68D391',  // Light
    100: 'rgba(56, 161, 105, 0.08)',
  },
  amber: {
    600: '#D69E2E',  // Pressed
    500: '#ECC94B',  // Warning
    400: '#F6E05E',  // Light
    100: 'rgba(236, 201, 75, 0.08)',
  },

  // Base
  white: '#FFFFFF',
  black: '#000000',
};

// =============================================================================
// SEMANTIC TOKENS (Use these in components)
// =============================================================================
export const tokens = {
  // -------------------------------------------------------------------------
  // BACKGROUNDS (Light theme)
  // -------------------------------------------------------------------------
  background: {
    primary: primitives.white,           // Main app background
    secondary: primitives.gray[50],      // Cards, panels
    elevated: primitives.white,          // Modals, dropdowns
    hover: primitives.gray[100],         // Hover state on surfaces

    // Interactive backgrounds
    accent: primitives.blue[100],        // Subtle accent background
    accentOrange: primitives.orange[100],
    success: primitives.green[100],
    danger: primitives.red[100],
    warning: primitives.amber[100],
  },

  // -------------------------------------------------------------------------
  // TEXT
  // -------------------------------------------------------------------------
  text: {
    primary: primitives.gray[800],       // Main text
    secondary: primitives.gray[600],     // Supporting text
    muted: primitives.gray[500],         // Disabled, hints
    inverse: primitives.white,           // Text on dark/accent backgrounds

    // Semantic text
    accent: primitives.blue[600],
    accentOrange: primitives.orange[500],
    success: primitives.green[500],
    danger: primitives.red[500],
    warning: primitives.amber[600],
  },

  // -------------------------------------------------------------------------
  // BORDERS
  // -------------------------------------------------------------------------
  border: {
    default: primitives.gray[200],       // Standard border
    subtle: primitives.gray[100],        // Very subtle
    strong: primitives.gray[300],        // Emphasized
    focus: primitives.blue[600],         // Focus rings
  },

  // -------------------------------------------------------------------------
  // INTERACTIVE (Buttons, links, controls)
  // -------------------------------------------------------------------------
  interactive: {
    primary: {
      default: primitives.blue[600],
      hover: primitives.blue[500],
      pressed: primitives.blue[700],
      text: primitives.white,
    },
    secondary: {
      default: primitives.gray[100],
      hover: primitives.gray[200],
      pressed: primitives.gray[300],
      text: primitives.gray[800],
    },
    accent: {
      default: primitives.orange[500],
      hover: primitives.orange[400],
      pressed: primitives.orange[600],
      text: primitives.white,
    },
    danger: {
      default: primitives.red[500],
      hover: primitives.red[400],
      pressed: primitives.red[600],
      text: primitives.white,
    },
  },

  // -------------------------------------------------------------------------
  // STATUS (Semantic feedback)
  // -------------------------------------------------------------------------
  status: {
    success: {
      base: primitives.green[500],
      light: primitives.green[400],
      bg: primitives.green[100],
    },
    danger: {
      base: primitives.red[500],
      light: primitives.red[400],
      bg: primitives.red[100],
    },
    warning: {
      base: primitives.amber[500],
      light: primitives.amber[400],
      bg: primitives.amber[100],
    },
    info: {
      base: primitives.blue[600],
      light: primitives.blue[400],
      bg: primitives.blue[100],
    },
  },

  // -------------------------------------------------------------------------
  // SURFACES (Cards, panels, containers)
  // -------------------------------------------------------------------------
  surface: {
    base: primitives.gray[50],           // Default card/panel
    raised: primitives.white,            // Elevated card
    overlay: 'rgba(0, 0, 0, 0.5)',        // Modal overlay
    sunken: primitives.gray[100],        // Inset areas
  },
};

// =============================================================================
// COMPONENT TOKENS (Specific UI elements)
// =============================================================================
export const components = {
  // Sidebar
  sidebar: {
    bg: primitives.blue[600],
    itemHover: primitives.blue[500],
    itemActive: primitives.orange[500],
    textActive: primitives.white,
    text: 'rgba(255, 255, 255, 0.85)',
  },

  // Cards
  card: {
    bg: tokens.surface.raised,
    border: tokens.border.subtle,
    headerBg: primitives.gray[50],
  },

  // Forms
  input: {
    bg: primitives.white,
    border: tokens.border.default,
    borderFocus: tokens.border.focus,
    placeholder: tokens.text.muted,
  },

  // Predictions (Domain-specific)
  prediction: {
    safe: {
      border: tokens.status.success.base,
      bg: tokens.status.success.bg,
      icon: tokens.status.success.base,
    },
    threat: {
      border: tokens.status.danger.base,
      bg: tokens.status.danger.bg,
      icon: tokens.status.danger.base,
    },
    warning: {
      border: tokens.status.warning.base,
      bg: tokens.status.warning.bg,
      icon: tokens.status.warning.base,
    },
  },
};

// =============================================================================
// SHADOWS
// =============================================================================
export const shadows = {
  sm: '0 1px 2px rgba(0, 0, 0, 0.05)',
  md: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
  lg: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
  xl: '0 20px 25px -5px rgba(0, 0, 0, 0.1)',
  glow: {
    primary: '0 0 20px rgba(0, 75, 142, 0.2)',
    accent: '0 0 20px rgba(242, 110, 41, 0.2)',
    danger: '0 0 20px rgba(229, 62, 62, 0.2)',
  },
};

// =============================================================================
// TYPOGRAPHY & SPACING
// =============================================================================
export const typography = {
  fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
  fontSize: {
    xs: '0.75rem',
    sm: '0.875rem',
    base: '1rem',
    lg: '1.125rem',
    xl: '1.25rem',
    '2xl': '1.5rem',
    '3xl': '2rem',
  },
  fontWeight: {
    normal: 400,
    medium: 500,
    semibold: 600,
    bold: 700,
  },
};

export const spacing = {
  xs: '0.25rem',
  sm: '0.5rem',
  md: '1rem',
  lg: '1.5rem',
  xl: '2rem',
  '2xl': '3rem',
};

export const radius = {
  sm: '0.25rem',
  md: '0.375rem',
  lg: '0.5rem',
  xl: '1rem',
  full: '9999px',
};

// =============================================================================
// LEGACY SUPPORT (For existing components)
// =============================================================================
export const theme = {
  primary: {
    dark: primitives.blue[700],
    medium: primitives.blue[600],
    light: primitives.blue[500],
    accent: primitives.orange[500],
  },
  success: {
    main: primitives.green[500],
    light: primitives.green[400],
    dark: primitives.green[600],
    bg: primitives.green[100],
  },
  danger: {
    main: primitives.red[500],
    light: primitives.red[400],
    dark: primitives.red[600],
    bg: primitives.red[100],
  },
  warning: {
    main: primitives.amber[500],
    light: primitives.amber[400],
    dark: primitives.amber[600],
    bg: primitives.amber[100],
  },
  info: {
    main: primitives.blue[600],
    light: primitives.blue[400],
    dark: primitives.blue[700],
    bg: primitives.blue[100],
  },
  text: {
    primary: primitives.gray[800],
    secondary: primitives.gray[600],
    muted: primitives.gray[500],
    inverse: primitives.white,
  },
  border: {
    light: primitives.gray[100],
    medium: primitives.gray[200],
    strong: primitives.gray[300],
  },
  bg: {
    primary: primitives.white,
    secondary: primitives.gray[50],
    tertiary: primitives.gray[100],
    overlay: 'rgba(0, 0, 0, 0.5)',
  },
  shadow: shadows,
  radius,
  spacing,
};

// =============================================================================
// HELPER FUNCTIONS
// =============================================================================
export const getThreatColor = (level) => {
  const colors = {
    safe: tokens.status.success.base,
    low: tokens.status.success.base,
    medium: tokens.status.warning.base,
    high: tokens.status.danger.base,
    critical: tokens.status.danger.base,
    legitimate: tokens.status.success.base,
    phishing: tokens.status.danger.base,
    attack: tokens.status.danger.base,
    normal: tokens.status.success.base,
  };
  return colors[level?.toLowerCase()] || tokens.text.secondary;
};

export const getPredictionBg = (label) => {
  const backgrounds = {
    legitimate: tokens.status.success.bg,
    phishing: tokens.status.danger.bg,
    attack: tokens.status.danger.bg,
    normal: tokens.status.success.bg,
    'ataque sospechoso': tokens.status.danger.bg,
    'trafico normal': tokens.status.success.bg,
    'ataque de fuerza bruta': tokens.status.danger.bg,
    'actividad normal': tokens.status.success.bg,
  };
  return backgrounds[label?.toLowerCase()] || tokens.status.info.bg;
};

export default theme;
