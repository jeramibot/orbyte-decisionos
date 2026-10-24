# GitHub handoff

The user confirmed `jeramibot` as the repository owner and approved publication. Genuine local history and code were pushed to the **public** [jeramibot/orbyte-decisionos](https://github.com/jeramibot/orbyte-decisionos) repository, and the local `origin` points to it. An anonymous request returned HTTP 200 on 24 October 2026. The current owner is the only listed collaborator; obtain the organiser-designated handles before inviting anyone else.

1. Review the local tracked files, author metadata and substantial AI assistance disclosure. Keep credentials and runtime databases excluded. The prepared PDFs are drafts; final signed/contact-filled forms need a separate publication review.
2. Keep `main` current with the reviewed submission files. Do not squash, backdate or manufacture earlier work.
3. The [latest tested GitHub Actions run passed](https://github.com/jeramibot/orbyte-decisionos/actions/runs/40105180876), including Linux Chromium and the full workflow tests. Check later runs after any changes.
4. Add the genuine repository, Replit and prototype links to the README and submission documents. Confirm required committee usernames from organisers before granting access.
5. The repository is published. Verify links while signed out, freeze by the reviewed deadline and retain submission confirmation.

## Portable history

The sibling output `DecisionOS-history.bundle` contains all current local branches/history. To restore into a new directory:

```bash
git clone /path/to/DecisionOS-history.bundle orbyte-decisionos
cd orbyte-decisionos
git remote remove origin
```

Then configure the confirmed GitHub destination after approval. `DecisionOS-source.zip` is convenient for import but does not itself carry Git history. Prefer the bundle or existing local checkout for the competition repository. Neither package includes the separate AGPL MiroFish checkout or its environment.
