# The Longevity Journal - Deployment Guide

## GitHub Pages Deployment (FREE)

### Step 1: Create GitHub Account
1. Go to https://github.com/join
2. Sign up (free)
3. Verify your email

### Step 2: Create Repository
1. Click "New Repository"
2. Name: `thelongevityjournal` (or any name)
3. Make it **Public**
4. Check "Add a README file"
5. Click "Create repository"

### Step 3: Upload Files
1. In your repo, click "Add file" > "Upload files"
2. Upload ALL these files from `C:\Openclaw\agents\longevity-journal\`:
   - `index.html`
   - `styles.css`
   - `script.js`
   - `articles/` folder (all 6 HTML files)
3. Click "Commit changes"

### Step 4: Enable GitHub Pages
1. Go to Settings (tab in your repo)
2. Scroll down to "Pages" section
3. Under "Source", select "Deploy from a branch"
4. Select "main" branch, "/ (root)" folder
5. Click "Save"
6. Wait 2-5 minutes

### Step 5: Your Site Is Live!
Your site will be at:
```
https://YOUR_USERNAME.github.io/thelongevityjournal/
```

Example: `https://joe72.github.io/thelongevityjournal/`

### Optional: Custom Domain
1. Buy domain (Namecheap ~$10/year)
2. In repo Settings > Pages > Custom domain, enter your domain
3. Add DNS records (GitHub provides instructions)
4. Enable HTTPS (GitHub does this automatically)

---

## Netlify Alternative (Also FREE)

If GitHub feels too technical:

1. Go to https://www.netlify.com/
2. Drag and drop your `longevity-journal` folder
3. Site goes live instantly
4. Custom domain: Settings > Domain management

---

## Current File Structure

```
longevity-journal/
├── index.html              <-- Homepage
├── styles.css              <-- Dark theme
├── script.js               <-- Newsletter form
├── articles/
│   ├── nad-precursors.html     <-- NAD+ article
│   ├── rapamycin-dogs.html     <-- Rapamycin article
│   ├── epigenetic-clocks.html  <-- Biological age testing
│   ├── zone-2-cardio.html      <-- Exercise for longevity
│   ├── spermidine.html         <-- Autophagy supplement
│   └── fasting-mimicking-diet.html  <-- 5-day immune reset
└── DEPLOY.md               <-- This file
```

---

## Total Cost Breakdown

| Item | Cost |
|---|---|
| GitHub account | FREE |
| GitHub Pages hosting | FREE |
| Netlify hosting | FREE |
| Domain (optional) | ~$10-15/year |
| **Total minimum** | **$0** |
| **With custom domain** | **~$15/year** |

---

## Next Steps After Deployment

1. Set up ConvertKit or Mailchimp (free tier) for newsletter
2. Add Google Analytics (free) to track visitors
3. Share on Twitter/Reddit/longevity forums
4. Start publishing new articles weekly

## AI Agent Content Pipeline

See `AGENTS.md` for the automated article generation system.
