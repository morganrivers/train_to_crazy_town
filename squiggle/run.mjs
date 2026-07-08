// run.mjs — run every node model straight from this repo and print its ranking.
//
// Runs the node models from this repo. A custom linker maps every Hub import name
// (`hub:morganrivers/base_model` and `hub:morganrivers/<node-id>`) to the local
// file, so the same files that publish to Squiggle Hub unchanged also run here on
// disk. Node models form an IMPORT CHAIN: each imports its parent node and
// Dict.merges one coefficient delta, so the linker must resolve those parent
// imports transitively. The same linker pattern feeds the @quri/squiggle-components
// React player.
//
//   cd squiggle && npm install && node run.mjs
//   node run.mjs nodes/s3_inverts.squiggle      # just one

import { SqProject, SqModule, makeSelfContainedLinker } from "@quri/squiggle-lang";
import { readFileSync, readdirSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const HERE = dirname(fileURLToPath(import.meta.url));

// Hub import name -> local source. base_model plus every node, keyed by id so a
// child's `import "hub:morganrivers/<parent>"` resolves to the parent on disk.
const sources = {
  "hub:morganrivers/base_model": readFileSync(join(HERE, "base_model.squiggle"), "utf8"),
};
for (const f of readdirSync(join(HERE, "nodes")).filter((f) => f.endsWith(".squiggle"))) {
  sources[`hub:morganrivers/${f.replace(/\.squiggle$/, "")}`] =
    readFileSync(join(HERE, "nodes", f), "utf8");
}
const linker = makeSelfContainedLinker(sources);

async function rank(file) {
  const code = readFileSync(file, "utf8");
  const project = new SqProject({ linker });
  project.setHead("root", { module: new SqModule({ name: "main", code }) });
  const output = await project.waitForOutput("root");
  const bindings = output.getBindings();
  if (!bindings.ok) throw new Error(bindings.value.toString());
  const arr = bindings.value.get("ranking").value.getValues();
  return arr.map((v) => ({
    name: v.value.get("name").value,
    wdaly_per_usd: v.value.get("wdaly_per_usd").value,
  }));
}

const args = process.argv.slice(2);
const files = args.length
  ? args
  : readdirSync(join(HERE, "nodes")).sort()
      .filter((f) => f.endsWith(".squiggle"))
      .map((f) => join(HERE, "nodes", f));

for (const file of files) {
  const ranked = await rank(file);
  const name = file.split("/").pop();
  console.log(`\n${name}`);
  ranked.forEach((r, i) =>
    console.log(`  ${i === 0 ? "→" : " "} ${String(r.name).padEnd(24)} ${r.wdaly_per_usd}`)
  );
}
