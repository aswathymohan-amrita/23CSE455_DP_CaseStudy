/** Read text from saved provider events using the selected function. */
import { readFileSync } from 'node:fs';
import { pathToFileURL } from 'node:url';

function* streamClaude(events) {
  for (const event of events) {
    const delta = event.delta;
    const text = event.type === 'content_block_delta' &&
      delta && typeof delta === 'object' && delta.type === 'text_delta'
      ? delta.text : null;
    if (typeof text === 'string' && text) yield text;
  }
}

function* streamOpenAI(events) {
  for (const event of events) {
    const choices = event.choices;
    const delta = Array.isArray(choices) && choices[0] &&
      typeof choices[0] === 'object' ? choices[0].delta : null;
    const text = delta && typeof delta === 'object' ? delta.content : null;
    if (typeof text === 'string' && text) yield text;
  }
}

function* streamGemini(events) {
  for (const event of events) {
    if (typeof event.text === 'string' && event.text) yield event.text;
  }
}

const strategies = { claude: streamClaude, openai: streamOpenAI, gemini: streamGemini };

export function run(input) {
  if (input === null || typeof input !== 'object' || Array.isArray(input)) {
    return { error: 'input must be an object' };
  }
  if (typeof input.provider !== 'string') return { error: 'provider must be a string' };
  if (!Object.hasOwn(strategies, input.provider)) {
    return { error: `Unsupported provider: ${input.provider}` };
  }
  const strategy = strategies[input.provider];
  if (!Array.isArray(input.events)) return { error: 'events must be an array' };
  if (input.events.some((event) => event === null || typeof event !== 'object' || Array.isArray(event))) {
    return { error: 'each event must be an object' };
  }
  const chunks = [...strategy(input.events)];
  return { chunks, text: chunks.join('') };
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  if (process.argv.length !== 3) throw new Error('usage: node implementation.mjs INPUT_JSON');
  const input = JSON.parse(readFileSync(process.argv[2], 'utf8'));
  console.log(JSON.stringify(run(input)));
}
