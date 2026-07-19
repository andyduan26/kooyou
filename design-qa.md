# Design QA

## Home Page

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

## Play Page

Source: `/Users/andyduan26/Downloads/v.youku.com_v_show_id_XNjU0OTEwMDE0MA==.html_spm=a2hkl.14919748_WEBCULTURE_JINGXUAN.drawer2.d_zj1_4&s=fadcbc4d3d9545088ea9&scm=20140719.manual.48465.show_fadcbc4d3d9545088ea9.png`
Prototype: `http://127.0.0.1:5174/play/1`
Viewport: 1290 x 900

Checks completed:
- Playback page switches to the screenshot's horizontal top bar instead of the movie-channel left rail.
- Member-only player container aligns to the reference at approximately `54,84,720x400`.
- Right content rail aligns to the reference at approximately `798,84`, with tabs, title, metadata, actions, member upsell card, episodes, and surrounding-video stack.
- Recommendation poster wall uses the screenshot's three-column poster density and dark Youku spacing.
- Footer information block reproduces the long dark Youku legal/service area.
- No base64 or data URI assets remain in frontend source.

Known follow-up polish:
- Individual poster imagery uses the extracted local asset pool, so some titles do not match the exact live screenshot posters.
- Topbar and action icons use text/icon fallbacks where Youku's private icon font is not available.

Final result: passed
