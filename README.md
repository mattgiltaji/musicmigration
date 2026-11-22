# musicmigration

Used to move song playcount metadata from the Apple Music app to a navidrome instance.

[![LICENSE](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Unfortunately the Apple Music app (local only, not the website)
does not store its library in an easily accessible xml like iTunes did.
And since I'm on a windows machine, I don't have the Apple Music SDKs available on a mac.
So we get the playcount data out of Apple Music via **manual data entry** into an excel sheet, 
then use this script to process the excel sheet and repeatedly hit the relevant navidrome APIs for scrobbling.


## Prep

Set up navidrome credentials and url in the .env file.

Populate the excel sheet with artist, album, song title, playcount, and last played time

## Test

pytest command tbd

## Go!

```
uv run --env-file .env musicmigration
```
