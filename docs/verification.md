# Teststatus

Oppdatert 13. november 2026. Dette er en testlogg, ikke en påstand om at alt er publisert.

## Kontrollert

- JavaScript består `node --check`.
- Alle seks HTML-sider har én h1, unike ID-er, gyldig JSON-LD og fungerende interne ankermål.
- Bilder har alt-attributt og eksplisitte dimensjoner. Videoer bruker `playsinline`, poster og `preload="none"` utenfor første skjerm.
- Chromium, responsiv testflate: 360, 768 og 1920 px. Ingen horisontal overflyt i dokumentet. 360 px er også inspisert visuelt med åpent kontaktskjema.
- Kontaktpanelet åpnes fra fast CTA, kan rulles på mobil og får fokus på lukkeknappen. Escape lukker og returnerer fokus.
- Skjemasuksess og avvist sending er testet med lokale simulerte HTTP-svar. Suksess viser bekreftelse og tømmer feltene. Feil beholder verdiene og viser reserveknapp og e-postmulighet. Ingen e-post ble sendt av disse testene.
- Innsendingsdata beholder `navn`, `epost`, `bedrift`, `melding`; `email` legges ved for svaradresse. Formspree-endepunktet er bevart.
- Første skjerm laster ingen av videofilene: videoelementene hadde ingen src og var pauset.
- Porteføljefilter «Film» viste to prosjekter i tidligere nettlesertest.
- En feil med klikkflaten og en feil ved rask gjenåpning av filmdialog er rettet.

- Én reell testhenvendelse ble sendt 12. november til det eksisterende Formspree-endepunktet. Tjenesten godtok innsendingen, siden viste bekreftelse og tømte feltene. Navn: «Teknisk test av Norden-nettsiden». Emne: «Ny henvendelse fra Norden Consulting». Innholdet var tydelig merket som teknisk test uten bestilling. Mottak i innboksen er ikke bekreftet. Ikke send en ny test bare for å gjenskape dokumentasjonen.
- De gjenopprettede KAVU- og Rab-filmene ble spilt i Chromium 12. november, både WebM og MP4. MP4-filene er dessuten dekodet helt med ffmpeg uten feil. Begge har H.264/AAC, 1080 × 1920 og faststart. Fem sekunders preview er uten lyd. Rask lukking og bytte mellom filmdialogene er kontrollert.

## Kontroll 13. november, etter bildeopprydding

- Galleriet er redusert til 12 bilder som peker til faktiske filer i GitHub-branchen. Siden har seks tematiske samlinger samt «Bak kameraet».
- Den opprinnelige metadataoversikten med 207 Dropbox-bilder er bevart i `docs/full-photo-manifest.json` og vises ikke som ødelagte bildehenvisninger.
- Aktiv `assets/media.json` er filtrert til bilder med begge filvariantene til stede.
- Tjenestene har nå egne dekorative, tilgjengelighetsskjulte SVG-ikoner.
- SEO-tittel, meta-beskrivelse og JSON-LD-tjenestekatalog er oppdatert. JSON-LD ble pars-et uten feil.
- Dette er kode- og referansekontroller, ikke en ny fullstendig nettleser- eller Lighthouse-test.

## Gjenstår før merge

- Kjør siste sidetest og kontroller at mediefilene har riktige URL-er. Flere originale bilder og filmer kan importeres senere uten ødelagte referanser.
- Ådne bekrefter mottak i innboksen av den allerede innsendte testhenvendelsen.
- Avspilling på en fysisk iPhone/Safari. H.264/AAC, `playsinline` og faststart er valgt for kompatibilitet, men enhetstesten er ikke utført.
- Lighthouse mobil. Et tidligere forsøk kunne ikke starte Chrome i testmiljøet. Ingen Lighthouse-score, LCP eller 60 fps-måling er derfor oppgitt som bestått.
- Bekreftet dato for første publisering av filmene før `uploadDate` legges til i VideoObject. Eksportdato er ikke brukt som en oppdiktet publiseringsdato.
- Publisering er autorisert av eier. Bekreft publiseringsløsningen og produksjonsdomener før main endres.

## Medier som kommer senere

Stereo Skis, liggende Rab-reklame, Bolletest, Patagonia påske, Pinneskitur og Madshus ski manglet i den gjennomgåtte leveransen. Siden viser ikke ødelagte kort for disse. Se medieplanen for filstier og videre innlegging.

## Siste kontroll, 13. november 2026

- Tjenesteseksjonen har fire dekorative, tilgjengelighetsnøytrale SVG-ikoner som bruker gjeldende Norden-farge.
- Forsidens JSON-LD er oppdatert med en tjenestekatalog. Den ble parsret som gyldig JSON etter endringen.
- `assets/media.json` har 207 bilder med fullversjon og miniatyr. Sammenligning mot GitHub-treet viste 411 manglende referanser. Dette er en **publiseringsblokkering**.
- `tools/check-site.py` kontrollerer nå også alle manifestbildene, og `.github/workflows/validate.yml` er lagt til for automatiske PR-/push-kontroller.
- Kildemateriale til foto og flere videoer er funnet i Dropbox; se `docs/media-plan.md`.
- Vercel-tilgangen viser ikke Norden Consulting som prosjekt. `CNAME` i GitHub er `nordenconsulting.no`, men dette alene bekrefter ikke hvilken hosting som leverer domenet. Publiseringsmålet må derfor bekreftes før release.

**Status:** Ikke klar for merge/publisering. Ingen endringer er gjort i `main`, DNS eller domenet.
