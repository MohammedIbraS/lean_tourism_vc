"""
Scenario save/load functionality
"""
import json
import streamlit as st
from datetime import datetime

def save_scenario_config(config_dict, scenario_name=None):
    """Save scenario configuration to session state"""
    if scenario_name is None:
        scenario_name = f"scenario_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    if 'saved_scenarios' not in st.session_state:
        st.session_state.saved_scenarios = {}
    
    st.session_state.saved_scenarios[scenario_name] = {
        'config': config_dict,
        'timestamp': datetime.now().isoformat(),
        'name': scenario_name
    }
    
    return scenario_name

def load_scenario_config(scenario_name):
    """Load scenario configuration from session state"""
    if 'saved_scenarios' not in st.session_state:
        return None
    
    if scenario_name in st.session_state.saved_scenarios:
        return st.session_state.saved_scenarios[scenario_name]['config']
    
    return None

def get_saved_scenarios():
    """Get list of all saved scenarios"""
    if 'saved_scenarios' not in st.session_state:
        return {}
    
    return st.session_state.saved_scenarios

def delete_scenario(scenario_name):
    """Delete a saved scenario"""
    if 'saved_scenarios' in st.session_state:
        if scenario_name in st.session_state.saved_scenarios:
            del st.session_state.saved_scenarios[scenario_name]
            return True
    return False

def export_scenario_to_json(config_dict, scenario_name):
    """Export scenario to JSON string"""
    export_data = {
        'scenario_name': scenario_name,
        'timestamp': datetime.now().isoformat(),
        'config': config_dict
    }
    return json.dumps(export_data, indent=2)

def import_scenario_from_json(json_string):
    """Import scenario from JSON string"""
    try:
        data = json.loads(json_string)
        return data.get('config', {}), data.get('scenario_name', 'imported_scenario')
    except json.JSONDecodeError:
        return None, None

def create_scenario_config(global_params, scenario_a_params, scenario_b_params):
    """Create a complete scenario configuration dictionary"""
    return {
        'global': global_params,
        'scenario_a': scenario_a_params,
        'scenario_b': scenario_b_params,
        'metadata': {
            'created': datetime.now().isoformat(),
            'version': '1.0'
        }
    }

def apply_scenario_config(config):
    """Apply a scenario configuration and return parameters"""
    global_params = config.get('global', {})
    scenario_a = config.get('scenario_a', {})
    scenario_b = config.get('scenario_b', {})
    
    return global_params, scenario_a, scenario_b

