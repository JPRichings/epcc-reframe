"""ReFrame Base XCompact3D"""

import reframe as rfm
import reframe.utility.sanity as sn


class XCompact3DBaseEnvironment(rfm.RunOnlyRegressionTest):
    """Definition of functions used for all XCompact3D ReFrame tests"""

    maintainers = ["j.richings@epcc.ed.ac.uk", "e.broadway@epcc.ed.ac.uk"]
    strict_check = True
    use_multithreading = False

    valid_systems = ["archer2:compute"]
    valid_prog_environs = ["PrgEnv-gnu"]

    @sanity_function
    def assert_finished(self):
        """Sanity check that simulation finished successfully"""
        return sn.assert_found("Good job!", self.stdout)

    @performance_function("seconds", perf_key="performance")
    def extract_perf(self):
        """Extract performance value to compare with reference value"""
        return sn.extractsingle(
            r"Averaged time per step \(s\):\s+(?P<steptime>\S+)",
            self.stdout,
            "steptime",
            float,
        )
