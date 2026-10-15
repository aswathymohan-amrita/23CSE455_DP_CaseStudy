export class Block {
  names() { throw new Error("abstract"); }
}
export class Node extends Block {
  constructor(name) { super(); this.name = name; }
  names() { return [this.name]; }
}
export class Group extends Block {
  constructor() { super(); this.children = []; }
  names() { return this.children.flatMap(child => child.names()); }
}
export class Model {
  add(name) { throw new Error("abstract"); }
}
export class Diagram extends Model {
  constructor() {
    super(); this.root = new Group(); this.stack = [this.root]; this.links = [];
  }
  add(name) {
    if (this.root.names().includes(name)) throw new Error("duplicate");
    this.stack.at(-1).children.push(new Node(name));
  }
  link(left, right) {
    const names = this.root.names();
    if (!names.includes(left) || !names.includes(right)) throw new Error("missing endpoint");
    this.links.push(`${left}->${right}`);
  }
}
export class Command {
  execute(model, args) { throw new Error("abstract"); }
}
export class Create extends Command {
  execute(model, args) { model.add(args[0]); }
}
export class Link extends Command {
  execute(model, args) { model.link(...args); }
}
export class OpenGroup extends Command {
  execute(model) {
    const group = new Group();
    model.stack.at(-1).children.push(group); model.stack.push(group);
  }
}
export class CloseGroup extends Command {
  execute(model) {
    if (model.stack.length === 1) throw new Error("unmatched end");
    model.stack.pop();
  }
}
export class Parser {
  constructor() {
    this.commands = new Map([
      ["class", [1, new Create()]], ["link", [2, new Link()]],
      ["group", [0, new OpenGroup()]], ["end", [0, new CloseGroup()]]
    ]);
  }
  createModel() { throw new Error("abstract"); }
  parse(lines) {
    const model = this.createModel();
    for (const line of lines) {
      if (!line.trim()) continue;
      const words = line.trim().split(/\s+/);
      const entry = this.commands.get(words[0]);
      if (!entry) throw new Error("syntax");
      const [arity, command] = entry;
      if (words.length !== arity + 1) throw new Error("syntax");
      command.execute(model, words.slice(1));
    }
    if (model.stack.length !== 1) throw new Error("unclosed group");
    return model;
  }
}
export class DiagramParser extends Parser {
  createModel() { return new Diagram(); }
}
export class Renderer {
  render(model) { throw new Error("abstract"); }
}
export class Compact extends Renderer {
  render(model) { return model.root.names().join(",") + "|" + model.links.join(","); }
}
export class Bracketed extends Renderer {
  render(model) {
    return model.root.names().map(name => `[${name}]`).join(",") + "|" + model.links.join(",");
  }
}
export class LegacyNames {
  encode(names) { return JSON.stringify(names); }
}
export class NamesAdapter extends Renderer {
  constructor() { super(); this.legacy = new LegacyNames(); }
  render(model) { return this.legacy.encode(model.root.names()); }
}
export class Exporter {
  constructor(renderer) { this.renderer = renderer; }
  export(model) { return this.renderer.render(model); }
}
