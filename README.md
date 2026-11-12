# Norden Consulting

Statisk portefølje for Ådne Bjella. HTML, CSS og JavaScript, uten byggesteg.

## Se redesignen lokalt

```sh
git clone --branch redesign/norden-portfolio https://github.com/aadne100/nordenconsulting.git
cd nordenconsulting
python3 -m http.server 8000
```

Åpne http://localhost:8000. Bruk en lokal webserver, ikke dobbeltklikk HTML-filen: sidene bruker stier fra nettstedets rot.

Endringene gjennomgås i [pull request #1](https://github.com/aadne100/nordenconsulting/pull/1). `main` og den publiserte siden oppdateres først etter Ådnes godkjenning. CNAME og DNS skal ikke endres.

## Filer

- `index.html`: forside, porteføljefilter og kontaktskjema.
- `css/site.css` og `js/site.js`: felles stil og interaksjon.
- `arbeid/foto/`: bildeserier sortert etter motiv.
- `arbeid/rab-vest/` og `arbeid/kavu-skjorte/`: egne filmsider.
- `assets/img/`, `assets/video/`, `assets/fonts/`: faktiske filer, ingen base64 eller eksterne videospillere.
- `personvern/`, `sitemap.xml`, `robots.txt`, `404.html`: informasjon og søkemotorgrunnlag.
- `docs/`: medieplan, avgrensninger og teststatus.
- `tools/encode-video.py`: valgfri ffmpeg-hjelper for nye originalfilmer. Den brukes ved innholdsarbeid, ikke ved publisering.

## Kontakt

Formspree-endepunktet er uendret: `https://formspree.io/f/xeenpybw`. Feltene heter `navn`, `epost`, `bedrift` og `melding`. JavaScript legger også ved `email` fra `epost` for svaradressen. Skjemaet har vanlig POST som reserve hvis JavaScript ikke er tilgjengelig.

Telefon: 905 27 474. E-post: adne@nordenconsulting.no.

## Nye filmer

Se [medieplanen](docs/media-plan.md). Originaler skal beholdes i Dropbox. Legg bare nettoptimaliserte versjoner i repoet. Ikke bruk Git LFS eller YouTube-nedlasting. Nye prosjekter skal først få synlige kort når filene faktisk finnes og kan spilles.

## Før publisering

Se [teststatus](docs/verification.md). Gjør en reell Formspree-test og kontroller mottak, sjekk begge filmene på iPhone/Safari og kjør Lighthouse på den endelige versjonen. Godkjenn deretter PR-en. Ikke endre domeneoppsettet.
