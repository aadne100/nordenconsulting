# Audit og medieplan

## Utgangspunkt

Den gamle forsiden samlet HTML, stil, logikk og omtrent 1,4 MB innhold i én fil, med bilder som base64. Det gjorde bildene vanskelige å cache separat og tilpasse skjermbredden. Redesignen skiller innhold, stil, funksjoner og medier. Ingen ytelsesscore for den gamle siden er antatt.

Designet bruker fortsatt Syne, DM Sans, mørk bakgrunn og turkis fra den originale logoen. Hovedendringen er tydeligere typografi, asymmetrisk portefølje og færre samtidige valg. Den viktigste handlingen, «Kontakt meg nå», er tilgjengelig i den faste toppmenyen.

## Kuratering

| Plassering | Utvalg og hensikt |
| --- | --- |
| Første skjerm | Ett ekte dronefoto. Ingen tung film lastes her. |
| Forsidens portefølje | Friluftsfoto, to korte produktfilmer, drone, bil og bak kameraet. Filtrering etter type. |
| Bildearkiv | Alle 207 Dropbox-bilder fordeles i seks serier. Samlingene åpnes ved behov. |
| Bak kameraet | Seks eksisterende bilder av Ådne, arbeid og utstyr fra den gamle siden. |
| Tjenester | Fire redaksjonelle grupper som samlet dekker alle oppgitte tjenester. |

| Bildeserie | Antall originalbilder |
| --- | ---: |
| Friluft | 37 |
| Vinter | 33 |
| Livsstil | 33 |
| Team HLA | 56 |
| Drone | 34 |
| Bil | 14 |
| Sum Dropbox-bilder | 207 |

Nære varianter beholdes i arkivet, men gjentas ikke som hovedmotiver på forsiden. Ingen fotografier erstattes med genererte bilder. Kunder og resultater uten bekreftelse er ikke lagt til.

## Video

Hver film får `/assets/video/<prosjekt>/full.mp4`, `full.webm` når det gir merkbar reduksjon, `preview.mp4` og `poster.webp`. MP4 bruker H.264/AAC og faststart. Full film lastes først når den åpnes. Forhåndsvisningen er stille, har pauseknapp og starter bare når kortet er synlig. Redusert bevegelse viser poster.

| Tilgjengelig film | Format | MP4 full | WebM full | Preview |
| --- | --- | ---: | ---: | ---: |
| Rab vest | 9:16, ca. 7,5 sekunder | 2,67 MB | 1,45 MB | 0,11 MB |
| KAVU skjorte | 9:16, ca. 8,4 sekunder | 3,03 MB | 1,53 MB | 0,16 MB |

Disse tallene er fra den første ffmpeg-eksporten. Endelig filkontroll dokumenteres i teststatus. Den stående Rab vest-filmen er ikke den etterspurte liggende Rab-reklamen.

## Seks originalfilmer som mangler i den gjennomgåtte leveransen

| Tittel | Format | Klargjort filplassering |
| --- | --- | --- |
| Stereo Skis reklame | 16:9 | `assets/video/stereo-skis/` |
| Rab reklame | 16:9 | `assets/video/rab-reklame/` |
| Bolletest | 9:16 | `assets/video/bolletest/` |
| Patagonia påske | 9:16 | `assets/video/patagonia-paske/` |
| Pinneskitur | 9:16 | `assets/video/pinneskitur/` |
| Madshus ski | 9:16 | `assets/video/madshus-ski/` |

Det legges ikke inn tomme videokort eller lenker til filer som ennå ikke finnes. Ådne laster opp originalene i Dropbox. Deretter eksporteres, kontrolleres og legges de til i porteføljen, egne filmsider, sitemap og VideoObject. Bekreft kundetilknytning og publiseringsdato samtidig. Originalfilens eksportdato er ikke automatisk publiseringsdato.

Budsjett for seks nye filmer: inntil 150 MB MP4 og 12 MB preview, pluss eventuelle WebM-filer og postere. Nåværende optimaliserte mediesett ble målt til omtrent 33 MB ved første eksport, mot omtrent 2,30 GB originalmateriale. Det planlegges derfor ingen betalt videohosting nå. Faktiske sluttstørrelser skal kontrolleres før merge. Ingen enkeltfil skal nærme seg 100 MB, og repoet skal holdes under 1 GB. Hvis videre materiale sprenger budsjettet, skal R2/Bunny vurderes og kostnader avklares før flytting.

## Bevegelse og tilgjengelighet

CSS-overganger, vanlig smooth scroll og IntersectionObserver er nok for dette innholdet. GSAP, Lenis, en egen musepeker og en låst horisontal scroll er valgt bort for å holde mobilnavigasjon og lasting enkel. Ingen innlastingsskjerm blokkerer innholdet. Videoene har kontroller og en kort tekstbeskrivelse. Dialoger kan lukkes med Escape, har navngitte knapper og returnerer fokus til åpneren.
