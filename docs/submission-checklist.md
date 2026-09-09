# Submission Verification Notes

The [original Baby Tools World checklist](Baby-Tools-World-Checkliste.md) is the authoritative course document supplied for this submission. Its wording and structure have been preserved; checked items are supported by the checks below. These notes supplement the original document and do not replace it.

## Local verification on 2026-09-09

| Area | Result |
| --- | --- |
| README | H1, three-sentence description, compact table of contents, ten-step Quickstart, Usage, feature list including Tags, configuration, Docker instructions and license are present. The style follows My Developer Blog. |
| Code checks | Black, isort and Flake8 pass over `src`. One trailing space in the existing Tag docstring was corrected. |
| Automated tests | All 50 Django tests pass. Branch coverage is 86%, exceeding the CI requirement of 69%. |
| Django and migrations | `manage.py check` passes, `makemigrations --check --dry-run` finds no changes, and all migrations are applied to the local database. The fresh container also applies migration `0002_tag_product_tags` successfully. |
| Dependencies | The Docker build installs the pinned requirements successfully. Both container `pip check` and local `uv pip check` report compatible dependencies. |
| Ignore rules | Python artifacts, virtual environments, `.env`, `local.env`, `development.env` and `.DS_Store` are ignored. `example.env` remains tracked. |
| Container | The README build command succeeds. The image starts with `src/.env` on port 8000 and is accessible in the browser. The audit used detached mode instead of the interactive foreground option. |
| Sample data | The first seed creates four categories and 15 products. Running it again creates no duplicates. All 15 bundled product images load in the browser. |
| Admin and static assets | Login with a temporary superuser succeeds. Admin styles load, and the JavaScript tag selector works. |
| Admin creation | A category, a product and two tags were created through the browser. Both tags were assigned to the product and saved. Tag timestamps have no editable form inputs. |
| Tag display | Both assigned tags appear on the product detail page. After removing them in the admin, `no tags available` appears with computed font style `italic`. |
| Reviews | Browser submissions as a signed-in user and as a guest succeed. The review appears, the comment field is empty and no rating stars remain selected after submission. |
| Accounts | Browser registration redirects to login. Login and logout both work. |
| Repository | GitHub reports `fork: false`; the existing feature PR targets `main`. CI results are available in the existing feature PR and must be checked for the latest commit. |

The browser audit used a fresh, disposable local container. Its test accounts and content are not part of the submitted VM or repository. It was stopped after verification.

The five new automated tag tests cover valid creation and reuse, duplicate and empty names, displayed tags and the italic empty placeholder. The suite also covers review updates and related-product ordering and limits.

## Remaining items

- **Type hints and docstrings:** These original checklist requirements are not consistently met throughout the existing code. For example, `product_list` and `product_detail` in `src/products/views.py` have neither annotations nor docstrings; several model methods also lack them. Those two checklist items remain unchecked. The mentor accepted the code, but that does not establish literal compliance with these broader requirements.
- **Submitted VM:** Current external reachability and the database state on the submitted VM still need confirmation. Local and container verification does not prove remote deployment status.
- **Video:** The user will retain the existing video. The mentor reviewed it positively and framed showing startup and admin login as advice for future projects, not a request for a replacement recording. The five-minute duration has not been independently checked, so the original combined video item remains open pending confirmation.
- **Campus submission:** Confirm the repository URL, PR URL, existing Loom link, VM address and admin credentials are present in the campus submission. Credentials belong in the campus comment, not the repository.
- **Review and resubmission:** Continue using PR #3 for the follow-up changes and include the filled original checklist in its description. Check CI for the latest commit before resubmission and keep the feature branch until the mentor approves merging.

Unchecked general advice and reference links in the original checklist are not failed application tests.

## References

- [Original course checklist](Baby-Tools-World-Checkliste.md)
- [Additional PR checklist](../.github/PULL_REQUEST_TEMPLATE/project_submission.md)
- [Mentor review and PR #3](https://github.com/FriggemannMichael/baby_tools_world_new/pull/3)
- [FAQ README guide](https://developer-akademie-devsecopskurs.github.io/dso-faq-site/docs/how-to-readme)
- [Blog README used as a style reference](https://github.com/FriggemannMichael/my-Blog/blob/main/README.md)
