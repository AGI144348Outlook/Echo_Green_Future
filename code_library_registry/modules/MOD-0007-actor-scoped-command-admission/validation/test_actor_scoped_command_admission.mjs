import assert from 'node:assert/strict';
import test from 'node:test';
import { admitCommand } from '../generalized/actor_scoped_command_admission.mjs';

const kinds = new Set(['chart']);
const resources = new Map([
  ['human-1', Object.freeze({ owner: 'human' })],
  ['agent-1', Object.freeze({ owner: 'agent' })],
]);

test('rejects malformed commands and unknown principals or actions', () => {
  assert.equal(admitCommand({ command: null }).code, 'INVALID_COMMAND');
  assert.equal(admitCommand({ command: { principal: 'root', action: 'FOCUS' } }).code, 'UNKNOWN_PRINCIPAL');
  assert.equal(admitCommand({ command: { action: 'EXECUTE' } }).code, 'UNKNOWN_ACTION');
});

test('open requires a registered kind and bounded finite geometry', () => {
  assert.equal(admitCommand({ command: { action: 'OPEN', spec: { kind: 'missing' } }, knownKinds: kinds }).code, 'UNKNOWN_KIND');
  assert.equal(admitCommand({ command: { action: 'OPEN', spec: { kind: 'chart', width: 0 } }, knownKinds: kinds }).code, 'INVALID_GEOMETRY');
  assert.equal(admitCommand({ command: { action: 'OPEN', spec: { kind: 'chart', x: Infinity } }, knownKinds: kinds }).code, 'INVALID_GEOMETRY');
});

test('agent cannot claim human ownership when opening', () => {
  const result = admitCommand({
    command: { principal: 'agent', action: 'OPEN', spec: { kind: 'chart', owner: 'human' } },
    knownKinds: kinds,
  });
  assert.equal(result.allowed, true);
  assert.equal(result.effectiveOwner, 'agent');
});

test('agent cannot rebind an existing human resource even to null', () => {
  const result = admitCommand({
    command: { principal: 'agent', action: 'OPEN', spec: { id: 'human-1', kind: 'chart', binding: null } },
    knownKinds: kinds,
    resources,
  });
  assert.equal(result.code, 'HUMAN_RESOURCE_REBIND');
});

test('agent cannot mutate human-owned resources', () => {
  for (const action of ['CLOSE', 'MOVE', 'RESIZE', 'DOCK', 'MINIMIZE', 'MAXIMIZE', 'BIND']) {
    const result = admitCommand({ command: { principal: 'agent', action, id: 'human-1' }, resources });
    assert.equal(result.code, 'HUMAN_RESOURCE_PROTECTED');
  }
});

test('focus remains available to an agent on a human resource', () => {
  const result = admitCommand({ command: { principal: 'agent', action: 'FOCUS', id: 'human-1' }, resources });
  assert.equal(result.allowed, true);
});

test('human and owning agent receive geometry validation', () => {
  assert.equal(admitCommand({ command: { action: 'MOVE', id: 'human-1', x: 1, y: NaN }, resources }).code, 'INVALID_GEOMETRY');
  assert.equal(admitCommand({ command: { principal: 'agent', action: 'RESIZE', id: 'agent-1', width: 1, height: -1 }, resources }).code, 'INVALID_GEOMETRY');
});

test('admission is pure and returns a frozen decision', () => {
  const before = JSON.stringify([...resources]);
  const result = admitCommand({ command: { action: 'FOCUS', id: 'human-1' }, resources });
  assert.equal(JSON.stringify([...resources]), before);
  assert.equal(Object.isFrozen(result), true);
});
