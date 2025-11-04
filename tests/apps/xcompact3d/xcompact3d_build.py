#!/usr/bin/env python3

"""Reframe test for XCompact3D"""

# Based on original work from:
#   Copyright 2016-2022 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
#   ReFrame Project Developers. See the top-level LICENSE file for details.
#   SPDX-License-Identifier: BSD-3-Clause

import reframe as rfm
import reframe.utility.sanity as sn


class XCompact3DSourceBuild(rfm.CompileOnlyRegressionTest):
    """Build XCompact3D from source"""

    valid_systems = ["archer2:compute"]
    valid_prog_environs = ["PrgEnv-gnu"]

    build_system = "CMake"
    modules = ["cmake"]
    local = True
    build_locally = True

    prebuild_cmds = [
        "git clone https://github.com/xcompact3d/Incompact3d.git",
        "cd Incompact3d",
        "git checkout v5.0",
    ]

    builddir = "build"
    executable = "build/bin/xcompact3d"
    max_concurreny = 8

    @sanity_function
    def assert_finished(self):
        """Sanity check that build finished successfully"""
        return sn.assert_not_found("ERROR", self.stdout)
