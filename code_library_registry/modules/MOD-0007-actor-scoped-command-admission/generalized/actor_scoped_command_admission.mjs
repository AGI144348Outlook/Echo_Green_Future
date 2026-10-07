const ACTIONS = new Set([
  'OPEN', 'CLOSE', 'FOCUS', 'MOVE', 'RESIZE',
  'DOCK', 'MINIMIZE', 'MAXIMIZE', 'BIND',
]);

const AGENT_DENIED_ON_HUMAN = new Set([
  'CLOSE', 'MOVE', 'RESIZE', 'DOCK',
  'MINIMIZE', 'MAXIMIZE', 'BIND',
]);

const own = (value, key) => Object.prototype.hasOwnProperty.call(value, key);

function decision(allowed, code, details = {}) {
  return Object.freeze({ allowed, code, ...details });
}

function resourceFor(resources, id) {
  if (resources instanceof Map) return resources.get(id);
  if (resources && typeof resources === 'object') return resources[id];
  return undefined;
}

function hasKind(knownKinds, kind) {
  if (knownKinds instanceof Set) return knownKinds.has(kind);
  return Array.isArray(knownKinds) && knownKinds.includes(kind);
}

function validGeometry(spec) {
  for (const key of ['x', 'y', 'width', 'height']) {
    if (own(spec, key) && spec[key] != null && !Number.isFinite(spec[key])) return false;
  }
  return (!own(spec, 'width') || spec.width == null || spec.width > 0) &&
    (!own(spec, 'height') || spec.height == null || spec.height > 0);
}

export function admitCommand({ command, resources = new Map(), knownKinds = new Set() }) {
  if (!command || typeof command !== 'object' || Array.isArray(command)) {
    return decision(false, 'INVALID_COMMAND');
  }
  const principal = command.principal ?? 'human';
  if (!['human', 'agent'].includes(principal)) {
    return decision(false, 'UNKNOWN_PRINCIPAL');
  }
  const action = command.action;
  if (!ACTIONS.has(action)) return decision(false, 'UNKNOWN_ACTION');

  if (action === 'OPEN') {
    const spec = command.spec;
    if (!spec || typeof spec !== 'object' || Array.isArray(spec)) {
      return decision(false, 'INVALID_SPEC');
    }
    if (!hasKind(knownKinds, spec.kind)) return decision(false, 'UNKNOWN_KIND');
    if (!validGeometry(spec)) return decision(false, 'INVALID_GEOMETRY');
    const existing = spec.id == null ? undefined : resourceFor(resources, spec.id);
    if (principal === 'agent' && existing?.owner === 'human' && own(spec, 'binding')) {
      return decision(false, 'HUMAN_RESOURCE_REBIND');
    }
    return decision(true, 'ALLOWED', {
      principal,
      action,
      resourceId: spec.id ?? null,
      effectiveOwner: principal,
    });
  }

  const resource = resourceFor(resources, command.id);
  if (!resource) return decision(false, 'MISSING_RESOURCE');
  if (principal === 'agent' && resource.owner === 'human' && AGENT_DENIED_ON_HUMAN.has(action)) {
    return decision(false, 'HUMAN_RESOURCE_PROTECTED');
  }
  if (action === 'MOVE' && ![command.x, command.y].every(Number.isFinite)) {
    return decision(false, 'INVALID_GEOMETRY');
  }
  if (action === 'RESIZE' &&
      (![command.width, command.height].every(Number.isFinite) ||
       command.width <= 0 || command.height <= 0)) {
    return decision(false, 'INVALID_GEOMETRY');
  }
  return decision(true, 'ALLOWED', {
    principal,
    action,
    resourceId: command.id,
    effectiveOwner: resource.owner,
  });
}
