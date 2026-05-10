# Two-Domain Wrapper Compatibility Audit

This audit verifies that root-level compatibility wrappers do not contain duplicated active product logic after the physical two-domain reorganization.

## Result

All tracked root-level compatibility wrappers are thin shims. They either:

- set `__path__` to the corresponding product-domain package under `Behavioral_Signals_AI/` or `Signal_CGE/`, or
- re-export symbols from the corresponding product-domain module.

No duplicated active implementation logic remains in tracked root wrappers.

## Behavioral Signals AI Wrappers

| Root wrapper | Canonical target | Wrapper type |
|---|---|---|
| `api/__init__.py` | `Behavioral_Signals_AI/api/` | package path shim |
| `behavioral_ai/__init__.py` | `Behavioral_Signals_AI/behavioral_ai/` | package path shim |
| `data/__init__.py` | `Behavioral_Signals_AI/data/` | package path shim |
| `live_trends/__init__.py` | `Behavioral_Signals_AI/live_trends/` | package path shim |
| `ml/__init__.py` | `Behavioral_Signals_AI/ml/` | package path shim |
| `src/__init__.py` | `Behavioral_Signals_AI/src/` | package path shim |
| `adaptive_learning.py` | `Behavioral_Signals_AI/adaptive_learning.py` | re-export shim |
| `explainability.py` | `Behavioral_Signals_AI/explainability.py` | re-export shim |
| `privacy.py` | `Behavioral_Signals_AI/privacy.py` | re-export shim |
| `train_model.py` | `Behavioral_Signals_AI/train_model.py` | re-export shim |
| `trend_intelligence.py` | `Behavioral_Signals_AI/trend_intelligence.py` | re-export shim |
| `x_trends.py` | `Behavioral_Signals_AI/x_trends.py` | re-export shim |

## Signal CGE Wrappers

| Root wrapper | Canonical target | Wrapper type |
|---|---|---|
| `backends/__init__.py` | `Signal_CGE/backends/` | package path shim |
| `cge_core/__init__.py` | `Signal_CGE/cge_core/` | package path shim |
| `cge_engine/__init__.py` | `Signal_CGE/cge_engine/` | package path shim |
| `cge_workbench/__init__.py` | `Signal_CGE/cge_workbench/` | package path shim plus re-export |
| `learning/__init__.py` | `Signal_CGE/learning/` | package path shim |
| `learning_memory/__init__.py` | `Signal_CGE/learning_memory/` | package path shim |
| `policy_ai/__init__.py` | `Signal_CGE/policy_ai/` | package path shim |
| `policy_intelligence/__init__.py` | `Signal_CGE/policy_intelligence/` | package path shim |
| `signal_ai/__init__.py` | `Signal_CGE/signal_ai/` | package path shim |
| `signal_execution/__init__.py` | `Signal_CGE/signal_execution/` | package path shim |
| `signal_learning/__init__.py` | `Signal_CGE/signal_learning/` | package path shim |
| `signal_modeling_language/__init__.py` | `Signal_CGE/signal_modeling_language/` | package path shim |
| `signal_sml/__init__.py` | `Signal_CGE/signal_sml/` | package path shim |
| `sml_workbench/__init__.py` | `Signal_CGE/sml_workbench/` | package path shim plus re-export |
| `solvers/__init__.py` | `Signal_CGE/solvers/` | package path shim |
| `signal_cge.py` | `Signal_CGE/signal_cge/` | package path shim plus top-level re-exports |

## Why Wrappers Remain

The wrappers are retained temporarily because tests, older docs, notebooks, and deployed import paths still refer to historical root package names. Removing them now would create avoidable breakage. New development should use the product-domain paths directly:

- `Behavioral_Signals_AI/...`
- `Signal_CGE/...`

The wrappers can be removed later after root imports are fully migrated and test coverage confirms that no external entry points depend on them.
