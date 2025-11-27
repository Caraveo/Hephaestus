#!/usr/bin/env python3
"""
Extensive Test Suite for Hephaestus
Tests all sampler algorithms, refinement modes, and key options
"""

import os
import sys
import subprocess
import json
import time
from pathlib import Path
from datetime import datetime

# Fix OpenMP conflict on Mac
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

# Test configuration
TEST_CONFIG = {
    "base_prompt": "a test robot",
    "test_dir": "test_results",
    "quick_test": False,  # Set to True for faster tests (fewer steps)
    "skip_refinement": False,  # Set to True to skip refinement tests
}

# Test cases
SAMPLERS = ["ddim", "plms", "dpm_solver"]
REFINEMENT_MODES = ["if2", "sd", "if", "if2_fixgeo", "sd_fixgeo", "if_fixgeo"]
CFG_SCALES = [1.0, 3.0, 7.5, 10.0]
STEP_COUNTS = [50, 100, 200] if not TEST_CONFIG["quick_test"] else [30, 50]
MESH_RESOLUTIONS = [64, 128, 256]
RENDER_RESOLUTIONS = [64, 128]


class TestResult:
    def __init__(self, test_name, success, duration, output_path=None, error=None):
        self.test_name = test_name
        self.success = success
        self.duration = duration
        self.output_path = output_path
        self.error = error
        self.timestamp = datetime.now().isoformat()


class TestRunner:
    def __init__(self):
        self.results = []
        self.test_dir = Path(TEST_CONFIG["test_dir"])
        self.test_dir.mkdir(exist_ok=True)
        
    def log(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")
        
    def run_command(self, cmd, timeout=600):
        """Run a command and return success status"""
        try:
            start_time = time.time()
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd="/Users/caraveo/Hephaestus"
            )
            duration = time.time() - start_time
            
            success = result.returncode == 0
            return success, duration, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return False, timeout, "", "Test timed out"
        except Exception as e:
            return False, 0, "", str(e)
    
    def test_basic_generation(self):
        """Test 1: Basic generation with default settings"""
        self.log("=" * 60)
        self.log("TEST 1: Basic Generation (Default Settings)")
        self.log("=" * 60)
        
        cmd = f"""python -u sample_stage1.py \\
            --text "{TEST_CONFIG['base_prompt']}" \\
            --samples 1 \\
            --sampler ddim \\
            --steps 50 \\
            --cfg_scale 7.5 \\
            --seed 42 \\
            --no_video"""
        
        success, duration, stdout, stderr = self.run_command(cmd)
        
        result = TestResult(
            "Basic Generation",
            success,
            duration,
            error=stderr if not success else None
        )
        self.results.append(result)
        
        if success:
            self.log(f"✅ PASSED in {duration:.2f}s")
        else:
            self.log(f"❌ FAILED: {stderr[:200]}")
        return success
    
    def test_all_samplers(self):
        """Test 2: All sampler algorithms"""
        self.log("=" * 60)
        self.log("TEST 2: Testing All Sampler Algorithms")
        self.log("=" * 60)
        
        all_passed = True
        for sampler in SAMPLERS:
            self.log(f"Testing sampler: {sampler}")
            
            cmd = f"""python -u sample_stage1.py \\
                --text "{TEST_CONFIG['base_prompt']}" \\
                --samples 1 \\
                --sampler {sampler} \\
                --steps {STEP_COUNTS[0]} \\
                --cfg_scale 7.5 \\
                --seed 42 \\
                --no_video \\
                --no_mcubes"""
            
            success, duration, stdout, stderr = self.run_command(cmd, timeout=300)
            
            result = TestResult(
                f"Sampler: {sampler}",
                success,
                duration,
                error=stderr if not success else None
            )
            self.results.append(result)
            
            if success:
                self.log(f"  ✅ {sampler} PASSED in {duration:.2f}s")
            else:
                self.log(f"  ❌ {sampler} FAILED: {stderr[:200]}")
                all_passed = False
        
        return all_passed
    
    def test_cfg_scales(self):
        """Test 3: Different CFG scales"""
        self.log("=" * 60)
        self.log("TEST 3: Testing Different CFG Scales")
        self.log("=" * 60)
        
        all_passed = True
        for cfg_scale in CFG_SCALES:
            self.log(f"Testing CFG scale: {cfg_scale}")
            
            cmd = f"""python -u sample_stage1.py \\
                --text "{TEST_CONFIG['base_prompt']}" \\
                --samples 1 \\
                --sampler ddim \\
                --steps {STEP_COUNTS[0]} \\
                --cfg_scale {cfg_scale} \\
                --seed 42 \\
                --no_video \\
                --no_mcubes"""
            
            success, duration, stdout, stderr = self.run_command(cmd, timeout=300)
            
            result = TestResult(
                f"CFG Scale: {cfg_scale}",
                success,
                duration,
                error=stderr if not success else None
            )
            self.results.append(result)
            
            if success:
                self.log(f"  ✅ CFG {cfg_scale} PASSED in {duration:.2f}s")
            else:
                self.log(f"  ❌ CFG {cfg_scale} FAILED: {stderr[:200]}")
                all_passed = False
        
        return all_passed
    
    def test_step_counts(self):
        """Test 4: Different step counts"""
        self.log("=" * 60)
        self.log("TEST 4: Testing Different Step Counts")
        self.log("=" * 60)
        
        all_passed = True
        for steps in STEP_COUNTS:
            self.log(f"Testing steps: {steps}")
            
            cmd = f"""python -u sample_stage1.py \\
                --text "{TEST_CONFIG['base_prompt']}" \\
                --samples 1 \\
                --sampler ddim \\
                --steps {steps} \\
                --cfg_scale 7.5 \\
                --seed 42 \\
                --no_video \\
                --no_mcubes"""
            
            success, duration, stdout, stderr = self.run_command(cmd, timeout=300)
            
            result = TestResult(
                f"Steps: {steps}",
                success,
                duration,
                error=stderr if not success else None
            )
            self.results.append(result)
            
            if success:
                self.log(f"  ✅ {steps} steps PASSED in {duration:.2f}s")
            else:
                self.log(f"  ❌ {steps} steps FAILED: {stderr[:200]}")
                all_passed = False
        
        return all_passed
    
    def test_mesh_resolutions(self):
        """Test 5: Different mesh resolutions"""
        self.log("=" * 60)
        self.log("TEST 5: Testing Different Mesh Resolutions")
        self.log("=" * 60)
        
        all_passed = True
        for res in MESH_RESOLUTIONS:
            self.log(f"Testing mesh resolution: {res}")
            
            cmd = f"""python -u sample_stage1.py \\
                --text "{TEST_CONFIG['base_prompt']}" \\
                --samples 1 \\
                --sampler ddim \\
                --steps {STEP_COUNTS[0]} \\
                --cfg_scale 7.5 \\
                --mcubes_res {res} \\
                --seed 42 \\
                --no_video"""
            
            success, duration, stdout, stderr = self.run_command(cmd, timeout=600)
            
            result = TestResult(
                f"Mesh Resolution: {res}",
                success,
                duration,
                error=stderr if not success else None
            )
            self.results.append(result)
            
            if success:
                self.log(f"  ✅ {res}³ resolution PASSED in {duration:.2f}s")
            else:
                self.log(f"  ❌ {res}³ resolution FAILED: {stderr[:200]}")
                all_passed = False
        
        return all_passed
    
    def test_mps_refinement(self):
        """Test 6: MPS refinement (Mac native)"""
        self.log("=" * 60)
        self.log("TEST 6: Testing MPS Refinement (Mac Native)")
        self.log("=" * 60)
        
        # Check if MPS is available
        check_cmd = "python -c 'import torch; print(torch.backends.mps.is_available())'"
        success, _, stdout, _ = self.run_command(check_cmd, timeout=10)
        
        if not stdout.strip() == "True":
            self.log("  ⚠️  MPS not available, skipping MPS refinement tests")
            return True
        
        self.log("Testing MPS refinement...")
        
        cmd = f"""python -u sample_stage1.py \\
            --text "{TEST_CONFIG['base_prompt']}" \\
            --samples 1 \\
            --sampler ddim \\
            --steps 50 \\
            --cfg_scale 7.5 \\
            --refine \\
            --refine_iters 200 \\
            --seed 42 \\
            --no_video"""
        
        success, duration, stdout, stderr = self.run_command(cmd, timeout=600)
        
        result = TestResult(
            "MPS Refinement",
            success,
            duration,
            error=stderr if not success else None
        )
        self.results.append(result)
        
        if success:
            self.log(f"  ✅ MPS Refinement PASSED in {duration:.2f}s")
        else:
            self.log(f"  ❌ MPS Refinement FAILED: {stderr[:200]}")
        
        return success
    
    def test_refinement_modes(self):
        """Test 7: All refinement modes (if CUDA available)"""
        if TEST_CONFIG["skip_refinement"]:
            self.log("Skipping refinement mode tests (skip_refinement=True)")
            return True
        
        self.log("=" * 60)
        self.log("TEST 7: Testing All Refinement Modes (CUDA only)")
        self.log("=" * 60)
        
        # Check if CUDA is available
        check_cmd = "python -c 'import torch; print(torch.cuda.is_available())'"
        success, _, stdout, _ = self.run_command(check_cmd, timeout=10)
        
        if not stdout.strip() == "True":
            self.log("  ⚠️  CUDA not available, skipping threefiner refinement tests")
            return True
        
        # Check if threefiner is available
        check_cmd = "threefiner --help > /dev/null 2>&1 && echo 'True' || echo 'False'"
        success, _, stdout, _ = self.run_command(check_cmd, timeout=10)
        
        if not stdout.strip() == "True":
            self.log("  ⚠️  threefiner not installed, skipping refinement mode tests")
            return True
        
        all_passed = True
        for mode in REFINEMENT_MODES:
            self.log(f"Testing refinement mode: {mode}")
            
            cmd = f"""python -u sample_stage1.py \\
                --text "{TEST_CONFIG['base_prompt']}" \\
                --samples 1 \\
                --sampler ddim \\
                --steps 50 \\
                --cfg_scale 7.5 \\
                --refine \\
                --refine_mode {mode} \\
                --refine_iters 200 \\
                --seed 42 \\
                --no_video"""
            
            success, duration, stdout, stderr = self.run_command(cmd, timeout=600)
            
            result = TestResult(
                f"Refinement Mode: {mode}",
                success,
                duration,
                error=stderr if not success else None
            )
            self.results.append(result)
            
            if success:
                self.log(f"  ✅ {mode} PASSED in {duration:.2f}s")
            else:
                self.log(f"  ❌ {mode} FAILED: {stderr[:200]}")
                all_passed = False
        
        return all_passed
    
    def test_edge_cases(self):
        """Test 8: Edge cases and error handling"""
        self.log("=" * 60)
        self.log("TEST 8: Testing Edge Cases")
        self.log("=" * 60)
        
        edge_cases = [
            {
                "name": "Very short prompt",
                "prompt": "robot",
                "steps": 30,
            },
            {
                "name": "Long prompt",
                "prompt": "a detailed mechanical robot with glowing blue eyes and articulated joints",
                "steps": 30,
            },
            {
                "name": "Minimum steps",
                "prompt": TEST_CONFIG['base_prompt'],
                "steps": 10,
            },
            {
                "name": "Low CFG scale",
                "prompt": TEST_CONFIG['base_prompt'],
                "steps": 30,
                "cfg_scale": 1.0,
            },
        ]
        
        all_passed = True
        for case in edge_cases:
            self.log(f"Testing: {case['name']}")
            
            prompt = case.get("prompt", TEST_CONFIG['base_prompt'])
            steps = case.get("steps", STEP_COUNTS[0])
            cfg = case.get("cfg_scale", 7.5)
            
            cmd = f"""python -u sample_stage1.py \\
                --text "{prompt}" \\
                --samples 1 \\
                --sampler ddim \\
                --steps {steps} \\
                --cfg_scale {cfg} \\
                --seed 42 \\
                --no_video \\
                --no_mcubes"""
            
            success, duration, stdout, stderr = self.run_command(cmd, timeout=300)
            
            result = TestResult(
                f"Edge Case: {case['name']}",
                success,
                duration,
                error=stderr if not success else None
            )
            self.results.append(result)
            
            if success:
                self.log(f"  ✅ {case['name']} PASSED in {duration:.2f}s")
            else:
                self.log(f"  ❌ {case['name']} FAILED: {stderr[:200]}")
                all_passed = False
        
        return all_passed
    
    def generate_report(self):
        """Generate test report"""
        self.log("=" * 60)
        self.log("GENERATING TEST REPORT")
        self.log("=" * 60)
        
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r.success)
        failed_tests = total_tests - passed_tests
        total_duration = sum(r.duration for r in self.results)
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total": total_tests,
                "passed": passed_tests,
                "failed": failed_tests,
                "success_rate": f"{(passed_tests/total_tests*100):.1f}%",
                "total_duration": f"{total_duration:.2f}s",
            },
            "results": [
                {
                    "test_name": r.test_name,
                    "success": r.success,
                    "duration": f"{r.duration:.2f}s",
                    "error": r.error[:500] if r.error else None,
                    "timestamp": r.timestamp,
                }
                for r in self.results
            ]
        }
        
        # Save report
        report_path = self.test_dir / "test_report.json"
        with open(report_path, "w") as f:
            json.dump(report, f, indent=2)
        
        # Print summary
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests} ✅")
        print(f"Failed: {failed_tests} ❌")
        print(f"Success Rate: {report['summary']['success_rate']}")
        print(f"Total Duration: {total_duration:.2f}s")
        print(f"\nReport saved to: {report_path}")
        
        if failed_tests > 0:
            print("\nFailed Tests:")
            for r in self.results:
                if not r.success:
                    print(f"  ❌ {r.test_name}")
                    if r.error:
                        print(f"     Error: {r.error[:200]}")
        
        return report
    
    def run_all_tests(self):
        """Run all tests"""
        start_time = time.time()
        
        self.log("Starting Extensive Test Suite for Hephaestus")
        self.log(f"Test directory: {self.test_dir}")
        self.log(f"Quick test mode: {TEST_CONFIG['quick_test']}")
        
        tests = [
            ("Basic Generation", self.test_basic_generation),
            ("All Samplers", self.test_all_samplers),
            ("CFG Scales", self.test_cfg_scales),
            ("Step Counts", self.test_step_counts),
            ("Mesh Resolutions", self.test_mesh_resolutions),
            ("MPS Refinement", self.test_mps_refinement),
            ("Refinement Modes", self.test_refinement_modes),
            ("Edge Cases", self.test_edge_cases),
        ]
        
        for test_name, test_func in tests:
            try:
                test_func()
            except Exception as e:
                self.log(f"Test '{test_name}' crashed: {e}", level="ERROR")
                result = TestResult(
                    test_name,
                    False,
                    0,
                    error=str(e)
                )
                self.results.append(result)
        
        total_time = time.time() - start_time
        self.log(f"\nAll tests completed in {total_time:.2f}s")
        
        return self.generate_report()


if __name__ == "__main__":
    runner = TestRunner()
    report = runner.run_all_tests()
    
    # Exit with error code if any tests failed
    failed_count = sum(1 for r in runner.results if not r.success)
    sys.exit(1 if failed_count > 0 else 0)

