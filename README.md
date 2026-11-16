# hi-ai-models

The model list that hi.ai uses. One file, `catalog.json`: the local models hi.ai offers (with download size, memory needed, licence and source), the embedding models for the brain, and the cloud subscriptions and pay as you go offers with a link to each official page.

hi.ai carries a copy of this list, so it works offline. Once a day while it runs, it fetches the newest one from here and keeps it only when three things are true:

1. The file `catalog.json.sig` is a valid ed25519 signature over the exact bytes of `catalog.json`, made with the key below.
2. The "checked" day in the file is newer than the day in the copy built into hi.ai.
3. `schema_version` in the file is the number this hi.ai reads (now 1), and every id, repo, file name, pooling and version is a plain name on hi.ai's allow-list: letters, digits and a few marks, nothing a shell, a path or an option flag could use. `catalog.schema.json` writes the format down for CI.

A file that fails any test is thrown away and the built-in list stays. Every entry names its source and the day it was checked.

## The public key

```
3b244186654a352e7bfbc2559a47752dd93b11bcb582c87e6ec7dbe52118d7b4
```

The signature file holds the signature as hex text.

## Check a signature by hand

You need `openssl` 3 or newer and `python3` (no other tool).

```sh
curl -sO https://raw.githubusercontent.com/thejocorp/hi-ai-models/main/catalog.json
curl -sO https://raw.githubusercontent.com/thejocorp/hi-ai-models/main/catalog.json.sig
# the public key in DER form (the fixed ed25519 header plus the 32 key bytes) and the signature as raw bytes
python3 -c "import sys;open('hi-ai-models.pub.der','wb').write(bytes.fromhex('302a300506032b6570032100'+'3b244186654a352e7bfbc2559a47752dd93b11bcb582c87e6ec7dbe52118d7b4'));open('catalog.json.sig.bin','wb').write(bytes.fromhex(open('catalog.json.sig').read().strip()))"
openssl pkeyutl -verify -pubin -keyform DER -inkey hi-ai-models.pub.der -rawin -in catalog.json -sigfile catalog.json.sig.bin
```

It prints `Signature Verified Successfully`.

## What the signature does not prove

The signature proves the file came from the key holder. It does not prove each fact is still true at its source; the "checked" day says when it was last looked at.

## Checks before a change

`pip install jsonschema && python3 validate.py` checks `catalog.json` against `catalog.schema.json` and refuses anything that looks like a shell command. GitHub Actions runs it on every push. After any change to `catalog.json`, sign it again (`catalog.json.sig`).

## Settings in hi.ai

- `HI_AI_CATALOG_URL`: where to fetch `catalog.json` from. Set it to an empty value to turn fetching off.
- `HI_AI_CATALOG_KEY`: the public key, in hex.

Both have defaults that point here.

## Licence

MIT, see `LICENSE`. The facts in the list belong to their makers; follow each source link.
