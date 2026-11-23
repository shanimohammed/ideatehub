# Putting the Ideate Hub site online

The finished website is the **`site`** folder. The same files are zipped in **`ideate-hub-site.zip`**.
It's a plain static site: one `index.html` plus images. It needs no database, no WordPress and no server code, so any web host can run it.

## What's in the package

| Path | What it is |
|---|---|
| `index.html` | The whole website |
| `images/` | Logos, case study images and studio artwork |
| `assets/favicon.png`, `assets/apple-touch-icon.png` | The amber "e" icon shown in browser tabs and on phone home screens |
| `assets/share.jpg` | The image shown when the link is shared on WhatsApp, Facebook or LinkedIn |
| `robots.txt` | Lets search engines index the site |

## Option 1: Netlify (free, about 5 minutes, easiest)

1. Go to **app.netlify.com/drop** and create a free account.
2. Drag the **`site`** folder (not the zip) onto the page.
3. You get a live address like `ideate-hub.netlify.app` straight away.
4. To use your own domain, go to **Domain management → Add a domain** and follow the steps. Netlify adds HTTPS for free.

To update the site later, drag the new `site` folder onto **Deploys** in your Netlify project.

## Option 2: Your web host's cPanel (if you already pay for hosting)

Many Ghanaian hosts use cPanel, including Truehost, Web4Africa and GhanaHost.

1. Log in to cPanel and open **File Manager**.
2. Open the **`public_html`** folder. If it has an old site, move those files into a backup folder first.
3. Click **Upload** and upload **`ideate-hub-site.zip`**.
4. Right-click the zip, choose **Extract**, then delete the zip.
5. Check that `index.html` sits directly inside `public_html`, not inside a subfolder.
6. In cPanel, turn on free HTTPS under **SSL/TLS Status** or **Let's Encrypt**.

## Option 3: GitHub Pages (free)

1. Create a new repository on github.com and upload the **contents** of the `site` folder.
2. Go to **Settings → Pages**, set the source to the `main` branch, and save.
3. The site goes live at `yourname.github.io/repository-name`. You can add a custom domain on the same settings page.

## After you have a domain

Rebuild once with your domain, so link previews on WhatsApp and Facebook show the share image reliably:

```bash
python3 build.py https://www.yourdomain.com
```

Then upload the new `site` folder again.

## Making changes later

1. Edit `index.html`. It is the source file, so don't edit `site/index.html` directly.
2. To add an image, put it in `images/` and reference it as `images/name.jpg`.
3. Run `python3 build.py` to rebuild the `site` folder and the zip.
4. Upload the new `site` folder.

## Still to add

- **TikTok and X links.** Copy one of the existing social links in the "Follow us" list in `index.html` and change the address and name.
