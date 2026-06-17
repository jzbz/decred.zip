# decred.zip

> An archive of Decred resources.

A small, static directory site that indexes Decred ecosystem websites,
explorers, tools, and governance.

## How it works

The list of resources lives in one human-editable file,
[`resources.txt`](resources.txt). A tiny build script reads it and writes a
static `index.html`. There is **no framework and no dependencies** — just
Python 3 to run the generator, and any static file host to serve the result.

```
resources.txt   ──build.py──▶   index.html
  (you edit)                      (generated)
```

## Add or edit a resource

1. Open [`resources.txt`](resources.txt) and add a line under the section you want:

   ```
   ## Tools

   timestamply.org | Anchor a file's hash to the Decred blockchain.
   ```

   - Format is `domain | description` — the domain becomes both the link
     text and the target (`https://` is added automatically).
   - Start a new section with a line beginning `## `.
   - Need a link target different from the displayed name? Use the
     three-field form: `name | https://full-url | description`.
   - Lines starting with `#` are comments; blank lines are ignored.

2. Regenerate the page:

   ```bash
   python3 build.py
   ```

3. Commit `resources.txt` **and** the regenerated `index.html`.

## Preview locally

```bash
python3 -m http.server 8765
# then open http://localhost:8765
```

## Files

| File            | Purpose                                            |
| --------------- | -------------------------------------------------- |
| `resources.txt` | Source of truth — the editable resource list.      |
| `build.py`      | Generates `index.html` from `resources.txt`.       |
| `index.html`    | Generated output. Do not edit by hand.             |
| `styles.css`    | Hand-written CSS (dark theme, blue→teal accent).   |
| `dcr.svg`       | Decred logo, used as the SVG favicon and header.   |
| `favicon.ico`   | Fallback favicon.                                  |

The site includes a client-side filter box, but the page works fully without
JavaScript — every resource is in the static HTML.
