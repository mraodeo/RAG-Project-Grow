---
name: Obsidian Flow
colors:
  surface: '#051424'
  surface-dim: '#051424'
  surface-bright: '#2c3a4c'
  surface-container-lowest: '#010f1f'
  surface-container-low: '#0d1c2d'
  surface-container: '#122131'
  surface-container-high: '#1c2b3c'
  surface-container-highest: '#273647'
  on-surface: '#d4e4fa'
  on-surface-variant: '#bac9cc'
  inverse-surface: '#d4e4fa'
  inverse-on-surface: '#233143'
  outline: '#849396'
  outline-variant: '#3b494c'
  surface-tint: '#00daf3'
  primary: '#c3f5ff'
  on-primary: '#00363d'
  primary-container: '#00e5ff'
  on-primary-container: '#00626e'
  inverse-primary: '#006875'
  secondary: '#bcc7de'
  on-secondary: '#263143'
  secondary-container: '#3e495d'
  on-secondary-container: '#aeb9d0'
  tertiary: '#e8ecff'
  on-tertiary: '#283044'
  tertiary-container: '#c8d0ea'
  on-tertiary-container: '#51596f'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#9cf0ff'
  primary-fixed-dim: '#00daf3'
  on-primary-fixed: '#001f24'
  on-primary-fixed-variant: '#004f58'
  secondary-fixed: '#d8e3fb'
  secondary-fixed-dim: '#bcc7de'
  on-secondary-fixed: '#111c2d'
  on-secondary-fixed-variant: '#3c475a'
  tertiary-fixed: '#dae2fd'
  tertiary-fixed-dim: '#bec6e0'
  on-tertiary-fixed: '#131b2e'
  on-tertiary-fixed-variant: '#3f465c'
  background: '#051424'
  on-background: '#d4e4fa'
  surface-variant: '#273647'
typography:
  headline-xl:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-md:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.05em
  mono-data:
    fontFamily: jetbrainsMono
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 4px
  gutter: 24px
  margin-mobile: 16px
  margin-desktop: 48px
  container-max: 1280px
---

## Brand & Style

The design system is engineered for a premium financial AI environment, prioritizing trust, precision, and futuristic sophistication. The aesthetic leans heavily into **Glassmorphism**, utilizing layered translucency to create a sense of depth without clutter. 

The personality is "High-Tech Concierge"—calm, authoritative, and ultra-modern. By mixing deep monochromatic foundations with vibrant technical accents, the UI feels like a precision instrument. Visual interest is maintained through subtle mesh gradients that simulate light refracting through dark glass, ensuring the dark mode feels expansive rather than oppressive.

## Colors

The palette is rooted in **Deep Slate** and **Navy** to provide a stable, institutional foundation. 
- **Primary (Cyan/Blue):** Used exclusively for interactive states, progress indicators, and AI-driven insights. It should glow against the dark backgrounds.
- **Surface Foundations:** Backgrounds use a tiered navy approach (`#020617` for base, `#0F172A` for containers) to maintain a logical hierarchy.
- **Accents:** High-fidelity gradients transition from a deep Cobalt to the primary Cyan to represent "active thought" or data processing.
- **System States:** Warning banners use a high-saturation Gold (`#F59E0B`) to contrast against the cool-toned UI, ensuring critical financial alerts are never missed.

## Typography

This design system utilizes **Inter** for all standard UI elements to ensure maximum legibility and a systematic, clean appearance. 
- **Headlines:** Use tight letter spacing and heavier weights to command authority.
- **Data Display:** For financial figures, account numbers, and tickers, use **JetBrains Mono** to ensure tabular alignment and a technical feel.
- **Hierarchical Contrast:** Labels use uppercase styling with increased tracking to differentiate "metadata" from interactive content.

## Layout & Spacing

The system follows a **12-column fluid grid** for desktop and a **4-column grid** for mobile. 
- **Rhythm:** An 8px linear scale is used for component spacing, while a 4px scale is reserved for tight internal element padding (e.g., icons inside buttons).
- **Margins:** Generous page margins (48px+) are required on desktop to maintain the "premium" airy feel.
- **Chat Interface:** The primary AI interaction area is center-aligned with a max-width of 800px to prevent long line lengths and improve readability of financial data.

## Elevation & Depth

Depth is communicated through **Backdrop Blurs** and **Inner Glows** rather than heavy drop shadows.
- **Surface 0 (Base):** Solid `#020617`.
- **Surface 1 (Floating Cards):** Semi-transparent Navy (`rgba(30, 41, 59, 0.7)`) with a 20px backdrop blur and a 1px border of `rgba(255, 255, 255, 0.1)`.
- **Surface 2 (Active/Modals):** Lighter transparency with a primary-tinted outer glow (Cyan, 10% opacity) to signify focus.
- **Edge Treatment:** All "glass" elements must feature a top-down white-to-transparent linear gradient border (0.5px width) to simulate a light-catching glass edge.

## Shapes

The shape language is refined and consistent, using a **Rounded (0.5rem)** base. 
- **Standard Components:** Buttons, inputs, and small cards use the `rounded` (8px) token.
- **Container Elements:** Large glass panels and chat bubble groupings use `rounded-xl` (24px) to soften the technical edge.
- **Interactive Indicators:** Small pills (chips) use `rounded-full` to distinguish them from structural elements.

## Components

- **Glass Chat Bubbles:** AI responses use the "Surface 1" glass treatment. User messages are simplified with a dark slate background to keep the focus on the AI's data.
- **Action Buttons:** Primary buttons are solid Cyan with black text for maximum contrast. Secondary buttons use the "Ghost" style—transparent with a 1px Cyan border.
- **Input Fields:** Search and prompt bars use a 20px backdrop blur, anchored at the bottom of the screen with a subtle "mesh gradient" glow behind them when active.
- **Warning Banners:** Critical financial alerts use a solid Gold background with black text, positioned at the top of the viewport or container, breaking the glass aesthetic to demand immediate attention.
- **Data Visualizations:** Charts should use the primary Cyan for growth/positive data and a muted Slate for historical/baseline data. Avoid standard red/green unless specifically indicating a catastrophic loss.