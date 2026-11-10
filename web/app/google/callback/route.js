import { createCipheriv, createHash, randomBytes, timingSafeEqual } from "node:crypto";

const ttl = 300;
const headers = { "Cache-Control": "no-store", "Referrer-Policy": "no-referrer" };
const validState = (state) => typeof state === "string" && /^[a-zA-Z0-9]{30}$/.test(state);

function reply(message, status) {
  return new Response(message, { status, headers });
}

function authorized(request, secret) {
  const actual = Buffer.from(request.headers.get("authorization") ?? "");
  const expected = Buffer.from(`Bearer ${secret}`);
  return actual.length === expected.length && timingSafeEqual(actual, expected);
}

async function redis(...command) {
  const url = process.env.KV_REST_API_URL || process.env.UPSTASH_REDIS_REST_URL;
  const token = process.env.KV_REST_API_TOKEN || process.env.UPSTASH_REDIS_REST_TOKEN;
  if (!url || !token || new URL(url).protocol !== "https:") throw new Error("Redis unavailable");
  const response = await fetch(url, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
    body: JSON.stringify(command),
    cache: "no-store",
    redirect: "error",
    signal: AbortSignal.timeout(5000),
  });
  if (!response.ok) throw new Error("Redis unavailable");
  const data = await response.json();
  if (data.error) throw new Error("Redis command failed");
  return data.result;
}

const key = (state) => `maurice:google:${createHash("sha256").update(state).digest("hex")}`;

function seal(secret, state, payload) {
  const encryptionKey = createHash("sha256").update(`maurice-oauth-relay:${secret}`).digest();
  const iv = randomBytes(12);
  const cipher = createCipheriv("aes-256-gcm", encryptionKey, iv);
  cipher.setAAD(Buffer.from(state));
  const body = Buffer.concat([cipher.update(JSON.stringify(payload)), cipher.final()]);
  return Buffer.concat([iv, body, cipher.getAuthTag()]).toString("base64");
}

export async function GET(request) {
  const params = new URL(request.url).searchParams;
  const [state] = params.getAll("state");
  if (!validState(state) || params.getAll("state").length !== 1) {
    return reply("Start Google sign-in from your Maurice WhatsApp chat.", 400);
  }
  const secret = process.env.MAURICE_GOOGLE_RELAY_SECRET;
  if (!secret) return reply("Google sign-in is temporarily unavailable.", 503);
  const codes = params.getAll("code");
  const code = codes.length === 1 && codes[0].length <= 2048 && !params.has("error") ? codes[0] : "";
  try {
    const saved = await redis("EVAL",
      "if redis.call('GET', KEYS[1]) == 'pending' then return redis.call('SET', KEYS[1], ARGV[1], 'KEEPTTL') end",
      1, key(state), seal(secret, state, { code }));
    if (saved !== "OK") return reply("This link expired or was already used. Start again in WhatsApp.", 400);
    return reply(code ? "Google responded. Return to WhatsApp to check your connection." : "Google access was not granted.", 200);
  } catch {
    return reply("Google sign-in is temporarily unavailable.", 503);
  }
}

export async function POST(request) {
  const secret = process.env.MAURICE_GOOGLE_RELAY_SECRET;
  if (!secret) return reply("Google sign-in is temporarily unavailable.", 503);
  if (!authorized(request, secret)) return reply("Unauthorized", 401);
  try {
    const { state, action } = await request.json();
    if (!validState(state) || !["start", "read"].includes(action)) return reply("Invalid request", 400);
    if (action === "start") {
      const created = await redis("SET", key(state), "pending", "EX", ttl, "NX");
      return reply(null, created === "OK" ? 204 : 409);
    }
    const result = await redis("GET", key(state));
    return result && result !== "pending" ? reply(result, 200) : reply(null, 204);
  } catch {
    return reply("Google sign-in is temporarily unavailable.", 503);
  }
}
