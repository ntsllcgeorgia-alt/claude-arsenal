---
name: youtube-content-package
description: Creates complete YouTube video packages including title, description, keywords, timestamps, thumbnail concepts, and posting via Late MCP. Use when user wants to publish a video, create YouTube content, or needs help with video SEO.
---

# YouTube Content Package

Create complete YouTube video packages with optimized titles, descriptions, keywords, timestamps, and thumbnail concepts.

## Full Workflow Overview

1. **Check video size** - Must be under 500MB
2. **Compress if needed** - Local HandBrake or FFmpeg
3. **Upload to Late storage** - Get video URL
4. **Extract transcript** - Local transcription tool
5. **Create content package** - Title, description, tags, etc.
6. **ASK USER FOR THUMBNAIL** - REQUIRED before posting
7. **Get user approval** - Confirm content package
8. **Post via Late API** - Publish to YouTube with all fields

---

## CRITICAL: Pre-Post Requirements

**NEVER post without:**
1. Asking user for thumbnail image
2. Confirming the title with user
3. Showing complete content package for review
4. Getting explicit approval to post

---

## Step 0: Check, Compress & Upload Video

See `late-social-media` skill → **Media Upload** section for compress + presign + upload steps.

---

## Step 1: Extract Transcript with Timestamps

Use any local transcription tool (WhisperX, faster-whisper, etc.):

```bash
# Example - adjust to your setup
python transcribe.py "VIDEO_PATH"
```

**Output:** Creates `.txt` (full transcript) and `.srt` (timestamps) in same directory.

---

## Step 2: Analyze Content & Create Title

Based on transcript, create 5 title options following these patterns:
- How-to: "How to [Outcome] in [Timeframe] ([Qualifier])"
- Curiosity: "I [Did Something Unexpected] and [Result]"
- Direct benefit: "[Outcome] with [Method/Tool]"
- Question: "Can [Tool/Method] Really [Achieve Outcome]?"
- Statement: "The [Adjective] Way to [Outcome]"

**Title rules:**
- 60 characters max (ideal for display)
- Front-load keywords
- Include power words: Free, New, Proven, Easy, Fast, Simple
- Add parenthetical qualifiers: (Full Demo), (Step-by-Step), (2026)

---

## Step 3: Research Tags

Tags should be **simple, short, and psychologically aligned** with how real people search.

### Tag Structure

**Core topic tags (3-5):** The simplest words describing what the video IS about.
- One or two words max.
- Example: "AI sales", "sales campaign", "AI marketing"

**Outcome tags (2-3):** What the viewer GETS from watching.
- Example: "get clients", "book appointments", "client acquisition"

**Identity tags (2-3):** WHO is this for.
- Example: "agency owner", "lead generation", "marketing agency"

**Tool/method tags (2-3):** Specific tools, systems, or methods shown.
- Example: "AI agent", "sales automation", "outreach system"

**Discovery tags (2-3):** Adjacent topics that bring in related audiences.
- Example: "AI tools", "business growth", "sales system"

### Tag Rules
- Keep tags simple: 1-3 words each
- No filler words ("how to use", "best way to")
- No duplicating the title verbatim as a tag
- Prioritize words people actually type
- Total of all tags combined must be under 500 characters

### Late API Format
Tags are a **string array** in the Late API:
```json
["AI sales", "sales campaign", "AI agent", "get clients", "agency owner"]
```

---

## Step 4: Create Description

**Structure (in order):**

1. **Lead Magnet CTA** (first 2 lines - visible before "Show more")
   ```
   [Hook sentence with value proposition]
   [LEAD_MAGNET_URL]
   ```

2. **Quick Overview** (100-150 words)
   - Simple, digestible language
   - What they'll learn/see
   - Why it matters to them

3. **Social Links**
   ```
   My Links:
   Subscribe: YOUR_YOUTUBE_URL
   LinkedIn: YOUR_LINKEDIN_URL
   Instagram: YOUR_INSTAGRAM_URL
   ```

4. **Timestamps** (consolidated into 10-15 key sections)
   ```
   Timestamps:
   0:00 Section Name
   1:23 Next Section
   ```

5. **Hashtags** (3-5 at the end)
   ```
   #Keyword1 #Keyword2 #Keyword3
   ```

---

## Step 5: Create First Comment CTA

Same CTA as description intro, formatted for engagement:
```
[Question or hook]

[LEAD_MAGNET_URL]

[Brief value statement + call to action]
```

---

## Step 6: ASK USER FOR THUMBNAIL (REQUIRED)

**This step is MANDATORY before posting.**

Ask the user:
1. Do you have a thumbnail ready to upload?
2. Or should I generate a thumbnail concept prompt?

If user provides thumbnail:
- Upload to Late storage and get URL
- Include in post

If user wants concept:
- Provide text-to-image prompt with:
  - Phrase (short, bold, benefit-focused)
  - Layout description
  - Color specs
  - Logo placement instructions

---

## Step 7: Get User Approval

**Before posting, show user:**
1. Title (confirm it's correct)
2. Description preview
3. Tags list
4. First comment CTA
5. Thumbnail status

Confirm: "Ready to post this to YouTube?"

---

## Step 8: Post via Late API

See `late-social-media` skill → **YouTube-Specific Fields** and **Posting Workflow** for the full curl command and platform fields.

---

## Configuration

> API key and account IDs: see `late-social-media` skill → **Configuration** section.

### Description Style Rules
- No em-dashes (use colons or periods instead)
- No emojis unless specifically requested
- Simple, conversational language
- Short paragraphs (2-3 sentences max)
- Blank lines between sections

---

## Timestamp Creation Guidelines

From SRT file, consolidate into 10-15 meaningful sections:

1. **Group related content** - Don't list every topic change
2. **Use clear labels** - "Setting Up X" not "X Setup Process Begins"
3. **Round timestamps** - Use :00, :30 increments when possible
4. **Start with context** - First timestamp explains what video covers
5. **End with value** - Last timestamps should highlight key outcomes

---

## Thumbnail Text-to-Image Template

```
Clean minimalist YouTube thumbnail, [BACKGROUND_COLOR] background, bold [TEXT_COLOR] sans-serif text on the left side reading "[LINE_1]" with the word "[HIGHLIGHT_WORD]" in [ACCENT_COLOR] with subtle underline, modern tech aesthetic, professional typography, high contrast, clean layout with empty space on right side for logo placement, 1280x720 aspect ratio, no gradients, flat design, editorial style
```

**Phrase guidelines:**
- 4-6 words maximum
- Benefit-focused (what they GET)
- Power words: Free, New, Easy, Fast, Automated, AI
- Avoid: "How to", "Tutorial", generic terms
