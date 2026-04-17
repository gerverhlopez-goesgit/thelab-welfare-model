"""Configuration framework for the hedonic pricing model pipeline.

Supports layered configuration with this precedence (low -> high):
1. Dataclass defaults
2. JSON file overrides
3. Environment variable overrides
"""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass, field, fields, is_dataclass
from typing import Any, Dict, Optional, Tuple, Type, TypeVar, get_type_hints

@dataclass
class DataConfig:
    """Configuration for synthetic data generation."""
    
    n_samples: int = 1000  # Number of property transactions
    random_seed: int = 42
    
    # Structural characteristics ranges
    sqft_mean: float = 2000
    sqft_std: float = 600
    bedrooms_mean: float = 3
    bedrooms_std: float = 1
    bathrooms_mean: float = 2
    bathrooms_std: float = 0.8
    age_mean: float = 30  # years
    age_std: float = 25
    
    # Neighborhood characteristics ranges
    school_rating_mean: float = 7.0  # 1-10 scale
    school_rating_std: float = 2.0
    crime_rate_mean: float = 5.0  # per 1000 residents
    crime_rate_std: float = 3.0
    walkability_mean: float = 6.0  # 1-10 scale
    walkability_std: float = 2.5
    
    # Environmental characteristics ranges
    pm25_mean: float = 12.0  # µg/m³
    pm25_std: float = 4.0
    no2_mean: float = 35.0  # ppb
    no2_std: float = 15.0
    ozone_mean: float = 45.0  # ppb
    ozone_std: float = 15.0
    tri_proximity_mean: float = 5.0  # km from nearest TRI site
    tri_proximity_std: float = 3.0
    flood_zone_probability: float = 0.15  # 15% in flood zone
    
    # Geographic/shock variables
    num_regions: int = 5
    shock_year: int = 2015  # Year of environmental shock
    shock_intensity: float = 0.2  # 20% price penalty post-shock

    def __post_init__(self) -> None:
        if self.n_samples <= 0:
            raise ValueError("n_samples must be > 0")
        if self.num_regions <= 0:
            raise ValueError("num_regions must be > 0")
        if not 0.0 <= self.flood_zone_probability <= 1.0:
            raise ValueError("flood_zone_probability must be in [0, 1]")
        if not 0.0 <= self.shock_intensity <= 1.0:
            raise ValueError("shock_intensity must be in [0, 1]")

@dataclass
class HedonicConfig:
    """Configuration for hedonic model estimation."""
    
    use_log_price: bool = True
    test_size: float = 0.2
    random_state: int = 42
    standardize_features: bool = True
    
    # Feature sets
    structural_features: list = field(
        default_factory=lambda: ['sqft', 'bedrooms', 'bathrooms', 'age']
    )
    neighborhood_features: list = field(
        default_factory=lambda: ['school_rating', 'crime_rate', 'walkability']
    )
    environmental_features: list = field(
        default_factory=lambda: ['pm25', 'no2', 'ozone', 'tri_proximity', 'flood_zone']
    )

    def __post_init__(self) -> None:
        if not 0.0 < self.test_size < 1.0:
            raise ValueError("test_size must be between 0 and 1")
        if not self.structural_features:
            raise ValueError("structural_features cannot be empty")
        if not self.neighborhood_features:
            raise ValueError("neighborhood_features cannot be empty")
        if not self.environmental_features:
            raise ValueError("environmental_features cannot be empty")

@dataclass
class EconometricConfig:
    """Configuration for econometric methods."""
    
    # Difference-in-Differences
    did_treatment_year: int = 2015
    did_bandwidth: float = 2.0  # Years before/after shock
    
    # Regression Discontinuity
    rdd_cutoff: float = 2.5  # km distance to TRI site (treatment threshold)
    rdd_bandwidth: float = 1.0  # km bandwidth around cutoff
    rdd_polynomial: int = 1  # 1 for linear, 2 for quadratic
    
    # Instrumental Variables
    iv_use_wind_pattern: bool = True
    iv_distance_threshold: float = 5.0  # km from freeway
    
    # Statistical settings
    robust_se: bool = True  # Use robust standard errors
    cluster_var: str = 'region'  # Variable to cluster standard errors
    confidence_level: float = 0.95

    def __post_init__(self) -> None:
        if self.rdd_polynomial < 1:
            raise ValueError("rdd_polynomial must be >= 1")
        if not 0.0 < self.confidence_level < 1.0:
            raise ValueError("confidence_level must be between 0 and 1")
        if not self.cluster_var:
            raise ValueError("cluster_var cannot be empty")


@dataclass
class APIConfig:
    """Configuration for external API connections (for future use)."""
    
    # EPA API
    EPA_BASE_URL: str = "https://api.epa.gov/api/"
    EPA_KEY: Optional[str] = None  # To be set from environment
    
    # Zillow API
    ZILLOW_BASE_URL: str = "https://api.zillow.com/api/"
    ZILLOW_KEY: Optional[str] = None
    
    # TRI Database
    TRI_BASE_URL: str = "https://www.epa.gov/enviro/tri_query_api"
    TRI_KEY: Optional[str] = None


@dataclass
class PipelineConfig:
    """Root configuration object for the full pipeline."""

    data: DataConfig = field(default_factory=DataConfig)
    hedonic: HedonicConfig = field(default_factory=HedonicConfig)
    econometric: EconometricConfig = field(default_factory=EconometricConfig)
    api: APIConfig = field(default_factory=APIConfig)
    output_dir: str = 'output'


T = TypeVar('T')


def _merge_dict(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    """Recursively merge dictionaries with override values taking precedence."""
    merged = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _merge_dict(merged[key], value)
        else:
            merged[key] = value
    return merged


def _coerce_value(raw_value: str, current_value: Any) -> Any:
    """Convert environment variable strings to the inferred target type."""
    if isinstance(current_value, bool):
        return raw_value.strip().lower() in {'1', 'true', 'yes', 'y', 'on'}
    if isinstance(current_value, int) and not isinstance(current_value, bool):
        return int(raw_value)
    if isinstance(current_value, float):
        return float(raw_value)
    if isinstance(current_value, list):
        value = raw_value.strip()
        if value.startswith('['):
            return json.loads(value)
        return [item.strip() for item in raw_value.split(',') if item.strip()]
    return raw_value


def _set_nested_value(config_dict: Dict[str, Any], path: list, raw_value: str) -> None:
    """Set a nested dictionary value using an environment-style key path."""
    current = config_dict
    for part in path[:-1]:
        if part not in current or not isinstance(current[part], dict):
            current[part] = {}
        current = current[part]

    leaf = path[-1]
    existing = current.get(leaf)
    if existing is not None:
        current[leaf] = _coerce_value(raw_value, existing)
    else:
        current[leaf] = raw_value


def _apply_env_overrides(config_dict: Dict[str, Any], env_prefix: str = 'HEDONIC_') -> Dict[str, Any]:
    """Apply environment variable overrides to a nested config dictionary.

    Expected format:
    - HEDONIC_DATA__N_SAMPLES=5000
    - HEDONIC_HEDONIC__TEST_SIZE=0.3
    - HEDONIC_OUTPUT_DIR=custom_output
    """
    updated = dict(config_dict)
    for env_key, env_value in os.environ.items():
        if not env_key.startswith(env_prefix):
            continue

        path = env_key[len(env_prefix):].lower().split('__')
        if path and path[0]:
            _set_nested_value(updated, path, env_value)
    return updated


def _from_dict(dataclass_type: Type[T], values: Dict[str, Any]) -> T:
    """Instantiate dataclass recursively from a dictionary."""
    kwargs: Dict[str, Any] = {}
    type_hints = get_type_hints(dataclass_type)
    for dataclass_field in fields(dataclass_type):
        key = dataclass_field.name
        if key not in values:
            continue

        raw_value = values[key]
        field_type = type_hints.get(key, dataclass_field.type)
        if is_dataclass(field_type) and isinstance(raw_value, dict):
            kwargs[key] = _from_dict(field_type, raw_value)
        else:
            kwargs[key] = raw_value
    return dataclass_type(**kwargs)


def load_pipeline_config(
    config_path: Optional[str] = None,
    env_prefix: str = 'HEDONIC_'
) -> PipelineConfig:
    """Load pipeline config from defaults, optional JSON file, and environment."""
    config_dict = asdict(PipelineConfig())

    if config_path:
        with open(config_path, 'r', encoding='utf-8') as file_obj:
            file_overrides = json.load(file_obj)
        config_dict = _merge_dict(config_dict, file_overrides)

    config_dict = _apply_env_overrides(config_dict, env_prefix=env_prefix)
    return _from_dict(PipelineConfig, config_dict)


def load_component_configs(
    config_path: Optional[str] = None,
    env_prefix: str = 'HEDONIC_'
) -> Tuple[DataConfig, HedonicConfig, EconometricConfig]:
    """Compatibility helper that returns the three core component configs."""
    pipeline_config = load_pipeline_config(config_path=config_path, env_prefix=env_prefix)
    return pipeline_config.data, pipeline_config.hedonic, pipeline_config.econometric


def save_default_config(filepath: str) -> None:
    """Write default pipeline configuration to JSON for quick customization."""
    defaults = asdict(PipelineConfig())
    with open(filepath, 'w', encoding='utf-8') as file_obj:
        json.dump(defaults, file_obj, indent=2)


# Default configurations
DEFAULT_DATA_CONFIG = DataConfig()
DEFAULT_HEDONIC_CONFIG = HedonicConfig()
DEFAULT_ECONOMETRIC_CONFIG = EconometricConfig()
DEFAULT_API_CONFIG = APIConfig()
DEFAULT_PIPELINE_CONFIG = PipelineConfig()