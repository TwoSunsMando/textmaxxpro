# textmaxxpro-site

Client site for **textmaxxpro.com** — TextMaxx Pro (business texting solutions).

- Single self-contained HTML file (`index.html`). CSS inline in `<head>`; JavaScript inline
  at the bottom.
- External requests: Google Fonts (`Playfair Display`, `Source Sans 3`) and the Base44
  demo-form endpoint that emails submissions to chris@leedomgroup.com, lisa@leedomgroup.com,
  and dave@textmaxxpro.com.
- **Content is read-only.** Do not modify, reformat, or "improve" the HTML.
  Treat the file as a delivered artifact from the client.
- Hosted on Coolify (`coolify.astridagent.ai`, droplet `159.203.174.128`),
  same git-push &rarr; redeploy workflow as `sde-tech.com`, `aivadealerteams.ai`, and
  `leedomgroup.com`.
- DNS is managed in the client&rsquo;s GoDaddy account (Dan is admin).
- Apex `textmaxxpro.com` is canonical; `www.` redirects to apex.

## Note on Tabler Icons

The delivered HTML uses `class="ti ti-*"` on 40 elements but does **not** include the
Tabler Icons CSS/webfont link. Per the client&rsquo;s delivery README, they offered to
inline it &mdash; check with them before shipping if the icon glyphs need to render.

## Local preview

```bash
docker build -t textmaxxpro-site .
docker run --rm -p 8086:80 textmaxxpro-site
# open http://localhost:8086/
```

## Contact / demo form

The form at the bottom of the page submits to a Base44-hosted endpoint via JavaScript.
Nothing to configure on this host. If Base44 is ever retired, the form action needs to be
re-pointed. See the source delivery README for details.
