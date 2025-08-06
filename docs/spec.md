### Background & Initial Observation

While casually browsing a video hosting site featuring spelling tutorials (commonly disguised as “family-themed drama”), I was particularly impressed by how swiftly the videos loaded. My technical curiosity was piqued—not by the content itself, but by the performance of the content delivery system behind it.

Using Chrome DevTools, I inspected the network activity and noticed a particularly interesting request routed through the following domain:

```
p21-ad-sg.ibyteimg.com
```

A quick analysis suggested the following structure in the domain name:

- `ad-sg`: Likely short for “ads” and “Singapore” (indicative of CDN location).
- `ibyteimg`: A strong indicator of affiliation with ByteDance (owner of TikTok), where `img` stands for image-related assets.

Further investigation via WHOIS and search engines traced this domain to **TikTok’s Business Center**, which offers services for advertisers, including image hosting and campaign management.

---

### Accessing TikTok’s Image Upload Endpoint

To validate this hypothesis, I created a test account on TikTok Ads. After exploring the platform, I located an image management page:

```
https://ads.tiktok.com/i18n/material/image
```

Here, TikTok provides an interface for advertisers to upload and manage media assets. By observing network requests during an upload action, I identified the backend API:

```
POST https://ads.tiktok.com/api/v2/i18n/material/image/upload/
```

Upon successful upload, the service returns a CDN-hosted image link—exactly in the format previously observed. However, I noticed that images were compressed and cropped, likely due to internal processing rules. To bypass these modifications, I replicated the exact POST request with custom-crafted payloads, which allowed me to upload arbitrary image files and receive raw links from TikTok’s CDN.

---

### Exploiting Image CDN for Video Hosting via HLS

The core discovery was that these CDN-hosted image URLs could be misused for delivering media content—**not just static images**. However, the TikTok Ads API strictly validates file content types, only allowing image uploads (e.g., `.jpg`, `.png`).

To circumvent this restriction, I exploited the following behavior:

- Created fake 1x1 PNG images (minimal size to pass validation).
- Embedded video data within HLS `.ts` (MPEG-TS) segments while disguising them as image references.
- Appended the resulting image URLs within `.m3u8` playlists (HLS manifests) as decoys.

By blending fake image URLs into the media playlist, the playback mechanism on web clients can still process video content—effectively using the TikTok CDN to serve pseudo-video streams.

---

### Implementation Strategy

1. **Upload Bypass**:

   - Use the TikTok Ads image upload API.
   - Prepare minimal fake `.png` images (1x1 pixel).
   - POST the image payloads and capture the returned CDN URLs.

2. **HLS Construction**:

   - Construct `.m3u8` playlist files referencing:

     - Regular `.ts` video segments (hosted elsewhere or embedded).
     - TikTok-hosted “image” links as part of playlist entries to obfuscate traffic.

3. **CORS Handling**:

   - Ensure that the temporary hosting location for the `.m3u8` playlist has `Access-Control-Allow-Origin: *` headers enabled for seamless cross-origin streaming.

4. **Distribution**:

   - Mass-upload fake image segments to TikTok CDN (automated via script).
   - Dynamically inject CDN links into playlist structure.
   - Serve the modified `.m3u8` to end users from a web player.

---

### Observations & Ethical Considerations

- This method effectively **offloads media delivery to TikTok's CDN**, reducing bandwidth usage and storage cost on the attacker’s infrastructure.
- It poses a **security risk** for TikTok if such misuse occurs at scale, potentially filling their image cache with gigabytes of disguised media content.
- The current implementation relies on **loose validation** of image uploads and permissive CORS settings from TikTok’s CDN endpoints.

---

### Potential Mitigation for TikTok

1. Implement strict **MIME-type and content inspection** for uploaded image payloads.
2. Set **file size limitations** and enforce pixel dimension checks on server-side.
3. Apply **rate limits** and anomaly detection for repeated uploads from unknown advertisers.
4. Monitor `.m3u8` pattern references pointing to CDN domains from non-partnered sources.

---
