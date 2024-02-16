import os
import random
import string
import yaml

import reframe as rfm
import reframe.utility.sanity as sn

from base import DeepCamBaseCheck

base_k8s_pod = {
    "apiVersion": "v1",
    "kind": "Pod",
    "metadata": {
        "generateName": "---CHANGE-NAME---"
    },
    "spec": {
        "restartPolicy": "Never",
        "containers": [
            {
                "name": "---CHANGE-NAME---",
                "image": "bigballoon8/mlperf-epcc",
                "workingDir": "---PATH-WORKDIR---",
                "command": [
                    "---ADD-CMDs---"
                ],
                "args": [
                    "---ADD-ARGS---"
                ],
                "env": [
                    {"name": "OMP_NUM_THREADS", "value": "4"}
                ],
                "resources": {
                    "requests": {
                        "cpu": 16,
                        "memory": "16Gi"
                    },
                    "limits": {
                        "cpu": 32,
                        "memory": "32Gi",
                        "nvidia.com/gpu": "---CHANGE INT--"
                    }
                },
                "volumeMounts": [
                    {
                        "mountPath": "/mnt/ceph_rbd",
                        "name": "volume"
                    },
                    {
                        "mountPath": "/dev/shm",
                        "name": "devshm"
                    }
                ]
            }
        ],
        "nodeSelector": {
            "nvidia.com/gpu.product": "---CHANGE-NAME---"
        },
        "volumes": [
            {
                "name": "volume",
                "persistentVolumeClaim": {
                    "claimName": "---CHANGE-NAME---"
                }
            },
            {
                "name": "devshm",
                "emptyDir": {
                    "medium": "Memory"
                }
            }
        ]
    }
}

@rfm.simple_test
class DeepCAMGPUServiceBenchmark(DeepCamBaseCheck):
    valid_prog_environs = ["*"]
    valid_systems = ['eidf:gpu-service']
    env_vars = {
        "KUBECONFIG":"/kubernetes/config"
    }
    
    executable = 'python'
    
    # num_gpus = parameter(1 << pow for pow in range(3))
    #num_gpus = variable(int, value=4) 
    num_gpus = parameter([4])
    lbs = parameter([64])
    
    #node_type = parameter(["NVIDIA-A100-SXM4-40GB", "NVIDIA-A100-SXM4-80GB"])
    node_type = variable(str, value="NVIDIA-A100-SXM4-40GB") 

    @run_after("init")
    def executable_setup(self):
        self.job_name = f"mlperf-deepcam-{self.num_gpus}-{self.node_type.lower()}-"
        pod_info = base_k8s_pod
        pod_info["metadata"]["generateName"] = self.job_name
        pod_info["spec"]["containers"][0]["name"] = self.job_name[:-1] # remove '...-' at the end of str
        pod_info["spec"]["containers"][0]["workingDir"] = "/workspace/ML_HPC/DeepCAM/Torch"
        pod_info["spec"]["containers"][0]["command"] = ["torchrun"]
        pod_info["spec"]["containers"][0]["args"] = [
            f"--nproc_per_node={self.num_gpus}", 
            "train.py", 
            "-lbs", f"{self.lbs}",
            "-c", "/workspace/ML_HPC/DeepCAM/Torch/config.yaml",
            "--t_subset_size", "65536",
            "--v_subset_size", "8192"  
        ]
        
        pod_info["spec"]["containers"][0]["resources"]["limits"]["nvidia.com/gpu"] = self.num_gpus
        pod_info["spec"]["nodeSelector"]["nvidia.com/gpu.product"] = self.node_type
        pod_info["spec"]["volumes"][0]["persistentVolumeClaim"]["claimName"] = "deepcam-pv"
        
        self.pod_config = pod_info

    
    @performance_function("W", perf_key="Avg GPU Power Draw:")
    def extract_gpu_power_draw(self):
        return sn.extractsingle(r"Avg GPU Power Draw: (.*)", self.stdout, tag= 1, conv=float)

    @run_before("performance")
    def set_perf_variables(self):
        self.perf_variables = {
            "Throughput": self.extract_throughput(),
            "Epoch Length": self.extract_epoch_length(),
            "Communication Time": self.extract_communication(),
            "Avg GPU Power Draw": self.extract_gpu_power_draw(),
            "Total IO Time": self.extract_IO()
        }
        
        
        
        

    
    
    
    
    