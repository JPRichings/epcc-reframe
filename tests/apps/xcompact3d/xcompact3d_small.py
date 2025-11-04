"""Small test for XCompact3D"""

# Based on original work from:
#   Copyright 2016-2022 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
#   ReFrame Project Developers. See the top-level LICENSE file for details.
#   SPDX-License-Identifier: BSD-3-Clause

import os

import reframe as rfm
from xcompact3d_base import XCompact3DBaseEnvironment
from xcompact3d_build import XCompact3DSourceBuild


@rfm.simple_test
class XCompact3DSmallTest(XCompact3DBaseEnvironment):
    """Using the source build, run a small XCompact3D test"""

    xcompact3d_binary = fixture(XCompact3DSourceBuild, scope="environment")
    tags = {"applications", "performance", "short"}

    num_nodes = 8
    num_tasks_per_node = 128
    num_cpus_per_task = 1
    num_tasks = num_nodes * num_tasks_per_node * num_cpus_per_task

    env_vars = {"OMP_NUM_THREADS": str(num_cpus_per_task)}

    time_limit = "20m"
    executable_opts = ["input-8.i3d"]

    reference = {"archer2:compute": {"performance": (1.07, -0.2, 0.2, "seconds")}}

    @run_after("setup")
    def set_executable(self):
        """Sets up executable"""
        self.executable = os.path.join(self.xcompact3d_binary.stagedir, "Incompact3d/bin/xcompact3d")
