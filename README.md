# hi-ai-models

The model list that hi.ai uses. One file, `catalog.json`: the local models hi.ai offers (with download size, memory needed, licence and source), the embedding models for the brain, and the cloud subscriptions and pay as you go offers with a link to each official page.

hi.ai carries a copy of this list, so it works offline. Once a day it fetches the newest one from here and keeps it only when two things are true:

1. The file `catalog.json.sig` is a valid ed25519 signature over the exact bytes of `catalog.json`, made with the key below.
2. The "checked" day in the file is newer than the day in the copy built into hi.ai.

A file that fails either test is thrown away and the built-in list stays. Every entry names its source and the day it was checked.

## The public key

```
3b244186654a352e7bfbc2559a47752dd93b11bcb582c87e6ec7dbe52118d7b4
```

The signature file holds the signature as hex text.

## Check a signature by hand

You need `openssl` 3 or newer and `xxd`.

```sh
curl -sO https://raw.githubusercontent.com/thejocorp/hi-ai-models/main/catalog.json
curl -sO https://raw.githubusercontent.com/thejocorp/hi-ai-models/main/catalog.json.sig
# the public key in DER form: the fixed ed25519 header plus the 32 key bytes
( printf '302a300506032b6570032100' ; echo 3b244186654a352e7bfbc2559a47752dd93b11bcb582c87e6ec7dbe52118d7b4 ) \
  | xxd -r -p > hi-ai-models.pub.der
tr -d '[:space:]' < catalog.json.sig | xxd -r -p > catalog.json.sig.bin
openssl pkeyutl -verify -pubin -keyform DER -inkey hi-ai-models.pub.der -rawin -in catalog.json -sigfile catalog.json.sig.bin
```

It prints `Signature Verified Successfully`.

## Settings in hi.ai

- `HI_AI_CATALOG_URL`: where to fetch `catalog.json` from. Set it to an empty value to turn fetching off.
- `HI_AI_CATALOG_KEY`: the public key, in hex.

Both have defaults that point here.

## Licence

MIT, see `LICENSE`. The facts in the list belong to their makers; follow each source link.
