# Design QA

Source: `/Users/andyduan26/Downloads/www.youku.com_ku_webmovie (1).png`
Prototype: `http://127.0.0.1:5174/`
Viewport: 1290 x 900

Checks completed:
- Left navigation rail resized to match screenshot density and prevent label clipping.
- Top search and user controls aligned to the movie channel header position.
- Hero title, metadata, body copy, play button, background image, and poster strip aligned to screenshot coordinates.
- Poster cards use extracted image assets from `src/assets/youku`; no base64 or data URI assets remain in source.
- Movie rows reproduce the screenshot section sequence, dark background, 6-card horizontal density, VIP/score badges, reservation buttons, and trailer row sizing.

Known follow-up polish:
- Some individual posters differ from the exact live Youku screenshot where the extracted baseline did not include the same source poster.
- Small icon glyphs use the available extracted icon assets and text fallbacks rather than Youku's private icon font.

Final result: passed
