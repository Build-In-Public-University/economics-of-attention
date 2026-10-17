const MAX_JSON_BYTES = 12_000;
const ALLOWED_EVENTS = new Set(['click', 'play_start', 'stimulus_ready', 'result', 'context_demo', 'context_request']);
const ALLOWED_HOOK = /^[a-z0-9_-]{1,48}$/;
const ALLOWED_ATTR = /^[a-zA-Z0-9._~:/?#\[\]@!$&'()*+,;=%-]{0,160}$/;

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store'}
  });
}

function boundedString(value, max = 120) {
  return typeof value === 'string' ? value.slice(0, max) : null;
}

export async function onRequestPost({request, env}) {
  const length = Number(request.headers.get('content-length') || 0);
  if (length > MAX_JSON_BYTES) return json({error: 'payload_too_large'}, 413);
  let body;
  try { body = await request.json(); } catch { return json({error: 'invalid_json'}, 400); }
  const eventName = boundedString(body.event_name, 24);
  if (!ALLOWED_EVENTS.has(eventName)) return json({error: 'invalid_event_name'}, 400);
  const runId = boundedString(body.run_id, 80);
  const participantId = boundedString(body.participant_id, 100);
  if (!runId || !participantId) return json({error: 'run_and_participant_required'}, 400);
  const hookId = boundedString(body.hook_id || 'unknown', 48);
  if (!ALLOWED_HOOK.test(hookId)) return json({error: 'invalid_hook_id'}, 400);
  const attribution = {};
  for (const key of ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content']) {
    const value = boundedString(body.attribution?.[key], 160);
    if (value && ALLOWED_ATTR.test(value)) attribution[key] = value;
  }
  const artifact = {};
  for (const key of ['progressive_sha256', 'question_set_sha256', 'protocol_sha256', 'control_pdf_sha256']) {
    const value = boundedString(body.artifact?.[key], 128);
    if (value) artifact[key] = value;
  }
  const now = new Date().toISOString();
  const eventId = crypto.randomUUID();
  const values = [
    eventId, eventName, now, runId, participantId, boundedString(body.variant, 32), hookId,
    boundedString(body.arm, 24), body.prior_exposure === true ? 1 : body.prior_exposure === false ? 0 : null,
    Number.isInteger(body.reading_seconds) ? Math.max(0, Math.min(body.reading_seconds, 86400)) : null,
    Number.isInteger(body.quiz_response_seconds) ? Math.max(0, Math.min(body.quiz_response_seconds, 86400)) : null,
    Number.isInteger(body.score) ? Math.max(0, Math.min(body.score, 5)) : null,
    JSON.stringify(attribution), JSON.stringify(artifact)
  ];
  await env.EVENTS.prepare(`INSERT INTO events (
    event_id,event_name,occurred_at,run_id,participant_id,variant,hook_id,arm,prior_exposure,
    reading_seconds,quiz_response_seconds,score,attribution_json,artifact_json
  ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`).bind(...values).run();
  return json({accepted: true, event_id: eventId});
}

export async function onRequestGet({env}) {
  const row = await env.EVENTS.prepare('SELECT COUNT(*) AS event_count FROM events').first();
  return json({ok: true, event_count: row?.event_count ?? 0});
}
