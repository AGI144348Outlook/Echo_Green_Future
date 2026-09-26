# Code Library Assessment — CLR-0012

# Absolute Coordinate FractalGrid — Multi-Scale 3D Workspace Prototype

**Short identity:** ABSOLUTE COORDINATE FRACTALGRID  
**Architectural tag:** Canonical Coordinates / Scale Projection / 3D Spatial Workspace  
**Lineage:** CLR-0009 Energy Fractal Grid + CLR-0011 Spatial Reasoning Grid  
**Research cross-reference:** RP-0002 Spatial AI Architecture  
**Disposition:** Candidate for extraction and modernization

## Executive assessment
This Three.js prototype introduces a significant architectural mechanism: objects retain canonical "absolute" positions independently of the current display scale, while rendered world positions are derived from those stored coordinates.

The core relationship is:

`absolute position → scale transform → rendered/world position`.

Changing scale therefore changes representation without changing the stored identity/location of the object.

This is directly relevant to Echo's EVE/NVE, nested Cartesian, notebook/canvas, and multiscale representation work.

## Core mechanism
`AbsoluteCoordinateSystem` maintains:
- absolute origin,
- named scale levels,
- scale factors,
- current scale,
- map of object IDs to canonical positions.

Principal operations:
- `worldToAbsolute()`
- `absoluteToWorld()`
- `setAbsolutePosition()`
- `getAbsolutePosition()`
- `updateWorldFromAbsolute()`
- scale navigation.

This is stronger than merely zooming a camera because object state is explicitly distinguished from its scale-dependent presentation.

## Current Echo mapping
A modern form should generalize:

`CanonicalState + CoordinateFrame + Transform → Local/RenderedState`.

For nested environments:

`EVE frame → NVE transform → NVE-local placement`

and, recursively:

`Frame_A --T_AB→ Frame_B --T_BC→ Frame_C`.

The term "absolute" should be used carefully. In a nested architecture, a globally privileged coordinate frame may be unnecessary. A better abstraction is a **canonical/root frame** plus explicitly related local frames.

## Rays as indexed entities
The five "Rays of Knowledge" are individually identified and stored with canonical positions. Their visibility is determined from distance in canonical coordinates and current scale.

Architecturally this suggests:

`entity identity + canonical placement + view/scale policy → visible representation`.

That can generalize to registry-backed Echo entities, where the canvas decides whether and how to render an entity without changing the entity's semantic state.

## Scale-dependent presentation
The prototype adapts:
- grid size/divisions,
- camera distance,
- near/far planes,
- object world positions,
- ray visibility thresholds.

This is an early level-of-detail/view-policy mechanism.

However, the mm/cm/m scale model is not a conventional unit conversion implementation. The world representation divides stored millimeter coordinates by factors 1, 10, and 1000, effectively changing display scale. Naming these states as units can obscure the distinction between **physical unit conversion** and **rendering scale**.

A modern design should separate:
- physical units,
- coordinate-frame transform,
- viewport zoom,
- semantic level of detail.

## Important implementation issue: mutation aliasing
`getAbsolutePosition()` returns the Vector3 stored in the map. In `moveAvatar()`:

`const newAbsPos = currentAbsPos.add(movement)`

mutates that stored vector before `setAbsolutePosition()` clones it again. The result currently works for this flow but breaks clean ownership semantics.

A safer API should return clones/immutable values or use explicit mutation methods.

## Visibility-threshold issue
Comments and numeric ranges do not consistently match. For example, values stored in millimeters such as 10,000 correspond to 10 meters, not 10 millimeters. The thresholds should be reviewed and expressed with explicit unit types rather than comments.

## Movement semantics
Movement is described as scale-invariant because updates occur in canonical coordinates. This is a useful principle.

However, the animation derives tiny floating direction components and multiplies them by a fixed 1000-mm movement scalar every frame, so actual trajectory/speed depends on frame cadence and the chosen procedural formula. It is not time-step independent despite maintaining a nominal `time += 0.016`.

A modern simulation should use delta time.

## Scientific/architectural boundary
The prototype demonstrates coordinate and rendering behavior. It does not demonstrate:
- physical simulation,
- Planck-scale accuracy,
- semantic knowledge rays,
- spatial cognition,
- general multiscale scientific correctness.

Its value is software architecture.

## Dependencies
- Three.js 0.160.0 loaded from jsDelivr CDN.
- Browser/WebGL.

For reproducibility, modern archival/execution should pin dependency integrity or bundle the dependency rather than relying indefinitely on a live CDN.

## Recommended extraction
1. CoordinateFrame type.
2. canonical Placement type.
3. explicit Transform type.
4. Unit type distinct from viewport scale.
5. ViewScale/LOD policy.
6. frame graph for nested EVE/NVE transforms.
7. registry-backed entity IDs.
8. immutable/copy-safe coordinate access.
9. delta-time movement.
10. typed visibility policies.
11. renderer adapter separate from coordinate model.
12. tests for round-trip transforms:
   `canonical → local → canonical`.

## Relationship to prior artifacts
**CLR-0009** contributed scale transitions/adaptive resolution.

**CLR-0011** contributed a queryable Cartesian canvas/object workspace.

**CLR-0012** combines those lines by keeping object positions canonical while projecting them into a scale-dependent 3D world.

This makes CLR-0012 an important bridge artifact:

`scale-transition architecture + spatial workspace → scale-independent canonical placement`.

## Assessment note
For current Echo, the durable concept is not "everything has one absolute coordinate." It is that an entity's canonical state should remain stable while multiple views, scales, matrices, notebook canvases, and nested environments can project that state through explicit transforms. That distinction can prevent display operations from corrupting underlying registry state.
