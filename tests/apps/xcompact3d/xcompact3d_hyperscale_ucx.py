"""Hyperscale reframe test for XCompact3D"""

# Based on original work from:
#   Copyright 2016-2022 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
#   ReFrame Project Developers. See the top-level LICENSE file for details.
#   SPDX-License-Identifier: BSD-3-Clause

import os

import reframe as rfm
from xcompact3d_base import XCompact3DBaseEnvironment
from xcompact3d_build import XCompact3DSourceBuild


@rfm.simple_test
class XCompact3DHyperscaleUCXTest(XCompact3DBaseEnvironment):
    """Using the source build, run a hyperscale XCompact3D test with UCX"""

    xcompact3d_binary = fixture(XCompact3DSourceBuild, scope="environment")
    tags = {"performance", "hyperscale", "applications"}

    num_nodes = 2048
    num_tasks_per_node = 128
    num_cpus_per_task = 1
    num_tasks = num_nodes * num_tasks_per_node * num_cpus_per_task

    modules = ["craype-network-ucx", "cray-mpich-ucx"]

    env_vars = {
        "OMP_NUM_THREADS": str(num_cpus_per_task),
        "UCX_TLS": "dc,self,sm",
        "UCX_DC_MLX5_RX_QUEUE_LEN": "20000",
        "UCX_DC_RX_QUEUE_LEN": "20000",
        "UCX_DC_MLX5_TIMEOUT": "20m",
        "UCX_DC_TIMEOUT": "20m",
        "UCX_UD_MLX5_TX_NUM_GET_BYTES": "1G",
        "UCX_UD_MLX5_MAX_GET_ZCOPY": "128k",
    }

    time_limit = "1h"
    executable_opts = ["input-2048.i3d"]

    reference = {"archer2:compute": {"performance": (6.3, -0.2, 0.2, "seconds")}}

    @run_after("setup")
    def set_executable(self):
        """Sets up executable"""
        self.executable = os.path.join(self.xcompact3d_binary.stagedir, "Incompact3d/bin/xcompact3d")
