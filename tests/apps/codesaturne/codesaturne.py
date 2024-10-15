#!/usr/bin/env python3

"""Reframe test for code saturne"""

# Based on original work from:
#   Copyright 2016-2022 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
#   ReFrame Project Developers. See the top-level LICENSE file for details.
#   SPDX-License-Identifier: BSD-3-Clause

import reframe as rfm
import reframe.utility.sanity as sn
import reframe.utility.osext


@rfm.simple_test
class CodeSaturneSmallTest(rfm.RunOnlyRegressionTest):
    """XCompact 3D Large Test"""

    valid_systems = ["archer2:compute"]
    valid_prog_environs = ["PrgEnv-cray"]

    tags = {"applications"}

    num_nodes = 1
    num_tasks_per_node = 4
    num_cpus_per_task = 32
    num_tasks = num_nodes * num_tasks_per_node

    env_vars = {"OMP_NUM_THREADS": 1, "SRUN_CPUS_PER_TASK": "$SLURM_CPUS_PER_TASK"}

    time_limit = "20m"
    build_system = None
    # build_system.ftn = "ftn"
    # prebuild_cmds = [
    #     "git clone https://github.com/xcompact3d/Incompact3d.git",
    #    "cd Incompact3d",
    #]
    # builddir = "Incompact3d"
    
    executable = "./cs_solver"
    executable_opts = ["--mpi $@"]
    modules = ["code_saturne","craype-network-ucx","cray-mpich-ucx"]

    # reference = {"archer2:compute": {"steptime": (6.3, -0.2, 0.2, "seconds")}}

    @run_before("run")
    def setup_input(self):
        self.prerun_cmds = ["code_saturne create -s T_junction -c case1",
                            "cp setup.xml ./T_junction/case1/DATA",
                            "cp downcomer.des ./T_junction/MESH",
                            "cd ./T_junction/case1/DATA",
                            "code_saturne run --initialize --param setup.xml --nprocs 4",
                            "cd ../RESU/202*"  
                            ]

    @sanity_function
    def assert_finished(self):
        """Sanity check that simulation finished successfully"""
        # T_junction/case1/RESU/20241003-1433/run_solver.log END OF CALCULATION
        print(reframe.utility.osext.run_command("pwd"))
        log_file = reframe.utility.osext.run_command("find . -name run_solver.log")
        print(log_file)
        log_file_strip = str(log_file.stdout).strip("\n")
        print(log_file_strip)
        return sn.assert_found("END OF CALCULATION", log_file_strip)

    #@performance_function("seconds", perf_key="performance")
    #def extract_perf(self):
    #    """Extract performance value to compare with reference value"""
    #    return sn.extractsingle(
    #        r"Averaged time per step \(s\):\s+(?P<steptime>\S+)",
    #        self.stdout,
    #        "steptime",
    #        float,
    #    )
