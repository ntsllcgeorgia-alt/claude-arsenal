# Higgsfield Setup

Higgsfield is the engine behind every image and video skill in this arsenal. Without it, the visual generation skills don't fire. Setting it up takes about 5 minutes.

---

## What Higgsfield does for you

| If you want to... | Higgsfield model |
|---|---|
| Generate a stylized image from a description | GPT Image 2 |
| Generate from reference photos (keeps your house looking like YOUR house) | Nano Banana 2 / Pro |
| Generate a short video clip | Seedance 2.0 |
| Generate a polished brand ad with a presenter | Marketing Studio |
| Generate cinematic video (TV-quality) | Soul Cinema Studio |
| Train Higgsfield on YOUR face | Soul Character (Soul ID) |

---

## Step 1 — Make a Higgsfield account

1. Go to https://higgsfield.ai
2. Sign up (Google sign-in is fastest)
3. Free tier gives you a starter credit pool — good for learning the system
4. Plans start around $20/month for serious volume — pay-as-you-go also available

---

## Step 2 — Install the Higgsfield CLI

The skills use the official `higgsfield` command-line tool.

**Windows (PowerShell):**
```powershell
iex (iwr "https://raw.githubusercontent.com/higgsfield-ai/cli/main/install.ps1").Content
```

**Mac/Linux:**
```bash
curl -fsSL https://raw.githubusercontent.com/higgsfield-ai/cli/main/install.sh | sh
```

Verify it installed:
```bash
higgsfield --version
```

---

## Step 3 — Authenticate

```bash
higgsfield auth login
```

A browser window opens. Approve the access. Done.

Verify:
```bash
higgsfield account status
```

Should print your username + credit balance.

---

## Step 4 — Test it

Try a simple image generation from the command line:

```bash
higgsfield generate create \
  --model gpt_image_2 \
  --prompt "A cozy living room in golden hour, editorial style, magazine-quality"
```

It'll print a job ID. After ~30 seconds, fetch the result:

```bash
higgsfield generate get <job-id>
```

If you got a URL back — you're armed.

---

## Step 5 — Use it through Claude

Now in Claude Code, just describe what you want:

```
Generate a hero image for my listing landing page at 123 Maple St.
Reference: [paste 1-3 URLs of your actual photos]
Style: golden hour exterior, warm light through the windows, 16:9
```

Claude triggers `higgsfield-product-photoshoot` (because you provided reference photos) or `higgsfield-generate` (if you didn't). The skill handles cost estimation, calls the CLI, polls for the job, and shows you the result.

---

## Cost management

Higgsfield charges per generation. The skills are built to:

1. **Cost-check before running** — they call `higgsfield generate cost` first and tell you the price before submitting.
2. **Prefer cheaper models when quality difference is marginal** — e.g. uses Seedance for first-draft video, only escalates to Cinema Studio if you ask.
3. **Reuse outputs** — when generating carousel slides, slide 1 becomes the style reference for slides 2-N so you only pay for one "expensive" gen.

You can set a per-session budget cap:

```bash
higgsfield config set max_cost_per_session 5.00
```

---

## What models you'll actually use as a realtor

| Use case | Model | Approx cost per output |
|---|---|---|
| Listing hero image (with photo references) | Nano Banana 2 | $0.06 / image |
| Editorial / lifestyle hero photo | GPT Image 2 | $0.04 / image |
| 5-second listing tour video | Seedance 2.0 | $0.50 / video |
| 15-second cinematic spot | Cinema Studio | $2-4 / video |
| UGC testimonial video | Marketing Studio + Soul | $1-2 / video |
| Instagram carousel (5 slides) | GPT Image 2 × 5 | $0.20 / carousel |

(Prices change. Always run `higgsfield generate cost` for the real number.)

---

## Troubleshooting

**`higgsfield: command not found`** — installer didn't add it to PATH. Close and reopen your terminal. If still missing, run the installer again.

**`Session expired`** — re-run `higgsfield auth login`.

**Job stuck in pending** — Higgsfield queues during peak hours. Be patient or escalate plan tier.

**The output doesn't look like my reference photos** — make sure you're calling Nano Banana 2 (not GPT Image 2) — Nano Banana respects references; GPT Image 2 uses them as loose inspiration.
