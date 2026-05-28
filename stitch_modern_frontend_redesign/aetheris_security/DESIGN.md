---
name: Aetheris Security
colors:
  surface: '#0b1326'
  surface-dim: '#0b1326'
  surface-bright: '#31394d'
  surface-container-lowest: '#060e20'
  surface-container-low: '#131b2e'
  surface-container: '#171f33'
  surface-container-high: '#222a3d'
  surface-container-highest: '#2d3449'
  on-surface: '#dae2fd'
  on-surface-variant: '#c4c5d9'
  inverse-surface: '#dae2fd'
  inverse-on-surface: '#283044'
  outline: '#8e90a2'
  outline-variant: '#434656'
  surface-tint: '#b8c3ff'
  primary: '#b8c3ff'
  on-primary: '#002388'
  primary-container: '#2e5bff'
  on-primary-container: '#efefff'
  inverse-primary: '#124af0'
  secondary: '#ceffdf'
  on-secondary: '#003921'
  secondary-container: '#01f5a0'
  on-secondary-container: '#006b43'
  tertiary: '#d1bcff'
  on-tertiary: '#3c0090'
  tertiary-container: '#803eff'
  on-tertiary-container: '#f5edff'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#dde1ff'
  primary-fixed-dim: '#b8c3ff'
  on-primary-fixed: '#001356'
  on-primary-fixed-variant: '#0035be'
  secondary-fixed: '#50ffaf'
  secondary-fixed-dim: '#00e293'
  on-secondary-fixed: '#002111'
  on-secondary-fixed-variant: '#005232'
  tertiary-fixed: '#e9ddff'
  tertiary-fixed-dim: '#d1bcff'
  on-tertiary-fixed: '#23005b'
  on-tertiary-fixed-variant: '#5700c9'
  background: '#0b1326'
  on-background: '#dae2fd'
  surface-variant: '#2d3449'
  glass-surface: rgba(30, 41, 59, 0.7)
  glass-border: rgba(255, 255, 255, 0.1)
  electric-blue: '#2E5BFF'
  mint-green: '#00F5A0'
  status-critical: '#FF4B4B'
  bg-deep: '#020617'
typography:
  display-lg:
    fontFamily: Hanken Grotesk
    fontSize: 48px
    fontWeight: '800'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Hanken Grotesk
    fontSize: 32px
    fontWeight: '700'
    lineHeight: '1.2'
  headline-lg-mobile:
    fontFamily: Hanken Grotesk
    fontSize: 24px
    fontWeight: '700'
    lineHeight: '1.2'
  headline-md:
    fontFamily: Hanken Grotesk
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.3'
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.5'
  label-sm:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '500'
    lineHeight: '1.4'
    letterSpacing: 0.05em
  label-xs:
    fontFamily: JetBrains Mono
    fontSize: 10px
    fontWeight: '600'
    lineHeight: '1.2'
    letterSpacing: 0.1em
rounded:
  sm: 0.5rem
  DEFAULT: 1rem
  md: 1.5rem
  lg: 2rem
  xl: 3rem
  full: 9999px
spacing:
  container-margin: 24px
  gutter: 16px
  stack-sm: 8px
  stack-md: 16px
  stack-lg: 32px
  section-gap: 48px
---

## Brand & Style

The design system embodies a **Futuristic, Secure, and Premium** persona, tailored for high-stakes environments like biometric attendance tracking. The aesthetic is rooted in **Glassmorphism** and **Modern Minimalism**, utilizing deep translucent layers to create a sense of digital depth and sophistication.

The primary theme is a refined **Dark Mode** that prioritizes visual comfort and focus. High-fidelity textures are achieved through backdrop blurs and subtle "inner glow" strokes. The interface should feel like a high-end security terminal—utilitarian yet polished—evoking confidence and technological superiority.

**Key Stylistic Principles:**
- **Translucency:** Use varying levels of backdrop-blur (12px to 24px) to separate surfaces.
- **Luminance:** Accent colors (Electric Blue and Mint) act as light sources against the dark canvas.
- **Precision:** High-contrast typography and generous whitespace ensure immediate data legibility.
- **Softness:** Extreme corner radii balance the technical nature of the system with an approachable, modern feel.

## Colors

The palette is anchored by a deep, monochromatic foundation of **Midnight Navy (#0F172A)** and **Obsidian (#020617)**. This provides a high-contrast backdrop for the vibrant functional accents.

- **Primary (Electric Blue):** Used for primary actions, active states, and biometric scanning indicators. It represents security and intelligence.
- **Secondary (Mint Green):** Reserved for "Success" states, verified identities, and "Present" status indicators. It provides a refreshing contrast to the deep blues.
- **Glass Surfaces:** Components utilize a semi-transparent fill with a subtle white stroke (10% opacity) to simulate the "frosted glass" effect.
- **Functional Accents:** A Tertiary Purple is used sparingly for administrative or secondary data insights to maintain a futuristic "neon" rhythm.

## Typography

The typography system uses a tri-font strategy to balance character and utility:
- **Hanken Grotesk** handles display and headline roles. Its sharp, contemporary geometry reinforces the futuristic brand identity.
- **Inter** is the workhorse for body copy and data descriptions, chosen for its exceptional legibility on mobile screens and neutral professional tone.
- **JetBrains Mono** is utilized for labels, IDs, and timestamps. This monospaced choice evokes a "system code" feel, emphasizing the technical precision of facial recognition.

**Usage Notes:**
- Headlines should utilize tighter letter-spacing to appear more cohesive.
- Labels and "Micro-data" (like ID numbers) should always be uppercase with slight tracking to enhance scanability.

## Layout & Spacing

This design system follows a **Fluid Grid** model designed specifically for a mobile-first experience. 

- **Grid:** A 4-column system for mobile, expanding to an 8-column layout for tablets.
- **Margins:** A standard 24px safe area on horizontal edges to ensure content doesn't feel cramped against device bezels.
- **Rhythm:** An 8px base unit drives all spacing. For glassmorphic panels, use a minimum of 24px internal padding to maintain the "airy" premium feel.
- **Reflow:** Components like "Attendance Stats" should switch from a horizontal scroll on mobile to a multi-column grid on tablet devices.

## Elevation & Depth

Hierarchy is established through **Tonal Layers** and **Backdrop Blurs** rather than traditional heavy shadows.

- **Level 0 (Base):** The deepest background layer (#020617).
- **Level 1 (Panels):** Glassmorphic surfaces with `backdrop-filter: blur(16px)` and a 1px `glass-border` stroke. 
- **Level 2 (Interactive):** Elements like buttons or active cards use a subtle "Outer Glow" (a soft shadow tinted with the primary blue color) to appear as if they are emitting light.
- **Modals/Overlays:** Highest elevation, using `blur(32px)` on the background content and a slightly higher opacity fill for the modal surface to ensure focus.

## Shapes

The design system utilizes an **Ultra-Rounded** shape language to contrast the technicality of facial recognition with a user-friendly, organic feel. 

- **Standard Elements:** Buttons, inputs, and small cards use a 24px radius (`rounded-xl`).
- **Main Containers:** Top-level glass panels and the primary video feed container use a 32px radius.
- **Pills:** Status badges (e.g., "Verified", "Late") and navigation tabs must always use a fully rounded/pill-shaped radius.
- **Inputs:** Form fields should maintain a consistent 24px radius to match primary buttons.

## Components

### Buttons
Primary buttons use a solid **Electric Blue** to **Tertiary Purple** gradient with white text. Secondary buttons use a glassmorphic style with a stroke color matching the primary blue. All buttons have a height of 56px for optimal touch targets.

### The Scanner Frame
The central component of the system. It should feature a "Scanning" animation using a horizontal Mint Green line with a soft glow. The corners of the scanner frame should be accented with thicker L-shaped brackets.

### Chips & Badges
Small, high-contrast indicators. "Present" uses a Mint Green background with black text for maximum punch. "Absent" or "Error" uses a soft red glass effect.

### Input Fields
Glassmorphic fields with a 24px radius. On focus, the border transitions from 10% white to 100% Electric Blue with a soft 8px outer glow.

### Cards
Identity cards for students/employees should feature a circular avatar on the left and JetBrains Mono labels on the right. The background of the card is a Level 1 Glass surface.

### List Items
Attendance logs should be presented in a clean, borderless list where items are separated by a 1px glass line. Each row should have a subtle hover/tap state that increases the backdrop-blur intensity.