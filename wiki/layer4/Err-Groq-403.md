# Groq returns `403 error 1010`

Audio transcription fails with an HTTP 403 whose body mentions `error 1010`.

## What it is not

It is **not** an invalid API key. A bad key returns `401 Unauthorized`. Chasing
the key is the usual wasted hour.

## What it is

`error 1010` is Cloudflare rejecting the request because of its **user-agent**.
Groq sits behind Cloudflare, and a client that sends a bare or unusual
user-agent (Python's default `python-urllib/3.x`, or an empty one) gets blocked
before the request reaches Groq's API.

## Fix

Send a normal browser-like user-agent:

```bash
curl https://api.groq.com/openai/v1/audio/transcriptions \
  -H "Authorization: Bearer $GROQ_API_KEY" \
  -H "User-Agent: Mozilla/5.0" \
  -F file=@voice.m4a \
  -F model=whisper-large-v3 \
  -F language=fa
```

In Python:

```python
headers = {
    "Authorization": f"Bearer {key}",
    "User-Agent": "Mozilla/5.0",          # ← the fix
}
```

## The other Groq limits, for reference

| Limit | Value | Symptom if exceeded |
|---|---|---|
| file size | 25 MB | `413` or a truncation warning |
| request rate | per plan | `429 Too Many Requests` |
| audio length | ~10 min per file comfortably | timeout or empty transcript |

For a file over 25 MB, split before sending:

```bash
ffmpeg -i long.m4a -f segment -segment_time 600 -c copy part-%03d.m4a
```

600 seconds keeps each part well inside both the size and length limits, and
`-c copy` means no re-encoding — fast and lossless.

## Verify the key separately

```bash
curl -s https://api.groq.com/openai/v1/models \
  -H "Authorization: Bearer $GROQ_API_KEY" \
  -H "User-Agent: Mozilla/5.0" | head -c 200
```

A model list means the key is fine and the problem was the user-agent. A `401`
means the key itself is wrong.

## Persian quality note

`whisper-large-v3` with `language=fa` handles Persian well. Smaller models
(`whisper-large-v3-turbo`) are faster and noticeably worse on Persian
technical vocabulary — equipment names and contract terms come out
transliterated. For maintenance and contract audio, use the full model.

## After transcription

The transcript is a sidecar, and the sidecar is what gets indexed:

```
raw/audio/voice-1405-08-20.m4a
raw/audio/voice-1405-08-20.transcript.md
```

```bash
python3 ~/archive/doclib.py add \
  ~/archive/collections/office-works/raw/audio/voice-1405-08-20.transcript.md \
  -c office-works
```

The audio file itself is never indexed — it is kept as the original evidence,
so a disputed transcript can be re-checked against the recording.
