# Setup

Tested on macOS (Apple Silicon), CPU-only. All tools are free and open source.

## 1. Docking + cheminformatics (micromamba / conda)

```bash
# install micromamba (single static binary) if you don't have it, then:
micromamba create -y -n dock -c conda-forge python=3.11 vina rdkit meeko "numpy<2"
```

## 2. Open Babel (format conversion + RMSD)

```bash
# macOS
brew install open-babel
# or via conda-forge: micromamba install -n dock -c conda-forge openbabel
```

## 3. Structure prediction (optional — only needed to re-fold)

[LocalColabFold](https://github.com/YoshitakaMo/localcolabfold) provides AlphaFold2 locally.
The first run downloads ~3.5 GB of model weights (cached afterwards).

## 4. Point the scripts at your tools

`scripts/redock.sh` reads tool paths from environment variables (defaults assume they are on `PATH`):

```bash
export VINA=$(micromamba run -n dock which vina)
export OBABEL=$(which obabel)
export OBRMS=$(which obrms)
scripts/redock.sh 1FKB.pdb RAP A FKBP12_RAPA
```

## 5. Figures (optional)

```bash
micromamba create -y -n viz -c conda-forge pymol-open-source "numpy<2"
```
