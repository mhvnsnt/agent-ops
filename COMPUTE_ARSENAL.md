# Free Compute Arsenal — fmmg.mars@gmail.com (Mars FMMG)

Owner-set 2026-10-10, re-confirmed 2026-10-15. Every agent: USE THESE before
saying a render or GPU job needs rented/purchased compute. The owner already
has all of this — never tell him to rent GPU when this arsenal covers the job.

## Standing rule (owner)
NEVER put a card on anything, activate a billed trial, or spend money without
the owner's explicit permission. Replit ($200) and Emergent ($30) burned him
before. Free credit that requires no card is fine to *evaluate*; activating
anything billing-adjacent gets asked first.

## The arsenal (all on fmmg.mars@gmail.com unless noted)

| Service | What we have | How to drive it | Best for |
|---|---|---|---|
| **Kaggle** (`marsfmmg`) | 30 GPU-hrs/week, T4×2, phone-verified 2026-10-10 | Browser session (Google OAuth as Mars FMMG). API token was NEVER saved — `~/workspace/cloud-wiring/kaggle/kaggle.json` is still a template | Blender Cycles renders, batch GPU jobs, image/video model runs |
| **Google Colab** | Free T4 + v5e-1 TPU confirmed live 2026-10-10; availability not guaranteed, no paid units | Browser session as Mars FMMG | Backup GPU when Kaggle quota is out |
| **Lightning AI** | Credits on account (5 + disputed 30 — see billing incident 2026-10-10) | Browser session | Backup GPU |
| **Hugging Face** | Verified account, ZeroGPU + Spaces | API / browser | Inference, Spaces demos |
| **Pollinations.ai** | Tested working 2026-10-10, zero-signup text+image API | Direct HTTPS API | Quick text/image generation, no GPU needed |
| **Modal** (`mhvnsnt`) | $1 of $30/mo remaining — needs card for more | `~/workspace/tools/modal-venv` client | DO NOT USE without owner OK (card required) |
| **Google Cloud** | $300/90-day trial NOT activated; 2FA done; projects `valid-bloom-23bk6`, `gen-lang-client-0686773195` | Console as Mars FMMG | Ask owner before activating trial |
| **Oracle Cloud** | Not signed up | — | Future option only |
| **Saturn Cloud** | Signed in, billing locked without card | Browser session | Backup only |

## Notes for agents
- Kaggle is the default for GPU renders (Blender, video). Chunk long jobs
  (~250-frame chunks) — Kaggle sessions have time limits.
- The render package pattern: notebook installs Blender headless with CUDA,
  pulls the job from the repo branch, renders chunks, uploads results.
- If a job truly exceeds the free arsenal, report that with numbers and ask
  the owner — do not freelance a paid solution.
- Keep this file current: when a quota changes, a token gets saved, or an
  account lapses, update it in the same PR as the work that discovered it.
