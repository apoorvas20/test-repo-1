# Two way sync

Two-way sync keeps a folder of docs in step across Falconer and GitHub. Edit in either place and the other side reflects the change.

## How it works

Two directions, one linked folder:

- **GitHub to Falconer:** push a commit and the change ingests into the linked Falconer folder.
- **Falconer to GitHub:** edit a doc in Falconer and write the change back to the repo.

A folder opts in by becoming a `REPO_SYNCED` folder, bound to a repository, branch, and base path.

## Sync triggers

Syncs fire from three sources:

- **Webhooks:** a push to the tracked branch syncs the changed files.
- Editing on github too
- **Cron:** a scheduled job re-syncs tracked repos to catch anything missed.
- **Manual:** kick off a sync from the folder sync dialog and watch it complete.

Back-to-back triggers for the same folder collapse into one in-flight run, so a burst of pushes (or a webhook overlapping a cron tick) never fans out into concurrent syncs. Editing same on github

## Writing back to GitHub

When you push Falconer edits to GitHub, pick a merge strategy:

- **Direct commit:** commit straight to the tracked branch.
- **Create pull request:** open a PR with the changes for review.

## Under the hood

- **Connector:** clones the repo (single branch, shallow), walks the doc directory, and reads the markdown to ingest.
- **File handler:** for webhook syncs, pins each fetch to the exact commit SHA from the event so ingested content matches the recorded base anchor.
- **Hunk stitching:** reconciles edits at the diff-hunk level so changes on both sides merge cleanly.

## TL;DR

- Keeps a `REPO_SYNCED` folder in sync with a GitHub repo, both directions.
- GitHub pushes ingest into Falconer; Falconer edits write back via direct commit or PR.
- Creating conflicts here too again
- Lets test text only push now 
- Editing more, again. Trying