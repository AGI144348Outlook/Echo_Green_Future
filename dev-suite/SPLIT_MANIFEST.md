# Data/code split — replacement files

Unpack over the branch root (paths start with dev-suite/). Only these files change or are added:

```
d07c1c577a75c936  dev-suite/build.py
17a012ec5b8374a7  dev-suite/README.md
05f3df5f7d71b8d0  dev-suite/suite/src/app_part.html
ca7fb3daf8ab5c4a  dev-suite/suite/src/data/dictionary.json.gz.b64
7c59034c3e29cd95  dev-suite/suite/src/data/echo_matrices.json.gz.b64
ebafa5bc475d4768  dev-suite/suite/src/data/genesis_skeleton.py
0c7e762da4819735  dev-suite/suite/src/data/genesis_structure.json
9d6dd20d863c2d89  dev-suite/suite/src/data/latin_registries.json
986f72847ce8916e  dev-suite/suite/src/data/registries.json
9b93a03483a6023c  dev-suite/suite/src/data/symbols.json
```

Verification: with these files, `python build.py` produces

```
dist/dev-suite.html                 sha256 97bfb73e2a9a104d4750c3a2baf0c42e5943d2b71ec9f769125b98f73d290932
dist/canvas-keyboard-terminal.html  sha256 21bcef638bf64302fa58eaebfb8159573619ac75c776462e3543d6d145cc6590
```

Both are byte-identical to the build before the split. No storage behavior changed; dist/ is not included (it is unchanged).
