# Teststatus

Oppdatert 11. november 2026. Dette er en testlogg, ikke en påstand om at alt er publisert.

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
- Begge eksisterende filmer spilte i Chromium før gjenoppretting av mediefilene. En feil med klikkflaten og en feil ved rask gjenåpning av filmdialog er rettet. Sluttkontroll av de gjenopprettede filene gjenstår.

## Gjenstår før merge

- Fullføre og kontrollere alle mediefiler i GitHub-branchen. Lenker og størrelser skal kontrolleres mot sluttversjonen.
- Reell Formspree-innsending og bekreftelse på mottatt e-post. De lokale simuleringene bekrefter bare grensesnittet.
- Avspilling på en fysisk iPhone/Safari. H.264/AAC, `playsinline` og faststart er valgt for kompatibilitet, men enhetstesten er ikke utført.
- Lighthouse mobil. Et tidligere forsøk kunne ikke starte Chrome i testmiljøet. Ingen Lighthouse-score, LCP eller 60 fps-måling er derfor oppgitt som bestått.
- Bekreftet dato for første publisering av filmene før `uploadDate` legges til i VideoObject. Eksportdato er ikke brukt som en oppdiktet publiseringsdato.
- Ådnes gjennomgang og godkjenning av pull request. DNS, CNAME og main skal forbli uendret frem til godkjent merge.

## Medier som kommer senere

Stereo Skis, liggende Rab-reklame, Bolletest, Patagonia påske, Pinneskitur og Madshus ski manglet i den gjennomgåtte leveransen. Siden viser ikke ødelagte kort for disse. Se medieplanen for filstier og videre innlegging.
