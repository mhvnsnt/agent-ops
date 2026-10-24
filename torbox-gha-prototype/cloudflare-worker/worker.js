// OPTIONAL dumb Range proxy — NOT a transfer engine. Read the verdict in
// ../../torbox-lane4-compute.md before deploying this.
//
// What it can do on Workers Free (100k req/day, 10 ms CPU/invocation,
// 128 MB RAM, 50 subrequests): pass ONE Range request through untouched.
// CPU time is not charged while waiting on the network, and response body
// size is not enforced, so a pure pass-through survives. What it cannot
// do: parse a Zip64 central directory, decompress, hash 350 GB, or drive
// uploads.github.com — the 10 ms CPU cap kills any real work per request.
//
// Its one legitimate job: URL laundering. The bearer CDN link lives as a
// Worker secret (set in the Cloudflare dashboard by a human, never in
// chat / git / wrangler.toml). Callers authenticate with a revocable
// PROXY_KEY instead of ever seeing the real link, and forward a Range.
//
// Secrets (Cloudflare dashboard -> Worker -> Settings -> Variables):
//   SOURCE_URL  (secret)  the CDN / debrid link
//   PROXY_KEY   (secret)  any random string the caller must present
export default {
  async fetch(request, env) {
    if (request.headers.get("x-proxy-key") !== env.PROXY_KEY) {
      return new Response("forbidden", { status: 403 });
    }
    const range = request.headers.get("range");
    if (!range) return new Response("Range header required", { status: 400 });
    const upstream = await fetch(env.SOURCE_URL, {
      headers: { Range: range, "User-Agent": "Mozilla/5.0" },
      redirect: "follow",
    });
    // Stream the body straight through; never buffer it.
    return new Response(upstream.body, {
      status: upstream.status,
      headers: {
        "Content-Range": upstream.headers.get("Content-Range") || "",
        "Content-Length": upstream.headers.get("Content-Length") || "",
        "Accept-Ranges": "bytes",
      },
    });
  },
};
