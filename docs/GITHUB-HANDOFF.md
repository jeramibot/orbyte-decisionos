# GitHub handoff

No remote has been created or pushed. The connected account observed during preparation was `jeramibot`; the actual team owner and destination need confirmation. The supplied build instructions require approval before remote pushes and repository access changes.

1. Confirm the team account and new repository name (`orbyte-decisionos` is the proposed default). Create an empty private repository without an initial README or license so the existing local history can be pushed intact.
2. Review the local tracked files, author metadata and substantial AI assistance disclosure. Keep credentials and runtime databases excluded. The prepared PDFs are drafts; final signed/contact-filled forms need a separate publication review.
3. With explicit push approval, add the confirmed remote and push `main`. Do not squash, backdate or manufacture earlier work.
4. Inspect the GitHub Actions run. It installs Linux Chromium and runs the existing full workflow tests. Resolve real failures; no CI result is claimed yet.
5. Add the genuine repository, Replit and prototype links to the README and submission documents. Confirm required committee usernames from organisers before granting access.
6. Publish the repository before final submission only after the authorised access change. Verify links while signed out, freeze by the reviewed deadline and retain submission confirmation.

## Portable history

The sibling output `DecisionOS-history.bundle` contains all current local branches/history. To restore into a new directory:

```bash
git clone /path/to/DecisionOS-history.bundle orbyte-decisionos
cd orbyte-decisionos
git remote remove origin
```

Then configure the confirmed GitHub destination after approval. `DecisionOS-source.zip` is convenient for import but does not itself carry Git history. Prefer the bundle or existing local checkout for the competition repository. Neither package includes the separate AGPL MiroFish checkout or its environment.
