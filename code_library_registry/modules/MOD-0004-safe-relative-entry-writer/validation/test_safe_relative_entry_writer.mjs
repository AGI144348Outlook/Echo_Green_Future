import assert from "node:assert/strict";
import test from "node:test";

import {
  EntryPathError,
  normalizeRelativeEntryPath,
  writeRelativeEntry,
} from "../generalized/safe_relative_entry_writer.mjs";

function fakeRoot(events) {
  function directory(prefix = []) {
    return {
      async getDirectoryHandle(name, options) {
        events.push(["directory", [...prefix, name].join("/"), options]);
        return directory([...prefix, name]);
      },
      async getFileHandle(name, options) {
        events.push(["file", [...prefix, name].join("/"), options]);
        return {
          async createWritable() {
            const writable = { path: [...prefix, name].join("/") };
            events.push(["writable", writable.path]);
            return writable;
          },
        };
      },
    };
  }
  return directory();
}

test("normalizes a bounded relative file path", () => {
  const parts = normalizeRelativeEntryPath("alpha/beta/report.json");
  assert.deepEqual(parts, ["alpha", "beta", "report.json"]);
  assert.equal(Object.isFrozen(parts), true);
});

test("rejects ambiguous, absolute, traversal and directory-only paths", () => {
  const invalid = [
    "",
    "/absolute.txt",
    "C:/drive.txt",
    "alpha\\file.txt",
    "alpha//file.txt",
    "./file.txt",
    "alpha/../file.txt",
    "alpha/",
    "bad\0name.txt",
  ];
  for (const path of invalid) {
    assert.throws(() => normalizeRelativeEntryPath(path), EntryPathError, path);
  }
});

test("enforces depth, total length and segment length budgets", () => {
  assert.throws(
    () => normalizeRelativeEntryPath("a/b/c.txt", { maxDepth: 2 }),
    /maxDepth/,
  );
  assert.throws(
    () => normalizeRelativeEntryPath("abcdef", { maxPathLength: 5 }),
    /maxPathLength/,
  );
  assert.throws(
    () => normalizeRelativeEntryPath("abcdef", { maxSegmentLength: 5 }),
    /maxSegmentLength/,
  );
});

test("invalid paths cause no destination or source mutation", async () => {
  const events = [];
  let streamCalls = 0;
  await assert.rejects(
    writeRelativeEntry(fakeRoot(events), "../escape.txt", {
      stream() {
        streamCalls += 1;
      },
    }),
    EntryPathError,
  );
  assert.deepEqual(events, []);
  assert.equal(streamCalls, 0);
});

test("creates validated directory handles and streams one file", async () => {
  const events = [];
  const source = {
    stream() {
      events.push(["stream"]);
      return {
        async pipeTo(writable) {
          events.push(["pipe", writable.path]);
        },
      };
    },
  };

  const receipt = await writeRelativeEntry(
    fakeRoot(events),
    "one/two/file.txt",
    source,
  );

  assert.deepEqual(receipt, {
    path: "one/two/file.txt",
    directoryDepth: 2,
  });
  assert.deepEqual(events, [
    ["stream"],
    ["directory", "one", { create: true }],
    ["directory", "one/two", { create: true }],
    ["file", "one/two/file.txt", { create: true }],
    ["writable", "one/two/file.txt"],
    ["pipe", "one/two/file.txt"],
  ]);
});

test("propagates a streaming failure without reporting success", async () => {
  const events = [];
  const failure = new Error("write failed");
  await assert.rejects(
    writeRelativeEntry(fakeRoot(events), "folder/file.txt", {
      stream() {
        return {
          async pipeTo() {
            throw failure;
          },
        };
      },
    }),
    failure,
  );
  assert.equal(events.some(([kind]) => kind === "file"), true);
});
