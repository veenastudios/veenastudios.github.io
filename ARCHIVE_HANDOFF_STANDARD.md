# Veena Studios — Archive & Professional Handoff Standard

Date: 2026-11-23. Status: operating standard; **not a claim of complete backups**.

## Universal file rules
- Preserve every significant file regardless of size. Record exact location, owner, version, format, approval, checksum if available, access class, and backup status.
- Maintain original/editable source separately from approved delivery exports.
- Preserve original filenames and live links until any relocation is tested.
- Private documents, contracts, unpublished manuscripts, personal data, passwords and signing keys must never go into this public repository.
- For large video/audio/game build assets, use private storage suited to their size, with an independent second backup.
- Use date/version suffixes; never overwrite an approved master without a retained previous version.

## Per-project private folder template
```
PROJECT-ID/
  00-MANIFEST/
  01-ORIGINAL-SOURCE/
  02-WORKING-VERSIONS/
  03-APPROVED-MASTERS/
  04-ARTWORK-AND-MEDIA/
  05-RIGHTS-AND-AGREEMENTS/
  06-DELIVERY-PACKAGES/
  07-BACKUP-VERIFICATION/
```

## Publisher submission package
Book synopsis, author bio, title/edition/ISBN if applicable, editable manuscript if requested, approved PDF, print-ready cover with specifications, rights declaration, sample chapters, publisher correspondence where appropriate, dated manifest. Include only what recipient requests; review confidentiality first.

## Game handoff package
Full version-controlled source, build instructions and dependencies, verified assets/licenses, version/build identifiers, tested release build, privacy policy, store metadata and screenshots, QA report, dated manifest. Never include keystore secrets or credentials in shared packages.

## Video handoff package
Original master, final approved render, script/storyboard, subtitle files, thumbnail, audio/source license evidence, aspect ratio, duration, export settings, dated manifest. Avoid sharing unlicensed assets.

## Readiness statuses
- VERIFIED PATH: file fetched at exact location; may not be approved or backed up.
- APPROVED MASTER: content/version approved by project owner.
- BACKED UP: independent copy verified.
- HANDOFF READY: requested deliverables assembled and checked.
- MISSING/UNVERIFIED: location, contents, approval, or backup not yet confirmed.

## Release gate
Do not mark HANDOFF READY without approval, content check, delivery file integrity check, rights check, and verified independent backup.
