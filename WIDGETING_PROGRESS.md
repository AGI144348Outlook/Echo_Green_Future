# Widgeting continuation

Based on existing PWA widget source at 70642cf4a2b20b580b8497e7102f27bba689b6a2. This branch is independent of notebook 0.4 and the blank dev-suite surface.

Fixed: unknown widget types and missing targets return failure; nonfinite geometry and nonpositive sizes are rejected; Echo cannot rebind a user widget through BIND_WIDGET, OPEN_WIDGET or the public open API; Echo ownership cannot be overridden by a spec. Very small viewports cannot produce negative dimensions.

Checked: JavaScript syntax and six command/ownership cases. Full browser pointer interactions remain to be tested.

Next: explicit Canvas WidgetSpec schema and registry-reference resolution; responsive updates from changed registry entities; touch and keyboard drag/drop tests. Pyodide supplies Python execution, while pointer/DOM logic supplies drag/drop. No developer panels were added to dev-suite.

Primary runtime reference: https://pyodide.org/en/0.29.3/usage/index.html
