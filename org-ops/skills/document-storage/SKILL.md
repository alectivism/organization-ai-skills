---
name: document-storage
description: "Read, edit, upload, and locally sync documents in your organization's SharePoint/OneDrive or Google Drive. Use for 'update the file on [platform]', 'save this to [platform]', 'edit this document in place', or when someone asks to set up local access to a site or shared drive. For just locating a document, use document-find instead."
status: template
---

> **Template skill.** Fill in the [BRACKETED] placeholders with your organization's details — or paste your org context and ask Claude to populate them for you.

# Document Storage — [YOUR ORGANIZATION]

This skill covers reading, editing, uploading, and locally syncing documents once you
know where they live. Use `document-find` first if you don't yet know the location.

**Tenant/workspace:** `[yourorg.sharepoint.com]` (Microsoft 365) or `[yourorg.com]`
Google Workspace domain, whichever your org runs.

## Which route to use

Two routes reach the same files. Try them in this order and stop at the first that works.

1. **A first-party connector (default).** Both Claude and ChatGPT support Microsoft 365
   and Google Drive connectors that read and write files directly, no install. Check it
   is connected before anything else: run one search call. If the tool is missing, send
   the person to their platform's connector settings, have them connect it, and wait.
2. **A locally synced folder (backup).** Only when the connector cannot do the job (see
   limits below) or the person already has the site or drive synced locally. On macOS,
   Microsoft 365 sync lands under `~/Library/CloudStorage/OneDrive-[YOUR ORG]/<Site> -
   Documents/…`; Google Drive sync lands under `~/Library/CloudStorage/GoogleDrive-
   [account]/My Drive/…` or a shared drive folder. If the folder does not exist, run the
   setup wizard at the end of this file.

There is no third route. Do not install or suggest a separate Microsoft Graph or Google
Drive API MCP server on top of the connector. Tool names below describe the Microsoft
365 connector's shape; a Google Drive connector's tool names differ but the same
find/read/write/limits structure applies. In ChatGPT the same routes exist through its
own connectors, with different tool names and, for Microsoft 365, no folder-create or
delete.

## Route 1: the connector

**Find:** a content/filename/metadata search, with filters (author, file type, folder,
modified-after) that AND together. A separate folder-search call finds folders by
partial name. Unscoped search covers every site, drive, or shared drive the person can
see, so scope only when the request names a team or region or when results need
narrowing. (This is the `document-find` skill's job in more depth — reach for that
skill first if you're not sure where the file is.)

**Read:** fetch by the file/item ID a search result returns. Office files and PDFs come
back as extracted text, paged for long documents; follow the "truncated, re-call with
the next page" pattern if one appears. Folder references list their contents.

**Write:**
- An upload call creates a file in a folder (needs the folder's drive/parent ID from a
  folder search). Default is fail-on-conflict; use a rename option for a safe copy, an
  overwrite/replace option only when the person has said to overwrite.
- An update call replaces an existing file's content in full. Libraries with versioning
  keep the old version in history.
- Create-folder, rename, move, copy, and delete calls do what their names say. Confirm
  before delete or replace: state the file, the location, and what is lost.

**Limits that decide the route:**
- Connectors cap upload/update size (roughly 1 MB for Microsoft 365's connector, check
  your platform's current limit), with no chunking. Larger files go through Route 2.
- Text payloads (Markdown, CSV, JSON, .txt) upload as plain content. Office and PDF
  files must be a complete binary; plain text under a `.docx` name is refused. Build the
  file first (python-docx, openpyxl, python-pptx, or your own document-building skill if
  you have one), then encode it as the connector expects.
- Reading returns extracted text, never the original bytes. To edit a Word or Excel
  file in place while keeping its formatting, work on the local copy (Route 2) or
  rebuild the file and re-upload it.
- Per-user write rate limits apply. For batches, pace the calls and retry after a short
  pause.

## Route 2: the synced local folder

The editor is the same either way (python-docx, openpyxl, python-pptx); this route only
changes where the bytes live.

- Files in a sync folder are usually online-only placeholders. Opening the path
  downloads the file; saving to the same path re-uploads it and preserves the link back
  to the source.
- Before editing, check for a lock file in the same folder (`ls | grep '~\$'` for
  Office files). If one exists, someone has it open: stop and tell the person.
- After editing, save a dated copy outside the sync folder, re-open the file to confirm
  the change landed on disk, and tell the person to verify through Finder/Explorer
  rather than the app's Open Recent list, which can show a stale cloud copy.

## Sites / shared drives

Map your organization's structure here — sites for Microsoft 365, shared drives for
Google Workspace:

| Need | Site/Drive | Path |
|---|---|---|
| Staff directory, org chart, brand kit | [e.g., Company Intranet] | `[/sites/... or drive link]` |
| [Department 1] materials | [Name] | `[path or URL]` |
| [Department 2] materials | [Name] | `[path or URL]` |
| Event materials | [Name] | `[path or URL]` |
| Reports, studies, research | [Name] | `[path or URL]` |
| Board materials, governance | [Name] | `[path or URL]` |
| [Region]-owned work | [Name] | `[path or URL]` |
| [Add your key sites/drives] | | |

Note each site or drive's default library/folder name (e.g. Microsoft 365's default is
usually `Shared Documents`), and flag any that are access-restricted so the agent asks a
member of that team to confirm rather than guessing. Verify this table against your own
tenant periodically: site structures and permissions drift.

## Common locations

List your organization's most frequently needed files:
- Brand kit: `[path or URL]`
- Research reports: `[path or URL]`
- Event materials: `[path or URL]`
- Board materials: `[path or URL]`

## Setup wizard: sync a site or drive to a local machine

Run this when Route 2 is needed and the sync folder is missing the site or drive.
One site/drive at a time, in the person's own browser.

1. Confirm the sync app (OneDrive, or Google Drive for desktop) is installed and signed
   in with their org account. If not, they install it and sign in first.
2. Open the site's document library, or the shared drive, for them using the path from
   the Sites/Drives table above. For a subfolder, open that folder.
3. Tell them to use the platform's "add shortcut" / "add to my drive" action (Microsoft
   365: **Add shortcut to OneDrive** in the command bar, in **More** if the bar is
   narrow; Google Drive: **Add shortcut to Drive**). A full **Sync** option also works
   but is heavier. Do not click it for them.
4. Wait, then check the local sync folder for a new entry named after the library or
   drive. Report the exact path you found.
5. Repeat for each site or drive they work in.

The new folder shows files as online-only placeholders. That is expected; opening one
downloads it.
