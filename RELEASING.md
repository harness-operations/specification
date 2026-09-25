# Release automation

Reference-model releases are cut from reviewed `main` commits through `.github/workflows/release.yml`.

The workflow is triggered only when `RELEASE.json` changes on `main`. Before publishing, it:

1. validates the release request;
2. refuses to overwrite an existing tag or release;
3. validates the complete comparison dataset;
4. reruns the approved-artifact handoff tests and demo;
5. reruns exact-version Harness interface smoke tests;
6. creates an **annotated tag at the exact triggering commit**;
7. publishes the GitHub release from a reviewed release-notes file.

The workflow has only `contents: write` permission and does not deploy the website. Website promotion remains a separate reviewable PR and deployment pipeline.
