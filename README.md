Tourism Virtual Clinic Simulator (Modular)
==========================================

Files:
- app.py : launcher that selects pages
- pages/1_comparison.py : main landing comparison with multiple surface plots
- pages/2_whatif.py : detailed what-if simulator with KPIs
- utils/calculations.py : core scenario logic and KPI calculators
- utils/plots.py : plotting helpers (plotly surface)
- requirements.txt : python dependencies

How to run:
1. create a virtual environment and install dependencies:
   python -m venv venv
   source venv/bin/activate   (Windows: .\venv\Scripts\activate)
   pip install -r requirements.txt

2. run:
   streamlit run app.py

Notes:
- The app includes two scenarios:
  Scenario A — Paid VC (company revenue from VC fee)
  Scenario B — Free VC (company covers VC costs; premium funds emergency insurance)
- The Comparison page shows multiple 3D surface plots (Plotly). Use the sidebar to adjust global ranges and defaults.
- The What-If page allows input of specific numbers and shows detailed KPIs for each scenario.
