# How to Build an AI-Powered Spec Ad Pipeline in Under 4 Hours

I've been doing spec work for a few years now — mostly to build a reel and test creative directions before pitching clients. Six months ago I rebuilt my entire spec pipeline around AI tools and cut my per-project time from about 3 days down to 4 hours on a good run. Here's exactly how I do it.

This assumes you have accounts with the main tools already set up. Cold-starting all of this from scratch adds maybe 2 hours of setup the first time.

---

## What "spec ad" means in this context

I'm talking about a 30–60 second produced spot — finished enough to show a client or post publicly. Not a mood board, not a storyboard PDF. An actual video with narration, music, B-roll, and a rough color grade.

---

## The Stack

- **ChatGPT-4o** — script and brief generation
- **Midjourney v6.1** — hero product stills, lifestyle imagery
- **Kling 1.6 Pro** — motion clips from stills (5s and 10s)
- **ElevenLabs v2** — voiceover (I use the "Daniel" or "Charlotte" voice depending on brand tone)
- **CapCut Pro** (desktop) — assembly, captions, basic grade
- **Suno v4** — background music
- Total monthly spend for this stack: ~$105/month across all tools

---

## Step 1: Brief → Script (20–30 min)

Start with a tight brief. I use this prompt structure in GPT-4o:

```
Brand: [name]
Product: [one sentence]
Target audience: [specific]
Tone: [3 adjectives]
Spot length: 30 seconds
Format: Write a shooting script with scene descriptions and VO lines separated.
No more than 6 scenes.
```

I iterate 2–3 times max. The goal is a script you'd actually shoot — scenes that are visually distinct and VO that doesn't sound like a press release.

**Time check: 20–30 min including iterations**

---

## Step 2: Visual Assets (60–90 min)

Each scene in the script gets 2–3 image options from Midjourney. My standard prompt structure:

`[subject], [setting], [lighting style], [camera angle], [film stock or aesthetic], --ar 16:9 --style raw --v 6.1`

For product shots I usually run:
`product flatlay on marble surface, soft diffused window light, overhead shot, muted warm tones, shot on Hasselblad --ar 1:1 --style raw --v 6.1 --q 2`

Pick your best image per scene. You need 5–6 finals.

**Pro tip:** Run all prompts in a batch — don't wait for each one. Start 6 jobs, go get coffee, come back and curate.

**Time check: 60–90 min including iteration and selection**

---

## Step 3: Motion Clips (45–60 min)

Take your selected stills into Kling 1.6 Pro. For most product/lifestyle spots, 5-second clips are enough — 10-second clips are worth the extra credits if you need a slow reveal or camera move.

Settings I use consistently:
- **Mode:** Pro
- **Motion strength:** 4–5 (anything above 6 usually distorts the product)
- **Camera movement:** Slow zoom in OR slow push forward — not both in the same spot
- **Negative prompt:** "blur, distortion, morphing faces, watermark"

Expect a ~30% failure rate where the clip is unusable. Generate 2 options per scene so you're not stuck.

**Time check: 45–60 min including regenerates**

---

## Step 4: Voiceover (15–20 min)

Paste your VO script lines into ElevenLabs. I use the v2 Turbo model for faster generation, v2 standard when I need better breath control on long sentences.

Settings that work well for ad VO:
- **Stability:** 55–65
- **Similarity:** 70–75
- **Style:** 20–30 (higher makes it sound "performed," which works for some spots)

Export as WAV, not MP3. CapCut handles WAV better and you won't get compression artifacts on the master.

**Time check: 15–20 min**

---

## Step 5: Music (10–15 min)

Suno v4 with a specific prompt works better than browsing their library. I describe the feeling, not the genre:

`Understated, modern. Clean piano with light percussion. Builds slightly at 20 seconds. No lyrics. 45 seconds long. For a premium brand commercial.`

Generate 3 options, pick one. If none work, try Artlist or Epidemic Sound — I have subscriptions to both as backup. Budget ~$20/month for Epidemic if you're doing this regularly.

**Time check: 10–15 min**

---

## Step 6: Assembly in CapCut (45–60 min)

My timeline order:
1. Drop all video clips in sequence
2. Rough cut to VO timing — the VO drives everything
3. Add music track, duck it to -18dB under the VO
4. Auto-captions on the VO track (CapCut's built-in, clean up manually)
5. Color grade: I use the "Matte Film" LUT preset, then pull highlights down slightly and push the mid contrast up
6. Export: 1080p, H.264, 25 Mbps for client delivery

**Time check: 45–60 min**

---

## Total Time Breakdown

| Phase | Time |
|-------|------|
| Brief + Script | 25 min |
| Image generation + selection | 75 min |
| Motion clips | 50 min |
| Voiceover | 20 min |
| Music | 12 min |
| Assembly + export | 50 min |
| **Total** | **~3h 52min** |

---

## What to watch out for

**Kling face distortion** is the biggest quality killer. If a clip has a person in it, keep motion strength at 3–4 max and avoid prompting any camera movement toward the face. Generate two clips per scene with people.

**ElevenLabs pacing** — the AI doesn't breathe like a real VO artist. If a sentence is longer than 15 words, split it into two lines in the input. The pause it inserts is much more natural than a run-on.

**Midjourney consistency** — you won't get perfect brand consistency across scenes without using the `--cref` flag (character reference) or keeping a very tight prompt seed. For product shots, this matters less. For anything with a recurring character, use `--cref [image URL]` to maintain visual continuity.

---

This pipeline won't replace a full production for a paying client with real deliverable standards. But for spec, for pitching, or for internal mockups — it's fast enough that I'll run 3–4 variations of a concept in the time it used to take me to finish one.

Happy to answer questions on any specific step.
