# Mehar Foundation website

Static production website for `meharfoundation.store`, designed for deployment on Hostinger Business Web Hosting.

## What the source document establishes

- Enterprise: Mehar Foundation
- Enterprise type: Micro
- Major activity: Manufacturing
- Registered activity: Finishing of man-made and blended textiles (NIC 13134)
- Business operations commenced: 20 April 2021
- Location: Katni district, Madhya Pradesh
- Udyam registration: UDYAM-MP-26-0037154

Private financial, PAN, bank, turnover and personal-status details from the supplied certificate are intentionally excluded from the public site.

## Project structure

```text
index.html
robots.txt
sitemap.xml
assets/
  styles.css
  script.js
  logo.svg
  favicon.svg
  images/
```

The site is buildless. The repository root is the complete deployable website so Hostinger Git deployment can detect `index.html` directly.

## Local preview

From the repository root:

```powershell
python -m http.server 4173
```

Then open `http://localhost:4173`.

## Hostinger deployment

1. Open Hostinger hPanel.
2. Go to Websites, select `meharfoundation.store`, then open File Manager.
3. Open the domain's `public_html` directory.
4. Upload the repository website files into `public_html`, or use Hostinger Git deployment from the `main` branch.
5. Confirm `public_html/index.html` exists.
6. Enable the free SSL certificate and force HTTPS in Hostinger.
7. Verify the home page, phone, email, WhatsApp, mobile menu and enquiry form.

## Content notes before launch

- The enquiry form opens the visitor's email client and stores no data.
- The photography was generated specifically for this website and should be treated as representative brand imagery, not documentary photography of the actual facility.
- Confirm the public phone number, email address and preferred wording for services before the final DNS launch.
