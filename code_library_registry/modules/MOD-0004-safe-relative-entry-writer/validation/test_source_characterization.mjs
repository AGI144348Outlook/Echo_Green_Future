import assert from "node:assert/strict";
import fs from "node:fs/promises";
import test from "node:test";
import vm from "node:vm";

async function sourceContext() {
  const code = await fs.readFile(new URL("../original/app.js", import.meta.url), "utf8");
  const generic = {
    textContent: "",
    scrollTop: 0,
    scrollHeight: 0,
    style: {},
    files: [],
    addEventListener() {},
  };
  const canvas = {
    ...generic,
    getContext() {
      return {
        setTransform() {},
        clearRect() {},
        beginPath() {},
        moveTo() {},
        lineTo() {},
        stroke() {},
      };
    },
  };
  const elements = new Map([["#grid", canvas]]);
  const context = vm.createContext({
    document: {
      querySelector(selector) {
        if (!elements.has(selector)) elements.set(selector, { ...generic });
        return elements.get(selector);
      },
    },
    addEventListener() {},
    devicePixelRatio: 1,
    innerWidth: 24,
    innerHeight: 24,
    loadPyodide: async () => ({}),
    navigator: {},
    window: {},
    console,
  });
  vm.runInContext(code, context);
  return context;
}

test("source writer creates nested handles and streams the blob", async () => {
  const context = await sourceContext();
  const events = [];
  context.root = {
    async getDirectoryHandle(name, options) {
      events.push(["directory", name, options.create]);
      return {
        async getFileHandle(fileName, fileOptions) {
          events.push(["file", fileName, fileOptions.create]);
          return {
            async createWritable() {
              return { marker: "destination" };
            },
          };
        },
      };
    },
  };
  context.blob = {
    stream() {
      return {
        async pipeTo(destination) {
          events.push(["pipe", destination.marker]);
        },
      };
    },
  };
  await vm.runInContext("writeEntry(root, 'folder/file.txt', blob)", context);
  assert.deepEqual(events, [
    ["directory", "folder", true],
    ["file", "file.txt", true],
    ["pipe", "destination"],
  ]);
});

test("source writer passes a traversal segment to the directory adapter", async () => {
  const context = await sourceContext();
  const segments = [];
  context.root = {
    async getDirectoryHandle(name) {
      segments.push(name);
      return {
        async getFileHandle() {
          return {
            async createWritable() {
              return {};
            },
          };
        },
      };
    },
  };
  context.blob = {
    stream() {
      return { async pipeTo() {} };
    },
  };
  await vm.runInContext("writeEntry(root, '../escape.txt', blob)", context);
  assert.deepEqual(segments, [".."]);
});
