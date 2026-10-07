import assert from 'node:assert/strict';
import fs from 'node:fs';
import test from 'node:test';
import vm from 'node:vm';

function loadSource() {
  const source = fs.readFileSync(new URL('../original/widgets.js', import.meta.url), 'utf8');
  const audit = [];
  const window = {
    ECHO: { audit: { workspace: event => audit.push(event) } },
    innerWidth: 1024,
    innerHeight: 768,
    addEventListener() {},
  };
  vm.runInNewContext(source, { window, document: {} });
  return { widgets: window.ECHO.widgets, audit };
}

test('source rejects invalid actors, unknown kinds and absent targets', () => {
  const { widgets } = loadSource();
  widgets.register('chart', {});
  assert.equal(widgets.dispatch({ actor: 'admin', op: 'FOCUS_WIDGET', id: 'x' }), false);
  assert.equal(widgets.dispatch({ op: 'OPEN_WIDGET', spec: { type: 'missing' } }), false);
  assert.equal(widgets.dispatch({ op: 'MOVE_WIDGET', id: 'missing', x: 1, y: 2 }), false);
});

test('source blocks agent mutation of a user-owned widget before DOM calls', () => {
  const { widgets, audit } = loadSource();
  widgets.items.set('user-1', { owner: 'user' });
  assert.equal(widgets.dispatch({ actor: 'echo', op: 'BIND_WIDGET', id: 'user-1', binding: 'x' }), false);
  assert.equal(audit.at(-1).reason, 'user-owned widget');
});

test('source rejects nonfinite move and nonpositive resize geometry', () => {
  const { widgets } = loadSource();
  widgets.items.set('echo-1', { owner: 'echo' });
  assert.equal(widgets.dispatch({ actor: 'echo', op: 'MOVE_WIDGET', id: 'echo-1', x: Infinity, y: 0 }), false);
  assert.equal(widgets.dispatch({ actor: 'echo', op: 'RESIZE_WIDGET', id: 'echo-1', w: 1, h: 0 }), false);
});
