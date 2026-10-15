import fs from 'node:fs';
import {DiagramParser, Compact, Bracketed, NamesAdapter, Exporter} from './diagram.mjs';
try {
  const model = new DiagramParser().parse(fs.readFileSync(0, 'utf8').split(/\r?\n/));
  const choices = {compact: Compact, bracketed: Bracketed, json: NamesAdapter};
  console.log(new Exporter(new choices[process.argv[2]]()).export(model));
} catch (error) { console.log('ERROR:' + error.message); }
