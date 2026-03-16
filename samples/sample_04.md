# Case Study: Producing a 60-Second AI Commercial for Under $200

Last November I produced a 60-second commercial for a small skincare brand — a real client, real deliverable, meant for paid social and their website. Total production cost came in at $187. Here's the full breakdown of how it happened, what went wrong, and what I'd do differently.

---

## The Brief

The client runs a small natural skincare line — three products, DTC, primarily selling through Instagram and their Shopify store. They wanted a brand video: something that felt premium, clean, and could run as a pre-roll ad. Budget was tight because they'd spent most of their launch budget on inventory. We agreed on a flat fee of $1,200 for the project.

The deliverable: one 60-second master cut, one 30-second cut, and a 9:16 vertical version of the 30-second for Stories/Reels.

---

## Pre-Production

**Week 1 — 3 hours total**

I started with a strategy call (45 min) to get brand voice, target customer, and visual references. They sent me their brand guide PDF and a folder of reference ads they liked — mostly soft, warm, aspirational lifestyle content. Nothing fast-cut, nothing loud.

Script development took about 2 hours across two sessions. I used GPT-4o to generate 3 rough script options from the brief, then rewrote the best option by hand. The AI draft had the right structure but the language was too generic — "feel your best self" energy that the client specifically wanted to avoid.

**Final script:** 6 scenes, 78 words of VO, ~60 seconds at a natural speaking pace.

---

## Production

**Week 1–2 — ~8 hours total**

### Visual Assets

| Asset Type | Tool | Credits Used | Cost |
|------------|------|-------------|------|
| Product stills (6 images) | Midjourney v6.1 | ~30 generations | ~$4.50 (Fast hours) |
| Lifestyle imagery (8 images) | Midjourney v6.1 | ~40 generations | ~$6.00 |
| Motion clips (12 clips × 5 sec) | Kling 1.6 Pro | 360 credits | ~$17.60 |
| 3 regenerates (unusable clips) | Kling 1.6 Pro | 90 credits | ~$4.40 |

Midjourney prompts centered on: natural light, linen textures, warm neutral tones, overhead flat lays, and hands holding product. The `--style raw` flag was essential — without it the images looked like stock photography, which wasn't right for the brand.

Kling settings: Pro mode, motion strength 4, slow zoom for product reveals, push forward for lifestyle clips. Two clips had face drift artifacts and had to be regenerated. One clip of water pouring was unusable at any motion strength — switched to a still image with a slow zoom instead, which worked fine.

### Voiceover

Used ElevenLabs "Rachel" voice — warm, measured, not overtly "ad voice." Generated 4 takes with slightly different stability/style settings:
- Take 1: Stability 60, Style 15 — too flat
- Take 2: Stability 55, Style 25 — slightly too performative
- Take 3: Stability 58, Style 20 — used this one
- Take 4: Stability 65, Style 10 — too robotic

Cost: ~$0.80 in ElevenLabs credits for all takes (short script, Turbo v2 model).

### Music

Pulled a track from Artlist ($199/year subscription, amortized). The client needed music they could run in paid ads — Suno-generated music technically has usage rights but some ad platforms flag it during review. Artlist has explicit commercial rights documentation, which matters when you're running Meta ads.

For the purposes of cost attribution: $199/12 = ~$16.60/month. Call it $5 for this project.

---

## Post-Production

**Week 2 — 4 hours total**

Assembly in DaVinci Resolve Free (CapCut for the vertical cut):

1. Rough assembly synced to VO — 45 min
2. Timing adjustments (a few clips ran a bit long) — 30 min
3. Color grade: started with DaVinci's "Film" LUT, then reduced saturation 8%, increased mid-contrast, cooled the highlights slightly to complement the brand's blue-tinted packaging — 45 min
4. Music mix: ducked to -20dB under VO, slight fade in at top, longer fade out at end — 20 min
5. Captions: generated in Premiere, manually corrected 3 words — 15 min
6. Vertical cut (9:16): reframe in CapCut, repositioned some text — 30 min
7. Exports and delivery — 15 min

---

## Full Cost Breakdown

| Item | Cost |
|------|------|
| Midjourney credits (month, prorated) | $10 |
| Kling 1.6 Pro credits | $22 |
| ElevenLabs credits | $1 |
| Artlist (prorated) | $5 |
| Stock photo backup (not used) | $0 |
| DaVinci Resolve | $0 (free version) |
| CapCut Pro (prorated) | $4 |
| GPT-4o (monthly plan, prorated) | $2 |
| Miscellaneous (exports, cloud storage) | $3 |
| **Total** | **$47** |

Wait — I said $187 at the top. The difference: I bought an additional 600 Kling credits mid-project ($29) because I burned through my monthly allocation faster than expected. I also paid $111 for a brand-new Artlist annual subscription specifically to cover this client's ad rights. If I amortize that subscription across 12 months it's $16/year, but I bought it for this project, so I'm counting the full cost honestly.

Adjusted actual cost: **$187**. Margin on a $1,200 project: ~$1,013 before taxes and any overhead.

---

## What Went Wrong

**Kling credit burn.** I underestimated how many regenerates I'd need. For a project with a specific product that needs to look right — product shape, label legibility — plan for a 40–50% reject rate on motion clips, not 30%.

**Client revision on VO.** After the first cut, the client wanted the VO to sound "a little warmer." I regenerated 3 takes at different ElevenLabs settings and they picked one. No big deal, but it added 45 minutes I didn't account for. Build VO iteration time into your quote.

**The water pour scene.** I spent probably 45 minutes trying to make a product-in-water pour clip work in Kling. Nothing looked right. Should have cut to a still with motion blur earlier. Time lost: 45 min.

---

## What I'd Do Differently

- **Pre-generate motion test clips** before committing to final still images. Test the Kling behavior before you finalize the source image.
- **Budget more Kling credits upfront.** For product work, I now plan for 50% over my clip count.
- **Lock VO first.** The voice sets the pace for everything. Now I generate and approve VO before I start cutting motion clips.

---

## Client Outcome

The client ran the 30-second cut as a Meta ad for 6 weeks. They reported it outperformed their previous static image ads on click-through rate. They've since booked two more projects.

The $1,200 fee was below what I'd charge today for the same project — I've since moved that type of work to $2,200 — but it was the right price to land a new client and build a case study. Which is what you're reading now.
