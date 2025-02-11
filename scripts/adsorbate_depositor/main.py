#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path

from src.configHandler import ConfigHandler
from src.adsorbateGenerator import AdsorbateGenerator
from src.siteGenerator import SiteGenerator
from src.adsorbateDepositor import AdsorbateDepositor

def main():
    # Read config.yaml or copy the template
    cfg_handler = ConfigHandler()

    if cfg_handler.check_config_exists():
        config = cfg_handler.load_config()
    else:
        cfg_handler.copy_config_template(template_path=Path("database") / "config_template.yaml")

    # Generate sites
    site_generator = SiteGenerator(
        POSCAR_substrate=config["substrate"]["path"],
        distance=config["deposit"]["distance"],
        sites=config["substrate"]["sites"]
        )
    sites = site_generator.generate()

    # Generate adsorbates
    adsorbate_generator = AdsorbateGenerator(generate_rotations=config["adsorbate"]["rotation"])
    adsorbates = adsorbate_generator.generate(
        work_mode=config["adsorbate"]["source"],
        path=config["adsorbate"]["path"],
        atom_indexes=config["adsorbate"]["atom_indexes"],
        pathway_name=config["adsorbate"]["pathway_name"]
        )

    # Generate adsorbate-on-site structure files
    structure_generator = AdsorbateDepositor(
        POSCAR_substrate=config["substrate"]["path"],
        sites=sites,
        adsorbates=adsorbates,
        auto_reposition_along_z=config["deposit"]["auto_reposition_along_z"],
        distance=config["deposit"]["distance"],
        output_dir=config["deposit"]["output_dir"]
        )

    structure_generator.deposit()

if __name__ == "__main__":
    main()
