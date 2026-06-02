# VueDependencyAnalyzer  (still under developing)

AST-based Dependency Analysis Tool for Large-scale Vue.js Applications

## Overview

VueDependencyAnalyzer is a research-oriented static analysis tool designed to extract and analyze dependency relationships within large-scale Vue.js applications.

The project focuses on improving the analyzability and maintainability of frontend systems by making component dependencies and state management relationships explicit and traceable.

This tool is being developed as part of ongoing research on frontend software architecture and dependency-aware engineering approaches.

---

## Motivation

As Vue.js applications grow in scale, dependency relationships between components, stores, and modules often become increasingly implicit.

This can make architectural analysis, maintenance, and system evolution difficult.

VueDependencyAnalyzer aims to address this challenge by providing automated dependency extraction and analysis mechanisms based on Abstract Syntax Tree (AST) analysis.

---

## Research Goals

* Extract component dependencies from Vue.js applications
* Analyze component-store relationships
* Support dependency visualization and architecture analysis
* Improve frontend system analyzability
* Enable architecture-aware tooling for large-scale projects

---

## Analysis Workflow

Vue Source Code
→ AST Parsing
→ Dependency Extraction
→ Relationship Modeling
→ Architecture Analysis

---

## Current Features

* Vue component parsing
* AST-based dependency extraction
* Import relationship analysis
* Component-store dependency detection
* Dependency graph generation (experimental)

---

## Current Status

Research Prototype

This project is currently being developed as a research prototype and experimental analysis platform.

The primary focus is dependency analysis and architectural modeling rather than production deployment.

---

## Related Research

This project is related to ongoing research on:

* Frontend software architecture
* Dependency analysis
* Configuration-driven frontend engineering
* State management systems in Vue.js ecosystems

---

## Author

Yizhi Mei
Ph.D. Candidate, Oita University
Frontend Software Engineering Research

GitHub: https://github.com/Cozymyz
E-mail:yizhimei0302@gmail.com / v25f1001@oita-u.ac.jp
