# BSidesFrankfurt Design System - Color Palette

This document contains the official color palette for the BSidesFrankfurt website redesign.

## Core Brand Colors

| Color | Name | HEX | Usage |
| :--- | :--- | :--- | :--- |
| <div style="background-color: #9acd32; width: 50px; height: 50px; border: 1px solid #ccc;"></div> | **Yellowgreen** | `#9acd32` | **Primary Brand Color**. Used for buttons, active states, links, borders, and key highlights. |
| <div style="background-color: #eb3812; width: 50px; height: 50px; border: 1px solid #ccc;"></div> | **Reddish Orange** | `#eb3812` | **Secondary Brand Color**. Used for hover states, alerts, and accent details. |

## Backgrounds & Surfaces

| Color | Name | HEX | Usage |
| :--- | :--- | :--- | :--- |
| <div style="background-color: #011023; width: 50px; height: 50px; border: 1px solid #ccc;"></div> | **Dark Blue** | `#011023` | **Main Background**. Used for the body background and primary canvas. |
| <div style="background-color: #121314; width: 50px; height: 50px; border: 1px solid #ccc;"></div> | **Dark Grey** | `#121314` | **Surface Color**. Used for cards, modals, and content containers. |

## Typography

| Color | Name | HEX | Usage |
| :--- | :--- | :--- | :--- |
| <div style="background-color: #ffffff; width: 50px; height: 50px; border: 1px solid #ccc;"></div> | **White** | `#ffffff` | **Primary Text**. Headings, body text, and icons. |
| <div style="background-color: #b3b3b3; width: 50px; height: 50px; border: 1px solid #ccc;"></div> | **Muted Text** | `rgba(255, 255, 255, 0.7)` | **Secondary Text**. Metadata, footers, and less important information. |

## CSS Variables
These colors are defined in `css/style.css`:

```css
:root {
  --color-bg: #011023;        /* Dark Blue */
  --color-surface: #121314;   /* Dark Grey */
  --color-primary: #9acd32;   /* Yellowgreen */
  --color-secondary: #eb3812; /* Reddish Orange */
  --color-text: #ffffff;
}
```
