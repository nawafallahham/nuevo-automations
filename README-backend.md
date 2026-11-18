# Backend: Cloudflare Worker + D1

One Worker (`worker/index.js`) serves the static site from this folder (Workers static assets) plus `/api/*`. Data lives in the D1 database `nuevo-site`.

| Path | What it does |
|---|---|
| `GET /api/slots?days=14` | Taken slots per date (no customer data) |
| `POST /api/book` | Create a booking (validation, honeypot, 5/hour/IP limit, 409 on a taken slot) |
| `POST /api/track` | Anonymous, cookieless analytics beacon (from `js/track.js`) |
| `GET /api/calendar.ics?key=…` | Private iCal feed for Google Calendar |
| `/api/admin/*` | Dashboard API (`Authorization: Bearer ADMIN_KEY`), UI at `/admin/` |

After each booking these run in the background and are skipped when their secrets aren't set: Meta CAPI `Schedule` (only if the visitor accepted cookies), Resend email alert with an .ics (plus a confirmation to the customer if they gave an email), and the OrcaFlo webhook.

A nightly cron (23:17 UTC) deletes bookings 90 days after their date, analytics events older than 400 days, and stale rate-limit rows. The privacy policy depends on this.

## Files
- `wrangler.toml`: config. **`database_id` is a placeholder.** The custom-domain `routes` are commented out.
- `worker/`: `index.js` (router + cron), `api.js`, `admin.js`, `notify.js` (CAPI/email/OrcaFlo), `ics.js`, `lib.js`
- `migrations/0001_init.sql`: tables `bookings`, `events`, `rate`
- `_headers`, `_redirects`, `.assetsignore`: static asset config (the ignore list keeps worker/, migrations/, booking-api/ and similar folders from being published)
- `admin/index.html`: private dashboard (noindex, not linked)
- `js/track.js`, `js/booking.js`: front end
- `booking-api/`: the old Vercel + Upstash API, no longer used. Delete it after cut-over.

## First deploy
```sh
npm install
npx wrangler login
npx wrangler d1 create nuevo-site          # paste the printed database_id into wrangler.toml
npx wrangler d1 migrations apply nuevo-site --remote

# secrets (each prompts for the value)
npx wrangler secret put ADMIN_KEY          # long random string, e.g. `openssl rand -hex 24`
npx wrangler secret put CALENDAR_KEY       # another long random string
npx wrangler secret put HASH_SALT          # optional but recommended: random string for IP/visitor hashing
npx wrangler secret put META_CAPI_TOKEN    # Events Manager > Settings > Conversions API > Generate access token
npx wrangler secret put RESEND_API_KEY     # nuevoautomations.com must be a verified domain in Resend
npx wrangler secret put ORCAFLO_HOOK_URL
npx wrangler secret put ORCAFLO_HOOK_SECRET
# optional:
npx wrangler secret put MAIL_FROM          # default "Nuevo Automations <bookings@nuevoautomations.com>"
npx wrangler secret put META_TEST_EVENT_CODE   # only while testing in Events Manager; delete afterwards

npx wrangler deploy                        # goes to https://nuevo-site.<account>.workers.dev
```
`META_PIXEL_ID`, `NOTIFY_EMAIL` and `SITE_URL` are plain `[vars]` in `wrangler.toml`. To override `NOTIFY_EMAIL`, edit it there or delete it from `[vars]` and set it as a secret.

### Go live on the domain
1. The zone `nuevoautomations.com` must be on Cloudflare. In DNS, delete the old Vercel `A`/`CNAME` records for `@` and `www`.
2. Uncomment `routes` in `wrangler.toml`, then run `npx wrangler deploy`. Cloudflare creates the DNS records and certificates. The Worker 301s `www` to the apex.
3. In Meta Events Manager, test with `META_TEST_EVENT_CODE`, then delete that secret: `npx wrangler secret delete META_TEST_EVENT_CODE`.
4. Open `/admin/`, sign in with `ADMIN_KEY`, and copy the calendar URL into Google Calendar (Other calendars → From URL).

## Local development
```sh
printf 'ADMIN_KEY="local-admin"\nCALENDAR_KEY="local-cal"\n' > .dev.vars   # gitignored
npx wrangler d1 migrations apply nuevo-site --local
npx wrangler dev --local --port 8787
```
Local D1 data lives in `.wrangler/` (gitignored).

## Ops snippets
```sh
# upcoming bookings
npx wrangler d1 execute nuevo-site --remote --command "SELECT date,time,name,phone,business,status FROM bookings WHERE date >= date('now') ORDER BY date,time"
# live logs (side-effect failures are logged as [meta_capi] / [email] / [orcaflo])
npx wrangler tail
```
Rotating `ADMIN_KEY` or `CALENDAR_KEY`: `wrangler secret put` the new value. Rotating `CALENDAR_KEY` means re-subscribing to the calendar URL in Google Calendar.
