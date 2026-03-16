# Step-by-Step: Creating Consistent AI Characters Across Multiple Scenes

Character consistency is the hardest unsolved problem in AI video production right now. If your project needs a recurring character — a brand mascot, a narrator avatar, a protagonist — you will fight drift in every tool you use. This is my current workflow for getting as close to consistency as the tooling allows.

Fair warning: this is not a perfect solution. It's a system for minimizing drift to an acceptable level for most production contexts.

---

## What "Consistent" Actually Means Here

For production purposes, a character is "consistent enough" when:
- Viewers recognize them as the same person across cuts
- Skin tone, hair, and general facial structure don't noticeably change
- Clothing and props match scene-to-scene if the narrative requires it

You won't get frame-perfect identity matching without a real actor or a 3D rig. Aim for recognizable, not identical.

---

## Tool Requirements

- **Midjourney v6.1** — character still generation
- **Kling 1.6 Pro** — image-to-video, with `--cref` equivalent in the prompt approach
- **Adobe Firefly** (or Photoshop Generative Fill) — optional, for cleanup
- **CapCut Pro or DaVinci Resolve** — assembly

This workflow does not require ComfyUI or LoRA training. If you're comfortable with those, you can get better consistency — but this tutorial assumes you want results without that overhead.

---

## Phase 1: Building the Character Reference Sheet

This is the most important step. Rush it and you'll pay for it in drift later.

**Step 1: Write a detailed character description**

Before you open Midjourney, write a plain-text description of your character. Include:

- Age range (be specific: "early 30s" not "young adult")
- Gender presentation
- Ethnicity/skin tone (be specific and respectful)
- Hair: length, color, texture, style
- Notable facial features: jawline, eye shape, any distinctive marks
- Build/body type
- Default expression

Example:
```
Woman, early 30s, South Asian, warm medium-brown skin, thick dark brown
hair in a low bun with loose strands framing face, almond-shaped dark
brown eyes, defined brows, small nose, natural lip color, lean build,
calm and approachable expression.
```

Write this once. This is your character bible. Do not change it mid-project.

---

**Step 2: Generate your anchor image in Midjourney**

Use your character description in a neutral, well-lit context. The anchor image should be:
- Neutral background (white, light gray, or soft gradient)
- Frontal or slight 3/4 angle — enough to see the full face
- Natural lighting (not dramatic shadows that obscure features)
- Waist-up or full body depending on how much of the character will be visible in your spots

Prompt structure:
```
[Character description], standing, neutral studio background, soft even
lighting, natural expression, photorealistic, shot on Sony A7 IV,
85mm lens, --ar 2:3 --style raw --v 6.1 --q 2
```

Generate at least 4–6 options. Pick the one that most closely matches your description. **This is your character reference image.** Save it somewhere permanent.

---

**Step 3: Generate scene-specific character images using `--cref`**

For every scene that features your character, use Midjourney's Character Reference flag to anchor new generations to your reference image.

```
[Character description], [scene-specific context and environment],
[lighting], [camera angle], --cref [URL of your anchor image] --cw 80
--ar 16:9 --style raw --v 6.1
```

The `--cw` (character weight) flag controls how strongly the reference is applied. Settings:
- `--cw 100` — very strong adherence, can feel stiff
- `--cw 80` — good balance for most production use
- `--cw 60` — looser, more expressive, higher drift risk

For each scene, generate at least 4 options. Pick the one with the strongest resemblance to your anchor image.

**Important:** Always include your full character description in the prompt even when using `--cref`. The flag helps with facial structure, but the text prompt still drives hair, expression, and clothing.

---

## Phase 2: Bringing the Character Into Motion

**Step 4: Evaluate your stills before animating**

Before you go to Kling, compare all your selected scene stills side by side. Common issues to catch now:
- Skin tone drift (one image reads significantly lighter or darker)
- Hair changes (length, texture, or color inconsistencies)
- Facial proportions that don't match the anchor

If a still has obvious drift, regenerate it rather than animating it — drift gets worse in motion.

---

**Step 5: Animate in Kling with conservative settings**

Character clips are where you need the most conservative Kling settings.

Settings that minimize facial drift:
- **Motion strength: 2–3** for close-ups and medium shots with the character's face
- **Motion strength: 4** maximum for full-body or environmental shots where face is small
- **Camera movement:** slow push forward or very subtle static — no lateral sweeps across the face
- **Negative prompt:** "morphing, distortion, facial deformation, multiple faces, blurry features"

For dialogue-adjacent scenes (character appears to be speaking or reacting), target motion strength 2. Higher strength values almost always produce lip movement artifacts and eye drift.

Generate 2 clips per scene minimum. Compare them against your anchor still before choosing.

---

**Step 6: Handle problem clips**

If you can't get an acceptable clip after 3 regenerates, you have a few options:

**Option A — Static with Ken Burns:** Use the still image in your edit with a slow zoom or crop animation. This reads as a deliberate stylistic choice when used consistently, not as a technical limitation.

**Option B — Cut away:** Restructure the scene to cut away before or after the problem moment. Often a reaction shot or product close-up can replace a clip that isn't working.

**Option C — Firefly Generative Fill cleanup:** Export the first frame of a problematic clip, clean up obvious artifacts in Photoshop's Generative Fill, then use the cleaned still as a new Kling source image. This adds time but can salvage a scene composition that you're otherwise happy with.

---

## Phase 3: Maintaining Consistency in Post

**Step 7: Color grading for character continuity**

Even with consistent generation, skin tone often varies slightly between clips due to different lighting conditions in the scene prompts. Fix this in post:

In DaVinci Resolve, use the **Color Match** feature (Color > Color Match) with your anchor reference image as the target. Apply this to all clips featuring the character, then do a manual pass to verify — Color Match isn't always accurate on skin tones.

Alternatively, in CapCut Pro, use the **Color Curves** and **Hue/Saturation/Luminance** (HSL) tools to manually match skin tones across clips. Target the orange-red channel in HSL for most skin tone work.

---

**Step 8: Edit order and pacing to mask inconsistencies**

Cut away from your character before inconsistencies would be obvious. Practical rules:
- Don't hold on a character close-up for more than 3–4 seconds
- Use product shots, environment shots, or text cards between character clips
- If two character clips have visible drift, don't cut directly between them — put a cutaway between them

Viewers are more forgiving of character inconsistency when the cuts are clean and the pacing is confident. Slow, lingering holds on drifted character clips are what break immersion.

---

## Expected Results

With this workflow, you should be able to produce a 30–60 second spot where a single character appears in 4–6 scenes and reads as the same person throughout. You won't fool anyone who's looking closely, but for normal viewing at normal speed, it holds.

The `--cref` flag in Midjourney made a significant difference when it launched — I'd estimate it reduced my character drift issues by 40–50% compared to prompt-only consistency attempts.

If you need frame-accurate identity consistency — same person, every shot, no exceptions — you're going to need either a real actor, a 3D avatar pipeline (HeyGen Pro does this for talking head content), or LoRA fine-tuning in ComfyUI. Those are different tutorials.

---

Questions or edge cases you've hit — drop them in the comments. Character consistency is a moving target and the tooling is changing fast.
