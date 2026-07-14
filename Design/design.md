# CareerLens - UI/UX Design Specification

## 1. Design Philosophy
The primary goal of CareerLens is to provide college students with a clear, professional, and intuitive interface to understand their career trajectory. The design must feel like a premium, enterprise-grade software product rather than a generic or AI-generated tool. 

**Key Directives:**
- **Professionalism:** Clean lines, structured layouts, and data-driven visualization.
- **No Shadows:** We will rely on border colors, background contrast, and typography to create depth and hierarchy, explicitly avoiding drop shadows or shadow animations.
- **Iconography over Emojis:** All graphical representations will use scalable vector graphics (SVGs), specifically from professional icon sets (e.g., Feather Icons, Heroicons). Emojis are strictly prohibited.
- **Color Constraints:** Blue and Purple are strictly excluded from the color palette.

---

## 2. Color Palette
To maintain a professional and trustworthy environment while avoiding blue and purple, we will utilize a sophisticated Emerald and Slate color scheme. This combination feels academic, growth-oriented, and modern.

### Base Colors
- **Background (Light Mode):** `#FAFAFA` (Off-White)
- **Background (Dark Mode):** `#121212` (Deep Charcoal)
- **Surface/Card (Light Mode):** `#FFFFFF` (Pure White, separated by `#E0E0E0` borders)
- **Surface/Card (Dark Mode):** `#1E1E1E` (Dark Grey, separated by `#333333` borders)

### Primary Accent (Growth & Success)
- **Primary Emerald:** `#10B981` (Used for primary buttons, active states, progress bars)
- **Emerald Hover:** `#059669`
- **Emerald Light (Backgrounds):** `#D1FAE5`

### Secondary Accent (Alerts & Highlights)
- **Warning/Gap Indicator:** `#F59E0B` (Amber - used for highlighting skill gaps)
- **Danger/Low Probability:** `#EF4444` (Red)

### Typography Colors
- **Primary Text:** `#1F2937` (Dark Mode: `#F9FAFB`)
- **Secondary Text (Muted):** `#6B7280` (Dark Mode: `#9CA3AF`)

---

## 3. Typography
A modern, highly readable sans-serif typeface is required for a professional software look.

- **Primary Font Family:** `Inter` or `Roboto`
- **Headings (H1-H3):** Font-weight 600 or 700. Clean, tight tracking.
- **Body Text:** Font-weight 400. Size 14px or 16px for optimal readability.
- **Data/Numbers:** Use tabular numerals for aligning statistics in the dashboard.

---

## 4. Structural Layout

The application will follow a classic dashboard architecture, prioritizing ease of navigation and quick access to core functionalities.

### 4.1 Global Navigation
- **Sidebar (Left):** Collapsible vertical navigation containing links to:
  - Dashboard (Overview)
  - Placement Prediction
  - Skill Gap Analyzer
  - Roadmap Generation
  - Profile Settings
- **Top Header:** Contains breadcrumbs, page title, user profile thumbnail, and a theme toggle (Light/Dark mode).

### 4.2 Page Structure
- **Container Width:** Max-width of 1440px to ensure the UI does not stretch excessively on large monitors.
- **Grid System:** 12-column responsive grid layout. 
- **Card-Based UI:** Information is chunked into distinct containers (cards). Since shadows are prohibited, cards will be defined by a solid `1px` border (e.g., `border: 1px solid #E5E7EB`) and a slight background color variance.

---

## 5. Core Feature UI Specifications

### 5.1 Dashboard (Overview)
- **Greeting & Summary:** A clean header welcoming the user, displaying their current academic standing (CGPA, Branch).
- **Quick Metrics Cards:** 3 adjacent cards showing:
  - Current Placement Probability (Large typography, circular progress SVG).
  - Number of identified Skill Gaps.
  - Next milestone in the Roadmap.

### 5.2 Placement Prediction Module
- **Input Form:** A structured, multi-step form or a clean grid layout for entering parameters (DSA score, Internships, Projects, etc.).
  - Input fields will have sharp corners (2px or 4px border-radius) and clear borders.
- **Result Visualization:** 
  - A prominent gauge chart (SVG based) showing the probability percentage.
  - A breakdown of factors positively and negatively affecting the score, using horizontal bar charts (Emerald for positive, Amber for negative).

### 5.3 Skill Gap Analyzer
- **Comparison View:** A side-by-side or radar chart layout comparing "Current Student Skills" vs "Industry Requirements".
- **Gap List:** A data table listing specific missing skills.
  - Columns: Skill Name, Importance Level, Current Proficiency, Required Proficiency.
  - Use colored tags (e.g., solid background with text) for "High", "Medium", "Low" importance.

### 5.4 Roadmap Generation
- **Timeline UI:** A vertical or horizontal step-by-step timeline graph.
  - Nodes represent milestones (e.g., "Learn Advanced Python", "Complete 2 ML Projects").
  - Connecting lines indicate progression.
  - Active/Completed nodes are filled with Primary Emerald. Future nodes are outlined.
- **Actionable Steps:** Clicking a node expands a bordered panel containing detailed steps, resources, and time estimations.

---

## 6. Interaction & Animation Guidelines
To maintain a snappy and professional feel, animations should be subtle and functional. **No shadow-based animations (e.g., hovering to increase drop-shadow) are allowed.**

- **Hover States:** 
  - Buttons: Background color darkens slightly, or border color changes.
  - Cards/Rows: Background color shifts from `#FFFFFF` to `#F9FAFB` (light mode) or border color turns to Primary Emerald.
- **Transitions:** 
  - Use short durations (e.g., `150ms ease-in-out`) for color and background changes.
- **Loading States:** 
  - Prefer skeleton loaders (flat, pulsing background rectangles) over generic spinning icons to keep the interface looking customized and high-end.

---

## 7. Iconography Assets
All icons must be SVGs. Examples of mappings using Feather Icons:
- **Dashboard:** `<polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>` (Activity)
- **Skill Gap:** `<path d="M12 20v-6M6 20V10M18 20V4"></path>` (Bar Chart)
- **Prediction:** `<circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline>` (Clock/Future)
- **Roadmap:** `<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle>` (Map Pin)
