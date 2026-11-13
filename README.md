# Explosion_sim

Orifice-plate flow and thermal-box heat-release model for a blast device.

## Setup

Requires Python 3.13+.

With [uv](https://docs.astral.sh/uv/):

```bash
git clone https://github.com/FridrikMagnusson/Explosion_sim.git
cd Explosion_sim
uv venv
uv pip install -r requirements.txt
```

Or with plain pip:

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

Plots are written to `output/` (created automatically).
