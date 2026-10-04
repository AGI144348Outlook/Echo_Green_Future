# Applications and limits

## Meaningful applications

- validate file-entry paths before a browser archive extractor writes them;
- import a bounded set of relative files into a user-selected directory;
- stream generated reports or exported records into nested local folders;
- provide a reusable path gate in offline-first PWAs;
- test archive-entry policies independently of ZIP parsing or decompression.

## Contract

Input: a forward-slash relative file path, a root adapter compatible with the File System Access handle shape, and a blob-like source whose `stream()` result provides `pipeTo()`.

Output: a streamed write to the validated relative destination and a detached receipt containing the canonical path and directory depth.

Rejected inputs include absolute paths, Windows drive prefixes, backslashes, NUL bytes, dot/traversal segments, empty segments, directory-only paths and configured depth/length excesses. Validation occurs before directory or file creation.

Dependencies: JavaScript runtime only. The implementation imports no package.

## Assumptions

- the supplied root and handles enforce their platform's permission model;
- the destination adapter makes a failed or aborted writable safe according to its own contract;
- the caller separately limits entry count, aggregate bytes and decompression ratios;
- archive filenames have already been decoded to JavaScript strings under an explicit encoding policy.

## Non-applications

This is not a ZIP parser, decompressor, quota manager, malware scanner, symlink policy, Unicode-confusable detector, concurrent-writer coordinator or transactional multi-file extractor. It does not make the workbench's current `unzip()` function operational.
