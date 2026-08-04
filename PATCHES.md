# TextMaxx production patches

The client keeps delivering `textmaxxpro_index.html` without two things we need in
production. Rather than hand-editing every delivery (three rounds so far), we apply
them with a script.

## The two patches

1. **Tabler Icons `<link>` in `<head>`.** The client's HTML uses 40 `ti ti-*` icon
   classes but doesn't link the Tabler webfont. Without it, every icon renders as
   a blank rectangle. Delivery README line 15 has been saying "let us know and we'll
   inline the icon font reference" since May 2026 — hasn't happened.
2. **Phone field on the Request Demo form + `phone:` in the JS payload.** Added
   2026-07-07 per Chris and Dave (Head of Sales). Every delivery since then has
   dropped it.

Both patches are encoded verbatim (as string literals) in `apply-patches.py`. If
you ever need to tweak the styling or the payload, edit those constants at the top
of the script — don't hand-edit `index.html`.

## Delivery workflow

Whenever the client sends a new HTML file:

```bash
cd ~/projects/textmaxxpro-site

# 1. Back up the current live copy (belt and suspenders).
mkdir -p ../site-backups/$(date +%F)/textmaxxpro-site
cp index.html ../site-backups/$(date +%F)/textmaxxpro-site/

# 2. Drop the new delivery in.
cp "/path/to/client's/textmaxxpro_index.html" index.html

# 3. Apply the patches.
python3 apply-patches.py

# 4. Sanity check (should say '1' for each).
grep -c "tabler-icons.min.css" index.html
grep -c 'id="tf-phone"' index.html
grep -c "phone: document.getElementById" index.html

# 5. Ship it.
git add index.html
git commit -m "Content update: <date> client delivery + re-apply patches"
git push
# then Redeploy in Coolify if the webhook still isn't firing
```

## Script behavior

- **Idempotent.** If a patch is already present, it's skipped. Running the script
  twice produces the same result as running it once.
- **Fails loud** if the client's HTML template shifts and the expected anchor
  patterns aren't found. Non-zero exit + stderr message telling you which patch
  couldn't apply. That's the signal to look at the file by hand and possibly
  update the anchors in the script.
- **In-place edit.** Overwrites the target file.

Anchors used:

| Patch | Anchor text |
|---|---|
| Tabler `<link>` | The full Google Fonts stylesheet `<link>` line |
| Phone `<div>` | The Company `<input>` line (the whole tag with all its inline styles) |
| Phone payload | The line `company: document.getElementById('tf-company').value,` |

## When to update the script instead of the HTML

- Client changes the form styling → update the inline styles inside `PHONE_BLOCK`
  in `apply-patches.py`, not `index.html`. That way the next delivery still
  produces a form that matches.
- Client renames the endpoint or JSON schema → update `PHONE_PAYLOAD_LINE`.
- Client adds Tabler themselves → the script's `[skip]` message will confirm no
  work needed. Delete the patch from the script if you want it retired.
- Client's form structure changes (e.g. different field order, new outer wrapper)
  → the script will fail loud with an "anchor pattern not found" message. Read
  the failing anchor, look at the new file, update `apply-patches.py` accordingly.

## Rollback

Every delivery's pre-patch state is captured under
`/mnt/c/Users/Dan/projects/site-backups/<date>/textmaxxpro-site/`. The
`BACKUP-NOTE.txt` in each dated folder has exact `cp` + `git` commands.
