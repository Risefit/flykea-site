# KEA — flykea.com (static rebuild)

A clean, fast, static rebuild of flykea.com for Kampala Executive Aviation.
No build step, no framework, no database — just HTML/CSS/JS that deploys anywhere.

## What's inside
- `index.html` — home
- `solutions/` — 6 solution pages
- `fleet.html`, `about.html`, `careers.html`, `contact.html`
- `news.html` + `news/` — news index and 18 article pages
- `404.html`
- `assets/styles.css`, `assets/main.js` — shared source styles/scripts
- `build.py` — the generator (optional; see "Editing" below)

## Deploy to Vercel (2 minutes)
**Easiest:** go to vercel.com → Add New → Project → drag this whole folder onto the page. Done.
**Or via Git:** push this folder to a GitHub repo and import it in Vercel. No framework preset needed ("Other" / static). No build command, output dir = root.
The site is plain static files, so it also works on Netlify, Cloudflare Pages, or any web host.

## One thing to do before go-live
**Activate the forms (60 seconds, no signup/API key).** The Contact and Careers forms post to **FormSubmit**, which emails submissions to `reservations@flykea.com` and supports CV file uploads — no account or key required. FormSubmit just needs a one-time confirmation:
   - Deploy the site, open the Contact page, and send one test message.
   - The first time, FormSubmit emails `reservations@flykea.com` an activation link. Click it once. From then on, every submission is delivered to that inbox.
   - To change the destination address, edit `FORM_EMAIL` at the top of `build.py` and run `python3 build.py`.

How the forms behave: the **Contact** form submits via AJAX and shows an inline "thank you" without leaving the page. The **Careers** form (which carries a CV file upload) submits normally and lands the visitor on `thank-you.html`. Both include a hidden honeypot field for spam protection.

**Images are baked in.** Every image, the banner video, and the safety-policy PDF live in `assets/img/` — the site has no dependency on the old flykea.com server.

## Editing
You can edit in **two** ways — pick whichever you prefer:
- **Directly:** open any `.html` file and edit the text. Styles live in the `<style>` block of each page (and mirrored in `assets/styles.css`).
- **Via the generator:** edit content in `build.py` (news articles, fleet specs, copy) and/or `assets/styles.css`, then run `python3 build.py` to regenerate every page consistently. This keeps the shared header/footer/design in one place.

## Brand
- Green `#90B820`, logo grey `#585858` (sampled from the KEA logo).
- Fonts: Sora (headings), Inter (body), IBM Plex Mono (data labels).

## Notes
- The homepage banner video and all imagery are KEA's own assets.
- The old WordPress admin/plugins are not part of this build (static sites have no backend); the forms above replace the contact/CV plugins.

## Bake images locally (one command)
If you'd rather make the site fully self-contained yourself (no dependency on flykea.com),
unzip the project, open a terminal in this folder and run:

    python3 bake-images.py

It downloads every image/video/PDF into `assets/img/`, rewrites all paths to point at the
local copies, and keeps `build.py` in sync. Needs only Python 3. After it finishes, deploy
the folder as usual. (This runs on your machine, so it isn't affected by any sandbox network limits.)
