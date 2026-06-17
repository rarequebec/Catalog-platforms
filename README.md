# RARE.Qc Research Infrastructure Catalog

A bilingual (English / French) interactive web catalog for RARE.Qc research platforms and resources.

---

## Folder Structure

```
rare-qc/
├── data/
│   ├── platforms.json      ← Platforms data (auto-generated from Excel)
│   └── resources.json      ← Resources data (auto-generated from Excel)
├── app/
│   └── index.html          ← The complete web application (single file)
├── convert_data.py         ← Excel → JSON conversion script
└── README.md               ← This file
```

---

## How to Open the Catalog

Open `app/index.html` in any modern browser.  
The app loads `../data/platforms.json` and `../data/resources.json` automatically.

> **Note:** Because the app fetches local JSON files, you may need to serve it
> from a local HTTP server (not just double-click the file) in some browsers.
>
> Quick local server options:
> ```bash
> # Python (from inside the rare-qc/ folder)
> python3 -m http.server 8080
> # Then open: http://localhost:8080/app/
>
> # Node.js (npx)
> npx serve .
> ```

---

## Updating the Data

### Step 1 – Edit the Excel file

Open `List_of_resources_-_Platforms.xlsx` and make your changes:
- **Sheet 1 "Technology Platforms"** → platforms data
- **Sheet 2 "Resources"** → resources data

Keep the column headers exactly as they are. Add new rows anywhere below the header row.

### Step 2 – Run the conversion script

```bash
# From the rare-qc/ folder:
python3 convert_data.py

# Or specify a different file path:
python3 convert_data.py path/to/UpdatedExcel.xlsx
```

Requirements: `pip install pandas openpyxl`

### Step 3 – Done

The script writes updated `data/platforms.json` and `data/resources.json`.
Refresh the browser — the catalog automatically reflects the new data. **No code changes needed.**

---

## Adding New Entries

Simply add a new row to the correct Excel sheet with the appropriate column values, then re-run the converter. Fields can be left blank if unknown.

### Required fields (at minimum):
- **Institution** — the hosting organization
- **Platform / Department** — the name of the platform or core facility
- **Description** — a brief explanation of what the platform offers

---

## Bilingual Support

The UI language toggles between English and French using the button in the top-right corner.

- **UI labels** are fully translated (stored in the `i18n` object in `index.html`)
- **Data fields** (descriptions, platform names) are displayed as-is from the data file
- To add bilingual descriptions: add a `description_fr` field to the JSON entries and update the card rendering logic in `index.html` to display `description_fr` when `lang === 'fr'`

To add or modify a UI translation:
1. Open `app/index.html`
2. Find the `const i18n = { en: {...}, fr: {...} }` block
3. Add or edit the key in both `en` and `fr` sections

---

## Filters Available

| Filter | Source field |
|---|---|
| Institution | `institution` |
| Scientific Domain | `domain` |
| Type | `type` |
| City | `city` |
| Access Type | `access` (keyword match) |
| Global search | All fields combined |

---

## Deploying to a Website

Upload the entire `rare-qc/` folder to any static web host (GitHub Pages, Netlify, institutional web server, etc.). No server-side code is required.

To update data on a live site: run the converter locally, then upload the new `data/platforms.json` and `data/resources.json` files only.

---

## Technical Notes

- **No framework dependencies** — vanilla HTML, CSS, JavaScript
- **No build step** — the app runs directly from the file system or any HTTP server
- **Data layer is fully separate** — replace JSON files to update without touching app code
- **Responsive** — works on desktop and mobile
- **Accessible** — keyboard-navigable, visible focus states, semantic HTML

