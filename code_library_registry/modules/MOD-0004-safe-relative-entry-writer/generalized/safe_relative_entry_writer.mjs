export class EntryPathError extends TypeError {}

function positiveInteger(value, name) {
  if (!Number.isSafeInteger(value) || value < 1) {
    throw new RangeError(`${name} must be a positive safe integer`);
  }
}

export function normalizeRelativeEntryPath(
  path,
  { maxDepth = 64, maxPathLength = 4096, maxSegmentLength = 255 } = {},
) {
  positiveInteger(maxDepth, "maxDepth");
  positiveInteger(maxPathLength, "maxPathLength");
  positiveInteger(maxSegmentLength, "maxSegmentLength");

  if (typeof path !== "string" || path.length === 0) {
    throw new EntryPathError("entry path must be a non-empty string");
  }
  if (path.length > maxPathLength) {
    throw new EntryPathError("entry path exceeds maxPathLength");
  }
  if (path.includes("\0")) {
    throw new EntryPathError("entry path contains a NUL byte");
  }
  if (path.includes("\\")) {
    throw new EntryPathError("entry path must use forward slashes only");
  }
  if (path.startsWith("/") || /^[A-Za-z]:/.test(path)) {
    throw new EntryPathError("entry path must be relative");
  }
  if (path.endsWith("/")) {
    throw new EntryPathError("entry path must name a file, not a directory");
  }

  const parts = path.split("/");
  if (parts.length > maxDepth) {
    throw new EntryPathError("entry path exceeds maxDepth");
  }
  for (const part of parts) {
    if (part.length === 0) {
      throw new EntryPathError("entry path contains an empty segment");
    }
    if (part === "." || part === "..") {
      throw new EntryPathError("entry path contains a traversal segment");
    }
    if (part.length > maxSegmentLength) {
      throw new EntryPathError("entry path segment exceeds maxSegmentLength");
    }
  }

  return Object.freeze([...parts]);
}

async function ensureDirectories(root, parts) {
  let directory = root;
  for (const part of parts) {
    directory = await directory.getDirectoryHandle(part, { create: true });
  }
  return directory;
}

export async function writeRelativeEntry(root, path, source, options = {}) {
  const parts = normalizeRelativeEntryPath(path, options);
  if (!root || typeof root.getDirectoryHandle !== "function") {
    throw new TypeError("root must provide getDirectoryHandle");
  }
  if (!source || typeof source.stream !== "function") {
    throw new TypeError("source must provide stream()");
  }

  const stream = source.stream();
  if (!stream || typeof stream.pipeTo !== "function") {
    throw new TypeError("source.stream() must return an object with pipeTo()");
  }

  const name = parts.at(-1);
  const directory = await ensureDirectories(root, parts.slice(0, -1));
  if (typeof directory.getFileHandle !== "function") {
    throw new TypeError("destination directory must provide getFileHandle");
  }
  const file = await directory.getFileHandle(name, { create: true });
  if (!file || typeof file.createWritable !== "function") {
    throw new TypeError("destination file must provide createWritable");
  }
  const writable = await file.createWritable();
  await stream.pipeTo(writable);

  return Object.freeze({
    path: parts.join("/"),
    directoryDepth: parts.length - 1,
  });
}
