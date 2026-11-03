# Empire Labs AI Language Standard

Standing architecture rule under MOP-EMPIRE-COMPETITIVE-ENGINEERING-001. Issued by Eddie 2026-11-03. Applies to every Empire Labs build unless a documented exception exists.

**AI research and training: Python-first. Production, local and edge runtime: Rust-first. Web UI: TypeScript-first. Exceptions require technical justification, not preference.**

Not "Rust everywhere". The language follows the stage of the system.

## Python-first

Model research, training, fine-tuning, quantisation experiments, data science, dataset preparation, evaluation harnesses, benchmark tooling, rapid AI prototypes, PyTorch, Transformers and JAX work.

Python remains the fastest path for AI experimentation and rewriting working research code into Rust for consistency buys nothing a customer will pay for.

## Rust-first

Production inference where practical, local and offline AI runtimes, mobile and edge runtimes, agent runtime infrastructure, deterministic business logic, high-performance APIs and services, reconciliation and synchronisation, cryptography, evidence generation, audit and governance functions, device integration and long-running reliable services.

## Frontend

Browser and PWA work uses a TypeScript web stack for the interface, with Rust compiled to WASM for high-integrity reusable core logic. Packaged applications reuse the same Rust core through Tauri or native bindings rather than re-implementing it.

## The default pipeline

```
Python: research, train, fine-tune, quantise, evaluate
        |
   model artefact: GGUF, ONNX or safetensors
        v
Rust: inference, business rules, device services, evidence, crypto,
      APIs, local storage, sync
        |
   phone, PC, edge, server
```

Python builds the intelligence. Rust ships it.

## What this rules out and rules in

Do not rewrite functioning Python evaluation code into Rust for consistency. Do move durable production components into Rust where the advantage is measurable in performance, memory, reliability, portability, offline deployment, security, deterministic behaviour or reusable platform infrastructure.

## Reusable crates over isolated implementations

As competitive builds accumulate, infrastructure becomes shared crates rather than copy-paste:

```
EmpireCore/
    empire-runtime
    empire-inference
    empire-evidence
    empire-sync
    empire-local-store
    empire-import
    empire-crypto
    empire-api
    empire-device
    empire-licensing
```

A new product should increasingly be domain logic, interface and integrations, not another rebuild of the plumbing.

## Exception rule

A component may stay Python, TypeScript, Kotlin, Go or C++ where that is objectively the better engineering choice. The deviation is recorded with five things: the reason, the expected benefit, the deployment impact, the maintenance impact and why the Rust or Python default is inferior for that component. Untested preferences are not exceptions.

## Application to CYCLE-001

VoltLedger is a rules-and-evidence product, not an ML product, so the standard lands almost entirely on the Rust side:

| Component | Language | Why |
|---|---|---|
| Rules, reconciliation, sync, CSV validation | Rust, `core-rs` | Deterministic, auditable, one implementation for phone, server and plugin |
| Browser core | Rust compiled to WASM | Same bytes on the device as on the server; no second implementation to drift |
| Capture interface | Browser stack, TypeScript target | PWA first, packagable later via Tauri without touching the core |
| Evaluation harness | Python, unchanged | Independent oracle. Deliberately a different language and different arithmetic path |
| Future inference (photograph an item, read a tag) | Python to train, Rust to serve | Per the pipeline above |

The Python harness is not discarded and is not ported. Its value is that it disagrees with the product if the product is wrong. The WASM core must reproduce every vector in `eval/tests` before it is allowed to replace anything, which is what the browser parity gate enforces on load.

Verified 2026-11-03: Rust suite 11/11, Node suite 11/11, WASM parity 8/8 in a real browser, E2E 13/13.
