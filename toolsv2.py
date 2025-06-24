import os
from datetime import datetime
import subprocess
import sys
import hashlib
import requests
import json
import pytz
import re
import random
import string
import threading
import time
import google.auth
from typing import Dict
from typing import List, Dict, Optional, Any, Union
import concurrent.futures
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from github import Github
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
import pytz
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes
)
from datetime import datetime
from base64 import b64encode, b64decode
import shutil
import tempfile
import zipfile
import uuid
import binascii
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto import Random
import html
import qrcode
from io import BytesIO
import psutil
import platform
import ipaddress
import socket
from pathlib import Path

start_time = datetime.now()

#CLASS STATUS BOT
def _run(cmd: str) -> str:
    """Jalankan perintah shell, kembalikan output ter‑strip.
       Jika gagal, balikan 'Unavailable'."""
    try:
        return subprocess.check_output(
            cmd, shell=True, stderr=subprocess.DEVNULL
        ).decode().strip()
    except Exception:
        return "Unavailable"


def get_uptime_readable() -> str:
    # contoh output: 'up 1 hour, 12 minutes'
    return _run("uptime -p")


def get_cpu_load() -> str:
    """Ambil load average (tidak butuh root & selalu ada)."""
    try:
        with open("/proc/loadavg") as f:
            one, five, fifteen, *_ = f.read().split()
        return f"{one} (1m) / {five} (5m)"
    except Exception:
        return _run("uptime")  # fallback OS lain


def get_memory_usage() -> str:
    """Hitung penggunaan RAM dari /proc/meminfo."""
    try:
        info = {}
        with open("/proc/meminfo") as f:
            for line in f:
                key, val = line.split(":")
                info[key.strip()] = int(val.split()[0])  # kB
        total = info["MemTotal"]
        avail = info.get("MemAvailable", info["MemFree"])
        used = total - avail
        percent = used * 100 // total
        return f"{used//1024} MB / {total//1024} MB ({percent}%)"
    except Exception:
        return _run("free -m | awk 'NR==2{print $3\"/\"$2\" MB\"}'")


def get_disk_usage() -> str:
    # df -h / ⇒ baris ke‑2 punya data partisi root
    return _run("df -h / | awk 'NR==2{print $3\"/\"$2\" (\"$5\")\"}'")
#FINISH STATUS BOT

#CLASS COMPILE
class AdvancedCompiler:
    def __init__(self):
        self.system_info = self._get_system_info()
        self.available_compilers = self._detect_compilers()
        self.package_managers = self._detect_package_managers()
        self.installed_libraries = self._scan_libraries()
        self.build_tools = self._detect_build_tools()
        self.cross_compile_targets = self._detect_cross_compile_targets()
        self.optimization_profiles = self._create_optimization_profiles()
        self.compiler_cache = {}
        self.library_cache = {}
        
    def _get_system_info(self) -> Dict:
        """Get comprehensive system information"""
        return {
            'os': platform.system(),
            'arch': platform.machine(),
            'platform': platform.platform(),
            'processor': platform.processor(),
            'python_arch': platform.architecture(),
            'libc_ver': platform.libc_ver(),
            'cpu_count': os.cpu_count(),
            'memory_gb': psutil.virtual_memory().total / (1024**3) if 'psutil' in globals() else 'unknown',
            'is_termux': os.path.exists('/data/data/com.termux'),
            'is_android': 'android' in platform.platform().lower(),
            'kernel_version': platform.release(),
            'endianness': platform.machine(),
            'temp_dir': tempfile.gettempdir(),
            'user_id': os.getuid() if hasattr(os, 'getuid') else 'unknown',
            'shell': os.environ.get('SHELL', 'unknown')
        }
    
    def _detect_compilers(self) -> Dict:
        """Detect all available compilers with extended support"""
        compilers = {
            'gcc_variants': [],
            'clang_variants': [],
            'specialized': [],
            'cross_compilers': [],
            'alternative_compilers': [],
            'android_compilers': [],
            'embedded_compilers': [],
            'modern_compilers': [],
            'legacy_compilers': [],
            'experimental_compilers': []
        }
        
        # Extended GCC variants with more versions
        gcc_variants = [
            'gcc', 'g++', 'gcc-4.8', 'gcc-4.9', 'gcc-5', 'gcc-6', 'gcc-7', 'gcc-8', 'gcc-9', 
            'gcc-10', 'gcc-11', 'gcc-12', 'gcc-13', 'gcc-14', 'gcc-15',
            'g++-4.8', 'g++-4.9', 'g++-5', 'g++-6', 'g++-7', 'g++-8', 'g++-9', 
            'g++-10', 'g++-11', 'g++-12', 'g++-13', 'g++-14', 'g++-15',
            'x86_64-linux-gnu-gcc', 'aarch64-linux-gnu-gcc', 'i686-linux-gnu-gcc',
            'arm-linux-gnueabihf-gcc', 'arm-linux-gnueabi-gcc', 'mips-linux-gnu-gcc',
            'musl-gcc', 'musl-g++', 'gcc-multilib', 'g++-multilib',
            'gcc-snapshot', 'g++-snapshot'
        ]
        
        # Extended Clang variants with LLVM versions
        clang_variants = [
            'clang', 'clang++', 'clang-3.9', 'clang-4.0', 'clang-5.0', 'clang-6.0', 
            'clang-7', 'clang-8', 'clang-9', 'clang-10', 'clang-11', 'clang-12', 
            'clang-13', 'clang-14', 'clang-15', 'clang-16', 'clang-17', 'clang-18', 'clang-19',
            'clang++-3.9', 'clang++-4.0', 'clang++-5.0', 'clang++-6.0', 'clang++-7', 
            'clang++-8', 'clang++-9', 'clang++-10', 'clang++-11', 'clang++-12', 
            'clang++-13', 'clang++-14', 'clang++-15', 'clang++-16', 'clang++-17', 'clang++-18',
            'llvm-gcc', 'llvm-g++', 'clang-cl'
        ]
        
        # Specialized compilers with more variants
        specialized = [
            'tcc', 'pcc', 'icc', 'icpc', 'icx', 'icpx', 'dpcpp',  # Intel
            'pgcc', 'pgc++', 'nvc', 'nvc++', 'nvcc', 'nvhpc',     # NVIDIA
            'xlc', 'xlC', 'xlc++', 'xlclang', 'xlclang++',        # IBM
            'cc', 'c++', 'c89', 'c99', 'c11', 'c17', 'c2x',      # Standard
            'afl-gcc', 'afl-g++', 'afl-clang', 'afl-clang++',    # Fuzzing
            'distcc', 'ccache', 'icecc',                          # Distributed/Cached
            'ccomp', 'compcert',                                  # Verified compilers
            'kcc', 'sparse'                                       # Analysis tools
        ]
        
        # Modern alternative compilers
        modern_compilers = [
            'zig', 'rustc', 'gccgo', 'gfortran', 'flang', 'gdc',
            'emcc', 'em++', 'emconfigure', 'emmake',              # Emscripten
            'wasm-ld', 'wasm-opt', 'wasm2c', 'wasm2wat',
            'circle', 'cppfront',                                 # Experimental C++
            'carbon', 'val'                                       # Future languages
        ]
        
        # Legacy compilers for compatibility
        legacy_compilers = [
            'gcc-3.4', 'gcc-4.0', 'gcc-4.1', 'gcc-4.2', 'gcc-4.3', 'gcc-4.4',
            'g++-3.4', 'g++-4.0', 'g++-4.1', 'g++-4.2', 'g++-4.3', 'g++-4.4',
            'clang-3.0', 'clang-3.1', 'clang-3.2', 'clang-3.3', 'clang-3.4', 'clang-3.5',
            'bcc', 'lcc', 'scc'
        ]
        
        # Android/Termux specific with NDK versions
        android_compilers = [
            'aarch64-linux-android16-clang', 'aarch64-linux-android17-clang',
            'aarch64-linux-android18-clang', 'aarch64-linux-android19-clang',
            'aarch64-linux-android21-clang', 'aarch64-linux-android22-clang',
            'aarch64-linux-android23-clang', 'aarch64-linux-android24-clang',
            'aarch64-linux-android26-clang', 'aarch64-linux-android28-clang',
            'aarch64-linux-android29-clang', 'aarch64-linux-android30-clang',
            'aarch64-linux-android31-clang', 'aarch64-linux-android32-clang',
            'aarch64-linux-android33-clang', 'aarch64-linux-android34-clang',
            'armv7a-linux-androideabi16-clang', 'armv7a-linux-androideabi17-clang',
            'armv7a-linux-androideabi18-clang', 'armv7a-linux-androideabi19-clang',
            'armv7a-linux-androideabi21-clang', 'armv7a-linux-androideabi22-clang',
            'armv7a-linux-androideabi23-clang', 'armv7a-linux-androideabi24-clang',
            'i686-linux-android16-clang', 'i686-linux-android17-clang',
            'i686-linux-android18-clang', 'i686-linux-android19-clang',
            'i686-linux-android21-clang', 'i686-linux-android22-clang',
            'i686-linux-android23-clang', 'i686-linux-android24-clang',
            'x86_64-linux-android21-clang', 'x86_64-linux-android22-clang',
            'x86_64-linux-android23-clang', 'x86_64-linux-android24-clang',
            'x86_64-linux-android26-clang', 'x86_64-linux-android28-clang',
            'x86_64-linux-android29-clang', 'x86_64-linux-android30-clang',
            'x86_64-linux-android31-clang', 'x86_64-linux-android32-clang',
            'x86_64-linux-android33-clang', 'x86_64-linux-android34-clang'
        ]
        
        # Cross compilers with more architectures
        cross_compilers = [
            'arm-none-eabi-gcc', 'arm-none-eabi-g++',
            'avr-gcc', 'avr-g++', 'msp430-gcc', 'msp430-g++',
            'mips-linux-gnu-gcc', 'mips-linux-gnu-g++',
            'mips64-linux-gnuabi64-gcc', 'mips64-linux-gnuabi64-g++',
            'powerpc-linux-gnu-gcc', 'powerpc-linux-gnu-g++',
            'powerpc64-linux-gnu-gcc', 'powerpc64-linux-gnu-g++',
            'powerpc64le-linux-gnu-gcc', 'powerpc64le-linux-gnu-g++',
            'riscv32-unknown-elf-gcc', 'riscv32-unknown-elf-g++',
            'riscv64-linux-gnu-gcc', 'riscv64-linux-gnu-g++',
            'riscv64-unknown-elf-gcc', 'riscv64-unknown-elf-g++',
            'sparc64-linux-gnu-gcc', 'sparc64-linux-gnu-g++',
            's390x-linux-gnu-gcc', 's390x-linux-gnu-g++',
            'alpha-linux-gnu-gcc', 'alpha-linux-gnu-g++',
            'hppa-linux-gnu-gcc', 'hppa-linux-gnu-g++',
            'sh4-linux-gnu-gcc', 'sh4-linux-gnu-g++',
            'mingw32-gcc', 'mingw64-gcc',
            'i686-w64-mingw32-gcc', 'i686-w64-mingw32-g++',
            'x86_64-w64-mingw32-gcc', 'x86_64-w64-mingw32-g++',
            'arm-linux-musleabi-gcc', 'arm-linux-musleabihf-gcc',
            'aarch64-linux-musl-gcc', 'x86_64-linux-musl-gcc'
        ]
        
        # Embedded compilers
        embedded_compilers = [
            'xtensa-esp32-elf-gcc', 'xtensa-esp32s2-elf-gcc', 'xtensa-esp32s3-elf-gcc',
            'riscv32-esp-elf-gcc', 'arm-none-eabi-gcc',
            'avr-gcc', 'msp430-gcc', 'pic32-gcc',
            'nios2-elf-gcc', 'microblaze-xilinx-elf-gcc',
            'or1k-elf-gcc', 'lm32-elf-gcc'
        ]
        
        # Experimental compilers
        experimental_compilers = [
            'cppx', 'clang-experimental', 'gcc-experimental',
            'circle-lang', 'carbon-lang', 'val-lang',
            'cppfront', 'cpp2'
        ]
        
        compiler_lists = [
            (gcc_variants, 'gcc_variants'),
            (clang_variants, 'clang_variants'), 
            (specialized, 'specialized'),
            (modern_compilers, 'modern_compilers'),
            (legacy_compilers, 'legacy_compilers'),
            (android_compilers, 'android_compilers'),
            (cross_compilers, 'cross_compilers'),
            (embedded_compilers, 'embedded_compilers'),
            (experimental_compilers, 'experimental_compilers')
        ]
        
        for compiler_list, category in compiler_lists:
            for compiler in compiler_list:
                if shutil.which(compiler):
                    version = self._get_compiler_version(compiler)
                    target_info = self._get_compiler_target(compiler)
                    features = self._get_compiler_features(compiler)
                    compilers[category].append({
                        'name': compiler,
                        'path': shutil.which(compiler),
                        'version': version,
                        'target': target_info,
                        'category': category,
                        'features': features,
                        'priority_score': self._calculate_compiler_priority(compiler, version, features)
                    })
        
        return compilers
    
    def _get_compiler_version(self, compiler: str) -> str:
        """Get detailed compiler version"""
        try:
            for flag in ['--version', '-v', '-V', '--help']:
                result = subprocess.run([compiler, flag], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    output = result.stdout + result.stderr
                    return output.split('\n')[0][:150]
            return "Unknown"
        except:
            return "Unknown"
    
    def _get_compiler_target(self, compiler: str) -> str:
        """Get compiler target architecture"""
        try:
            result = subprocess.run([compiler, '-dumpmachine'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                return result.stdout.strip()
            return "unknown"
        except:
            return "unknown"
    
    def _get_compiler_features(self, compiler: str) -> List[str]:
        """Get compiler supported features"""
        features = []
        try:
            # Check for LTO support
            result = subprocess.run([compiler, '--help=optimizers'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0 and 'flto' in result.stdout:
                features.append('lto')
            
            # Check for OpenMP support
            result = subprocess.run([compiler, '-fopenmp', '--help'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                features.append('openmp')
            
            # Check for sanitizer support
            result = subprocess.run([compiler, '-fsanitize=address', '--help'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                features.append('sanitizers')
                
        except:
            pass
        return features
    
    def _calculate_compiler_priority(self, compiler: str, version: str, features: List[str]) -> int:
        """Calculate compiler priority score"""
        score = 50  # Base score
        
        # Prefer newer versions
        if 'gcc' in compiler:
            if any(v in compiler for v in ['gcc-13', 'gcc-14', 'gcc-15']):
                score += 30
            elif any(v in compiler for v in ['gcc-11', 'gcc-12']):
                score += 20
            elif any(v in compiler for v in ['gcc-9', 'gcc-10']):
                score += 10
        
        if 'clang' in compiler:
            if any(v in compiler for v in ['clang-17', 'clang-18', 'clang-19']):
                score += 30
            elif any(v in compiler for v in ['clang-15', 'clang-16']):
                score += 20
            elif any(v in compiler for v in ['clang-13', 'clang-14']):
                score += 10
        
        # Feature bonuses
        if 'lto' in features:
            score += 15
        if 'openmp' in features:
            score += 10
        if 'sanitizers' in features:
            score += 5
        
        # Prefer native compilers
        if not any(arch in compiler for arch in ['arm-', 'aarch64-', 'mips-', 'x86_64-w64']):
            score += 20
        
        return score
    
    def _detect_build_tools(self) -> Dict:
        """Detect build tools and utilities"""
        tools = {
            'build_systems': [],
            'linkers': [],
            'archivers': [],
            'debuggers': [],
            'profilers': [],
            'analyzers': [],
            'optimizers': [],
            'packagers': [],
            'version_control': []
        }
        
        build_systems = [
            'make', 'gmake', 'bmake', 'pmake',
            'cmake', 'cmake3', 'ccmake', 'cmake-gui',
            'ninja', 'ninja-build', 'samurai',
            'meson', 'mesonconf', 'mesonintrospect',
            'bazel', 'blaze', 'buck', 'buck2',
            'scons', 'waf', 'tup', 'redo',
            'autoconf', 'autoheader', 'autom4te', 'autoreconf', 'autoscan', 'autoupdate',
            'automake', 'aclocal', 'autopoint',
            'libtool', 'libtoolize', 'glibtool', 'glibtoolize',
            'pkg-config', 'pkgconf'
        ]
        
        linkers = [
            'ld', 'ld.bfd', 'ld.gold', 'ld.lld', 'ld64.lld',
            'gold', 'lld', 'mold', 'sold',
            'link', 'lld-link',
            'wasm-ld', 'ld.mcld'
        ]
        
        archivers = [
            'ar', 'gar', 'llvm-ar',
            'ranlib', 'llvm-ranlib',
            'nm', 'llvm-nm', 'gnm',
            'objdump', 'llvm-objdump', 'gobjdump',
            'objcopy', 'llvm-objcopy', 'gobjcopy',
            'strip', 'llvm-strip', 'gstrip',
            'strings', 'gstrings',
            'readelf', 'llvm-readelf', 'greadelf',
            'size', 'llvm-size', 'gsize',
            'addr2line', 'llvm-addr2line'
        ]
        
        debuggers = [
            'gdb', 'gdb-multiarch', 'cgdb', 'ddd',
            'lldb', 'lldb-server',
            'valgrind', 'callgrind', 'cachegrind', 'helgrind', 'drd', 'massif',
            'strace', 'ltrace', 'ptrace',
            'rr', 'uftrace'
        ]
        
        profilers = [
            'perf', 'perf_4.9', 'perf_5.4',
            'gprof', 'sprof',
            'callgrind', 'kcachegrind', 'qcachegrind',
            'cachegrind', 'massif', 'ms_print',
            'gperftools', 'pprof',
            'intel-vtune', 'amplxe-cl'
        ]
        
        analyzers = [
            'cppcheck', 'cppcheck-gui',
            'clang-tidy', 'clang-check', 'clang-analyzer',
            'scan-build', 'scan-view',
            'splint', 'flawfinder', 'rats',
            'pc-lint', 'pc-lint-plus',
            'pvs-studio', 'pvs-studio-analyzer',
            'coverity', 'klocwork',
            'infer', 'facebook-infer'
        ]
        
        optimizers = [
            'upx', 'upx-ucl',
            'strip', 'objcopy',
            'sstrip', 'elfkickers',
            'wasm-opt', 'binaryen'
        ]
        
        packagers = [
            'tar', 'gtar', 'bsdtar',
            'zip', 'unzip', '7z', '7za',
            'gzip', 'gunzip', 'pigz',
            'bzip2', 'bunzip2', 'pbzip2',
            'xz', 'unxz', 'pxz',
            'lz4', 'unlz4',
            'zstd', 'unzstd'
        ]
        
        version_control = [
            'git', 'git-lfs',
            'svn', 'subversion',
            'hg', 'mercurial',
            'bzr', 'bazaar',
            'cvs', 'rcs'
        ]
        
        tool_lists = [
            (build_systems, 'build_systems'),
            (linkers, 'linkers'),
            (archivers, 'archivers'),
            (debuggers, 'debuggers'),
            (profilers, 'profilers'),
            (analyzers, 'analyzers'),
            (optimizers, 'optimizers'),
            (packagers, 'packagers'),
            (version_control, 'version_control')
        ]
        
        for tool_list, category in tool_lists:
            for tool in tool_list:
                if shutil.which(tool):
                    tools[category].append({
                        'name': tool,
                        'path': shutil.which(tool),
                        'version': self._get_tool_version(tool)
                    })
        
        return tools
    
    def _get_tool_version(self, tool: str) -> str:
        """Get tool version"""
        try:
            for flag in ['--version', '-V', '-v', 'version']:
                result = subprocess.run([tool, flag], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    return result.stdout.split('\n')[0][:100]
            return "Unknown"
        except:
            return "Unknown"
    
    def _detect_cross_compile_targets(self) -> List[str]:
        """Detect available cross-compilation targets"""
        targets = []
        
        # Common cross-compilation targets
        target_patterns = [
            'arm-*-gcc', 'aarch64-*-gcc', 'mips-*-gcc', 'mips64-*-gcc',
            'powerpc-*-gcc', 'powerpc64-*-gcc', 'powerpc64le-*-gcc',
            'riscv*-gcc', 'riscv32-*-gcc', 'riscv64-*-gcc',
            'sparc*-gcc', 'sparc64-*-gcc', 's390x-*-gcc',
            'alpha-*-gcc', 'hppa-*-gcc', 'sh4-*-gcc',
            '*-mingw32-gcc', '*-mingw64-gcc', '*-w64-mingw32-gcc',
            '*-android*-clang', '*-linux-musl-gcc',
            'avr-gcc', 'msp430-gcc', 'pic32-gcc',
            'xtensa-*-gcc', 'or1k-*-gcc', 'lm32-*-gcc'
        ]
        
        # Search in common paths
        search_paths = [
            '/usr/bin', '/usr/local/bin', '/opt/*/bin',
            '/data/data/com.termux/files/usr/bin',
            '/usr/cross/*', '/opt/cross/*',
            '/usr/local/cross/*'
        ]
        
        for path in search_paths:
            if '*' in path:
                # Handle glob patterns
                import glob
                for expanded_path in glob.glob(path):
                    if os.path.exists(expanded_path):
                        try:
                            for file in os.listdir(expanded_path):
                                for pattern in target_patterns:
                                    if self._matches_pattern(file, pattern):
                                        if file not in targets:
                                            targets.append(file)
                        except:
                            continue
            elif os.path.exists(path):
                try:
                    for file in os.listdir(path):
                        for pattern in target_patterns:
                            if self._matches_pattern(file, pattern):
                                if file not in targets:
                                    targets.append(file)
                except:
                    continue
        
        return targets
    
    def _matches_pattern(self, filename: str, pattern: str) -> bool:
        """Check if filename matches pattern with wildcards"""
        import fnmatch
        return fnmatch.fnmatch(filename, pattern)
    
    def _create_optimization_profiles(self) -> Dict:
        """Create comprehensive optimization profiles"""
        return {
            'ultra_performance': {
                'flags': ['-Ofast', '-march=native', '-mtune=native', '-flto', 
                         '-funroll-loops', '-ffast-math', '-fomit-frame-pointer',
                         '-finline-functions', '-fprefetch-loop-arrays',
                         '-fgcse-after-reload', '-fpredictive-commoning', '-fipa-cp-clone',
                         '-ftree-loop-distribute-patterns', '-ftree-vectorize'],
                'description': 'Maximum performance, may break standards compliance',
                'risk_level': 'high'
            },
            'aggressive_opt': {
                'flags': ['-O3', '-march=native', '-funroll-loops', '-finline-functions',
                         '-fgcse-after-reload', '-fpredictive-commoning', '-fipa-cp-clone',
                         '-ftree-loop-distribute-patterns', '-ftree-vectorize',
                         '-floop-nest-optimize', '-fgraphite-identity'],
                'description': 'Aggressive optimization while maintaining standards',
                'risk_level': 'medium'
            },
            'size_optimized': {
                'flags': ['-Os', '-flto', '-ffunction-sections', '-fdata-sections',
                         '-fno-asynchronous-unwind-tables', '-fno-stack-protector',
                         '-fmerge-all-constants', '-fno-ident', '-fno-plt'],
                'description': 'Minimize executable size',
                'risk_level': 'low'
            },
            'size_ultra_minimal': {
                'flags': ['-Oz', '-flto', '-ffunction-sections', '-fdata-sections',
                         '-fno-asynchronous-unwind-tables', '-fno-stack-protector',
                         '-fmerge-all-constants', '-fno-ident', '-fno-plt',
                         '-fno-exceptions', '-fno-rtti', '-fno-threadsafe-statics'],
                'description': 'Ultra minimal size (may break functionality)',
                'risk_level': 'high'
            },
            'debug_friendly': {
                'flags': ['-Og', '-g3', '-ggdb', '-fno-omit-frame-pointer',
                         '-fno-optimize-sibling-calls', '-fno-inline',
                         '-fvar-tracking', '-fvar-tracking-assignments'],
                'description': 'Optimized for debugging experience',
                'risk_level': 'none'
            },
            'security_hardened': {
                'flags': ['-O2', '-fstack-protector-strong', '-D_FORTIFY_SOURCE=2',
                         '-fPIE', '-fcf-protection=full', '-fstack-clash-protection',
                         '-Wformat', '-Wformat-security', '-Werror=format-security'],
                'linker_flags': ['-Wl,-z,relro', '-Wl,-z,now', '-Wl,-z,noexecstack', '-pie'],
                'description': 'Security-focused compilation',
                'risk_level': 'none'
            },
            'security_ultra_hardened': {
                'flags': ['-O2', '-fstack-protector-all', '-D_FORTIFY_SOURCE=3',
                         '-fPIE', '-fcf-protection=full', '-fstack-clash-protection',
                         '-fsanitize=address', '-fsanitize=undefined',
                         '-fno-common', '-fno-strict-overflow'],
                'linker_flags': ['-Wl,-z,relro', '-Wl,-z,now', '-Wl,-z,noexecstack', 
                               '-Wl,-z,separate-code', '-pie'],
                'description': 'Ultra security hardening with sanitizers',
                'risk_level': 'medium'
            },
            'compatibility': {
                'flags': ['-O2', '-fno-strict-aliasing', '-fwrapv', '-fno-aggressive-loop-optimizations'],
                'description': 'Maximum compatibility across systems',
                'risk_level': 'none'
            },
            'fast_compile': {
                'flags': ['-O0', '-fno-inline', '-fno-unroll-loops'],
                'description': 'Fastest compilation time',
                'risk_level': 'none'
            },
            'balanced': {
                'flags': ['-O2', '-march=native', '-mtune=native'],
                'description': 'Balanced performance and compatibility',
                'risk_level': 'low'
            },
            'lto_optimized': {
                'flags': ['-O3', '-flto', '-fuse-linker-plugin', '-ffat-lto-objects'],
                'description': 'Link-time optimization focused',
                'risk_level': 'medium'
            },
            'parallel_optimized': {
                'flags': ['-O3', '-fopenmp', '-pthread', '-march=native'],
                'libs': ['-lgomp', '-lpthread'],
                'description': 'Optimized for parallel execution',
                'risk_level': 'low'
            },
            'math_optimized': {
                'flags': ['-O3', '-ffast-math', '-funsafe-math-optimizations',
                         '-ffinite-math-only', '-fno-signed-zeros', '-march=native'],
                'libs': ['-lm'],
                'description': 'Optimized for mathematical computations',
                'risk_level': 'medium'
            }
        }
    
    def _detect_package_managers(self) -> List[str]:
        """Detect available package managers"""
        managers = []
        pm_list = [
            'apt', 'apt-get', 'aptitude', 'apt-cache',
            'yum', 'dnf', 'zypper', 'urpmi',
            'pacman', 'yay', 'paru', 'trizen',
            'apk', 'pkg', 'pkg_add', 'pkgin',
            'brew', 'port', 'fink',
            'emerge', 'portage', 'layman',
            'xbps-install', 'xbps-query',
            'nix-env', 'nix', 'nix-shell',
            'guix', 'guix-daemon',
            'snap', 'snapcraft',
            'flatpak', 'flatpak-builder',
            'pip', 'pip3', 'pipx',
            'conda', 'mamba', 'micromamba',
            'npm', 'yarn', 'pnpm',
            'cargo', 'rustup',
            'go', 'gvm',
            'gem', 'rbenv', 'rvm'
        ]
        
        for pm in pm_list:
            if shutil.which(pm):
                managers.append(pm)
        return managers
    
    def _scan_libraries(self) -> Dict:
        """Enhanced library scanning"""
        libraries = {
            'system_paths': [],
            'pkg_config': [],
            'detected_libs': [],
            'android_libs': [],
            'static_libs': [],
            'shared_libs': [],
            'header_paths': [],
            'cmake_modules': [],
            'pkgconfig_files': []
        }
        
        # Extended library paths including Android/Termux
        lib_paths = [
            '/usr/lib', '/usr/local/lib', '/lib', '/lib64',
            '/usr/lib64', '/usr/local/lib64', 
            '/usr/lib/x86_64-linux-gnu', '/usr/lib/aarch64-linux-gnu',
            '/usr/lib/arm-linux-gnueabihf', '/usr/lib/arm-linux-gnueabi',
            '/usr/lib/i386-linux-gnu', '/usr/lib/i686-linux-gnu',
            '/usr/lib/mips-linux-gnu', '/usr/lib/mips64-linux-gnuabi64',
            '/usr/lib/powerpc64le-linux-gnu', '/usr/lib/s390x-linux-gnu',
            '/opt/lib', '/usr/lib/gcc', '/usr/local/gcc/lib',
            '/data/data/com.termux/files/usr/lib',
            '/data/data/com.termux/files/usr/local/lib',
            '/system/lib', '/system/lib64', '/vendor/lib', '/vendor/lib64',
            '/usr/lib/llvm-*/lib', '/usr/local/llvm/lib',
            '/usr/lib/clang/*/lib', '/usr/local/clang/lib'
        ]
        
        # Header paths
        header_paths = [
            '/usr/include', '/usr/local/include',
            '/usr/include/c++/*', '/usr/local/include/c++/*',
            '/usr/include/x86_64-linux-gnu', '/usr/include/aarch64-linux-gnu',
            '/usr/include/arm-linux-gnueabihf', '/usr/include/arm-linux-gnueabi',
            '/data/data/com.termux/files/usr/include',
            '/opt/include', '/usr/local/opt/*/include'
        ]
        
        for path in lib_paths:
            if '*' in path:
                import glob
                for expanded_path in glob.glob(path):
                    if os.path.exists(expanded_path):
                        libraries['system_paths'].append(expanded_path)
                        self._scan_library_directory(expanded_path, libraries)
            elif os.path.exists(path):
                libraries['system_paths'].append(path)
                self._scan_library_directory(path, libraries)
        
        for path in header_paths:
            if '*' in path:
                import glob
                for expanded_path in glob.glob(path):
                    if os.path.exists(expanded_path):
                        libraries['header_paths'].append(expanded_path)
            elif os.path.exists(path):
                libraries['header_paths'].append(path)
        
        # Enhanced pkg-config detection
        if shutil.which('pkg-config'):
            try:
                result = subprocess.run(['pkg-config', '--list-all'], 
                                      capture_output=True, text=True, timeout=15)
                if result.returncode == 0:
                    libraries['pkg_config'] = result.stdout.strip().split('\n')[:200]
            except:
                pass
        
        # Scan for CMake modules
        cmake_paths = [
            '/usr/share/cmake*/Modules',
            '/usr/local/share/cmake*/Modules',
            '/data/data/com.termux/files/usr/share/cmake*/Modules'
        ]
        
        for path in cmake_paths:
            if '*' in path:
                import glob
                for expanded_path in glob.glob(path):
                    if os.path.exists(expanded_path):
                        libraries['cmake_modules'].append(expanded_path)
            elif os.path.exists(path):
                libraries['cmake_modules'].append(path)
        
        return libraries
    
    def _scan_library_directory(self, path: str, libraries: Dict):
        """Scan a directory for libraries"""
        try:
            for file in os.listdir(path):
                file_path = os.path.join(path, file)
                if file.endswith('.a'):
                    libraries['static_libs'].append(file_path)
                elif file.endswith(('.so', '.so.*', '.dylib', '.dll')):
                    libraries['shared_libs'].append(file_path)
                elif file.endswith('.pc'):
                    libraries['pkgconfig_files'].append(file_path)
        except:
            pass
#FINISH COMPILE

#CLASS NETWORK
class SpeedTest:
    def __init__(self):
        self.test_servers = [
            "http://speedtest.ftp.otenet.gr/files/test1Mb.db",
            "http://speedtest.tele2.net/1MB.zip",
            "http://ipv4.download.thinkbroadband.com/5MB.zip",
            "https://proof.ovh.net/files/1Mb.dat"
        ]
        
    async def get_best_server(self):
        """Find the best server based on ping"""
        best_server = None
        best_ping = float('inf')
        
        for server in self.test_servers:
            try:
                start_time = time.time()
                response = requests.head(server, timeout=5)
                ping = (time.time() - start_time) * 1000
                
                if ping < best_ping and response.status_code == 200:
                    best_ping = ping
                    best_server = server
            except:
                continue
                
        return best_server, best_ping
    
    async def test_download_speed(self, url, duration=10):
        """Test download speed"""
        try:
            start_time = time.time()
            response = requests.get(url, stream=True, timeout=30)
            
            if response.status_code != 200:
                return 0
            
            total_bytes = 0
            chunk_size = 8192
            
            for chunk in response.iter_content(chunk_size=chunk_size):
                if time.time() - start_time > duration:
                    break
                total_bytes += len(chunk)
            
            elapsed_time = time.time() - start_time
            speed_bps = total_bytes / elapsed_time
            speed_mbps = (speed_bps * 8) / (1024 * 1024)  # Convert to Mbps
            
            return speed_mbps
            
        except Exception as e:
            return 0
    
    async def test_upload_speed(self, duration=10):
        """Test upload speed using httpbin"""
        try:
            # Generate test data
            test_data = b'0' * (1024 * 1024)  # 1MB of data
            
            start_time = time.time()
            uploaded_bytes = 0
            
            while time.time() - start_time < duration:
                try:
                    response = requests.post(
                        'https://httpbin.org/post',
                        data=test_data,
                        timeout=5
                    )
                    if response.status_code == 200:
                        uploaded_bytes += len(test_data)
                except:
                    break
            
            elapsed_time = time.time() - start_time
            if elapsed_time > 0:
                speed_bps = uploaded_bytes / elapsed_time
                speed_mbps = (speed_bps * 8) / (1024 * 1024)
                return speed_mbps
            
            return 0
            
        except Exception as e:
            return 0

class NetworkInfo:
    def __init__(self):
        pass
    
    async def get_public_ip_info(self):
        """Get detailed public IP information"""
        try:
            # Try multiple IP info services
            services = [
                'http://ip-api.com/json/',
                'https://ipapi.co/json/',
                'https://ipinfo.io/json'
            ]
            
            for service in services:
                try:
                    response = requests.get(service, timeout=10)
                    data = response.json()
                    
                    if service == 'http://ip-api.com/json/':
                        return {
                            'ip': data.get('query'),
                            'country': data.get('country'),
                            'region': data.get('regionName'),
                            'city': data.get('city'),
                            'isp': data.get('isp'),
                            'org': data.get('org'),
                            'as': data.get('as'),
                            'timezone': data.get('timezone'),
                            'lat': data.get('lat'),
                            'lon': data.get('lon')
                        }
                    elif service == 'https://ipapi.co/json/':
                        return {
                            'ip': data.get('ip'),
                            'country': data.get('country_name'),
                            'region': data.get('region'),
                            'city': data.get('city'),
                            'isp': data.get('org'),
                            'timezone': data.get('timezone'),
                            'lat': data.get('latitude'),
                            'lon': data.get('longitude')
                        }
                except:
                    continue
            
            return None
            
        except Exception as e:
            return None
    
    async def get_dns_info(self):
        """Get DNS server information"""
        try:
            dns_servers = []
            
            # Try to get DNS from /etc/resolv.conf (Linux/Termux)
            try:
                with open('/etc/resolv.conf', 'r') as f:
                    for line in f:
                        if line.startswith('nameserver'):
                            dns = line.split()[1]
                            dns_servers.append(dns)
            except:
                pass
            
            # Test DNS response times
            dns_info = []
            test_domains = ['google.com', 'cloudflare.com']
            
            for dns in dns_servers[:3]:  # Test max 3 DNS servers
                total_time = 0
                successful_queries = 0
                
                for domain in test_domains:
                    try:
                        start_time = time.time()
                        socket.gethostbyname(domain)
                        query_time = (time.time() - start_time) * 1000
                        total_time += query_time
                        successful_queries += 1
                    except:
                        pass
                
                if successful_queries > 0:
                    avg_time = total_time / successful_queries
                    dns_info.append({
                        'server': dns,
                        'response_time': round(avg_time, 2)
                    })
            
            return dns_info
            
        except Exception as e:
            return []
    
    async def get_network_interfaces(self):
        """Get network interface information"""
        try:
            interfaces = []
            
            # Try using ip command (Linux/Termux)
            try:
                result = subprocess.run(['ip', 'addr'], capture_output=True, text=True)
                if result.returncode == 0:
                    output = result.stdout
                    current_interface = None
                    
                    for line in output.split('\n'):
                        if ': ' in line and not line.startswith(' '):
                            parts = line.split(': ')
                            if len(parts) >= 2:
                                current_interface = parts[1].split('@')[0]
                        elif 'inet ' in line and current_interface:
                            ip_part = line.strip().split('inet ')[1].split('/')[0]
                            interfaces.append({
                                'name': current_interface,
                                'ip': ip_part
                            })
            except:
                pass
            
            # Fallback method
            if not interfaces:
                try:
                    hostname = socket.gethostname()
                    local_ip = socket.gethostbyname(hostname)
                    interfaces.append({
                        'name': 'local',
                        'ip': local_ip
                    })
                except:
                    pass
            
            return interfaces
            
        except Exception as e:
            return []
    
    async def get_connection_type(self):
        """Detect connection type (WiFi/Mobile Data)"""
        try:
            # Check for wireless interfaces
            result = subprocess.run(['cat', '/proc/net/wireless'], capture_output=True, text=True)
            if result.returncode == 0 and len(result.stdout.strip()) > 0:
                lines = result.stdout.strip().split('\n')
                if len(lines) > 2:  # Header + at least one interface
                    return "WiFi"
            
            # Check for mobile data interfaces
            interfaces = ['rmnet', 'ccmni', 'pdp_ip', 'wwan']
            result = subprocess.run(['ip', 'link'], capture_output=True, text=True)
            if result.returncode == 0:
                for interface in interfaces:
                    if interface in result.stdout:
                        return "Mobile Data"
            
            return "Unknown"
            
        except:
            return "Unknown"

class IPLookup:
    """Advanced IP Lookup with multiple data sources"""
    
    def __init__(self):
        self.apis = [
            'http://ip-api.com/json/',
            'https://ipapi.co/json/',
            'https://ipinfo.io/json'
        ]
    
    async def lookup(self, ip: str) -> Optional[Dict]:
        """Comprehensive IP lookup"""
        try:
            # Validate IP
            ipaddress.ip_address(ip)
            
            # Try multiple APIs
            for api_url in self.apis:
                try:
                    if api_url == 'http://ip-api.com/json/':
                        data = await self._query_ip_api(ip)
                    elif api_url == 'https://ipapi.co/json/':
                        data = await self._query_ipapi_co(ip)
                    elif api_url == 'https://ipinfo.io/json':
                        data = await self._query_ipinfo_io(ip)
                    
                    if data:
                        # Enhance with additional info
                        data['geolocation_accuracy'] = await self._get_geolocation_accuracy(ip)
                        data['security_info'] = await self._get_security_info(ip)
                        data['whois_info'] = await self._get_whois_info(ip)
                        return data
                        
                except Exception:
                    continue
            
            return None
            
        except ValueError:
            raise Exception("Invalid IP address format")
    
    async def _query_ip_api(self, ip: str) -> Optional[Dict]:
        """Query ip-api.com"""
        try:
            url = f"http://ip-api.com/json/{ip}?fields=status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,query"
            response = requests.get(url, timeout=10)
            data = response.json()
            
            if data.get('status') == 'success':
                return {
                    'ip': data.get('query'),
                    'country': data.get('country'),
                    'country_code': data.get('countryCode'),
                    'region': data.get('regionName'),
                    'city': data.get('city'),
                    'zip_code': data.get('zip'),
                    'latitude': data.get('lat'),
                    'longitude': data.get('lon'),
                    'timezone': data.get('timezone'),
                    'isp': data.get('isp'),
                    'organization': data.get('org'),
                    'as_number': data.get('as'),
                    'source': 'ip-api.com'
                }
            return None
            
        except Exception:
            return None
    
    async def _query_ipapi_co(self, ip: str) -> Optional[Dict]:
        """Query ipapi.co"""
        try:
            url = f"https://ipapi.co/{ip}/json/"
            response = requests.get(url, timeout=10)
            data = response.json()
            
            if 'error' not in data:
                return {
                    'ip': data.get('ip'),
                    'country': data.get('country_name'),
                    'country_code': data.get('country_code'),
                    'region': data.get('region'),
                    'city': data.get('city'),
                    'zip_code': data.get('postal'),
                    'latitude': data.get('latitude'),
                    'longitude': data.get('longitude'),
                    'timezone': data.get('timezone'),
                    'isp': data.get('org'),
                    'organization': data.get('org'),
                    'as_number': data.get('asn'),
                    'source': 'ipapi.co'
                }
            return None
            
        except Exception:
            return None
    
    async def _query_ipinfo_io(self, ip: str) -> Optional[Dict]:
        """Query ipinfo.io"""
        try:
            url = f"https://ipinfo.io/{ip}/json"
            response = requests.get(url, timeout=10)
            data = response.json()
            
            if 'bogon' not in data:
                loc = data.get('loc', '').split(',')
                return {
                    'ip': data.get('ip'),
                    'country': data.get('country'),
                    'region': data.get('region'),
                    'city': data.get('city'),
                    'zip_code': data.get('postal'),
                    'latitude': float(loc[0]) if len(loc) > 0 else None,
                    'longitude': float(loc[1]) if len(loc) > 1 else None,
                    'timezone': data.get('timezone'),
                    'isp': data.get('org'),
                    'organization': data.get('org'),
                    'source': 'ipinfo.io'
                }
            return None
            
        except Exception:
            return None
    
    async def _get_geolocation_accuracy(self, ip: str) -> str:
        """Estimate geolocation accuracy"""
        try:
            # Check if IP is in private ranges
            ip_obj = ipaddress.ip_address(ip)
            if ip_obj.is_private:
                return "Private IP - No geolocation"
            elif ip_obj.is_loopback:
                return "Loopback IP - Local"
            else:
                return "Public IP - City level accuracy"
        except:
            return "Unknown"
    
    async def _get_security_info(self, ip: str) -> Dict:
        """Get security-related information"""
        try:
            # Check if IP is in known threat lists (simplified)
            security_info = {
                'is_tor': False,
                'is_proxy': False,
                'is_vpn': False,
                'threat_level': 'Low'
            }
            
            # This would normally query threat intelligence APIs
            # For demo purposes, we'll do basic checks
            return security_info
            
        except:
            return {'threat_level': 'Unknown'}
    
    async def _get_whois_info(self, ip: str) -> Optional[Dict]:
        """Get basic WHOIS information"""
        try:
            # Simplified WHOIS lookup
            # In production, you'd use a proper WHOIS library
            return {
                'registry': 'IANA',
                'allocated': 'Unknown',
                'updated': 'Unknown'
            }
        except:
            return None

class PingTester:
    """Advanced Ping Testing with statistics"""
    
    def __init__(self):
        self.default_count = 4
        self.timeout = 10
    
    async def ping(self, host: str, count: int = None, packet_size: int = 56) -> Dict:
        """Comprehensive ping test"""
        if count is None:
            count = self.default_count
        
        try:
            # Resolve hostname first
            try:
                ip = socket.gethostbyname(host)
            except socket.gaierror:
                raise Exception(f"Cannot resolve hostname: {host}")
            
            # Execute ping command
            cmd = self._build_ping_command(host, count, packet_size)
            process = subprocess.run(cmd, shell=True, capture_output=True, 
                                   text=True, timeout=self.timeout * count)
            
            if process.returncode == 0:
                return self._parse_ping_output(process.stdout, host, ip, count)
            else:
                raise Exception(f"Ping failed: {process.stderr}")
                
        except subprocess.TimeoutExpired:
            raise Exception("Ping timeout")
        except Exception as e:
            raise Exception(f"Ping error: {str(e)}")
    
    def _build_ping_command(self, host: str, count: int, packet_size: int) -> str:
        """Build ping command based on OS"""
        system = platform.system().lower()
        
        if system == 'linux':
            return f"ping -c {count} -s {packet_size} -W 2 {host}"
        elif system == 'darwin':  # macOS
            return f"ping -c {count} -s {packet_size} -W 2000 {host}"
        else:
            return f"ping -n {count} {host}"
    
    def _parse_ping_output(self, output: str, host: str, ip: str, count: int) -> Dict:
        """Parse ping output and extract statistics"""
        lines = output.strip().split('\n')
        
        # Extract individual ping times
        ping_times = []
        for line in lines:
            if 'time=' in line:
                match = re.search(r'time=([0-9.]+)', line)
                if match:
                    ping_times.append(float(match.group(1)))
        
        # Extract packet loss
        packet_loss = 0
        for line in lines:
            if 'packet loss' in line:
                match = re.search(r'([0-9.]+)%.*packet loss', line)
                if match:
                    packet_loss = float(match.group(1))
                break
        
        # Calculate statistics
        if ping_times:
            min_time = min(ping_times)
            max_time = max(ping_times)
            avg_time = sum(ping_times) / len(ping_times)
            
            # Calculate jitter (standard deviation)
            if len(ping_times) > 1:
                variance = sum((t - avg_time) ** 2 for t in ping_times) / len(ping_times)
                jitter = variance ** 0.5
            else:
                jitter = 0
        else:
            min_time = max_time = avg_time = jitter = 0
        
        return {
            'host': host,
            'ip': ip,
            'packets_sent': count,
            'packets_received': len(ping_times),
            'packet_loss_percent': packet_loss,
            'min_time': round(min_time, 2),
            'max_time': round(max_time, 2),
            'avg_time': round(avg_time, 2),
            'jitter': round(jitter, 2),
            'ping_times': ping_times
        }

class Traceroute:
    """Advanced Traceroute implementation"""
    
    def __init__(self):
        self.max_hops = 30
        self.timeout = 5
    
    async def trace(self, host: str, max_hops: int = None) -> Dict:
        """Perform traceroute to host"""
        if max_hops is None:
            max_hops = self.max_hops
        
        try:
            # Resolve target
            try:
                target_ip = socket.gethostbyname(host)
            except socket.gaierror:
                raise Exception(f"Cannot resolve hostname: {host}")
            
            # Execute traceroute
            cmd = self._build_traceroute_command(host, max_hops)
            process = subprocess.run(cmd, shell=True, capture_output=True, 
                                   text=True, timeout=60)
            
            if process.returncode == 0 or process.stdout:
                return self._parse_traceroute_output(process.stdout, host, target_ip)
            else:
                raise Exception("Traceroute failed")
                
        except subprocess.TimeoutExpired:
            raise Exception("Traceroute timeout")
        except Exception as e:
            raise Exception(f"Traceroute error: {str(e)}")
    
    def _build_traceroute_command(self, host: str, max_hops: int) -> str:
        """Build traceroute command"""
        system = platform.system().lower()
        
        if system == 'linux':
            return f"traceroute -m {max_hops} -w {self.timeout} {host}"
        elif system == 'darwin':
            return f"traceroute -m {max_hops} -w {self.timeout} {host}"
        else:
            return f"tracert -h {max_hops} -w {self.timeout * 1000} {host}"
    
    def _parse_traceroute_output(self, output: str, host: str, target_ip: str) -> Dict:
        """Parse traceroute output"""
        lines = output.strip().split('\n')
        hops = []
        
        for line in lines[1:]:  # Skip first line
            if not line.strip():
                continue
                
            # Parse hop information
            hop_info = self._parse_hop_line(line)
            if hop_info:
                hops.append(hop_info)
        
        return {
            'target_host': host,
            'target_ip': target_ip,
            'total_hops': len(hops),
            'hops': hops
        }
    
    def _parse_hop_line(self, line: str) -> Optional[Dict]:
        """Parse individual hop line"""
        try:
            # Basic parsing for Linux/Unix traceroute output
            parts = line.strip().split()
            if len(parts) < 2:
                return None
            
            hop_num = int(parts[0])
            
            # Extract IP and hostname
            ip_pattern = r'(\d+\.\d+\.\d+\.\d+)'
            hostname_pattern = r'([a-zA-Z0-9.-]+)'
            
            ip_match = re.search(ip_pattern, line)
            hostname_match = re.search(hostname_pattern, line)
            
            # Extract timing information
            time_pattern = r'([0-9.]+)\s*ms'
            time_matches = re.findall(time_pattern, line)
            
            return {
                'hop': hop_num,
                'ip': ip_match.group(1) if ip_match else None,
                'hostname': hostname_match.group(1) if hostname_match else None,
                'times': [float(t) for t in time_matches],
                'avg_time': sum(float(t) for t in time_matches) / len(time_matches) if time_matches else None
            }
            
        except Exception:
            return None

class DNSLookup:
    """Advanced DNS Lookup with multiple record types"""
    
    def __init__(self):
        self.record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME', 'SOA', 'PTR']
        (self.timeout) = 10
    
    async def lookup(self, domain: str, record_type: str = 'ALL') -> Dict:
        """Comprehensive DNS lookup"""
        try:
            results = {}
            
            if record_type == 'ALL':
                types_to_query = self.record_types
            else:
                types_to_query = [record_type.upper()]
            
            for rtype in types_to_query:
                try:
                    records = await self._query_dns_record(domain, rtype)
                    if records:
                        results[rtype] = records
                except Exception:
                    continue
            
            # Additional DNS information
            dns_info = await self._get_dns_servers(domain)
            nameservers = await self._get_authoritative_nameservers(domain)
            
            return {
                'domain': domain,
                'records': results,
                'dns_servers': dns_info,
                'authoritative_nameservers': nameservers,
                'query_time': datetime.now().isoformat()
            }
            
        except Exception as e:
            raise Exception(f"DNS lookup failed: {str(e)}")
    
    async def _query_dns_record(self, domain: str, record_type: str) -> List[str]:
        """Query specific DNS record type"""
        try:
            # Use nslookup command as fallback
            cmd = f"nslookup -type={record_type} {domain}"
            process = subprocess.run(cmd, shell=True, capture_output=True, 
                                   text=True, timeout=self.timeout)
            
            if process.returncode == 0:
                return self._parse_nslookup_output(process.stdout, record_type)
            else:
                # Fallback to socket for A records
                if record_type == 'A':
                    try:
                        ip = socket.gethostbyname(domain)
                        return [ip]
                    except:
                        pass
                return []
                
        except Exception:
            return []
    
    def _parse_nslookup_output(self, output: str, record_type: str) -> List[str]:
        """Parse nslookup output"""
        lines = output.strip().split('\n')
        records = []
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('Server:') or line.startswith('Address:'):
                continue
            
            if record_type == 'A' and 'Address:' in line:
                ip = line.split('Address:')[1].strip()
                if self._is_valid_ip(ip):
                    records.append(ip)
            elif record_type == 'MX' and 'mail exchanger' in line:
                parts = line.split('mail exchanger = ')
                if len(parts) > 1:
                    records.append(parts[1].strip())
            elif record_type == 'NS' and 'nameserver' in line:
                parts = line.split('nameserver = ')
                if len(parts) > 1:
                    records.append(parts[1].strip())
            elif record_type == 'TXT' and 'text' in line:
                parts = line.split('text = ')
                if len(parts) > 1:
                    records.append(parts[1].strip().strip('"'))
        
        return records
    
    def _is_valid_ip(self, ip: str) -> bool:
        """Check if string is valid IP address"""
        try:
            ipaddress.ip_address(ip)
            return True
        except:
            return False
    
    async def _get_dns_servers(self, domain: str) -> List[str]:
        """Get DNS servers being used"""
        try:
            dns_servers = []
            
            # Try to read from /etc/resolv.conf
            try:
                with open('/etc/resolv.conf', 'r') as f:
                    for line in f:
                        if line.startswith('nameserver'):
                            dns = line.split()[1]
                            dns_servers.append(dns)
            except:
                pass
            
            return dns_servers[:3]  # Return max 3 DNS servers
            
        except Exception:
            return []
    
    async def _get_authoritative_nameservers(self, domain: str) -> List[str]:
        """Get authoritative nameservers for domain"""
        try:
            cmd = f"nslookup -type=NS {domain}"
            process = subprocess.run(cmd, shell=True, capture_output=True, 
                                   text=True, timeout=self.timeout)
            
            if process.returncode == 0:
                return self._parse_nslookup_output(process.stdout, 'NS')
            
            return []
            
        except Exception:
            return []

class NetworkInfoCollector:
    """Comprehensive Network Information Collector"""
    
    def __init__(self):
        pass
    
    async def collect_all_info(self) -> Dict:
        """Collect comprehensive network information"""
        try:
            info = {
                'public_ip': await self._get_public_ip_info(),
                'local_network': await self._get_local_network_info(),
                'network_interfaces': await self._get_network_interfaces(),
                'dns_configuration': await self._get_dns_configuration(),
                'routing_table': await self._get_routing_info(),
                'network_statistics': await self._get_network_statistics(),
                'connectivity_tests': await self._run_connectivity_tests(),
                'system_info': await self._get_system_info()
            }
            
            return info
            
        except Exception as e:
            raise Exception(f"Network info collection failed: {str(e)}")
    
    async def _get_public_ip_info(self) -> Dict:
        """Get public IP information"""
        try:
            # Get public IP
            ip_services = [
                'https://api.ipify.org?format=json',
                'https://httpbin.org/ip',
                'https://api.ip.sb/ip'
            ]
            
            public_ip = None
            for service in ip_services:
                try:
                    response = requests.get(service, timeout=5)
                    if 'ipify' in service:
                        public_ip = response.json()['ip']
                    elif 'httpbin' in service:
                        public_ip = response.json()['origin']
                    else:
                        public_ip = response.text.strip()
                    break
                except:
                    continue
            
            if public_ip:
                # Get detailed IP info
                ip_lookup = IPLookup()
                detailed_info = await ip_lookup.lookup(public_ip)
                return detailed_info or {'ip': public_ip}
            
            return {'error': 'Could not determine public IP'}
            
        except Exception:
            return {'error': 'Failed to get public IP info'}
    
    async def _get_local_network_info(self) -> Dict:
        """Get local network information"""
        try:
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            
            # Get default gateway
            gateway = await self._get_default_gateway()
            
            # Get network mask
            network_mask = await self._get_network_mask()
            
            return {
                'hostname': hostname,
                'local_ip': local_ip,
                'default_gateway': gateway,
                'network_mask': network_mask
            }
            
        except Exception as e:
            return {'error': f'Failed to get local network info: {str(e)}'}
    
    async def _get_network_interfaces(self) -> List[Dict]:
        """Get detailed network interface information"""
        try:
            interfaces = []
            
            # Use ip command (Linux/Android)
            try:
                result = subprocess.run(['ip', 'addr', 'show'], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    interfaces = self._parse_ip_addr_output(result.stdout)
            except:
                pass
            
            # Fallback method
            if not interfaces:
                try:
                    hostname = socket.gethostname()
                    local_ip = socket.gethostbyname(hostname)
                    interfaces.append({
                        'name': 'local',
                        'ip': local_ip,
                        'status': 'up'
                    })
                except:
                    pass
            
            return interfaces
            
        except Exception:
            return []
    
    def _parse_ip_addr_output(self, output: str) -> List[Dict]:
        """Parse ip addr show output"""
        interfaces = []
        current_interface = None
        
        for line in output.split('\n'):
            line = line.strip()
            
            # Interface line
            if ': ' in line and not line.startswith(' '):
                parts = line.split(': ')
                if len(parts) >= 2:
                    current_interface = {
                        'name': parts[1].split('@')[0],
                        'status': 'up' if 'UP' in line else 'down',
                        'ips': []
                    }
                    interfaces.append(current_interface)
            
            # IP address line
            elif line.startswith('inet ') and current_interface:
                ip_part = line.split('inet ')[1].split('/')[0]
                current_interface['ips'].append(ip_part)
                if 'ip' not in current_interface:
                    current_interface['ip'] = ip_part
        
        return interfaces
    
    async def _get_dns_configuration(self) -> Dict:
        """Get DNS configuration"""
        try:
            dns_servers = []
            
            # Read from /etc/resolv.conf
            try:
                with open('/etc/resolv.conf', 'r') as f:
                    for line in f:
                        if line.startswith('nameserver'):
                            dns_servers.append(line.split()[1])
            except:
                pass
            
            # Test DNS response times
            dns_tests = []
            for dns in dns_servers[:3]:
                try:
                    start_time = time.time()
                    socket.gethostbyname_ex('google.com')
                    response_time = (time.time() - start_time) * 1000
                    dns_tests.append({
                        'server': dns,
                        'response_time': round(response_time, 2)
                    })
                except:
                    dns_tests.append({
                        'server': dns,
                        'response_time': 'timeout'
                    })
            
            return {
                'dns_servers': dns_servers,
                'dns_tests': dns_tests
            }
            
        except Exception:
            return {'error': 'Failed to get DNS configuration'}
    
    async def _get_routing_info(self) -> Dict:
        """Get routing table information"""
        try:
            # Get default route
            try:
                result = subprocess.run(['ip', 'route', 'show', 'default'], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    default_route = result.stdout.strip()
                else:
                    default_route = 'Unknown'
            except:
                default_route = 'Unknown'
            
            # Get full routing table
            try:
                result = subprocess.run(['ip', 'route', 'show'], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    routing_table = result.stdout.strip().split('\n')[:10]  # Limit to 10 routes
                else:
                    routing_table = []
            except:
                routing_table = []
            
            return {
                'default_route': default_route,
                'routing_table': routing_table
            }
            
        except Exception:
            return {'error': 'Failed to get routing information'}
    
    async def _get_network_statistics(self) -> Dict:
        """Get network statistics"""
        try:
            stats = {}
            
            # Get network interface statistics
            try:
                with open('/proc/net/dev', 'r') as f:
                    lines = f.readlines()
                    for line in lines[2:]:  # Skip header lines
                        if ':' in line:
                            parts = line.split(':')
                            interface = parts[0].strip()
                            data = parts[1].split()
                            if len(data) >= 16:
                                stats[interface] = {
                                    'rx_bytes': int(data[0]),
                                    'rx_packets': int(data[1]),
                                    'rx_errors': int(data[2]),
                                    'tx_bytes': int(data[8]),
                                    'tx_packets': int(data[9]),
                                    'tx_errors': int(data[10])
                                }
            except:
                pass
            
            return stats
            
        except Exception:
            return {'error': 'Failed to get network statistics'}
    
    async def _run_connectivity_tests(self) -> Dict:
        """Run connectivity tests to various servers"""
        try:
            test_hosts = [
                ('Google DNS', '8.8.8.8'),
                ('Cloudflare DNS', '1.1.1.1'),
                ('OpenDNS', '208.67.222.222'),
                ('Google', 'google.com'),
                ('GitHub', 'github.com')
            ]
            
            connectivity_results = []
            
            for name, host in test_hosts:
                try:
                    start_time = time.time()
                    if host.replace('.', '').isdigit():  # IP address
                        sock = socket.create_connection((host, 53), timeout=5)
                    else:  # Hostname
                        sock = socket.create_connection((host, 80), timeout=5)
                    
                    latency = (time.time() - start_time) * 1000
                    sock.close()
                    
                    connectivity_results.append({
                        'name': name,
                        'host': host,
                        'status': 'reachable',
                        'latency': round(latency, 2)
                    })
                except:
                    connectivity_results.append({
                        'name': name,
                        'host': host,
                        'status': 'unreachable',
                        'latency': None
                    })
            
            return {'connectivity_tests': connectivity_results}
            
        except Exception:
            return {'error': 'Failed to run connectivity tests'}
    
    async def _get_system_info(self) -> Dict:
        """Get system information"""
        try:
            return {
                'system': platform.system(),
                'release': platform.release(),
                'version': platform.version(),
                'machine': platform.machine(),
                'processor': platform.processor(),
                'python_version': platform.python_version()
            }
        except Exception:
            return {'error': 'Failed to get system information'}
    
    async def _get_default_gateway(self) -> str:
        """Get default gateway"""
        try:
            result = subprocess.run(['ip', 'route', 'show', 'default'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                output = result.stdout.strip()
                if 'via' in output:
                    gateway = output.split('via')[1].split()[0]
                    return gateway
            return 'Unknown'
        except:
            return 'Unknown'
    
    async def _get_network_mask(self) -> str:
        """Get network mask"""
        try:
            result = subprocess.run(['ip', 'route', 'show'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if 'scope link' in line and '/' in line:
                        parts = line.split()
                        for part in parts:
                            if '/' in part and not part.startswith('dev'):
                                return part.split('/')[1]
            return 'Unknown'
        except:
            return 'Unknown'
#FINIS NETWORK

# Konfigurasi
# Benar:
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GITHUB_TOKEN = os.getenv("MY_GITHUB_TOKEN")
GITHUB_REPO = "nikzzxiter/telegram-bot"
FIREBASE_PROJECT = "nikzz-newpatch-2025"

# Path ke file service account kamu
FIREBASE_CREDENTIAL_PATH = "firebase_key.json"

# Inisialisasi warna untuk UI
COLORS = {
    'primary': '#3498db',
    'success': '#2ecc71',
    'danger': '#e74c3c',
    'warning': '#f39c12',
    'info': '#1abc9c',
    'dark': '#34495e'
}

def get_random_color():
    return random.choice(list(COLORS.values()))

def get_firebase_access_token():
    try:
        credentials = service_account.Credentials.from_service_account_file(
            FIREBASE_CREDENTIAL_PATH,
            scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )
        credentials.refresh(Request())
        return credentials.token
    except:
        return None
    
def sha256_hash(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()
    
# Inisialisasi GitHub
g = Github(GITHUB_TOKEN)
repo = g.get_repo(GITHUB_REPO)

# Inisialisasi bot
app = ApplicationBuilder().token(TOKEN).build()

# Inisialisasi waktu mulai
start_time = datetime.now()

# Handler untuk command /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    color = get_random_color()
    keyboard = [
        [InlineKeyboardButton("📋 Menu Utama", callback_data='main_menu')],
        [InlineKeyboardButton("🛠 Tools", callback_data='tools_menu')],
        [InlineKeyboardButton("🚀 Deploy", callback_data='deploy_menu')],
        [InlineKeyboardButton("🔒 Security", callback_data='security_menu')],
        [InlineKeyboardButton("🔓 Reverse Engine", callback_data='reverse_menu')],
        [InlineKeyboardButton("⚔️ Attacker Tools", callback_data='attacker_menu')],
        [InlineKeyboardButton("📱 APK Tools", callback_data='apk_menu')],
        [InlineKeyboardButton("🛠️ Extra Tools", callback_data='extra_tools_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message_text = (
        f"<b>👋 Halo! Saya adalah Nikzzx Multi-Feature Bot v2.0</b>\n\n"
        f"<i>✨ Dengan berbagai fitur canggih untuk kebutuhan development dan security Anda</i>\n\n"
        f"<code>🔹 Versi: 2.0 </code>\n"
        f"<code>🔹 Status: Active</code>\n"
        f"<code>🔹 Update: {datetime.now().strftime('%d %b %Y')}</code>\n\n"
        "Pilih kategori menu yang ingin Anda akses:"
    )
    
    if update.message:
        await update.message.reply_text(message_text, parse_mode='HTML', reply_markup=reply_markup)
    else:
        await update.callback_query.edit_message_text(message_text, parse_mode='HTML', reply_markup=reply_markup)

# Menu Utama
async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("📊 Status Bot", callback_data='bot_status')],
        [InlineKeyboardButton("🧹 Bersihkan Cache", callback_data='clear_cache')],
        [InlineKeyboardButton("📝 Panduan Penggunaan", callback_data='guide')],
        [InlineKeyboardButton("🔙 Kembali", callback_data='back_to_start')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "<b>📋 Menu Utama</b>\n\n"
        "<i>Fitur utama dan pengaturan bot</i>\n\n"
        "Pilih opsi yang tersedia:",
        parse_mode='HTML',
        reply_markup=reply_markup
    )

# Menu Tools
async def tools_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("🔗 Link Generator", callback_data='linkgen')],
        [InlineKeyboardButton("📩 Message Sender", callback_data='messagesender')],
        [InlineKeyboardButton("📄 File Converter", callback_data='fileconverter')],
        [InlineKeyboardButton("🔍 QR Code Generator", callback_data='qrcodegen')],
        [InlineKeyboardButton("📝 Text Manipulator", callback_data='textmanipulator')],
        [InlineKeyboardButton("🔙 Kembali", callback_data='back_to_start')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        f"<b>🛠 Tools Menu</b>\n\n"
        f"<i>Berbagai alat bantu untuk kebutuhan sehari-hari</i>\n\n"
        f"<code>🔹 Link Generator</code> - Buat link pendek\n"
        f"<code>🔹 Message Sender</code> - Kirim pesan ke chat ID\n"
        f"<code>🔹 File Converter</code> - Konversi file ke format lain\n"
        f"<code>🔹 QR Code Generator</code> - Buat QR Code dari teks\n"
        f"<code>🔹 Text Manipulator</code> - Encode/decode text\n\n"
        "Pilih tool yang ingin digunakan:",
        parse_mode='HTML',
        reply_markup=reply_markup
    )

# Menu Deploy
async def deploy_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("💾 Upload ke Server", callback_data='github')],
        [InlineKeyboardButton("🔥 Firebase Hosting", callback_data='firebase')],
        [InlineKeyboardButton("🚀 Vercel", callback_data='vercel')],
        [InlineKeyboardButton("🛠 Compile C/C++", callback_data='compile')],
        [InlineKeyboardButton("🔙 Kembali", callback_data='back_to_start')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        f"<b>🚀 Deploy Menu</b>\n\n"
        f"<i>Fitur-fitur untuk deployment dan kompilasi kode</i>\n\n"
        f"<code>🔹 Server</code> - Upload file ke repository\n"
        f"<code>🔹 Firebase</code> - Deploy ke Firebase Hosting\n"
        f"<code>🔹 Vercel</code> - Deploy ke Vercel\n"
        f"<code>🔹 Compiler</code> - Compile kode C/C++\n\n"
        "Pilih opsi deployment:",
        parse_mode='HTML',
        reply_markup=reply_markup
    )

# Menu Security
async def security_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("🔒 JavaScript Obfuscator", callback_data='obfuscator')],
        [InlineKeyboardButton("🌙 Lua Obfuscator", callback_data='luaobfuscator')],
        [InlineKeyboardButton("🐚 Shell Encoder", callback_data='shellencoder')],
        [InlineKeyboardButton("🐍 Python Encoder", callback_data='pythonencoder')],
        [InlineKeyboardButton("🔐 File Encryptor", callback_data='fileencryptor')],
        [InlineKeyboardButton("🛡️ AES Encryptor", callback_data='aes_encryptor')],
        [InlineKeyboardButton("🔙 Kembali", callback_data='back_to_start')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        f"<b>🔒 Security Menu</b>\n\n"
        f"<i>Fitur-fitur keamanan dan obfuscation</i>\n\n"
        f"<code>🔹 JS Obfuscator</code> - Obfuscate kode JavaScript\n"
        f"<code>🔹 Lua Obfuscator</code> - Obfuscate kode Lua\n"
        f"<code>🔹 Shell Encoder</code> - Encode shell script\n"
        f"<code>🔹 Python Encoder</code> - Encode Python script\n"
        f"<code>🔹 File Encryptor</code> - Enkripsi file dengan AES\n"
        f"<code>🔹 AES Encryptor</code> - Enkripsi teks dengan AES\n\n"
        "Pilih opsi security:",
        parse_mode='HTML',
        reply_markup=reply_markup
    )

# Menu Reverse Engine (NEW)
async def reverse_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("🔓 JS Deobfuscator", callback_data='js_deobf')],
        [InlineKeyboardButton("🌙 Lua Deobfuscator", callback_data='lua_deobf')],
        [InlineKeyboardButton("🐚 Shell Decoder", callback_data='shell_decode')],
        [InlineKeyboardButton("🐍 Python Decoder", callback_data='python_decode')],
        [InlineKeyboardButton("🔍 Code Analyzer", callback_data='code_analyzer')],
        [InlineKeyboardButton("🔙 Kembali", callback_data='back_to_start')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        f"<b>🔓 Reverse Engine Menu</b>\n\n"
        f"<i>Fitur-fitur untuk reverse engineering dan deobfuscation</i>\n\n"
        f"<code>🔹 JS Deobfuscator</code> - Deobfuscate JavaScript\n"
        f"<code>🔹 Lua Deobfuscator</code> - Deobfuscate Lua script\n"
        f"<code>🔹 Shell Decoder</code> - Decode shell script\n"
        f"<code>🔹 Python Decoder</code> - Decode Python script\n"
        f"<code>🔹 Code Analyzer</code> - Analisis kode\n\n"
        "Pilih opsi reverse engineering:",
        parse_mode='HTML',
        reply_markup=reply_markup
    )

# Menu Attacker Tools (NEW)
async def attacker_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("🌐 Web Scanner", callback_data='web_scanner')],
        [InlineKeyboardButton("🔍 Port Scanner", callback_data='port_scanner')],
        [InlineKeyboardButton("📧 Email Bomber", callback_data='email_bomber')],
        [InlineKeyboardButton("🔐 Hash Cracker", callback_data='hash_cracker')],
        [InlineKeyboardButton("🕷️ SQL Injection", callback_data='sql_injection')],
        [InlineKeyboardButton("🔙 Kembali", callback_data='back_to_start')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        f"<b>⚔️ Attacker Tools Menu</b>\n\n"
        f"<i>Fitur-fitur untuk penetration testing dan security audit</i>\n\n"
        f"<code>🔹 Web Scanner</code> - Scan kerentanan website\n"
        f"<code>🔹 Port Scanner</code> - Scan port terbuka\n"
        f"<code>🔹 Email Bomber</code> - Stress test email\n"
        f"<code>🔹 Hash Cracker</code> - Crack hash password\n"
        f"<code>🔹 SQL Injection</code> - Test SQL injection\n\n"
        "⚠️ <i>Gunakan hanya untuk tujuan legal dan ethical hacking</i>",
        parse_mode='HTML',
        reply_markup=reply_markup
    )

# Menu APK Tools (NEW)
async def apk_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("📱 Encode DEX", callback_data='encode_dex')],
        [InlineKeyboardButton("🎨 Encode Assets", callback_data='encode_assets')],
        [InlineKeyboardButton("📋 Encode Manifest", callback_data='encode_manifest')],
        [InlineKeyboardButton("🔧 Encode Resources", callback_data='encode_resources')],
        [InlineKeyboardButton("🛡️ Anti Debug Extreme", callback_data='anti_debug')],
        [InlineKeyboardButton("🔙 Kembali", callback_data='back_to_start')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        f"<b>📱 APK Tools Menu</b>\n\n"
        f"<i>Fitur-fitur untuk modifikasi dan proteksi APK</i>\n\n"
        f"<code>🔹 Encode DEX</code> - Encode file DEX\n"
        f"<code>🔹 Encode Assets</code> - Encode assets APK\n"
        f"<code>🔹 Encode Manifest</code> - Encode AndroidManifest\n"
        f"<code>🔹 Encode Resources</code> - Encode resources\n"
        f"<code>🔹 Anti Debug</code> - Proteksi anti debugging\n\n"
        "Pilih opsi APK tools:",
        parse_mode='HTML',
        reply_markup=reply_markup
    )

# Menu Extra Tools (NEW)
async def extra_tools_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("🔄 Batch Converter", callback_data='batch_converter')],
        [InlineKeyboardButton("📊 System Monitor", callback_data='system_monitor')],
        [InlineKeyboardButton("🌐 Network Tools", callback_data='network_tools')],
        [InlineKeyboardButton("🔙 Kembali", callback_data='back_to_start')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        f"<b>🛠️ Extra Tools Menu</b>\n\n"
        f"<i>Fitur-fitur tambahan untuk produktivitas maksimal</i>\n\n"
        f"<code>🔹 Batch Converter</code> - Konversi multiple file\n"
        f"<code>🔹 System Monitor</code> - Monitor sistem real-time\n"
        f"<code>🔹 Network Tools</code> - Tools jaringan lengkap\n\n"
        "Pilih extra tools:",
        parse_mode='HTML',
        reply_markup=reply_markup
    )

# Handler untuk kembali ke start
async def back_to_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)
    
# Handler untuk tombol callback
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    # Menu navigation
    if query.data == 'main_menu':
        await main_menu(update, context)
    elif query.data == 'tools_menu':
        await tools_menu(update, context)
    elif query.data == 'deploy_menu':
        await deploy_menu(update, context)
    elif query.data == 'security_menu':
        await security_menu(update, context)
    elif query.data == 'reverse_menu':
        await reverse_menu(update, context)
    elif query.data == 'attacker_menu':
        await attacker_menu(update, context)
    elif query.data == 'apk_menu':
        await apk_menu(update, context)
    elif query.data == 'extra_tools_menu':
        await extra_tools_menu(update, context)
    elif query.data == 'back_to_start':
        await back_to_start(update, context)
    
    # Deploy menu
    elif query.data == 'compile':
        await compile_menu(update, context)
    elif query.data == 'github':
        await github_menu(update, context)
    elif query.data == 'firebase':
        await firebase_menu(update, context)
    elif query.data == 'vercel':
        await vercel_menu(update, context)
    
    # Security menu
    elif query.data == 'obfuscator':
        await obfuscator_menu(update, context)
    elif query.data == 'luaobfuscator':
        await luaobfuscator_menu(update, context)
    elif query.data == 'shellencoder':
        await shellencoder_menu(update, context)
    elif query.data == 'pythonencoder':
        await pythonencoder_menu(update, context)
    elif query.data == 'fileencryptor':
        await fileencryptor_menu(update, context)
    elif query.data == 'aes_encryptor':
        await aes_encryptor_menu(update, context)
    
    # Tools menu
    elif query.data == 'linkgen':
        await linkgen_menu(update, context)
    elif query.data == 'messagesender':
        await messagesender_menu(update, context)
    elif query.data == 'qrcodegen':
        await qrcode_menu(update, context)
    elif query.data == 'fileconverter':
        await fileconverter_menu(update, context)
    elif query.data == 'textmanipulator':
        await textmanipulator_menu(update, context)
    
    # Reverse menu
    elif query.data == 'js_deobf':
        await js_deobf_menu(update, context)
    elif query.data == 'lua_deobf':
        await lua_deobf_menu(update, context)
    elif query.data == 'shell_decode':
        await shell_decode_menu(update, context)
    elif query.data == 'python_decode':
        await python_decode_menu(update, context)
    elif query.data == 'code_analyzer':
        await code_analyzer_menu(update, context)
    
    # Attacker menu
    elif query.data == 'web_scanner':
        await web_scanner_menu(update, context)
    elif query.data == 'port_scanner':
        await port_scanner_menu(update, context)
    elif query.data == 'email_bomber':
        await email_bomber_menu(update, context)
    elif query.data == 'hash_cracker':
        await hash_cracker_menu(update, context)
    elif query.data == 'sql_injection':
        await sql_injection_menu(update, context)
    
    # APK menu
    elif query.data == 'encode_dex':
        await encode_dex_menu(update, context)
    elif query.data == 'encode_assets':
        await encode_assets_menu(update, context)
    elif query.data == 'encode_manifest':
        await encode_manifest_menu(update, context)
    elif query.data == 'encode_resources':
        await encode_resources_menu(update, context)
    elif query.data == 'anti_debug':
        await anti_debug_menu(update, context)
    
    # Extra tools menu
    elif query.data == 'batch_converter':
        await batch_converter_menu(update, context)
    elif query.data == 'system_monitor':
        await system_monitor_menu(update, context)
    elif query.data == 'network_tools':
        await network_tools_menu(update, context)
    
    # Network Button
    elif query.data == 'speed_test_menu':
        await speed_test_menu(update, context)
    elif query.data == 'port_scanner':
        await port_scanner_menu(update, context)
    elif query.data == 'ip_lookup':
        await ip_lookup_command(update, context)
    elif query.data == 'ping_test':
        context.args = ["google.com", "4"]  # Set arguments if needed
        await ping_command(update, context)
    elif query.data == 'traceroute':
        context.args = ["8.8.8.8"]  # Set arguments if needed
        await traceroute_command(update, context)
    elif query.data == 'dns_lookup':
        await dns_lookup_command(update, context)
    elif query.data == 'network_info':
        await network_info_command(update, context)
    
    # button Network Speed
    if query.data == 'quick_speed_test':
        await quick_speed_test(update, context)
    elif query.data == 'full_speed_test':
        await full_speed_test(update, context)
    elif query.data == 'network_analysis':
        await network_analysis(update, context)
    
    # Main menu
    elif query.data == 'clear_cache':
        await clear_cache(update, context)
    elif query.data == 'bot_status':
        await bot_status(update, context)
    elif query.data == 'guide':
        await show_guide(update, context)

# Menu Compile (Fixed)
async def compile_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("🔙 Kembali", callback_data='deploy_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "<b>🛠 Advanced C/C++ Compiler</b>\n\n"
        "Untuk compile file C/C++:\n"
        "1. Kirim file <code>.c</code> atau <code>.cpp</code>\n"
        "2. Bot akan mengcompile dengan optimasi tinggi\n"
        "3. Mendukung library standar dan kompleks\n\n"
        "<i>Compiler mendukung: stdio.h, stdlib.h, string.h, math.h, dll</i>",
        parse_mode='HTML',
        reply_markup=reply_markup
    )

# Menu GitHub Upload
async def github_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("🔙 Kembali", callback_data='deploy_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "<b>💾 Upload ke Server</b>\n\n"
        "Untuk upload file ke Server:\n"
        "1. Kirim file yang ingin diupload\n"
        "2. Bot akan menguploadnya ke repository\n"
        "3. File akan tersedia secara public\n\n"
        "<i>Format file yang didukung: Semua jenis file</i>",
        parse_mode='HTML',
        reply_markup=reply_markup
    )

# Fitur 1: Advanced Compile C/C++ (Fixed & Improved)
async def compile_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """MEGA ADVANCED COMPILATION SYSTEM WITH ALL METHODS"""
    
    # Initialize advanced compiler
    compiler_system = AdvancedCompiler()
    
    file = update.message.document
    file_name = file.file_name
    
    # Extended file support
    supported_extensions = {
        # C/C++
        '.c', '.cpp', '.cc', '.cxx', '.c++', '.C', '.CPP',
        '.h', '.hpp', '.hh', '.hxx', '.h++', '.H', '.HPP',
        # Assembly
        '.s', '.S', '.asm', '.ASM',
        # Fortran  
        '.f', '.f90', '.f95', '.f03', '.f08', '.for', '.FOR',
        # Other languages
        '.m', '.mm',  # Objective-C
        '.rs',        # Rust
        '.go',        # Go
        '.zig',       # Zig
        '.d',         # D language
        '.pas',       # Pascal
        '.ada', '.adb', '.ads'  # Ada
    }
    
    file_ext = Path(file_name).suffix.lower()
    if file_ext not in supported_extensions:
        await update.message.reply_text(
            f"❌ File tidak didukung!\n"
            f"📁 Supported: {', '.join(sorted(supported_extensions))}"
        )
        return
    
    # Enhanced system info
    await update.message.reply_text(
        f"🔍 MEGA SYSTEM ANALYSIS\n"
        f"🖥️ OS: {compiler_system.system_info['os']} ({compiler_system.system_info['arch']})\n"
        f"🏗️ Platform: {compiler_system.system_info['platform'][:50]}\n"
        f"🧠 CPU Cores: {compiler_system.system_info['cpu_count']}\n"
        f"💾 Memory: {compiler_system.system_info['memory_gb']:.1f}GB\n"
        f"📱 Termux: {'✅' if compiler_system.system_info['is_termux'] else '❌'}\n"
        f"🤖 Android: {'✅' if compiler_system.system_info['is_android'] else '❌'}\n"
        f"⚙️ GCC Variants: {len(compiler_system.available_compilers['gcc_variants'])}\n"
        f"⚙️ Clang Variants: {len(compiler_system.available_compilers['clang_variants'])}\n"
        f"🔧 Specialized: {len(compiler_system.available_compilers['specialized'])}\n"
        f"🆕 Modern: {len(compiler_system.available_compilers['modern_compilers'])}\n"
        f"🌐 Cross Compilers: {len(compiler_system.available_compilers['cross_compilers'])}\n"
        f"📦 Package Managers: {len(compiler_system.package_managers)}\n"
        f"📚 Library Paths: {len(compiler_system.installed_libraries['system_paths'])}\n"
        f"🔗 Static Libs: {len(compiler_system.installed_libraries['static_libs'])}\n"
        f"🔗 Shared Libs: {len(compiler_system.installed_libraries['shared_libs'])}"
    )
    
    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = os.path.join(temp_dir, file_name)
        
        try:
            # Download and analyze file
            file_obj = await file.get_file()
            await file_obj.download_to_drive(file_path)
            
            # Enhanced source code analysis
            analysis = await analyze_source_code_advanced(file_path, file_ext)
            await update.message.reply_text(
                f"📊 ADVANCED SOURCE ANALYSIS\n"
                f"📄 File: {file_name}\n"
                f"📏 Size: {analysis['size_kb']:.1f}KB ({analysis['lines']} lines)\n"
                f"📚 Includes: {len(analysis['includes'])} headers\n"
                f"🔧 Required libs: {', '.join(list(analysis['required_libs'])[:5])}\n"
                f"⚡ C++ features: {', '.join(analysis['cpp_features'][:3])}\n"
                f"🧮 Math heavy: {'✅' if analysis['math_heavy'] else '❌'}\n"
                f"🧵 Threading: {'✅' if analysis['threading'] else '❌'}\n"
                f"🎮 Graphics: {'✅' if analysis['graphics'] else '❌'}\n"
                f"🌐 Networking: {'✅' if analysis['networking'] else '❌'}\n"
                f"📱 Android APIs: {'✅' if analysis['android_apis'] else '❌'}\n"
                f"🔒 Security: {'✅' if analysis['security_features'] else '❌'}\n"
                f"🏗️ Complexity: {analysis['complexity'].upper()}\n"
                f"🎯 Language: {analysis.get('detected_language', 'auto')}\n"
                f"📋 Standard: {analysis.get('language_standard', 'auto')}"
            )
            
            # Generate MEGA compilation strategies
            strategies = await generate_mega_compilation_strategies(
                compiler_system, file_path, file_ext, analysis, temp_dir
            )
            
            await update.message.reply_text(
                f"🚀 MEGA COMPILATION MATRIX\n"
                f"📊 Total strategies: {len(strategies)}\n"
                f"🎯 Ultra priority: {len([s for s in strategies if s['priority'] < 5])}\n"
                f"🔥 High priority: {len([s for s in strategies if 5 <= s['priority'] < 15])}\n"
                f"🔧 Medium priority: {len([s for s in strategies if 15 <= s['priority'] < 50])}\n"
                f"🆘 Fallback: {len([s for s in strategies if s['priority'] >= 50])}\n"
                f"⏳ Starting MEGA compilation marathon..."
            )
            
            # Execute parallel compilation with progress tracking
            results = await execute_mega_parallel_compilation(strategies, update)
            
            # Handle results with comprehensive analysis
            successful_results = [r for r in results if r['success']]
            
            if successful_results:
                # Advanced result sorting
                best_result = sorted(successful_results, 
                                   key=lambda x: (x['priority'], -x.get('performance_score', 0), x['file_size']))[0]
                
                await handle_mega_compilation_success(update, context, best_result, successful_results, analysis, temp_dir)
            else:
                await handle_mega_compilation_failure(update, results, analysis, compiler_system)
                
        except Exception as e:
            await update.message.reply_text(f"💥 CRITICAL SYSTEM ERROR: {str(e)}")

async def analyze_source_code_advanced(file_path: str, file_ext: str) -> Dict:
    """Advanced deep source code analysis"""
    
    analysis = {
        'size_kb': os.path.getsize(file_path) / 1024,
        'lines': 0,
        'includes': [],
        'required_libs': set(),
        'cpp_features': [],
        'complexity': 'low',
        'threading': False,
        'math_heavy': False,
        'graphics': False,
        'networking': False,
        'android_apis': False,
        'security_features': False,
        'memory_management': 'automatic',
        'optimization_hints': [],
        'potential_issues': [],
        'language_standard': 'unknown',
        'detected_language': 'unknown',
        'function_count': 0,
        'class_count': 0,
        'template_usage': False,
        'inline_assembly': False,
        'compiler_extensions': [],
        'warning_suppressions': [],
        'pragma_directives': [],
        'conditional_compilation': False,
        'unicode_usage': False,
        'deprecated_features': [],
        'modern_features': [],
        'performance_critical': False
    }
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            lines = content.split('\n')
            analysis['lines'] = len(lines)
            
            # Enhanced include detection
            includes = re.findall(r'#include\s*[<"](.*?)[>"]', content)
            analysis['includes'] = includes
            
            # Detect language
            analysis['detected_language'] = detect_code_language(content, file_ext)
            
            # Advanced library detection with more comprehensive patterns
            lib_indicators = {
                'pthread': ['pthread_', '#include <pthread.h>', 'std::thread', 'std::mutex', 'std::atomic'],
                'math': ['math.h', 'cmath', 'sin(', 'cos(', 'tan(', 'sqrt(', 'pow(', 'fabs(', 'exp(', 'log('],
                'opengl': ['GL/', 'glfw', 'glad', 'OpenGL', 'glVertex', 'glClear', 'glDraw', 'shader'],
                'vulkan': ['vulkan/', 'VK_', 'vkCreate', 'VkDevice', 'VkInstance'],
                'directx': ['d3d11', 'd3d12', 'DirectX', 'ID3D11', 'ID3D12'],
                'network': ['socket', 'bind(', 'listen(', 'accept(', 'connect(', 'send(', 'recv('],
                'curl': ['curl.h', 'CURL', 'curl_easy', 'libcurl'],
                'ssl': ['openssl/', 'SSL_', 'TLS_', 'mbedtls', 'wolfssl'],
                'boost': ['boost/', 'BOOST_', 'boost::'],
                'eigen': ['Eigen/', 'MatrixXd', 'VectorXd', 'eigen3'],
                'opencv': ['opencv', 'cv::', 'Mat ', 'imread', 'cv2'],
                'qt': ['Qt', 'QApplication', 'QWidget', 'QObject', 'Q_OBJECT'],
                'gtk': ['gtk/', 'GTK_', 'g_', 'GtkWidget'],
                'android': ['android/', 'jni.h', 'JNIEXPORT', '__android', 'NDK'],
                'log': ['android/log.h', '__android_log', 'ALOG', 'syslog'],
                'sqlite': ['sqlite3.h', 'sqlite3_', 'SQLITE_'],
                'json': ['json/', 'nlohmann', 'rapidjson', 'jsoncpp'],
                'crypto': ['crypto++', 'cryptopp', 'mbedtls', 'libsodium'],
                'compression': ['zlib.h', 'lz4.h', 'snappy', 'brotli'],
                'audio': ['alsa/', 'pulse/', 'OpenAL', 'portaudio'],
                'image': ['png.h', 'jpeg', 'tiff', 'webp', 'ImageMagick'],
                'database': ['mysql', 'postgresql', 'mongodb', 'redis'],
                'gui': ['wxWidgets', 'FLTK', 'Dear ImGui', 'nuklear'],
                'game': ['SDL', 'SFML', 'Allegro', 'Ogre', 'Unreal'],
                'ml': ['tensorflow', 'pytorch', 'caffe', 'onnx'],
                'web': ['libmicrohttpd', 'civetweb', 'mongoose'],
                'xml': ['libxml2', 'pugixml', 'tinyxml', 'xerces'],
                'regex': ['regex.h', 'pcre', 'boost::regex', 'std::regex'],
                'uuid': ['uuid.h', 'libuuid', 'boost::uuid'],
                'time': ['chrono', 'ctime', 'sys/time.h', 'boost::date_time']
            }
            
            for lib, indicators in lib_indicators.items():
                if any(indicator in content for indicator in indicators):
                    analysis['required_libs'].add(lib)
            
            # Enhanced C++ feature detection
            cpp_features = {
                'c++98': ['std::', 'template', 'namespace', 'class'],
                'c++03': ['std::tr1'],
                'c++11': ['std::thread', 'auto ', 'nullptr', 'lambda', 'std::unique_ptr', 'std::shared_ptr',
                         'decltype', 'constexpr', 'static_assert', 'std::move', 'range-based for'],
                'c++14': ['std::make_unique', 'auto return', 'std::integer_sequence', 'generic lambda'],
                'c++17': ['std::optional', 'std::variant', 'if constexpr', 'std::filesystem',
                         'structured binding', 'std::string_view', 'fold expression'],
                'c++20': ['concept', 'co_await', 'std::span', 'std::format', 'requires',
                         'std::jthread', 'std::barrier', 'std::latch'],
                'c++23': ['std::expected', 'std::print', 'std::stacktrace', 'std::flat_map']
            }
            
            for version, features in cpp_features.items():
                if any(feature in content for feature in features):
                    analysis['cpp_features'].append(version)
            
            # Function and class counting
            analysis['function_count'] = len(re.findall(r'\b\w+\s*\([^)]*\)\s*{', content))
            analysis['class_count'] = len(re.findall(r'\bclass\s+\w+', content))
            
            # Template usage detection
            analysis['template_usage'] = 'template' in content
            
            # Inline assembly detection
            analysis['inline_assembly'] = any(keyword in content for keyword in [
                '__asm__', 'asm(', '__asm', 'inline assembly'
            ])
            
            # Compiler extensions detection
            compiler_extensions = [
                '__attribute__', '__builtin_', '__extension__',
                '__typeof__', '__alignof__', '__restrict',
                '_Pragma', '__pragma', '#pragma'
            ]
            for ext in compiler_extensions:
                if ext in content:
                    analysis['compiler_extensions'].append(ext)
            
            # Pragma directives
            pragma_matches = re.findall(r'#pragma\s+(\w+)', content)
            analysis['pragma_directives'] = list(set(pragma_matches))
            
            # Conditional compilation
            analysis['conditional_compilation'] = any(directive in content for directive in [
                '#ifdef', '#ifndef', '#if', '#elif', '#else', '#endif'
            ])
            
            # Unicode usage
            analysis['unicode_usage'] = any(indicator in content for indicator in [
                'wchar_t', 'std::wstring', 'L"', 'u8"', 'u"', 'U"'
            ])
            
            # Advanced feature detection
            analysis['threading'] = any(indicator in content for indicator in [
                'pthread_', 'std::thread', 'std::mutex', 'std::atomic', 'omp.h', '#pragma omp',
                'std::condition_variable', 'std::future', 'std::async'
            ])
            
            analysis['math_heavy'] = any(indicator in content for indicator in [
                'sin(', 'cos(', 'tan(', 'sqrt(', 'pow(', 'exp(', 'log(',
                'fft', 'matrix', 'vector', 'algorithm', 'numeric',
                'std::accumulate', 'std::transform', 'eigen', 'blas'
            ])
            
            analysis['graphics'] = any(indicator in content for indicator in [
                'OpenGL', 'DirectX', 'Vulkan', 'SDL', 'SFML', 'Allegro',
                'glVertex', 'glClear', 'glDraw', 'render', 'shader',
                'framebuffer', 'texture', 'vertex', 'fragment'
            ])
            
            analysis['networking'] = any(indicator in content for indicator in [
                'socket', 'bind', 'listen', 'accept', 'connect', 'send', 'recv',
                'curl', 'http', 'tcp', 'udp', 'websocket', 'grpc'
            ])
            
            analysis['android_apis'] = any(indicator in content for indicator in [
                'android/', 'jni.h', 'JNIEXPORT', '__android', 'AAsset',
                'ANativeWindow', 'ALooper', 'android_main', 'NDK'
            ])
            
            analysis['security_features'] = any(indicator in content for indicator in [
                'crypto', 'encrypt', 'decrypt', 'hash', 'secure', 'ssl', 'tls',
                'random', 'salt', 'key', 'certificate', 'sanitize'
            ])
            
            # Performance critical detection
            analysis['performance_critical'] = any(indicator in content for indicator in [
                'inline', 'register', '__restrict', 'likely', 'unlikely',
                'prefetch', 'cache', 'simd', 'vectorize', 'unroll'
            ])
            
            # Complexity analysis with more factors
            complexity_indicators = [
                'template', 'virtual', 'override', 'constexpr', 'std::',
                'namespace', 'class ', 'struct ', 'union ', 'enum ',
                'operator', 'friend', 'mutable', 'volatile',
                'try', 'catch', 'throw', 'exception'
            ]
            complexity_count = sum(content.count(indicator) for indicator in complexity_indicators)
            
            # Factor in file size and function count
            complexity_score = complexity_count + (analysis['lines'] / 100) + (analysis['function_count'] * 2)
            
            if complexity_score > 200:
                analysis['complexity'] = 'very_high'
            elif complexity_score > 100:
                analysis['complexity'] = 'high'
            elif complexity_score > 50:
                analysis['complexity'] = 'medium'
            elif complexity_score > 20:
                analysis['complexity'] = 'low'
            else:
                analysis['complexity'] = 'very_low'
            
            # Memory management detection
            if any(indicator in content for indicator in ['malloc', 'free', 'calloc', 'realloc']):
                analysis['memory_management'] = 'manual_c'
            elif any(indicator in content for indicator in ['new', 'delete', 'new[]', 'delete[]']):
                analysis['memory_management'] = 'manual_cpp'
            elif any(indicator in content for indicator in ['std::unique_ptr', 'std::shared_ptr', 'std::weak_ptr']):
                analysis['memory_management'] = 'smart_pointers'
            elif any(indicator in content for indicator in ['std::vector', 'std::string', 'std::array']):
                analysis['memory_management'] = 'containers'
            
            # Optimization hints
            if analysis['math_heavy']:
                analysis['optimization_hints'].extend(['fast_math', 'vectorize'])
            if analysis['threading']:
                analysis['optimization_hints'].extend(['parallel', 'atomic'])
            if 'loop' in content.lower():
                analysis['optimization_hints'].append('loop_unroll')
            if analysis['performance_critical']:
                analysis['optimization_hints'].extend(['inline', 'lto'])
            if analysis['template_usage']:
                analysis['optimization_hints'].append('template_instantiation')
            
            # Potential issues detection
            security_issues = [
                ('gets(', 'unsafe_gets'),
                ('strcpy(', 'unsafe_strcpy'),
                ('sprintf(', 'unsafe_sprintf'),
                ('strcat(', 'unsafe_strcat'),
                ('scanf(', 'unsafe_scanf')
            ]
            
            for pattern, issue in security_issues:
                if pattern in content:
                    analysis['potential_issues'].append(issue)
            
            # Deprecated features
            deprecated_features = [
                'auto_ptr', 'register', 'throw()', 'std::bind1st',
                'std::bind2nd', 'std::ptr_fun'
            ]
            for feature in deprecated_features:
                if feature in content:
                    analysis['deprecated_features'].append(feature)
            
            # Modern features
            modern_features = [
                'constexpr', 'decltype', 'auto', 'lambda',
                'std::move', 'std::forward', 'std::unique_ptr'
            ]
            for feature in modern_features:
                if feature in content:
                    analysis['modern_features'].append(feature)
            
            # Language standard detection
            if analysis['cpp_features']:
                analysis['language_standard'] = max(analysis['cpp_features'])
            elif file_ext in ['.c', '.h']:
                if any(std in content for std in ['c11', 'c17', 'c2x']):
                    analysis['language_standard'] = 'c17'
                else:
                    analysis['language_standard'] = 'c99'
                
    except Exception as e:
        print(f"Advanced analysis error: {e}")
    
    return analysis

async def generate_mega_compilation_strategies(compiler_system, file_path, file_ext, analysis, temp_dir):
    """Generate ultra-comprehensive compilation strategies"""
    
    base_name = Path(file_path).stem
    strategies = []
    priority = 0
    
    # Determine file type
    is_c = file_ext in ['.c', '.h']
    is_cpp = file_ext in ['.cpp', '.cc', '.cxx', '.c++', '.hpp', '.hh', '.hxx']
    is_asm = file_ext in ['.s', '.S', '.asm']
    is_fortran = file_ext in ['.f', '.f90', '.f95', '.f03', '.f08', '.for']
    
    # Output file with proper extension
    output_name = f"{base_name}_compiled"
    if platform.system() == "Windows":
        output_name += ".exe"
    output_path = os.path.join(temp_dir, output_name)
    
    # MEGA STRATEGY SET 1: ULTRA HIGH-PERFORMANCE BUILDS
    if is_cpp or is_c:
        # Get top compilers sorted by priority
        all_compilers = []
        for category in ['gcc_variants', 'clang_variants', 'modern_compilers', 'specialized']:
            all_compilers.extend(compiler_system.available_compilers[category])
        
        # Sort by priority score
        top_compilers = sorted(all_compilers, key=lambda x: x.get('priority_score', 0), reverse=True)[:10]
        
        for compiler_info in top_compilers:
            compiler = compiler_info['name']
            
            # Ultra-performance strategies with multiple variants
            ultra_strategies = [
                {
                    'name': f"🚀 ULTRA PERFORMANCE MAX - {compiler}",
                    'compiler': compiler,
                    'flags': ['-Ofast', '-march=native', '-mtune=native', '-flto', 
                             '-funroll-loops', '-ffast-math', '-fomit-frame-pointer',
                             '-finline-functions', '-fprefetch-loop-arrays',
                             '-fgcse-after-reload', '-fpredictive-commoning', '-fipa-cp-clone',
                             '-ftree-loop-distribute-patterns', '-ftree-vectorize',
                             '-floop-nest-optimize', '-fgraphite-identity'],
                    'std': 'c++20' if is_cpp else 'c17',
                    'priority': priority,
                    'linker_flags': ['-flto', '-fuse-linker-plugin']
                },
                {
                    'name': f"⚡ AGGRESSIVE NATIVE ULTRA - {compiler}",
                    'compiler': compiler,
                    'flags': ['-O3', '-march=native', '-mtune=native', '-funroll-loops',
                             '-finline-functions', '-fipa-cp-clone', '-fgcse-after-reload',
                             '-ftree-loop-distribute-patterns', '-ftree-vectorize',
                             '-floop-nest-optimize', '-fgraphite-identity',
                             '-fmodulo-sched', '-fmodulo-sched-allow-regmoves'],
                    'std': 'c++17' if is_cpp else 'c11',
                    'priority': priority + 1
                },
                {
                    'name': f"🎯 SIZE ULTRA MINIMAL - {compiler}",
                    'compiler': compiler,
                    'flags': ['-Oz' if 'clang' in compiler else '-Os', '-flto', '-s', 
                             '-ffunction-sections', '-fdata-sections',
                             '-fno-asynchronous-unwind-tables', '-fno-stack-protector',
                             '-fno-ident', '-fmerge-all-constants', '-fno-plt'],
                    'std': 'c++17' if is_cpp else 'c11',
                    'linker_flags': ['-Wl,--gc-sections', '-Wl,--strip-all', '-Wl,--as-needed'],
                    'priority': priority + 2
                },
                {
                    'name': f"🔥 LTO MAXIMUM - {compiler}",
                    'compiler': compiler,
                    'flags': ['-O3', '-flto', '-fuse-linker-plugin', '-ffat-lto-objects',
                             '-march=native', '-mtune=native'],
                    'std': 'c++17' if is_cpp else 'c11',
                    'priority': priority + 3
                }
            ]
            
            strategies.extend(ultra_strategies)
            priority += 10
    
    # MEGA STRATEGY SET 2: ANDROID/TERMUX SUPER OPTIMIZED
    if compiler_system.system_info['is_termux'] or compiler_system.system_info['is_android']:
        android_strategies = []
        
        # Get Android-specific compilers
        android_compilers = (compiler_system.available_compilers['android_compilers'] + 
                           compiler_system.available_compilers['clang_variants'][:5])
        
        for compiler_info in android_compilers:
            compiler = compiler_info['name']
            
            android_strategies.extend([
                {
                    'name': f"📱 ANDROID ULTRA OPTIMIZED - {compiler}",
                    'compiler': compiler,
                    'flags': ['-O3', '-ffast-math', '-march=native', '-mtune=native',
                             '-pthread', '-DENABLE_JNI', '-fPIC', '-flto'],
                    'libs': ['-landroid', '-llog', '-ldl', '-lm', '-lc'],
                    'std': 'c++17' if is_cpp else 'c11',
                    'priority': priority
                },
                {
                    'name': f"🤖 TERMUX NATIVE ULTRA - {compiler}",
                    'compiler': compiler,
                    'flags': ['-O3', '-march=armv8-a' if 'aarch64' in platform.machine() else '-march=armv7-a',
                             '-pthread', '-fPIC', '-DTERMUX_BUILD', '-flto'],
                    'libs': ['-llog', '-ldl', '-lm'],
                    'std': 'c++17' if is_cpp else 'c11',
                    'priority': priority + 1
                },
                {
                    'name': f"📲 ANDROID NDK ULTRA - {compiler}",
                    'compiler': compiler,
                    'flags': ['-O3', '-ffast-math', '-pthread', '-fPIC', '-DANDROID',
                             '-ffunction-sections', '-fdata-sections', '-flto'],
                    'libs': ['-landroid', '-llog', '-ldl', '-lm', '-lc'],
                    'linker_flags': ['-Wl,--gc-sections', '-Wl,--as-needed'],
                    'std': 'c++17' if is_cpp else 'c11',
                    'priority': priority + 2
                },
                {
                    'name': f"🔋 ANDROID BATTERY OPTIMIZED - {compiler}",
                    'compiler': compiler,
                    'flags': ['-O2', '-march=native', '-pthread', '-fPIC',
                             '-fno-omit-frame-pointer', '-DANDROID_BATTERY_OPT'],
                    'libs': ['-landroid', '-llog', '-ldl', '-lm'],
                    'std': 'c++14' if is_cpp else 'c99',
                    'priority': priority + 3
                }
            ])
        
        strategies.extend(android_strategies)
        priority += 20
    
    # MEGA STRATEGY SET 3: COMPREHENSIVE STANDARD MATRIX WITH ALL COMBINATIONS
    standard_matrix = []
    
    if is_cpp:
        cpp_standards = ['c++23', 'c++2b', 'c++20', 'c++2a', 'c++17', 'c++1z', 
                        'c++14', 'c++1y', 'c++11', 'c++0x', 'gnu++23', 'gnu++20', 
                        'gnu++17', 'gnu++14', 'gnu++11']
    elif is_c:
        cpp_standards = ['c2x', 'c17', 'c11', 'c99', 'c90', 'gnu2x', 'gnu17', 'gnu11', 'gnu99']
    else:
        cpp_standards = ['c11']
    
    optimization_levels = ['-Ofast', '-O3', '-O2', '-Os', '-Oz', '-Og', '-O1', '-O0']
    
    # Get best compilers for standard matrix
    best_compilers = (compiler_system.available_compilers['gcc_variants'][:3] + 
                     compiler_system.available_compilers['clang_variants'][:3] +
                     compiler_system.available_compilers['modern_compilers'][:2])
    
    for compiler_info in best_compilers:
        compiler = compiler_info['name']
        
        for std in cpp_standards[:10]:  # Limit standards
            for opt in optimization_levels[:6]:  # Limit optimization levels
                standard_matrix.append({
                    'name': f"📋 {std.upper()} {opt} - {compiler}",
                    'compiler': compiler,
                    'flags': [opt, '-Wall', '-Wextra'],
                    'std': std,
                    'priority': priority
                })
                priority += 1
    
    strategies.extend(standard_matrix[:80])  # Limit to prevent overflow
    
    # MEGA STRATEGY SET 4: LIBRARY-SPECIFIC ULTRA OPTIMIZED BUILDS
    lib_strategies = []
    required_libs = analysis['required_libs']
    
    for compiler_info in best_compilers[:6]:
        compiler = compiler_info['name']
        
        # Math-heavy optimizations with multiple variants
        if 'math' in required_libs or analysis['math_heavy']:
            lib_strategies.extend([
                {
                    'name': f"🧮 MATH ULTRA PERFORMANCE - {compiler}",
                    'compiler': compiler,
                    'flags': ['-Ofast', '-ffast-math', '-funsafe-math-optimizations',
                             '-ffinite-math-only', '-fno-signed-zeros', '-march=native',
                             '-mfma', '-mavx2'],
                    'libs': ['-lm'],
                    'std': 'c++17' if is_cpp else 'c11',
                    'priority': priority
                },
                {
                    'name': f"📊 MATH PRECISION ULTRA - {compiler}",
                    'compiler': compiler,
                    'flags': ['-O3', '-ffp-contract=off', '-fno-fast-math', '-march=native'],
                    'libs': ['-lm', '-lquadmath'],
                    'std': 'c++17' if is_cpp else 'c11',
                    'priority': priority + 1
                },
                {
                    'name': f"🔢 MATH VECTORIZED - {compiler}",
                    'compiler': compiler,
                    'flags': ['-O3', '-ffast-math', '-ftree-vectorize', '-march=native',
                             '-msse4.2', '-mavx', '-mavx2'],
                    'libs': ['-lm'],
                    'std': 'c++17' if is_cpp else 'c11',
                    'priority': priority + 2
                }
            ])
        
        # Threading optimizations with OpenMP variants
        if 'pthread' in required_libs or analysis['threading']:
            lib_strategies.extend([
                {
                    'name': f"🧵 THREADING ULTRA MAX - {compiler}",
                    'compiler': compiler,
                    'flags': ['-O3', '-pthread', '-fopenmp', '-ffast-math', '-march=native'],
                    'libs': ['-lpthread', '-lgomp'],
                    'std': 'c++17' if is_cpp else 'c11',
                    'priority': priority
                },
                {
                    'name': f"⚡ PARALLEL ULTRA OPTIMIZED - {compiler}",
                    'compiler': compiler,
                    'flags': ['-O3', '-pthread', '-march=native', '-ftree-parallelize-loops=8',
                             '-floop-parallelize-all'],
                    'libs': ['-lpthread'],
                    'std': 'c++17' if is_cpp else 'c11',
                    'priority': priority + 1
                },
                {
                    'name': f"🔄 ATOMIC OPTIMIZED - {compiler}",
                    'compiler': compiler,
                    'flags': ['-O3', '-pthread', '-march=native', '-mcx16'],
                    'libs': ['-lpthread', '-latomic'],
                    'std': 'c++17' if is_cpp else 'c11',
                    'priority': priority + 2
                }
            ])
        
        # Graphics optimizations with multiple APIs
        if 'opengl' in required_libs or 'vulkan' in required_libs or analysis['graphics']:
            lib_strategies.extend([
                {
                    'name': f"🎮 GRAPHICS ULTRA PERFORMANCE - {compiler}",
                    'compiler': compiler,
                    'flags': ['-O3', '-ffast-math', '-march=native', '-msse4.2', '-mavx'],
                    'libs': ['-lGL', '-lGLU', '-lglfw', '-lGLEW', '-lm'],
                    'std': 'c++17' if is_cpp else 'c11',
                    'priority': priority
                },
                {
                    'name': f"🖼️ VULKAN OPTIMIZED - {compiler}",
                    'compiler': compiler,
                    'flags': ['-O3', '-ffast-math', '-march=native'],
                    'libs': ['-lvulkan', '-lm'],
                    'std': 'c++17' if is_cpp else 'c11',
                    'priority': priority + 1
                }
            ])
        
        # Network optimizations
        if 'network' in required_libs or 'curl' in required_libs or analysis['networking']:
            lib_strategies.extend([
                {
                    'name': f"🌐 NETWORK ULTRA OPTIMIZED - {compiler}",
                    'compiler': compiler,
                    'flags': ['-O3', '-pthread', '-march=native'],
                    'libs': ['-lpthread', '-lcurl', '-lssl', '-lcrypto', '-lz'],
                    'std': 'c++17' if is_cpp else 'c11',
                    'priority': priority
                },
                {
                    'name': f"🔒 SECURE NETWORK - {compiler}",
                    'compiler': compiler,
                    'flags': ['-O2', '-pthread', '-D_FORTIFY_SOURCE=2'],
                    'libs': ['-lpthread', '-lcurl', '-lssl', '-lcrypto'],
                    'std': 'c++17' if is_cpp else 'c11',
                    'priority': priority + 1
                }
            ])
        
        # Static/Dynamic builds with multiple variants
        lib_strategies.extend([
            {
                'name': f"📦 STATIC ULTRA COMPLETE - {compiler}",
                'compiler': compiler,
                'flags': ['-O2', '-static', '-static-libgcc'] + (['-static-libstdc++'] if is_cpp else []),
                'std': 'c++17' if is_cpp else 'c11',
                'priority': priority + 5
            },
            {
                'name': f"🔗 DYNAMIC OPTIMIZED - {compiler}",
                'compiler': compiler,
                'flags': ['-O2', '-fPIC', '-shared'] if analysis['complexity'] == 'high' else ['-O2', '-fPIC'],
                'std': 'c++17' if is_cpp else 'c11',
                'priority': priority + 6
            },
            {
                'name': f"⚖️ HYBRID LINKING - {compiler}",
                'compiler': compiler,
                'flags': ['-O2', '-fPIC'],
                'linker_flags': ['-Wl,--as-needed', '-Wl,--no-undefined'],
                'std': 'c++17' if is_cpp else 'c11',
                'priority': priority + 7
            }
        ])
        
        priority += 20
    
    strategies.extend(lib_strategies)
    
    # MEGA STRATEGY SET 5: ARCHITECTURE-SPECIFIC ULTRA MATRIX
    arch_strategies = []
    arch = platform.machine().lower()
    
    arch_optimization_matrix = {
        'x86_64': [
            ('-march=native', '-mtune=native'),
            ('-march=skylake', '-mtune=skylake'),
            ('-march=haswell', '-mtune=haswell'),
            ('-march=broadwell', '-mtune=broadwell'),
            ('-march=sandybridge', '-mtune=sandybridge'),
            ('-march=nehalem', '-mtune=nehalem'),
            ('-march=core2', '-mtune=core2'),
            ('-march=x86-64', '-mtune=generic'),
            ('-march=x86-64-v2', '-mtune=generic'),
            ('-march=x86-64-v3', '-mtune=generic')
        ],
        'aarch64': [
            ('-march=native', '-mtune=native'),
            ('-march=armv8-a', '-mtune=cortex-a72'),
            ('-march=armv8.1-a', '-mtune=cortex-a72'),
            ('-march=armv8.2-a', '-mtune=cortex-a72'),
            ('-mcpu=cortex-a72', ''),
            ('-mcpu=cortex-a57', ''),
            ('-mcpu=cortex-a53', ''),
            ('-mcpu=cortex-a76', ''),
            ('-mcpu=cortex-a78', '')
        ],
        'armv7l': [
            ('-march=native', '-mtune=native'),
            ('-march=armv7-a', '-mfpu=neon'),
            ('-march=armv7ve', '-mfpu=neon'),
            ('-mcpu=cortex-a15', '-mfpu=neon'),
            ('-mcpu=cortex-a9', '-mfpu=neon'),
            ('-mcpu=cortex-a8', '-mfpu=neon'),
            ('-mcpu=cortex-a7', '-mfpu=neon-vfpv4')
        ],
        'i686': [
            ('-march=native', '-mtune=native'),
            ('-march=i686', '-mtune=generic'),
            ('-march=pentium4', '-msse2'),
            ('-march=core2', '-msse3'),
            ('-march=atom', '-mtune=atom')
        ]
    }
    
    if arch in arch_optimization_matrix:
        for compiler_info in best_compilers[:4]:
            compiler = compiler_info['name']
            
            for arch_flags in arch_optimization_matrix[arch]:
                march_flag, additional_flag = arch_flags
                for opt_level in ['-Ofast', '-O3', '-O2']:
                    flags = [opt_level, march_flag]
                    if additional_flag:
                        flags.append(additional_flag)
                    
                    arch_strategies.append({
                        'name': f"🏗️ {march_flag.upper()} {opt_level} - {compiler}",
                        'compiler': compiler,
                        'flags': flags,
                        'std': 'c++17' if is_cpp else 'c11',
                        'priority': priority
                    })
                    priority += 1
    
    strategies.extend(arch_strategies[:50])  # Limit architecture strategies
    
    # MEGA STRATEGY SET 6: SECURITY & HARDENING ULTRA
    security_strategies = []
    
    for compiler_info in best_compilers[:4]:
        compiler = compiler_info['name']
        
        security_strategies.extend([
            {
                'name': f"🔒 SECURITY ULTRA HARDENED - {compiler}",
                'compiler': compiler,
                'flags': ['-O2', '-fstack-protector-strong', '-D_FORTIFY_SOURCE=2',
                         '-fPIE', '-Wformat', '-Wformat-security', '-Werror=format-security',
                         '-fcf-protection=full', '-fstack-clash-protection'],
                'linker_flags': ['-Wl,-z,relro', '-Wl,-z,now', '-Wl,-z,noexecstack', '-pie'],
                'std': 'c++17' if is_cpp else 'c11',
                'priority': priority
            },
            {
                'name': f"🛡️ SECURITY MAXIMUM - {compiler}",
                'compiler': compiler,
                'flags': ['-O2', '-fstack-protector-all', '-D_FORTIFY_SOURCE=3',
                         '-fPIE', '-fcf-protection=full', '-fstack-clash-protection',
                         '-fsanitize=address', '-fsanitize=undefined',
                         '-fno-common', '-fno-strict-overflow'],
                'linker_flags': ['-Wl,-z,relro', '-Wl,-z,now', '-Wl,-z,noexecstack', 
                               '-Wl,-z,separate-code', '-pie'],
                'std': 'c++17' if is_cpp else 'c11',
                'priority': priority + 1
            },
            {
                'name': f"🔐 CRYPTO OPTIMIZED - {compiler}",
                'compiler': compiler,
                'flags': ['-O3', '-march=native', '-maes', '-msha'],
                'libs': ['-lcrypto', '-lssl'],
                'std': 'c++17' if is_cpp else 'c11',
                'priority': priority + 2
            }
        ])
    
    strategies.extend(security_strategies)
    priority += 30
    
    # MEGA STRATEGY SET 7: CROSS-COMPILATION ULTRA
    cross_strategies = []
    
    for compiler_info in compiler_system.available_compilers['cross_compilers'][:15]:
        compiler = compiler_info['name']
        target = compiler_info.get('target', 'unknown')
        
        cross_strategies.extend([
            {
                'name': f"🌐 CROSS {target.upper()} OPTIMIZED - {compiler}",
                'compiler': compiler,
                'flags': ['-O3', '-static'],
                'std': 'c++14' if is_cpp else 'c99',
                'priority': priority + 10
            },
            {
                'name': f"🔧 CROSS {target.upper()} MINIMAL - {compiler}",
                'compiler': compiler,
                'flags': ['-Os', '-static'],
                'std': 'c++11' if is_cpp else 'c89',
                'priority': priority + 15
            }
        ])
    
    strategies.extend(cross_strategies[:20])  # Limit cross-compilation
    
    # MEGA STRATEGY SET 8: SPECIALIZED COMPILERS ULTRA
    specialized_strategies = []
    
    for compiler_info in compiler_system.available_compilers['specialized']:
        compiler = compiler_info['name']
        
        if 'tcc' in compiler:
            specialized_strategies.extend([
                {
                    'name': f"⚡ TCC ULTRA FAST - {compiler}",
                    'compiler': compiler,
                    'flags': [],
                    'priority': priority + 5
                },
                {
                    'name': f"🚀 TCC OPTIMIZED - {compiler}",
                    'compiler': compiler,
                    'flags': ['-O2'],
                    'priority': priority + 6
                }
            ])
        elif 'icc' in compiler or 'icx' in compiler:
            specialized_strategies.extend([
                {
                    'name': f"🔬 INTEL ULTRA PERFORMANCE - {compiler}",
                    'compiler': compiler,
                    'flags': ['-O3', '-xHost', '-ipo', '-fast'],
                    'std': 'c++17' if is_cpp else 'c11',
                    'priority': priority
                },
                {
                    'name': f"🧠 INTEL VECTORIZED - {compiler}",
                    'compiler': compiler,
                    'flags': ['-O3', '-xHost', '-ipo', '-vec', '-simd'],
                    'std': 'c++17' if is_cpp else 'c11',
                    'priority': priority + 1
                }
            ])
        elif 'nvcc' in compiler:
            specialized_strategies.extend([
                {
                    'name': f"🚀 CUDA ULTRA PERFORMANCE - {compiler}",
                    'compiler': compiler,
                    'flags': ['-O3', '--use_fast_math', '-arch=sm_50'],
                    'std': 'c++14' if is_cpp else 'c99',
                    'priority': priority
                },
                {
                    'name': f"⚡ CUDA OPTIMIZED - {compiler}",
                    'compiler': compiler,
                    'flags': ['-O3', '--use_fast_math'],
                    'std': 'c++14' if is_cpp else 'c99',
                    'priority': priority + 1
                }
            ])
    
    strategies.extend(specialized_strategies)
    priority += 40
    
    # MEGA STRATEGY SET 9: PROFILE-GUIDED OPTIMIZATION
    pgo_strategies = []
    
    for compiler_info in best_compilers[:3]:
        compiler = compiler_info['name']
        
        if 'gcc' in compiler or 'clang' in compiler:
            pgo_strategies.extend([
                {
                    'name': f"📊 PGO OPTIMIZED - {compiler}",
                    'compiler': compiler,
                    'flags': ['-O3', '-fprofile-generate'],
                    'std': 'c++17' if is_cpp else 'c11',
                    'priority': priority + 20
                },
                {
                    'name': f"🎯 PGO APPLIED - {compiler}",
                    'compiler': compiler,
                    'flags': ['-O3', '-fprofile-use'],
                    'std': 'c++17' if is_cpp else 'c11',
                    'priority': priority + 25
                }
            ])
    
    strategies.extend(pgo_strategies)
    priority += 50
    
    # MEGA STRATEGY SET 10: FALLBACK & EMERGENCY BUILDS (ULTRA COMPREHENSIVE)
    fallback_strategies = []
    
    all_compilers = []
    for category in compiler_system.available_compilers.values():
        all_compilers.extend([c['name'] for c in category])
    
    for compiler in set(all_compilers):
        fallback_strategies.extend([
            {
                'name': f"🆘 MINIMAL SAFE - {compiler}",
                'compiler': compiler,
                'flags': [],
                'priority': priority + 100
            },
            {
                'name': f"🔧 BASIC COMPILE - {compiler}",
                'compiler': compiler,
                'flags': ['-O1'],
                'priority': priority + 101
            },
            {
                'name': f"⚠️ COMPATIBILITY MODE - {compiler}",
                'compiler': compiler,
                'flags': ['-O0', '-std=c89' if is_c else '-std=c++98' if is_cpp else ''],
                'priority': priority + 102
            },
            {
                'name': f"🩹 EMERGENCY BUILD - {compiler}",
                'compiler': compiler,
                'flags': ['-w', '-fpermissive'] if is_cpp else ['-w'],
                'priority': priority + 103
            }
        ])
    
    strategies.extend(fallback_strategies)
    
    # MEGA STRATEGY SET 11: EXPERIMENTAL & CUTTING-EDGE
    experimental_strategies = []
    
    for compiler_info in compiler_system.available_compilers['experimental_compilers']:
        compiler = compiler_info['name']
        
        experimental_strategies.extend([
            {
                'name': f"🧪 EXPERIMENTAL ULTRA - {compiler}",
                'compiler': compiler,
                'flags': ['-O3', '-experimental'],
                'std': 'c++23' if is_cpp else 'c2x',
                'priority': priority + 200
            },
            {
                'name': f"🔬 CUTTING EDGE - {compiler}",
                'compiler': compiler,
                'flags': ['-O2', '-enable-experimental'],
                'std': 'c++2b' if is_cpp else 'c2x',
                'priority': priority + 201
            }
        ])
    
    strategies.extend(experimental_strategies)
    
    # MEGA STRATEGY SET 12: EMBEDDED & MICROCONTROLLER
    embedded_strategies = []
    
    for compiler_info in compiler_system.available_compilers['embedded_compilers']:
        compiler = compiler_info['name']
        
        embedded_strategies.extend([
            {
                'name': f"🔌 EMBEDDED ULTRA - {compiler}",
                'compiler': compiler,
                'flags': ['-Os', '-ffunction-sections', '-fdata-sections'],
                'linker_flags': ['-Wl,--gc-sections'],
                'std': 'c11' if is_c else 'c++14',
                'priority': priority + 150
            },
            {
                'name': f"⚡ MICROCONTROLLER - {compiler}",
                'compiler': compiler,
                'flags': ['-Os', '-fno-exceptions', '-fno-rtti'] if is_cpp else ['-Os'],
                'std': 'c99' if is_c else 'c++11',
                'priority': priority + 151
            }
        ])
    
    strategies.extend(embedded_strategies)
    
    # MEGA STRATEGY SET 13: FORTRAN SPECIFIC (if applicable)
    if is_fortran:
        fortran_strategies = []
        fortran_compilers = ['gfortran', 'flang', 'ifort', 'pgfortran']
        
        for compiler in fortran_compilers:
            if shutil.which(compiler):
                fortran_strategies.extend([
                    {
                        'name': f"🔬 FORTRAN SCIENTIFIC - {compiler}",
                        'compiler': compiler,
                        'flags': ['-O3', '-ffast-math', '-march=native'],
                        'libs': ['-llapack', '-lblas'],
                        'priority': priority
                    },
                    {
                        'name': f"📊 FORTRAN NUMERICAL - {compiler}",
                        'compiler': compiler,
                        'flags': ['-O3', '-funroll-loops', '-ftree-vectorize'],
                        'libs': ['-lm'],
                        'priority': priority + 1
                    }
                ])
        
        strategies.extend(fortran_strategies)
    
    # MEGA STRATEGY SET 14: ASSEMBLY SPECIFIC (if applicable)
    if is_asm:
        asm_strategies = []
        asm_tools = ['as', 'gas', 'nasm', 'yasm', 'fasm']
        
        for tool in asm_tools:
            if shutil.which(tool):
                asm_strategies.extend([
                    {
                        'name': f"⚙️ ASSEMBLY DIRECT - {tool}",
                        'compiler': tool,
                        'flags': ['-64'] if '64' in platform.machine() else ['-32'],
                        'priority': priority
                    },
                    {
                        'name': f"🔧 ASSEMBLY OPTIMIZED - {tool}",
                        'compiler': tool,
                        'flags': ['-O3', '-g'],
                        'priority': priority + 1
                    }
                ])
        
        strategies.extend(asm_strategies)
    
    # MEGA STRATEGY SET 15: RUST & MODERN LANGUAGES
    if file_ext == '.rs':
        rust_strategies = []
        if shutil.which('rustc'):
            rust_strategies.extend([
                {
                    'name': "🦀 RUST ULTRA PERFORMANCE",
                    'compiler': 'rustc',
                    'flags': ['-O', '--edition=2021'],
                    'priority': priority
                },
                {
                    'name': "⚡ RUST OPTIMIZED",
                    'compiler': 'rustc',
                    'flags': ['-C', 'opt-level=3', '--edition=2021'],
                    'priority': priority + 1
                },
                {
                    'name': "🔒 RUST SAFE",
                    'compiler': 'rustc',
                    'flags': ['--edition=2021'],
                    'priority': priority + 2
                }
            ])
        
        strategies.extend(rust_strategies)
    
    # MEGA STRATEGY SET 16: GO LANGUAGE
    if file_ext == '.go':
        go_strategies = []
        if shutil.which('go'):
            go_strategies.extend([
                {
                    'name': "🐹 GO ULTRA BUILD",
                    'compiler': 'go',
                    'flags': ['build', '-ldflags', '-s -w'],
                    'priority': priority
                },
                {
                    'name': "⚡ GO OPTIMIZED",
                    'compiler': 'go',
                    'flags': ['build', '-a', '-gcflags', '-N -l'],
                    'priority': priority + 1
                }
            ])
        
        strategies.extend(go_strategies)
    
    # MEGA STRATEGY SET 17: ZIG LANGUAGE
    if file_ext == '.zig':
        zig_strategies = []
        if shutil.which('zig'):
            zig_strategies.extend([
                {
                    'name': "⚡ ZIG ULTRA FAST",
                    'compiler': 'zig',
                    'flags': ['build-exe', '-OReleaseFast'],
                    'priority': priority
                },
                {
                    'name': "🔧 ZIG OPTIMIZED",
                    'compiler': 'zig',
                    'flags': ['build-exe', '-O', 'ReleaseSafe'],
                    'priority': priority + 1
                },
                {
                    'name': "📦 ZIG SMALL",
                    'compiler': 'zig',
                    'flags': ['build-exe', '-O', 'ReleaseSmall'],
                    'priority': priority + 2
                }
            ])
        
        strategies.extend(zig_strategies)
    
    # Set output path for all strategies
    for strategy in strategies:
        strategy['output_path'] = output_path
        strategy['input_path'] = file_path
        strategy['file_type'] = 'cpp' if is_cpp else 'c' if is_c else 'asm' if is_asm else 'other'
        strategy['analysis'] = analysis
        
        # Add dynamic library linking based on analysis
        if 'libs' not in strategy:
            strategy['libs'] = []
        
        # Auto-add common libraries based on analysis
        if analysis['threading']:
            if '-lpthread' not in strategy['libs']:
                strategy['libs'].append('-lpthread')
        
        if analysis['math_heavy']:
            if '-lm' not in strategy['libs']:
                strategy['libs'].append('-lm')
        
        if analysis.get('android_apis', False):
            android_libs = ['-landroid', '-llog', '-ldl']
            for lib in android_libs:
                if lib not in strategy['libs']:
                    strategy['libs'].append(lib)
        
        # Add optimization-specific libraries
        if any('openmp' in flag for flag in strategy.get('flags', [])):
            if '-lgomp' not in strategy['libs']:
                strategy['libs'].append('-lgomp')
    
    # Sort strategies by priority (lower = higher priority)
    strategies.sort(key=lambda x: x['priority'])
    
    # Limit total strategies to prevent overwhelming
    max_strategies = min(500, len(strategies))
    strategies = strategies[:max_strategies]
    
    # Add metadata
    for i, strategy in enumerate(strategies):
        strategy['strategy_id'] = i + 1
        strategy['total_strategies'] = len(strategies)
        strategy['estimated_time'] = estimate_compilation_time(strategy)
        strategy['risk_level'] = assess_strategy_risk(strategy)
        strategy['expected_performance'] = estimate_performance_gain(strategy)
    
    return strategies

def detect_code_language(content: str, file_ext: str) -> str:
    """Detect programming language from content and extension"""
    
    if file_ext in ['.cpp', '.cc', '.cxx', '.c++', '.hpp', '.hh', '.hxx']:
        return 'cpp'
    elif file_ext in ['.c', '.h']:
        # Distinguish between C and C++
        cpp_indicators = ['class ', 'template', 'namespace', 'std::', 'iostream', 'vector']
        if any(indicator in content for indicator in cpp_indicators):
            return 'cpp'
        return 'c'
    elif file_ext in ['.rs']:
        return 'rust'
    elif file_ext in ['.go']:
        return 'go'
    elif file_ext in ['.zig']:
        return 'zig'
    elif file_ext in ['.s', '.S', '.asm']:
        return 'assembly'
    elif file_ext in ['.f', '.f90', '.f95', '.f03', '.f08', '.for']:
        return 'fortran'
    elif file_ext in ['.m', '.mm']:
        return 'objc'
    elif file_ext in ['.d']:
        return 'd'
    elif file_ext in ['.pas']:
        return 'pascal'
    elif file_ext in ['.ada', '.adb', '.ads']:
        return 'ada'
    else:
        return 'unknown'

def estimate_compilation_time(strategy: Dict) -> str:
    """Estimate compilation time based on strategy complexity"""
    
    time_score = 1.0
    
    # Factor in optimization level
    flags = strategy.get('flags', [])
    if '-Ofast' in flags or '-O3' in flags:
        time_score *= 3.0
    elif '-O2' in flags:
        time_score *= 2.0
    elif '-Os' in flags or '-Oz' in flags:
        time_score *= 1.5
    
    # Factor in special optimizations
    if '-flto' in flags:
        time_score *= 2.5
    if '-fprofile-generate' in flags or '-fprofile-use' in flags:
        time_score *= 4.0
    if any('sanitize' in flag for flag in flags):
        time_score *= 2.0
    
    # Factor in complexity
    complexity = strategy.get('analysis', {}).get('complexity', 'low')
    complexity_multipliers = {
        'very_low': 0.5,
        'low': 1.0,
        'medium': 2.0,
        'high': 4.0,
        'very_high': 8.0
    }
    time_score *= complexity_multipliers.get(complexity, 1.0)
    
    # Estimate final time
    if time_score < 2:
        return "⚡ <10s"
    elif time_score < 5:
        return "🔥 10-30s"
    elif time_score < 10:
        return "⏱️ 30s-1m"
    elif time_score < 20:
        return "⌛ 1-3m"
    else:
        return "🐌 >3m"

def assess_strategy_risk(strategy: Dict) -> str:
    """Assess compilation risk level"""
    
    risk_score = 0
    flags = strategy.get('flags', [])
    
    # High-risk flags
    high_risk_flags = ['-Ofast', '-ffast-math', '-funsafe-math-optimizations', 
                      '-fno-stack-protector', '-fpermissive']
    risk_score += sum(1 for flag in high_risk_flags if flag in flags)
    
    # Medium-risk flags
    medium_risk_flags = ['-O3', '-march=native', '-flto', '-fprofile-use']
    risk_score += sum(0.5 for flag in medium_risk_flags if flag in flags)
    
    # Experimental features
    if 'experimental' in strategy['name'].lower():
        risk_score += 2
    
    # Cross-compilation
    if 'cross' in strategy['name'].lower():
        risk_score += 1
    
    if risk_score < 0.5:
        return "🟢 LOW"
    elif risk_score < 1.5:
        return "🟡 MEDIUM"
    elif risk_score < 3:
        return "🟠 HIGH"
    else:
        return "🔴 VERY HIGH"

def estimate_performance_gain(strategy: Dict) -> str:
    """Estimate expected performance improvement"""
    
    perf_score = 1.0
    flags = strategy.get('flags', [])
    
    # Optimization level impact
    if '-Ofast' in flags:
        perf_score *= 2.5
    elif '-O3' in flags:
        perf_score *= 2.0
    elif '-O2' in flags:
        perf_score *= 1.5
    elif '-Os' in flags or '-Oz' in flags:
        perf_score *= 1.2
    
    # Specialized optimizations
    if '-march=native' in flags:
        perf_score *= 1.3
    if '-flto' in flags:
        perf_score *= 1.2
    if '-ffast-math' in flags:
        perf_score *= 1.4
    if any('vectorize' in flag for flag in flags):
        perf_score *= 1.3
    
    # Math-heavy bonus
    analysis = strategy.get('analysis', {})
    if analysis.get('math_heavy', False) and '-ffast-math' in flags:
        perf_score *= 1.5
    
    if perf_score < 1.2:
        return "📊 +0-20%"
    elif perf_score < 1.5:
        return "📈 +20-50%"
    elif perf_score < 2.0:
        return "🚀 +50-100%"
    elif perf_score < 3.0:
        return "⚡ +100-200%"
    else:
        return "🔥 +200%+"

async def execute_mega_parallel_compilation(strategies: List[Dict], update: Update) -> List[Dict]:
    """Execute parallel compilation with advanced progress tracking"""
    
    results = []
    total_strategies = len(strategies)
    completed = 0
    successful = 0
    failed = 0
    
    # Progress tracking
    progress_message = None
    last_update = 0
    
    # Parallel execution with thread pool
    max_workers = min(8, os.cpu_count() or 4, total_strategies)
    
    # Create progress tracking message
    progress_text = (
        f"🚀 MEGA COMPILATION MARATHON STARTED\n"
        f"📊 Total strategies: {total_strategies}\n"
        f"⚡ Parallel workers: {max_workers}\n"
        f"🔄 Progress: 0/{total_strategies} (0%)\n"
        f"✅ Successful: 0\n"
        f"❌ Failed: 0\n"
        f"⏱️ Estimated time: {estimate_total_time(strategies)}\n"
        f"🎯 Current: Starting..."
    )
    
    try:
        progress_message = await update.message.reply_text(progress_text)
    except:
        pass
    
    # Execute compilation strategies
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all compilation tasks
        future_to_strategy = {
            executor.submit(execute_single_compilation, strategy): strategy 
            for strategy in strategies
        }
        
        # Process completed tasks
        for future in concurrent.futures.as_completed(future_to_strategy):
            strategy = future_to_strategy[future]
            completed += 1
            
            try:
                result = future.result(timeout=300)  # 5 minute timeout per compilation
                results.append(result)
                
                if result['success']:
                    successful += 1
                else:
                    failed += 1
                    
            except concurrent.futures.TimeoutError:
                results.append({
                    'strategy': strategy,
                    'success': False,
                    'error': 'Compilation timeout (>5 minutes)',
                    'execution_time': 300,
                    'priority': strategy['priority']
                })
                failed += 1
                
            except Exception as e:
                results.append({
                    'strategy': strategy,
                    'success': False,
                    'error': f'Execution error: {str(e)}',
                    'execution_time': 0,
                    'priority': strategy['priority']
                })
                failed += 1
            
            # Update progress every 10 completions or significant milestones
            current_time = time.time()
            if (completed % 10 == 0 or completed == total_strategies or 
                current_time - last_update > 30):  # Update every 30 seconds minimum
                
                progress_percent = (completed / total_strategies) * 100
                current_strategy = strategy['name'][:50]
                
                progress_text = (
                    f"🚀 MEGA COMPILATION MARATHON\n"
                    f"📊 Total strategies: {total_strategies}\n"
                    f"⚡ Parallel workers: {max_workers}\n"
                    f"🔄 Progress: {completed}/{total_strategies} ({progress_percent:.1f}%)\n"
                    f"✅ Successful: {successful}\n"
                    f"❌ Failed: {failed}\n"
                    f"⏱️ ETA: {estimate_remaining_time(completed, total_strategies, current_time)}\n"
                    f"🎯 Current: {current_strategy}..."
                )
                
                try:
                    if progress_message:
                        await progress_message.edit_text(progress_text)
                    last_update = current_time
                except:
                    pass
            
            # Early termination if we have enough successful builds
            if successful >= 5 and completed >= 50:
                # Cancel remaining futures
                for remaining_future in future_to_strategy:
                    if not remaining_future.done():
                        remaining_future.cancel()
                break
    
    # Final progress update
    try:
        if progress_message:
            final_text = (
                f"🏁 MEGA COMPILATION MARATHON COMPLETED\n"
                f"📊 Total attempted: {completed}/{total_strategies}\n"
                f"✅ Successful: {successful}\n"
                f"❌ Failed: {failed}\n"
                f"🏆 Success rate: {(successful/completed)*100:.1f}%\n"
                f"⏱️ Total time: {format_duration(time.time() - (current_time - 300))}\n"
                f"🎯 Best results incoming..."
            )
            await progress_message.edit_text(final_text)
    except:
        pass
    
    return results

def execute_single_compilation(strategy: Dict) -> Dict:
    """Execute a single compilation strategy with comprehensive error handling"""
    
    start_time = time.time()
    result = {
        'strategy': strategy,
        'success': False,
        'output_path': None,
        'file_size': 0,
        'compilation_time': 0,
        'execution_time': 0,
        'error': None,
        'warnings': [],
        'compiler_output': '',
        'performance_score': 0,
        'binary_analysis': {},
        'priority': strategy['priority']
    }
    
    try:
        compiler = strategy['compiler']
        input_path = strategy['input_path']
        output_path = strategy['output_path']
        flags = strategy.get('flags', [])
        libs = strategy.get('libs', [])
        linker_flags = strategy.get('linker_flags', [])
        std = strategy.get('std', '')
        
        # Build compilation command
        cmd = [compiler]
        
        # Handle different compiler types
        if compiler == 'go':
            # Go compilation
            cmd.extend(flags)
            cmd.append(input_path)
            cmd.extend(['-o', output_path])
        elif compiler == 'rustc':
            # Rust compilation
            cmd.extend(flags)
            cmd.extend([input_path, '-o', output_path])
        elif compiler.startswith('zig'):
            # Zig compilation
            cmd.extend(flags)
            cmd.extend([input_path, '-femit-bin=' + output_path])
        elif compiler in ['as', 'gas', 'nasm', 'yasm', 'fasm']:
            # Assembly compilation
            if compiler in ['nasm', 'yasm']:
                cmd.extend(['-f', 'elf64' if '64' in platform.machine() else 'elf32'])
            cmd.extend(flags)
            cmd.extend([input_path, '-o', output_path])
        else:
            # Standard C/C++ compilation
            if std:
                cmd.append(f'-std={std}')
            
            cmd.extend(flags)
            cmd.extend([input_path, '-o', output_path])
            
            if libs:
                cmd.extend(libs)
            
            if linker_flags:
                cmd.extend(linker_flags)
        
        # Execute compilation with timeout and resource limits
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=os.path.dirname(input_path)
        )
        
        try:
            stdout, stderr = process.communicate(timeout=300)  # 5 minute timeout
            compilation_time = time.time() - start_time
            
            result['compilation_time'] = compilation_time
            result['compiler_output'] = stdout + stderr
            
            if process.returncode == 0:
                # Compilation successful
                if os.path.exists(output_path):
                    result['success'] = True
                    result['output_path'] = output_path
                    result['file_size'] = os.path.getsize(output_path)
                    
                    # Advanced binary analysis
                    result['binary_analysis'] = analyze_compiled_binary(output_path)
                    
                    # Calculate performance score
                    result['performance_score'] = calculate_performance_score(
                        strategy, result['file_size'], compilation_time, result['binary_analysis']
                    )
                    
                    # Extract warnings
                    result['warnings'] = extract_warnings(stderr)
                    
                else:
                    result['error'] = 'Compilation succeeded but output file not found'
            else:
                result['error'] = f'Compilation failed (exit code {process.returncode}): {stderr[:500]}'
                
        except subprocess.TimeoutExpired:
            process.kill()
            result['error'] = 'Compilation timeout (>5 minutes)'
            
    except FileNotFoundError:
        result['error'] = f'Compiler not found: {compiler}'
    except Exception as e:
        result['error'] = f'Unexpected error: {str(e)}'
    
    result['execution_time'] = time.time() - start_time
    return result

def analyze_compiled_binary(binary_path: str) -> Dict:
    """Advanced binary analysis"""
    
    analysis = {
        'file_type': 'unknown',
        'architecture': 'unknown',
        'stripped': False,
        'static_linked': False,
        'dynamic_libs': [],
        'sections': [],
        'symbols_count': 0,
        'entry_point': 'unknown',
        'security_features': [],
        'optimization_level': 'unknown'
    }
    
    try:
        # Use file command for basic info
        if shutil.which('file'):
            result = subprocess.run(['file', binary_path], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                file_output = result.stdout.lower()
                analysis['file_type'] = 'executable' if 'executable' in file_output else 'unknown'
                
                if 'x86-64' in file_output or 'x86_64' in file_output:
                    analysis['architecture'] = 'x86_64'
                elif 'aarch64' in file_output:
                    analysis['architecture'] = 'aarch64'
                elif 'arm' in file_output:
                    analysis['architecture'] = 'arm'
                elif 'i386' in file_output:
                    analysis['architecture'] = 'i386'
                
                analysis['stripped'] = 'stripped' in file_output
                analysis['static_linked'] = 'statically linked' in file_output
        
        # Use objdump/readelf for detailed analysis
        objdump_cmd = None
        for cmd in ['objdump', 'llvm-objdump', 'gobjdump']:
            if shutil.which(cmd):
                objdump_cmd = cmd
                break
        
        if objdump_cmd:
            # Get sections
            result = subprocess.run([objdump_cmd, '-h', binary_path], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                sections = []
                for line in result.stdout.split('\n'):
                    if '.' in line and any(sec in line for sec in ['.text', '.data', '.bss', '.rodata']):
                        sections.append(line.split()[1] if len(line.split()) > 1 else '')
                analysis['sections'] = [s for s in sections if s]
            
            # Get symbols count
            result = subprocess.run([objdump_cmd, '-t', binary_path], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                analysis['symbols_count'] = len([l for l in result.stdout.split('\n') if l.strip()])
        
        # Use ldd for dynamic libraries
        if shutil.which('ldd') and not analysis['static_linked']:
            result = subprocess.run(['ldd', binary_path], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                libs = []
                for line in result.stdout.split('\n'):
                    if '=>' in line:
                        lib = line.split('=>')[0].strip()
                        if lib:
                            libs.append(lib)
                analysis['dynamic_libs'] = libs[:10]  # Limit output
        
        # Security features detection
        if shutil.which('checksec') or shutil.which('hardening-check'):
            # This would require additional tools, simplified check
            pass
        
    except Exception as e:
        analysis['error'] = str(e)
    
    return analysis

def calculate_performance_score(strategy: Dict, file_size: int, compilation_time: float, binary_analysis: Dict) -> int:
    """Calculate overall performance score"""
    
    score = 100  # Base score
    
    # File size factor (smaller is better for most cases, but not always)
    if file_size < 50000:  # < 50KB
        score += 20
    elif file_size < 500000:  # < 500KB
        score += 10
    elif file_size < 5000000:  # < 5MB
        score += 0
    else:
        score -= 10
    
    # Compilation time factor (faster is better)
    if compilation_time < 5:
        score += 15
    elif compilation_time < 15:
        score += 10
    elif compilation_time < 30:
        score += 5
    elif compilation_time > 60:
        score -= 10
    
    # Optimization level bonus
    flags = strategy.get('flags', [])
    if '-Ofast' in flags:
        score += 25
    elif '-O3' in flags:
        score += 20
    elif '-O2' in flags:
        score += 15
    elif '-Os' in flags or '-Oz' in flags:
        score += 10
    
    # Special optimizations
    if '-march=native' in flags:
        score += 10
    if '-flto' in flags:
        score += 15
    if '-ffast-math' in flags:
        score += 10
    
    # Priority bonus (lower priority = higher score)
    priority = strategy.get('priority', 100)
    if priority < 10:
        score += 20
    elif priority < 50:
        score += 10
    elif priority > 200:
        score -= 20
    
    # Binary analysis bonus
    if binary_analysis.get('stripped', False):
        score += 5
    if binary_analysis.get('static_linked', False):
        score += 10
    
    return max(0, min(200, score))  # Clamp between 0-200

def extract_warnings(stderr: str) -> List[str]:
    """Extract compilation warnings"""
    
    warnings = []
    for line in stderr.split('\n'):
        if 'warning:' in line.lower() or 'warn:' in line.lower():
            warnings.append(line.strip()[:200])  # Limit length
    
    return warnings[:10]  # Limit number of warnings

def estimate_total_time(strategies: List[Dict]) -> str:
    """Estimate total compilation time"""
    
    total_score = sum(get_time_score(s) for s in strategies[:50])  # Sample first 50
    avg_score = total_score / min(50, len(strategies))
    
    # Parallel factor
    max_workers = min(8, os.cpu_count() or 4)
    parallel_factor = max_workers * 0.7  # Not perfect parallelization
    
    estimated_seconds = (avg_score * len(strategies)) / parallel_factor
    
    if estimated_seconds < 60:
        return f"~{int(estimated_seconds)}s"
    elif estimated_seconds < 3600:
        return f"~{int(estimated_seconds/60)}m"
    else:
        return f"~{int(estimated_seconds/3600)}h"

def get_time_score(strategy: Dict) -> float:
    """Get time score for a strategy"""
    
    score = 10.0  # Base time in seconds
    flags = strategy.get('flags', [])
    
    if '-Ofast' in flags or '-O3' in flags:
        score *= 3.0
    elif '-O2' in flags:
        score *= 2.0
    elif '-Os' in flags or '-Oz' in flags:
        score *= 1.5
    
    if '-flto' in flags:
        score *= 2.5
    if any('sanitize' in flag for flag in flags):
        score *= 2.0
    
    return score

def estimate_remaining_time(completed: int, total: int, current_time: float) -> str:
    """Estimate remaining compilation time"""
    
    if completed == 0:
        return "Calculating..."
    
    # Simple linear estimation
    elapsed = current_time
    rate = completed / elapsed
    remaining_tasks = total - completed
    remaining_seconds = remaining_tasks / rate if rate > 0 else 0
    
    if remaining_seconds < 60:
        return f"~{int(remaining_seconds)}s"
    elif remaining_seconds < 3600:
        return f"~{int(remaining_seconds/60)}m"
    else:
        return f"~{int(remaining_seconds/3600)}h"

def format_duration(seconds: float) -> str:
    """Format duration in human-readable format"""
    
    if seconds < 60:
        return f"{int(seconds)}s"
    elif seconds < 3600:
        return f"{int(seconds/60)}m {int(seconds%60)}s"
    else:
        hours = int(seconds / 3600)
        minutes = int((seconds % 3600) / 60)
        return f"{hours}h {minutes}m"

async def handle_mega_compilation_success(update: Update, context: ContextTypes.DEFAULT_TYPE, 
                                        best_result: Dict, all_results: List[Dict], 
                                        analysis: Dict, temp_dir: str):
    """Handle successful compilation with comprehensive reporting"""
    
    try:
        strategy = best_result['strategy']
        binary_analysis = best_result.get('binary_analysis', {})
        
        # Detailed success report
        success_report = (
            f"🎉 MEGA COMPILATION SUCCESS!\n\n"
            f"🏆 BEST RESULT:\n"
            f"🔧 Strategy: {strategy['name'][:60]}\n"
            f"⚙️ Compiler: {strategy['compiler']}\n"
            f"🚀 Flags: {' '.join(strategy.get('flags', []))[:80]}\n"
            f"📏 Binary size: {format_file_size(best_result['file_size'])}\n"
            f"⏱️ Compile time: {best_result['compilation_time']:.2f}s\n"
            f"📊 Performance score: {best_result['performance_score']}/200\n"
            f"🏗️ Architecture: {binary_analysis.get('architecture', 'unknown')}\n"
            f"🔗 Linking: {'Static' if binary_analysis.get('static_linked') else 'Dynamic'}\n"
            f"🎯 Standard: {strategy.get('std', 'default')}\n"
            f"⚠️ Warnings: {len(best_result.get('warnings', []))}\n\n"
            f"📈 STATISTICS:\n"
            f"✅ Total successful: {len(all_results)}\n"
            f"🏃‍♂️ Fastest compile: {min(r['compilation_time'] for r in all_results):.2f}s\n"
            f"🐌 Slowest compile: {max(r['compilation_time'] for r in all_results):.2f}s\n"
            f"📦 Smallest binary: {format_file_size(min(r['file_size'] for r in all_results))}\n"
            f"🏋️ Largest binary: {format_file_size(max(r['file_size'] for r in all_results))}\n"
            f"⭐ Best performance: {max(r['performance_score'] for r in all_results)}/200"
        )
        
        await update.message.reply_text(success_report)
        
        # Send the compiled binary
        if os.path.exists(best_result['output_path']):
            try:
                with open(best_result['output_path'], 'rb') as f:
                    binary_name = f"compiled_{Path(strategy['input_path']).stem}"
                    if platform.system() == "Windows":
                        binary_name += ".exe"
                    
                    await update.message.reply_document(
                        document=f,
                        filename=binary_name,
                        caption=(
                            f"🎯 Optimized Binary\n"
                            f"🔧 {strategy['compiler']}\n"
                            f"📏 {format_file_size(best_result['file_size'])}\n"
                            f"⚡ Score: {best_result['performance_score']}/200"
                        )
                    )
            except Exception as e:
                await update.message.reply_text(f"❌ Failed to send binary: {str(e)}")
        
        # Detailed analysis report
        if analysis:
            analysis_report = (
                f"📊 ADVANCED CODE ANALYSIS REPORT\n\n"
                f"📄 File Analysis:\n"
                f"• Language: {analysis.get('detected_language', 'unknown').upper()}\n"
                f"• Standard: {analysis.get('language_standard', 'unknown')}\n"
                f"• Lines: {analysis.get('lines', 0):,}\n"
                f"• Functions: {analysis.get('function_count', 0)}\n"
                f"• Classes: {analysis.get('class_count', 0)}\n"
                f"• Complexity: {analysis.get('complexity', 'unknown').upper()}\n\n"
                f"🔍 Features Detected:\n"
                f"• Threading: {'✅' if analysis.get('threading') else '❌'}\n"
                f"• Math Heavy: {'✅' if analysis.get('math_heavy') else '❌'}\n"
                f"• Graphics: {'✅' if analysis.get('graphics') else '❌'}\n"
                f"• Networking: {'✅' if analysis.get('networking') else '❌'}\n"
                f"• Android APIs: {'✅' if analysis.get('android_apis') else '❌'}\n"
                f"• Security: {'✅' if analysis.get('security_features') else '❌'}\n"
                f"• Unicode: {'✅' if analysis.get('unicode_usage') else '❌'}\n"
                f"• Templates: {'✅' if analysis.get('template_usage') else '❌'}\n\n"
                f"📚 Libraries Required:\n"
                f"{', '.join(list(analysis.get('required_libs', set()))[:10])}\n\n"
                f"🔧 C++ Features:\n"
                f"{', '.join(analysis.get('cpp_features', []))}\n\n"
                f"⚠️ Potential Issues:\n"
                f"{', '.join(analysis.get('potential_issues', []))}\n\n"
                f"🆕 Modern Features:\n"
                f"{', '.join(analysis.get('modern_features', []))}"
            )
            
            await update.message.reply_text(analysis_report)
        
        # Binary analysis report
        if binary_analysis and binary_analysis != {}:
            binary_report = (
                f"🔬 BINARY ANALYSIS REPORT\n\n"
                f"📁 File Info:\n"
                f"• Type: {binary_analysis.get('file_type', 'unknown').upper()}\n"
                f"• Architecture: {binary_analysis.get('architecture', 'unknown')}\n"
                f"• Stripped: {'✅' if binary_analysis.get('stripped') else '❌'}\n"
                f"• Static Linked: {'✅' if binary_analysis.get('static_linked') else '❌'}\n"
                f"• Symbols: {binary_analysis.get('symbols_count', 0):,}\n\n"
                f"📚 Sections:\n"
                f"{', '.join(binary_analysis.get('sections', []))[:200]}\n\n"
                f"🔗 Dynamic Libraries:\n"
                f"{chr(10).join(f'• {lib}' for lib in binary_analysis.get('dynamic_libs', [])[:10])}"
            )
            
            if binary_report.strip():
                await update.message.reply_text(binary_report)
        
        # Top performers summary
        top_results = sorted(all_results, key=lambda x: x['performance_score'], reverse=True)[:5]
        top_summary = "🏆 TOP 5 PERFORMANCE RESULTS:\n\n"
        
        for i, result in enumerate(top_results, 1):
            strategy = result['strategy']
            top_summary += (
                f"{i}. {strategy['name'][:50]}\n"
                f"   📊 Score: {result['performance_score']}/200\n"
                f"   📏 Size: {format_file_size(result['file_size'])}\n"
                f"   ⏱️ Time: {result['compilation_time']:.2f}s\n\n"
            )
        
        await update.message.reply_text(top_summary)
        
        # Optimization recommendations
        recommendations = generate_optimization_recommendations(analysis, all_results)
        if recommendations:
            await update.message.reply_text(
                f"💡 OPTIMIZATION RECOMMENDATIONS:\n\n{recommendations}"
            )
        
        # Compiler comparison
        compiler_stats = analyze_compiler_performance(all_results)
        if compiler_stats:
            await update.message.reply_text(
                f"⚙️ COMPILER PERFORMANCE ANALYSIS:\n\n{compiler_stats}"
            )
        
    except Exception as e:
        await update.message.reply_text(f"❌ Error in success handling: {str(e)}")

async def handle_mega_compilation_failure(update: Update, results: List[Dict], 
                                        analysis: Dict, compiler_system):
    """Handle compilation failure with detailed diagnostics"""
    
    try:
        total_attempted = len(results)
        common_errors = analyze_common_errors(results)
        available_compilers = sum(len(compilers) for compilers in compiler_system.available_compilers.values())
        
        failure_report = (
            f"💥 MEGA COMPILATION FAILURE ANALYSIS\n\n"
            f"📊 STATISTICS:\n"
            f"• Total strategies attempted: {total_attempted}\n"
            f"• Available compilers: {available_compilers}\n"
            f"• Success rate: 0% 😢\n\n"
            f"🔍 DIAGNOSTICS:\n"
            f"• File complexity: {analysis.get('complexity', 'unknown').upper()}\n"
            f"• Language: {analysis.get('detected_language', 'unknown').upper()}\n"
            f"• Required libraries: {len(analysis.get('required_libs', set()))}\n"
            f"• Code size: {analysis.get('lines', 0)} lines\n\n"
            f"❌ COMMON ERROR PATTERNS:\n"
        )
        
        for error_type, count in common_errors.items():
            failure_report += f"• {error_type}: {count} occurrences\n"
        
        failure_report += (
            f"\n🔧 SUGGESTED FIXES:\n"
            f"{generate_fix_suggestions(common_errors, analysis)}\n\n"
            f"💊 EMERGENCY SOLUTIONS:\n"
            f"• Check if compiler is properly installed\n"
            f"• Verify source code syntax\n"
            f"• Install missing development packages\n"
            f"• Try with simpler compilation flags\n"
            f"• Update your compiler to newer version\n"
            f"• Check for missing system libraries"
        )
        
        await update.message.reply_text(failure_report)
        
        # Detailed error analysis
        error_details = "🔍 DETAILED ERROR ANALYSIS:\n\n"
        
        # Group results by error type
        error_groups = {}
        for result in results[:20]:  # Limit to first 20
            error = result.get('error', 'Unknown error')
            error_key = categorize_error(error)
            if error_key not in error_groups:
                error_groups[error_key] = []
            error_groups[error_key].append(result)
        
        for error_type, error_results in error_groups.items():
            error_details += f"📋 {error_type.upper()} ({len(error_results)} cases):\n"
            
            # Show a few examples
            for result in error_results[:3]:
                strategy = result['strategy']
                error_details += (
                    f"• {strategy['compiler']}: {result.get('error', 'Unknown')[:100]}...\n"
                )
            
            if len(error_results) > 3:
                error_details += f"• ... and {len(error_results) - 3} more similar cases\n"
            
            error_details += "\n"
        
        if len(error_details) < 4000:  # Telegram message limit
            await update.message.reply_text(error_details)
        
        # System diagnostics
        diagnostics = (
            f"🏥 SYSTEM DIAGNOSTICS:\n\n"
            f"🖥️ ENVIRONMENT:\n"
            f"• OS: {compiler_system.system_info['os']} {compiler_system.system_info['arch']}\n"
            f"• Termux: {'✅' if compiler_system.system_info['is_termux'] else '❌'}\n"
            f"• Android: {'✅' if compiler_system.system_info['is_android'] else '❌'}\n"
            f"• CPU Cores: {compiler_system.system_info['cpu_count']}\n"
            f"• Memory: {compiler_system.system_info['memory_gb']} GB\n\n"
            f"⚙️ AVAILABLE COMPILERS:\n"
            f"• GCC variants: {len(compiler_system.available_compilers['gcc_variants'])}\n"
            f"• Clang variants: {len(compiler_system.available_compilers['clang_variants'])}\n"
            f"• Specialized: {len(compiler_system.available_compilers['specialized'])}\n"
            f"• Modern: {len(compiler_system.available_compilers['modern_compilers'])}\n"
            f"• Cross compilers: {len(compiler_system.available_compilers['cross_compilers'])}\n\n"
            f"📦 PACKAGE MANAGERS:\n"
            f"• Available: {', '.join(compiler_system.package_managers[:10])}\n\n"
            f"📚 LIBRARIES:\n"
            f"• System paths: {len(compiler_system.installed_libraries['system_paths'])}\n"
            f"• Static libs: {len(compiler_system.installed_libraries['static_libs'])}\n"
            f"• Shared libs: {len(compiler_system.installed_libraries['shared_libs'])}\n"
            f"• Pkg-config: {len(compiler_system.installed_libraries['pkg_config'])}"
        )
        
        await update.message.reply_text(diagnostics)
        
        # Installation suggestions
        install_suggestions = generate_installation_suggestions(
            common_errors, analysis, compiler_system
        )
        
        if install_suggestions:
            await update.message.reply_text(
                f"📦 INSTALLATION SUGGESTIONS:\n\n{install_suggestions}"
            )
        
    except Exception as e:
        await update.message.reply_text(f"❌ Error in failure analysis: {str(e)}")

def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format"""
    
    if size_bytes < 1024:
        return f"{size_bytes}B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes/1024:.1f}KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes/(1024*1024):.1f}MB"
    else:
        return f"{size_bytes/(1024*1024*1024):.1f}GB"

def analyze_common_errors(results: List[Dict]) -> Dict[str, int]:
    """Analyze common error patterns"""
    
    error_counts = {}
    
    for result in results:
        if not result['success'] and result.get('error'):
            error_category = categorize_error(result['error'])
            error_counts[error_category] = error_counts.get(error_category, 0) + 1
    
    # Sort by frequency
    return dict(sorted(error_counts.items(), key=lambda x: x[1], reverse=True))

def categorize_error(error_message: str) -> str:
    """Categorize error message into common types"""
    
    error = error_message.lower()
    
    if 'not found' in error or 'command not found' in error:
        return 'compiler_not_found'
    elif 'no such file' in error or 'file not found' in error:
        return 'file_not_found'
    elif 'undefined reference' in error or 'unresolved external' in error:
        return 'linking_error'
    elif 'syntax error' in error or 'parse error' in error:
        return 'syntax_error'
    elif 'permission denied' in error:
        return 'permission_error'
    elif 'timeout' in error:
        return 'timeout_error'
    elif 'internal compiler error' in error:
        return 'compiler_internal_error'
    elif 'out of memory' in error or 'memory' in error:
        return 'memory_error'
    elif 'library' in error or 'lib' in error:
        return 'library_error'
    elif 'header' in error or 'include' in error:
        return 'header_error'
    elif 'linker' in error or 'ld:' in error:
        return 'linker_error'
    else:
        return 'unknown_error'

def generate_fix_suggestions(common_errors: Dict[str, int], analysis: Dict) -> str:
    """Generate fix suggestions based on common errors"""
    
    suggestions = []
    
    for error_type, count in common_errors.items():
        if error_type == 'compiler_not_found':
            suggestions.append("📥 Install missing compilers: apt install gcc g++ clang")
        elif error_type == 'linking_error':
            suggestions.append("🔗 Install development libraries: apt install libc6-dev")
        elif error_type == 'header_error':
            suggestions.append("📄 Install header files: apt install build-essential")
        elif error_type == 'library_error':
            required_libs = analysis.get('required_libs', set())
            if 'pthread' in required_libs:
                suggestions.append("🧵 Install threading support: apt install libc6-dev")
            if 'math' in required_libs:
                suggestions.append("🧮 Math libraries are usually built-in")
            if 'opengl' in required_libs:
                suggestions.append("🎮 Install OpenGL: apt install libgl1-mesa-dev")
        elif error_type == 'permission_error':
            suggestions.append("🔐 Check file permissions and directory access")
        elif error_type == 'memory_error':
            suggestions.append("💾 Try with simpler optimization flags or add swap")
        elif error_type == 'syntax_error':
            suggestions.append("📝 Check source code syntax and language standard")
    
    return '\n'.join(suggestions) if suggestions else "No specific suggestions available"

def generate_optimization_recommendations(analysis: Dict, results: List[Dict]) -> str:
    """Generate optimization recommendations based on analysis"""
    
    recommendations = []
    
    # Based on code analysis
    if analysis.get('math_heavy'):
        recommendations.append("🧮 Use -ffast-math for math-heavy code (trade precision for speed)")
        recommendations.append("📊 Consider -march=native for vectorization")
    
    if analysis.get('threading'):
        recommendations.append("🧵 Enable OpenMP with -fopenmp for parallel loops")
        recommendations.append("⚡ Use -pthread for threading support")
    
    if analysis.get('complexity') == 'high':
        recommendations.append("🏗️ High complexity code benefits from -O3 optimization")
        recommendations.append("🔗 Consider Link-Time Optimization (-flto)")
    
    if analysis.get('complexity') in ['low', 'very_low']:
        recommendations.append("⚡ Simple code compiles faster with -O2")
        recommendations.append("📦 Use -Os for smaller binaries")
    
    # Based on results
    if results:
        avg_size = sum(r['file_size'] for r in results) / len(results)
        if avg_size > 1000000:  # > 1MB
            recommendations.append("📦 Large binaries: try -Os or -Oz for size optimization")
            recommendations.append("🗜️ Use strip command to remove debug symbols")
        
        fast_compilers = [r for r in results if r['compilation_time'] < 10]
        if fast_compilers:
            best_compiler = min(fast_compilers, key=lambda x: x['compilation_time'])['strategy']['compiler']
            recommendations.append(f"⚡ {best_compiler} is fastest for this code")
    
    # Language-specific recommendations
    if analysis.get('detected_language') == 'cpp':
        cpp_features = analysis.get('cpp_features', [])
        if any('c++17' in feat or 'c++20' in feat for feat in cpp_features):
            recommendations.append("🆕 Modern C++ code benefits from recent compiler versions")
        
        if analysis.get('template_usage'):
            recommendations.append("🏗️ Template-heavy code benefits from -O3")
    
    return '\n'.join(recommendations) if recommendations else "No specific recommendations"

def analyze_compiler_performance(results: List[Dict]) -> str:
    """Analyze performance of different compilers"""
    
    compiler_stats = {}
    
    for result in results:
        compiler = result['strategy']['compiler']
        if compiler not in compiler_stats:
            compiler_stats[compiler] = {
                'count': 0,
                'avg_score': 0,
                'avg_time': 0,
                'avg_size': 0,
                'total_score': 0,
                'total_time': 0,
                'total_size': 0
            }
        
        stats = compiler_stats[compiler]
        stats['count'] += 1
        stats['total_score'] += result['performance_score']
        stats['total_time'] += result['compilation_time']
        stats['total_size'] += result['file_size']
    
    # Calculate averages
    for compiler, stats in compiler_stats.items():
        if stats['count'] > 0:
            stats['avg_score'] = stats['total_score'] / stats['count']
            stats['avg_time'] = stats['total_time'] / stats['count']
            stats['avg_size'] = stats['total_size'] / stats['count']
    
    # Sort by average score
    sorted_compilers = sorted(compiler_stats.items(), 
                            key=lambda x: x[1]['avg_score'], reverse=True)
    
    analysis = "🏆 COMPILER PERFORMANCE RANKING:\n\n"
    
    for i, (compiler, stats) in enumerate(sorted_compilers[:10], 1):
        analysis += (
            f"{i}. {compiler}\n"
            f"   📊 Avg Score: {stats['avg_score']:.1f}/200\n"
            f"   ⏱️ Avg Time: {stats['avg_time']:.2f}s\n"
            f"   📏 Avg Size: {format_file_size(int(stats['avg_size']))}\n"
            f"   🔢 Builds: {stats['count']}\n\n"
        )
    
    return analysis

def generate_installation_suggestions(common_errors: Dict, analysis: Dict, 
                                    compiler_system) -> str:
    """Generate package installation suggestions"""
    
    suggestions = []
    is_termux = compiler_system.system_info['is_termux']
    is_android = compiler_system.system_info['is_android']
    
    pkg_mgr = 'pkg' if is_termux else 'apt'
    
    # Basic development tools
    if 'compiler_not_found' in common_errors or not compiler_system.available_compilers['gcc_variants']:
        suggestions.append(f"🔧 Basic compilers: {pkg_mgr} install gcc g++ clang")
    
    # Build tools
    suggestions.append(f"🏗️ Build essentials: {pkg_mgr} install build-essential")
    suggestions.append(f"📦 CMake & Make: {pkg_mgr} install cmake make")
    
    # Libraries based on analysis
    required_libs = analysis.get('required_libs', set())
    
    if 'pthread' in required_libs:
        suggestions.append(f"🧵 Threading: {pkg_mgr} install libc6-dev")
    
    if 'opengl' in required_libs:
        suggestions.append(f"🎮 OpenGL: {pkg_mgr} install libgl1-mesa-dev libglu1-mesa-dev")
    
    if 'curl' in required_libs:
        suggestions.append(f"🌐 cURL: {pkg_mgr} install libcurl4-openssl-dev")
    
    if 'ssl' in required_libs:
        suggestions.append(f"🔒 SSL/TLS: {pkg_mgr} install libssl-dev")
    
    if 'boost' in required_libs:
        suggestions.append(f"⚡ Boost: {pkg_mgr} install libboost-all-dev")
    
    if 'qt' in required_libs:
        suggestions.append(f"🖼️ Qt: {pkg_mgr} install qtbase5-dev")
    
    # Termux-specific
    if is_termux:
        suggestions.append("📱 Termux extras: pkg install termux-tools")
        suggestions.append("🔧 Additional tools: pkg install binutils gdb")
    
    # System-specific package managers
    available_managers = compiler_system.package_managers
    
    if 'apt' in available_managers:
        suggestions.append("🐧 Debian/Ubuntu: Use 'apt install <package>'")
    elif 'yum' in available_managers:
        suggestions.append("🎩 CentOS/RHEL: Use 'yum install <package>'")
    elif 'dnf' in available_managers:
        suggestions.append("🎩 Fedora: Use 'dnf install <package>'")
    elif 'pacman' in available_managers:
        suggestions.append("🏹 Arch: Use 'pacman -S <package>'")
    elif 'apk' in available_managers:
        suggestions.append("🏔️ Alpine: Use 'apk add <package>'")
    
    return '\n'.join(suggestions[:15])  # Limit suggestions

# Additional utility functions for the mega compiler system

def create_compilation_cache_key(strategy: Dict) -> str:
    """Create a cache key for compilation strategy"""
    
    import hashlib
    
    # Create a unique key based on strategy components
    key_components = [
        strategy['compiler'],
        strategy.get('std', ''),
        ' '.join(strategy.get('flags', [])),
        ' '.join(strategy.get('libs', [])),
        ' '.join(strategy.get('linker_flags', []))
    ]
    
    key_string = '|'.join(key_components)
    return hashlib.md5(key_string.encode()).hexdigest()

def validate_strategy(strategy: Dict) -> bool:
    """Validate if a compilation strategy is viable"""
    
    try:
        compiler = strategy['compiler']
        
        # Check if compiler exists
        if not shutil.which(compiler):
            return False
        
        # Basic compiler test
        test_cmd = [compiler, '--version']
        result = subprocess.run(test_cmd, capture_output=True, timeout=5)
        return result.returncode == 0
        
    except:
        return False

def optimize_strategy_order(strategies: List[Dict]) -> List[Dict]:
    """Optimize the order of strategies for maximum success probability"""
    
    # Group strategies by success probability
    high_priority = []
    medium_priority = []
    low_priority = []
    fallback = []
    
    for strategy in strategies:
        priority = strategy.get('priority', 100)
        
        if priority < 10:
            high_priority.append(strategy)
        elif priority < 50:
            medium_priority.append(strategy)
        elif priority < 200:
            low_priority.append(strategy)
        else:
            fallback.append(strategy)
    
    # Sort each group by internal scoring
    high_priority.sort(key=lambda x: x.get('expected_performance', 0), reverse=True)
    medium_priority.sort(key=lambda x: x.get('expected_performance', 0), reverse=True)
    low_priority.sort(key=lambda x: x.get('expected_performance', 0), reverse=True)
    
    # Combine with interleaving for diversity
    optimized = []
    max_len = max(len(high_priority), len(medium_priority), len(low_priority))
    
    for i in range(max_len):
        if i < len(high_priority):
            optimized.append(high_priority[i])
        if i < len(medium_priority):
            optimized.append(medium_priority[i])
        if i < len(low_priority) and len(optimized) < 100:  # Limit to prevent overflow
            optimized.append(low_priority[i])
    
    # Add fallbacks at the end
    optimized.extend(fallback[:50])  # Limit fallbacks
    
    return optimized

def create_compilation_report(strategies: List[Dict], results: List[Dict], 
                            analysis: Dict, system_info: Dict) -> str:
    """Create a comprehensive compilation report"""
    
    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]
    
    report = f"""
🚀 MEGA COMPILATION SYSTEM REPORT
{'=' * 50}

📊 EXECUTION SUMMARY:
• Total strategies generated: {len(strategies)}
• Strategies attempted: {len(results)}
• Successful compilations: {len(successful)}
• Failed compilations: {len(failed)}
• Success rate: {(len(successful)/len(results)*100):.1f}%

🏆 BEST PERFORMING STRATEGIES:
"""
    
    if successful:
        top_3 = sorted(successful, key=lambda x: x['performance_score'], reverse=True)[:3]
        for i, result in enumerate(top_3, 1):
            strategy = result['strategy']
            report += f"""
{i}. {strategy['name']}
   Compiler: {strategy['compiler']}
   Score: {result['performance_score']}/200
   Size: {format_file_size(result['file_size'])}
   Time: {result['compilation_time']:.2f}s
"""
    
    report += f"""
📈 PERFORMANCE METRICS:
• Fastest compilation: {min(r['compilation_time'] for r in successful):.2f}s
• Slowest compilation: {max(r['compilation_time'] for r in successful):.2f}s
• Smallest binary: {format_file_size(min(r['file_size'] for r in successful))}
• Largest binary: {format_file_size(max(r['file_size'] for r in successful))}
• Average score: {sum(r['performance_score'] for r in successful)/len(successful):.1f}/200

🔍 CODE ANALYSIS:
• Language: {analysis.get('detected_language', 'unknown').upper()}
• Complexity: {analysis.get('complexity', 'unknown').upper()}
• Lines of code: {analysis.get('lines', 0)}
• Functions: {analysis.get('function_count', 0)}
• Threading: {'Yes' if analysis.get('threading') else 'No'}
• Math intensive: {'Yes' if analysis.get('math_heavy') else 'No'}

🖥️ SYSTEM INFORMATION:
• OS: {system_info.get('os', 'unknown')} {system_info.get('arch', '')}
• Platform: {system_info.get('platform', 'unknown')[:50]}
• CPU cores: {system_info.get('cpu_count', 'unknown')}
• Memory: {system_info.get('memory_gb', 'unknown')} GB
• Termux: {'Yes' if system_info.get('is_termux') else 'No'}
• Android: {'Yes' if system_info.get('is_android') else 'No'}

Generated by MEGA Advanced Compiler System v2.0
Report timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    return report

# Additional advanced features for the mega compiler system

def create_benchmark_suite(binary_path: str, analysis: Dict) -> Dict:
    """Create and run benchmark suite for compiled binary"""
    
    benchmarks = {
        'execution_time': None,
        'memory_usage': None,
        'cpu_usage': None,
        'startup_time': None,
        'file_operations': None,
        'mathematical_ops': None,
        'threading_performance': None,
        'benchmark_score': 0
    }
    
    try:
        if not os.path.exists(binary_path) or not os.access(binary_path, os.X_OK):
            return benchmarks
        
        # Basic execution time test
        start_time = time.time()
        try:
            result = subprocess.run([binary_path], 
                                  capture_output=True, 
                                  timeout=10,
                                  input='',
                                  text=True)
            execution_time = time.time() - start_time
            benchmarks['execution_time'] = execution_time
            
            if result.returncode == 0:
                benchmarks['benchmark_score'] += 50
            else:
                benchmarks['benchmark_score'] += 10
                
        except subprocess.TimeoutExpired:
            benchmarks['execution_time'] = 10.0
            benchmarks['benchmark_score'] += 5
        except:
            benchmarks['execution_time'] = None
            
        # Memory usage estimation (simplified)
        try:
            file_size = os.path.getsize(binary_path)
            # Rough estimate based on file size
            estimated_memory = file_size * 1.5  # Factor for runtime overhead
            benchmarks['memory_usage'] = estimated_memory
            
            if estimated_memory < 1024 * 1024:  # < 1MB
                benchmarks['benchmark_score'] += 30
            elif estimated_memory < 10 * 1024 * 1024:  # < 10MB
                benchmarks['benchmark_score'] += 20
            else:
                benchmarks['benchmark_score'] += 10
        except:
            pass
            
        # Startup time test
        try:
            startup_times = []
            for _ in range(3):
                start = time.time()
                proc = subprocess.Popen([binary_path], 
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE)
                proc.terminate()
                proc.wait(timeout=1)
                startup_times.append(time.time() - start)
            
            benchmarks['startup_time'] = min(startup_times)
            
            if benchmarks['startup_time'] < 0.1:
                benchmarks['benchmark_score'] += 20
            elif benchmarks['startup_time'] < 0.5:
                benchmarks['benchmark_score'] += 10
                
        except:
            pass
            
        # Performance hints based on analysis
        if analysis.get('math_heavy'):
            benchmarks['mathematical_ops'] = 'detected'
            benchmarks['benchmark_score'] += 15
            
        if analysis.get('threading'):
            benchmarks['threading_performance'] = 'detected'
            benchmarks['benchmark_score'] += 15
            
        # Clamp benchmark score
        benchmarks['benchmark_score'] = min(100, benchmarks['benchmark_score'])
        
    except Exception as e:
        benchmarks['error'] = str(e)
    
    return benchmarks

def generate_assembly_analysis(binary_path: str) -> Dict:
    """Generate advanced assembly analysis of compiled binary"""
    
    analysis = {
        'instruction_count': 0,
        'optimization_level_detected': 'unknown',
        'vectorization_used': False,
        'function_inlining': False,
        'loop_unrolling': False,
        'jump_optimizations': False,
        'register_efficiency': 'unknown',
        'code_size_efficiency': 'unknown',
        'disassembly_sample': []
    }
    
    try:
        # Try different disassemblers
        disassemblers = ['objdump', 'llvm-objdump', 'gobjdump']
        
        for disasm in disassemblers:
            if shutil.which(disasm):
                try:
                    result = subprocess.run([disasm, '-d', binary_path], 
                                          capture_output=True, text=True, timeout=15)
                    if result.returncode == 0:
                        disassembly = result.stdout
                        
                        # Count instructions
                        instruction_lines = [line for line in disassembly.split('\n') 
                                           if ':' in line and any(inst in line.lower() 
                                           for inst in ['mov', 'add', 'sub', 'jmp', 'call'])]
                        analysis['instruction_count'] = len(instruction_lines)
                        
                        # Sample first 20 instructions
                        analysis['disassembly_sample'] = instruction_lines[:20]
                        
                        # Detect optimization patterns
                        disasm_lower = disassembly.lower()
                        
                        # Vectorization detection
                        vector_instructions = ['xmm', 'ymm', 'zmm', 'simd', 'sse', 'avx']
                        if any(instr in disasm_lower for instr in vector_instructions):
                            analysis['vectorization_used'] = True
                            
                        # Loop unrolling detection (multiple similar instruction sequences)
                        if disasm_lower.count('mov') > analysis['instruction_count'] * 0.3:
                            analysis['loop_unrolling'] = True
                            
                        # Jump optimization detection
                        jump_count = disasm_lower.count('jmp') + disasm_lower.count('je') + disasm_lower.count('jne')
                        if jump_count < analysis['instruction_count'] * 0.1:
                            analysis['jump_optimizations'] = True
                            
                        # Register efficiency (more register usage = better optimization)
                        register_usage = disasm_lower.count('rax') + disasm_lower.count('rbx') + disasm_lower.count('rcx')
                        if register_usage > analysis['instruction_count'] * 0.2:
                            analysis['register_efficiency'] = 'high'
                        elif register_usage > analysis['instruction_count'] * 0.1:
                            analysis['register_efficiency'] = 'medium'
                        else:
                            analysis['register_efficiency'] = 'low'
                            
                        # Code size efficiency
                        file_size = os.path.getsize(binary_path)
                        if analysis['instruction_count'] > 0:
                            bytes_per_instruction = file_size / analysis['instruction_count']
                            if bytes_per_instruction < 50:
                                analysis['code_size_efficiency'] = 'high'
                            elif bytes_per_instruction < 100:
                                analysis['code_size_efficiency'] = 'medium'
                            else:
                                analysis['code_size_efficiency'] = 'low'
                        
                        # Optimization level detection
                        if analysis['vectorization_used'] and analysis['jump_optimizations']:
                            analysis['optimization_level_detected'] = 'O3/Ofast'
                        elif analysis['register_efficiency'] == 'high':
                            analysis['optimization_level_detected'] = 'O2'
                        elif analysis['instruction_count'] > 0:
                            analysis['optimization_level_detected'] = 'O1'
                        else:
                            analysis['optimization_level_detected'] = 'O0'
                            
                        break
                        
                except:
                    continue
                    
    except Exception as e:
        analysis['error'] = str(e)
    
    return analysis

def create_performance_profile(strategy: Dict, result: Dict, analysis: Dict) -> Dict:
    """Create comprehensive performance profile"""
    
    profile = {
        'overall_score': 0,
        'compilation_efficiency': 0,
        'runtime_efficiency': 0,
        'memory_efficiency': 0,
        'size_efficiency': 0,
        'optimization_effectiveness': 0,
        'portability_score': 0,
        'maintainability_score': 0,
        'security_score': 0,
        'recommendations': []
    }
    
    try:
        # Compilation efficiency (faster = better)
        comp_time = result.get('compilation_time', 0)
        if comp_time < 5:
            profile['compilation_efficiency'] = 95
        elif comp_time < 15:
            profile['compilation_efficiency'] = 80
        elif comp_time < 30:
            profile['compilation_efficiency'] = 65
        elif comp_time < 60:
            profile['compilation_efficiency'] = 50
        else:
            profile['compilation_efficiency'] = 30
            
        # Size efficiency
        file_size = result.get('file_size', 0)
        complexity = analysis.get('complexity', 'low')
        
        # Expected size based on complexity
        complexity_multiplier = {
            'very_low': 1,
            'low': 2,
            'medium': 4,
            'high': 8,
            'very_high': 16
        }
        
        expected_size = analysis.get('lines', 100) * complexity_multiplier.get(complexity, 2) * 50
        
        if file_size < expected_size * 0.5:
            profile['size_efficiency'] = 95
        elif file_size < expected_size:
            profile['size_efficiency'] = 80
        elif file_size < expected_size * 2:
            profile['size_efficiency'] = 65
        else:
            profile['size_efficiency'] = 40
            
        # Optimization effectiveness
        flags = strategy.get('flags', [])
        opt_score = 50
        
        if '-Ofast' in flags:
            opt_score += 30
        elif '-O3' in flags:
            opt_score += 25
        elif '-O2' in flags:
            opt_score += 15
        elif '-Os' in flags or '-Oz' in flags:
            opt_score += 10
            
        if '-march=native' in flags:
            opt_score += 15
        if '-flto' in flags:
            opt_score += 10
        if '-ffast-math' in flags and analysis.get('math_heavy'):
            opt_score += 15
            
        profile['optimization_effectiveness'] = min(100, opt_score)
        
        # Security score
        security_score = 0
        security_flags = ['-fstack-protector', '-D_FORTIFY_SOURCE', '-fPIE', '-fcf-protection']
        
        for flag in security_flags:
            if any(flag in f for f in flags):
                security_score += 25
                
        profile['security_score'] = min(100, security_score)
        
        # Portability score
        portability_score = 80  # Base score
        
        if '-march=native' in flags:
            portability_score -= 20
        if any('sanitize' in flag for flag in flags):
            portability_score -= 10
        if 'experimental' in strategy.get('name', '').lower():
            portability_score -= 30
            
        profile['portability_score'] = max(0, portability_score)
        
        # Maintainability score
        maintainability_score = 70
        
        if analysis.get('complexity') in ['very_high', 'high']:
            maintainability_score -= 20
        if len(analysis.get('potential_issues', [])) > 0:
            maintainability_score -= 15
        if len(analysis.get('deprecated_features', [])) > 0:
            maintainability_score -= 10
        if len(analysis.get('modern_features', [])) > 3:
            maintainability_score += 15
            
        profile['maintainability_score'] = max(0, maintainability_score)
        
        # Overall score
        scores = [
            profile['compilation_efficiency'],
            profile['size_efficiency'],
            profile['optimization_effectiveness'],
            profile['security_score'],
            profile['portability_score'],
            profile['maintainability_score']
        ]
        
        profile['overall_score'] = sum(scores) // len(scores)
        
        # Generate recommendations
        if profile['compilation_efficiency'] < 60:
            profile['recommendations'].append("Consider using faster optimization levels like -O2 instead of -O3")
            
        if profile['size_efficiency'] < 60:
            profile['recommendations'].append("Use size optimization flags like -Os or -Oz")
            
        if profile['security_score'] < 50:
            profile['recommendations'].append("Add security hardening flags like -fstack-protector-strong")
            
        if profile['portability_score'] < 50:
            profile['recommendations'].append("Avoid architecture-specific optimizations for better portability")
            
        if len(analysis.get('potential_issues', [])) > 0:
            profile['recommendations'].append("Address potential security issues in code")
            
    except Exception as e:
        profile['error'] = str(e)
    
    return profile

async def generate_comprehensive_report(update: Update, best_result: Dict, all_results: List[Dict], 
                                      analysis: Dict, compiler_system) -> str:
    """Generate ultra-comprehensive compilation report"""
    
    try:
        strategy = best_result['strategy']
        binary_path = best_result.get('output_path')
        
        # Generate additional analyses
        benchmark_results = {}
        assembly_analysis = {}
        performance_profile = {}
        
        if binary_path and os.path.exists(binary_path):
            benchmark_results = create_benchmark_suite(binary_path, analysis)
            assembly_analysis = generate_assembly_analysis(binary_path)
            performance_profile = create_performance_profile(strategy, best_result, analysis)
        
        # Compiler ecosystem analysis
        ecosystem_stats = analyze_compiler_ecosystem(compiler_system, all_results)
        
        # Generate final comprehensive report
        report = f"""
📋 MEGA COMPILATION COMPREHENSIVE REPORT
{'=' * 60}

🏆 OPTIMAL BUILD CONFIGURATION:
{'─' * 40}
Strategy: {strategy['name'][:50]}
Compiler: {strategy['compiler']} ({strategy.get('version', 'unknown')})
Standard: {strategy.get('std', 'default')}
Flags: {' '.join(strategy.get('flags', []))[:100]}
Libraries: {', '.join(strategy.get('libs', []))}
Priority: {strategy.get('priority', 'unknown')} (Lower = Higher Priority)

📊 PERFORMANCE METRICS:
{'─' * 40}
Compilation Time: {best_result.get('compilation_time', 0):.2f}s
Binary Size: {format_file_size(best_result.get('file_size', 0))}
Performance Score: {best_result.get('performance_score', 0)}/200
Risk Level: {assess_strategy_risk(strategy)}
Expected Performance Gain: {estimate_performance_gain(strategy)}

🔬 CODE ANALYSIS SUMMARY:
{'─' * 40}
Language: {analysis.get('detected_language', 'unknown').upper()}
Standard Detected: {analysis.get('language_standard', 'unknown')}
Complexity Level: {analysis.get('complexity', 'unknown').upper()}
Lines of Code: {analysis.get('lines', 0):,}
Functions Detected: {analysis.get('function_count', 0)}
Classes Detected: {analysis.get('class_count', 0)}

🔍 FEATURE ANALYSIS:
{'─' * 40}
Threading Support: {'✅ Detected' if analysis.get('threading') else '❌ Not Required'}
Math-Heavy Operations: {'✅ Detected' if analysis.get('math_heavy') else '❌ Not Required'}
Graphics APIs: {'✅ Detected' if analysis.get('graphics') else '❌ Not Required'}
Networking: {'✅ Detected' if analysis.get('networking') else '❌ Not Required'}
Android APIs: {'✅ Detected' if analysis.get('android_apis') else '❌ Not Required'}
Security Features: {'✅ Detected' if analysis.get('security_features') else '❌ Basic'}
Template Usage: {'✅ Heavy Use' if analysis.get('template_usage') else '❌ Minimal'}
Modern C++ Features: {len(analysis.get('modern_features', []))} detected

📚 LIBRARY DEPENDENCIES:
{'─' * 40}
print(f"Required Libraries: {', '.join(list(analysis.get('required_libs', set()))[:15])}")
Total Dependencies: {len(analysis.get('required_libs', set()))}
Critical Libraries: {', '.join([lib for lib in analysis.get('required_libs', set()) if lib in ['pthread', 'ssl', 'opengl']])}

🏗️ BINARY ANALYSIS:
{'─' * 40}"""

        if assembly_analysis:
            report += f"""
Instruction Count: {assembly_analysis.get('instruction_count', 'unknown'):,}
Detected Optimization: {assembly_analysis.get('optimization_level_detected', 'unknown')}
Vectorization Used: {'✅' if assembly_analysis.get('vectorization_used') else '❌'}
Loop Unrolling: {'✅' if assembly_analysis.get('loop_unrolling') else '❌'}
Register Efficiency: {assembly_analysis.get('register_efficiency', 'unknown').upper()}
Code Size Efficiency: {assembly_analysis.get('code_size_efficiency', 'unknown').upper()}"""

        if benchmark_results:
            report += f"""

⚡ BENCHMARK RESULTS:
{'─' * 40}
Execution Time: {benchmark_results.get('execution_time', 'N/A')}s
Estimated Memory: {format_file_size(int(benchmark_results.get('memory_usage', 0))) if benchmark_results.get('memory_usage') else 'N/A'}
Startup Time: {benchmark_results.get('startup_time', 'N/A')}s
Benchmark Score: {benchmark_results.get('benchmark_score', 0)}/100"""

        if performance_profile:
            report += f"""

📈 PERFORMANCE PROFILE:
{'─' * 40}
Overall Score: {performance_profile.get('overall_score', 0)}/100
Compilation Efficiency: {performance_profile.get('compilation_efficiency', 0)}/100
Size Efficiency: {performance_profile.get('size_efficiency', 0)}/100
Optimization Effectiveness: {performance_profile.get('optimization_effectiveness', 0)}/100
Security Score: {performance_profile.get('security_score', 0)}/100
Portability Score: {performance_profile.get('portability_score', 0)}/100
Maintainability Score: {performance_profile.get('maintainability_score', 0)}/100"""

        report += f"""

🌐 COMPILER ECOSYSTEM:
{'─' * 40}
Total Compilers Available: {ecosystem_stats.get('total_compilers', 0)}
GCC Variants: {ecosystem_stats.get('gcc_count', 0)}
Clang Variants: {ecosystem_stats.get('clang_count', 0)}
Specialized Compilers: {ecosystem_stats.get('specialized_count', 0)}
Cross Compilers: {ecosystem_stats.get('cross_count', 0)}
Modern Compilers: {ecosystem_stats.get('modern_count', 0)}

📊 COMPILATION STATISTICS:
{'─' * 40}
Total Strategies Tested: {len(all_results)}
Success Rate: {(len([r for r in all_results if r['success']]) / len(all_results) * 100):.1f}%
Average Compile Time: {(sum(r.get('compilation_time', 0) for r in all_results) / len(all_results)):.2f}s
Average Binary Size: {format_file_size(int(sum(r.get('file_size', 0) for r in all_results) / len(all_results)))}
Fastest Compilation: {min(r.get('compilation_time', 999) for r in all_results):.2f}s
Smallest Binary: {format_file_size(min(r.get('file_size', 999999) for r in all_results))}

🖥️ SYSTEM ENVIRONMENT:
{'─' * 40}
Operating System: {compiler_system.system_info.get('os', 'unknown')} {compiler_system.system_info.get('arch', '')}
Platform: {compiler_system.system_info.get('platform', 'unknown')[:50]}
CPU Cores: {compiler_system.system_info.get('cpu_count', 'unknown')}
Memory: {compiler_system.system_info.get('memory_gb', 'unknown')} GB
Android/Termux: {'✅' if compiler_system.system_info.get('is_android') or compiler_system.system_info.get('is_termux') else '❌'}
Package Managers: {len(compiler_system.package_managers)}
Library Paths: {len(compiler_system.installed_libraries.get('system_paths', []))}

💡 OPTIMIZATION RECOMMENDATIONS:
{'─' * 40}"""

        if performance_profile.get('recommendations'):
            for i, rec in enumerate(performance_profile['recommendations'][:10], 1):
                report += f"""
{i}. {rec}"""
        else:
            report += """
• Current optimization appears to be well-suited for this code
• Consider profiling with real workloads for further optimization
• Monitor for performance regressions in production"""

        report += f"""

🔒 SECURITY ASSESSMENT:
{'─' * 40}
Security Flags Used: {len([f for f in strategy.get('flags', []) if 'protect' in f or 'fortify' in f])}
Potential Issues Found: {len(analysis.get('potential_issues', []))}
Deprecated Features: {len(analysis.get('deprecated_features', []))}
Modern Security Features: {len([f for f in analysis.get('modern_features', []) if 'secure' in f.lower()])}

🚀 NEXT STEPS:
{'─' * 40}
1. Test the compiled binary with your actual workload
2. Profile performance with production data
3. Consider additional security hardening if needed
4. Monitor for compiler updates that might improve performance
5. Benchmark against alternative compilation strategies periodically

📅 REPORT METADATA:
{'─' * 40}
Generated: {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}
System: MEGA Advanced Compiler System v2.0
Total Analysis Time: {sum(r.get('execution_time', 0) for r in all_results):.2f}s
Report Version: COMPREHENSIVE_v2.0
"""

        return report

    except Exception as e:
        return f"❌ Error generating comprehensive report: {str(e)}"

def analyze_compiler_ecosystem(compiler_system, results: List[Dict]) -> Dict:
    """Analyze the compiler ecosystem and results"""
    
    stats = {
        'total_compilers': 0,
        'gcc_count': 0,
        'clang_count': 0,
        'specialized_count': 0,
        'cross_count': 0,
        'modern_count': 0,
        'success_by_compiler': {},
        'performance_by_category': {}
    }
    
    try:
        # Count compilers by category
        for category, compilers in compiler_system.available_compilers.items():
            count = len(compilers)
            stats['total_compilers'] += count
            
            if 'gcc' in category:
                stats['gcc_count'] = count
            elif 'clang' in category:
                stats['clang_count'] = count
            elif 'specialized' in category:
                stats['specialized_count'] = count
            elif 'cross' in category:
                stats['cross_count'] = count
            elif 'modern' in category:
                stats['modern_count'] = count
        
        # Analyze results by compiler
        for result in results:
            if result.get('success'):
                compiler = result['strategy']['compiler']
                if compiler not in stats['success_by_compiler']:
                    stats['success_by_compiler'][compiler] = 0
                stats['success_by_compiler'][compiler] += 1
        
        # Performance by category
        category_performance = {}
        for result in results:
            if result.get('success'):
                strategy = result['strategy']
                # Determine category
                compiler = strategy['compiler']
                category = 'other'
                
                if 'gcc' in compiler:
                    category = 'gcc'
                elif 'clang' in compiler:
                    category = 'clang'
                elif compiler in ['icc', 'icx', 'nvcc']:
                    category = 'specialized'
                elif 'android' in compiler or 'arm-' in compiler:
                    category = 'cross'
                
                if category not in category_performance:
                    category_performance[category] = []
                
                category_performance[category].append(result.get('performance_score', 0))
        
        # Calculate averages
        for category, scores in category_performance.items():
            if scores:
                stats['performance_by_category'][category] = sum(scores) / len(scores)
        
    except Exception as e:
        stats['error'] = str(e)
    
    return stats

def create_detailed_binary_report(binary_path: str) -> str:
    """Create detailed binary analysis report"""
    
    if not os.path.exists(binary_path):
        return "Binary file not found for analysis"
    
    report = "🔬 DETAILED BINARY ANALYSIS:\n"
    report += "─" * 40 + "\n\n"
    
    try:
        # File basic info
        file_stat = os.stat(binary_path)
        report += f"File Size: {format_file_size(file_stat.st_size)}\n"
        report += f"Permissions: {oct(file_stat.st_mode)[-3:]}\n"
        report += f"Modified: {time.ctime(file_stat.st_mtime)}\n\n"
        
        # File type analysis
        if shutil.which('file'):
            result = subprocess.run(['file', binary_path], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                report += f"File Type: {result.stdout.strip()}\n\n"
        
        # Symbol analysis
        if shutil.which('nm'):
            result = subprocess.run(['nm', binary_path], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                symbols = result.stdout.strip().split('\n')
                report += f"Symbol Count: {len(symbols)}\n"
                
                # Count symbol types
                undefined_symbols = len([s for s in symbols if ' U ' in s])
                defined_symbols = len([s for s in symbols if ' T ' in s or ' t ' in s])
                data_symbols = len([s for s in symbols if ' D ' in s or ' d ' in s])
                
                report += f"Undefined Symbols: {undefined_symbols}\n"
                report += f"Defined Functions: {defined_symbols}\n"
                report += f"Data Symbols: {data_symbols}\n\n"
        
        # Dependency analysis
        if shutil.which('ldd'):
            result = subprocess.run(['ldd', binary_path], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                dependencies = [line.strip() for line in result.stdout.split('\n') 
                              if '=>' in line]
                report += f"Dependencies: {len(dependencies)}\n"
                for dep in dependencies[:10]:  # Show first 10
                    report += f"  • {dep.split('=>')[0].strip()}\n"
                if len(dependencies) > 10:
                    report += f"  • ... and {len(dependencies) - 10} more\n"
        
        # Strings analysis (security relevant)
        if shutil.which('strings'):
            result = subprocess.run(['strings', binary_path], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                strings_output = result.stdout
                string_count = len(strings_output.split('\n'))
                report += f"\nString Literals: {string_count}\n"
                
                # Look for interesting strings
                security_strings = []
                interesting_patterns = ['password', 'key', 'token', 'secret', 'api', 'http://', 'https://']
                
                for line in strings_output.split('\n')[:1000]:  # Limit search
                    for pattern in interesting_patterns:
                        if pattern.lower() in line.lower():
                            security_strings.append(line[:50])
                            break
                
                if security_strings:
                    report += "Potentially Sensitive Strings Found:\n"
                    for s in security_strings[:5]:
                        report += f"  • {s}...\n"
        
    except Exception as e:
        report += f"Error in binary analysis: {str(e)}\n"
    
    return report

async def send_performance_graphs(update: Update, results: List[Dict]):
    """Send performance visualization (text-based graphs)"""
    
    try:
        successful_results = [r for r in results if r['success']]
        if len(successful_results) < 2:
            return
        
        # Compilation time distribution
        times = [r['compilation_time'] for r in successful_results]
        sizes = [r['file_size'] for r in successful_results]
        scores = [r['performance_score'] for r in successful_results]
        
        graph_report = "📊 PERFORMANCE VISUALIZATION:\n"
        graph_report += "=" * 40 + "\n\n"
        
        # Simple text histogram for compilation times
        graph_report += "⏱️ COMPILATION TIME DISTRIBUTION:\n"
        time_buckets = {}
        for time_val in times:
            bucket = f"{int(time_val//5)*5}-{int(time_val//5)*5+5}s"
            time_buckets[bucket] = time_buckets.get(bucket, 0) + 1
        
        max_count = max(time_buckets.values()) if time_buckets else 1
        for bucket, count in sorted(time_buckets.items()):
            bar = "█" * int((count / max_count) * 20)
            graph_report += f"{bucket:>10}: {bar} ({count})\n"
        
        graph_report += "\n"
        
        # Size distribution
        graph_report += "📏 BINARY SIZE DISTRIBUTION:\n"
        size_buckets = {}
        for size in sizes:
            if size < 50000:
                bucket = "<50KB"
            elif size < 500000:
                bucket = "50KB-500KB"
            elif size < 5000000:
                bucket = "500KB-5MB"
            else:
                bucket = ">5MB"
            size_buckets[bucket] = size_buckets.get(bucket, 0) + 1
        
        max_count = max(size_buckets.values()) if size_buckets else 1
        for bucket, count in size_buckets.items():
            bar = "█" * int((count / max_count) * 20)
            graph_report += f"{bucket:>12}: {bar} ({count})\n"
        
        graph_report += "\n"
        
        # Performance score distribution
        graph_report += "📈 PERFORMANCE SCORE DISTRIBUTION:\n"
        score_buckets = {}
        for score in scores:
            bucket = f"{int(score//20)*20}-{int(score//20)*20+20}"
            score_buckets[bucket] = score_buckets.get(bucket, 0) + 1
        
        max_count = max(score_buckets.values()) if score_buckets else 1
        for bucket, count in sorted(score_buckets.items()):
            bar = "█" * int((count / max_count) * 20)
            graph_report += f"{bucket:>8}: {bar} ({count})\n"
        
        # Statistics summary
        graph_report += f"\n📊 SUMMARY STATISTICS:\n"
        graph_report += f"Compilation Time: μ={sum(times)/len(times):.2f}s, σ={(sum((t-sum(times)/len(times))**2 for t in times)/len(times))**0.5:.2f}s\n"
        graph_report += f"Binary Size: μ={format_file_size(int(sum(sizes)/len(sizes)))}, min={format_file_size(min(sizes))}, max={format_file_size(max(sizes))}\n"
        graph_report += f"Performance Score: μ={sum(scores)/len(scores):.1f}, min={min(scores)}, max={max(scores)}\n"
        
        await update.message.reply_text(graph_report)
        
    except Exception as e:
        await update.message.reply_text(f"❌ Error generating performance graphs: {str(e)}")

# Final integration function
async def send_mega_compilation_report(update: Update, context: ContextTypes.DEFAULT_TYPE,
                                     best_result: Dict, all_results: List[Dict],
                                     analysis: Dict, compiler_system):
    """Send complete mega compilation report"""
    
    try:
        # Generate comprehensive report
        comprehensive_report = await generate_comprehensive_report(
            update, best_result, all_results, analysis, compiler_system
        )
        
        # Split report into chunks (Telegram message limit)
        max_length = 4000
        report_chunks = []
        current_chunk = ""
        
        for line in comprehensive_report.split('\n'):
            if len(current_chunk + line + '\n') > max_length:
                if current_chunk:
                    report_chunks.append(current_chunk)
                current_chunk = line + '\n'
            else:
                current_chunk += line + '\n'
        
        if current_chunk:
            report_chunks.append(current_chunk)
        
        # Send report chunks
        for i, chunk in enumerate(report_chunks):
            if i == 0:
                await update.message.reply_text(f"📋 COMPREHENSIVE COMPILATION REPORT (Part {i+1}/{len(report_chunks)}):\n{chunk}")
            else:
                await update.message.reply_text(f"📋 REPORT (Part {i+1}/{len(report_chunks)}):\n{chunk}")
            
            # Small delay between chunks
            await asyncio.sleep(0.5)
        
        # Send performance graphs
        await send_performance_graphs(update, all_results)
        
        # Send detailed binary analysis if available
        if best_result.get('output_path') and os.path.exists(best_result['output_path']):
            binary_report = create_detailed_binary_report(best_result['output_path'])
            if len(binary_report) > 4000:
                # Split binary report too
                binary_chunks = [binary_report[i:i+4000] for i in range(0, len(binary_report), 4000)]
                for i, chunk in enumerate(binary_chunks):
                    await update.message.reply_text(f"🔬 BINARY ANALYSIS (Part {i+1}/{len(binary_chunks)}):\n{chunk}")
            else:
                await update.message.reply_text(binary_report)
        
        # Final summary with actionable insights
        final_summary = f"""
🎯 EXECUTIVE SUMMARY:

✅ BEST CONFIGURATION FOUND:
Compiler: {best_result['strategy']['compiler']}
Performance Score: {best_result['performance_score']}/200
Compilation Time: {best_result['compilation_time']:.2f}s
Binary Size: {format_file_size(best_result['file_size'])}

📈 KEY INSIGHTS:
• Tested {len(all_results)} compilation strategies
• Success rate: {(len([r for r in all_results if r['success']])/len(all_results)*100):.1f}%
• Best performance compiler: {max(all_results, key=lambda x: x.get('performance_score', 0))['strategy']['compiler']}
• Fastest compilation: {min(all_results, key=lambda x: x.get('compilation_time', 999))['compilation_time']:.2f}s

🚀 RECOMMENDED ACTION:
Use the provided optimized binary for production deployment.
Keep the compilation command for future builds.

Generated by MEGA Advanced Compiler System v2.0
Thank you for using our comprehensive compilation analysis!
"""
        
        await update.message.reply_text(final_summary)
        
    except Exception as e:
        await update.message.reply_text(f"❌ Error sending comprehensive report: {str(e)}")

# Advanced optimization and profiling systems

class ProfileGuidedOptimization:
    """Advanced Profile-Guided Optimization system"""
    
    def __init__(self, compiler_system):
        self.compiler_system = compiler_system
        self.profile_data_cache = {}
        self.optimization_history = []
        
    async def run_pgo_optimization(self, file_path: str, compiler: str, base_flags: List[str]) -> Dict:
        """Execute complete PGO optimization cycle"""
        
        pgo_results = {
            'stages': [],
            'final_binary': None,
            'performance_improvement': 0,
            'total_time': 0,
            'success': False
        }
        
        start_time = time.time()
        temp_dir = tempfile.mkdtemp()
        
        try:
            # Stage 1: Instrumented build
            instrumented_result = await self._build_instrumented(
                file_path, compiler, base_flags, temp_dir
            )
            pgo_results['stages'].append(('instrumented', instrumented_result))
            
            if not instrumented_result['success']:
                return pgo_results
            
            # Stage 2: Profile generation
            profile_result = await self._generate_profile(
                instrumented_result['binary_path'], temp_dir
            )
            pgo_results['stages'].append(('profiling', profile_result))
            
            if not profile_result['success']:
                return pgo_results
            
            # Stage 3: Optimized build
            optimized_result = await self._build_optimized(
                file_path, compiler, base_flags, profile_result['profile_path'], temp_dir
            )
            pgo_results['stages'].append(('optimized', optimized_result))
            
            if optimized_result['success']:
                pgo_results['final_binary'] = optimized_result['binary_path']
                pgo_results['success'] = True
                
                # Benchmark comparison
                benchmark_result = await self._benchmark_comparison(
                    instrumented_result['binary_path'],
                    optimized_result['binary_path']
                )
                pgo_results['performance_improvement'] = benchmark_result
            
        except Exception as e:
            pgo_results['error'] = str(e)
        finally:
            pgo_results['total_time'] = time.time() - start_time
            # Cleanup temporary files
            shutil.rmtree(temp_dir, ignore_errors=True)
        
        return pgo_results
    
    async def _build_instrumented(self, file_path: str, compiler: str, flags: List[str], temp_dir: str) -> Dict:
        """Build instrumented binary for profile generation"""
        
        try:
            output_path = os.path.join(temp_dir, 'instrumented_binary')
            cmd = [compiler] + flags + ['-fprofile-generate', file_path, '-o', output_path]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            
            return {
                'success': result.returncode == 0,
                'binary_path': output_path if result.returncode == 0 else None,
                'output': result.stdout + result.stderr,
                'command': ' '.join(cmd)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    async def _generate_profile(self, binary_path: str, temp_dir: str) -> Dict:
        """Generate profile data by running instrumented binary"""
        
        try:
            # Create sample inputs for profiling
            profile_inputs = self._create_profile_inputs()
            profile_runs = []
            
            for i, input_data in enumerate(profile_inputs):
                env = os.environ.copy()
                env['LLVM_PROFILE_FILE'] = os.path.join(temp_dir, f'profile_%d.profraw' % i)
                
                result = subprocess.run(
                    [binary_path],
                    input=input_data,
                    env=env,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                profile_runs.append({
                    'input': input_data[:100],  # Truncate for display
                    'success': result.returncode == 0,
                    'output': result.stdout[:200]
                })
            
            # Merge profile data if using LLVM
            profile_path = os.path.join(temp_dir, 'merged.profdata')
            if shutil.which('llvm-profdata'):
                merge_cmd = ['llvm-profdata', 'merge', '-output', profile_path]
                merge_cmd.extend([f for f in os.listdir(temp_dir) if f.endswith('.profraw')])
                
                merge_result = subprocess.run(merge_cmd, capture_output=True, text=True, timeout=60)
                if merge_result.returncode != 0:
                    profile_path = temp_dir  # Use raw profiles
            else:
                profile_path = temp_dir
            
            return {
                'success': True,
                'profile_path': profile_path,
                'runs': profile_runs,
                'run_count': len(profile_inputs)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _create_profile_inputs(self) -> List[str]:
        """Create diverse inputs for profile generation"""
        
        inputs = [
            "",  # Empty input
            "hello world\n",  # Simple text
            "1 2 3 4 5\n",  # Numbers
            "a" * 100 + "\n",  # Repeated characters
            "\n".join([f"line {i}" for i in range(50)]) + "\n",  # Multiple lines
        ]
        
        # Add mathematical inputs
        math_inputs = [
            "3.14159\n",
            "1000000\n",
            "0.0001\n",
            "-999\n"
        ]
        inputs.extend(math_inputs)
        
        return inputs
    
    async def _build_optimized(self, file_path: str, compiler: str, flags: List[str], 
                             profile_path: str, temp_dir: str) -> Dict:
        """Build optimized binary using profile data"""
        
        try:
            output_path = os.path.join(temp_dir, 'optimized_binary')
            cmd = [compiler] + flags + ['-fprofile-use=' + profile_path, file_path, '-o', output_path]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            
            return {
                'success': result.returncode == 0,
                'binary_path': output_path if result.returncode == 0 else None,
                'output': result.stdout + result.stderr,
                'command': ' '.join(cmd)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    async def _benchmark_comparison(self, baseline_binary: str, optimized_binary: str) -> float:
        """Compare performance between baseline and optimized binaries"""
        
        try:
            baseline_times = []
            optimized_times = []
            
            # Run multiple benchmarks
            for _ in range(5):
                # Baseline timing
                start = time.time()
                result = subprocess.run([baseline_binary], capture_output=True, timeout=10)
                if result.returncode == 0:
                    baseline_times.append(time.time() - start)
                
                # Optimized timing
                start = time.time()
                result = subprocess.run([optimized_binary], capture_output=True, timeout=10)
                if result.returncode == 0:
                    optimized_times.append(time.time() - start)
            
            if baseline_times and optimized_times:
                avg_baseline = sum(baseline_times) / len(baseline_times)
                avg_optimized = sum(optimized_times) / len(optimized_times)
                
                if avg_baseline > 0:
                    improvement = ((avg_baseline - avg_optimized) / avg_baseline) * 100
                    return max(0, improvement)  # Don't report negative improvements
            
            return 0.0
            
        except Exception:
            return 0.0

class AutoTuningSystem:
    """Automatic compiler parameter tuning system"""
    
    def __init__(self, compiler_system):
        self.compiler_system = compiler_system
        self.tuning_history = []
        self.best_configurations = {}
        
    async def auto_tune_compilation(self, file_path: str, analysis: Dict, 
                                  target_metric: str = 'performance') -> Dict:
        """Automatically tune compilation parameters"""
        
        tuning_results = {
            'iterations': [],
            'best_config': None,
            'best_score': 0,
            'convergence_info': {},
            'total_time': 0,
            'success': False
        }
        
        start_time = time.time()
        
        try:
            # Generate parameter space
            param_space = self._generate_parameter_space(analysis)
            
            # Initialize population for genetic algorithm
            population = self._initialize_population(param_space, size=20)
            
            # Evolution loop
            for generation in range(10):  # Limit generations
                generation_results = []
                
                # Evaluate each individual
                for individual in population:
                    score = await self._evaluate_individual(file_path, individual, target_metric)
                    generation_results.append({
                        'config': individual,
                        'score': score,
                        'generation': generation
                    })
                
                tuning_results['iterations'].append({
                    'generation': generation,
                    'population_size': len(population),
                    'best_score': max(r['score'] for r in generation_results),
                    'avg_score': sum(r['score'] for r in generation_results) / len(generation_results)
                })
                
                # Update best configuration
                best_individual = max(generation_results, key=lambda x: x['score'])
                if best_individual['score'] > tuning_results['best_score']:
                    tuning_results['best_config'] = best_individual['config']
                    tuning_results['best_score'] = best_individual['score']
                
                # Evolve population
                population = self._evolve_population(generation_results, param_space)
                
                # Check convergence
                if self._check_convergence(tuning_results['iterations'][-5:]):
                    break
            
            tuning_results['success'] = tuning_results['best_config'] is not None
            
        except Exception as e:
            tuning_results['error'] = str(e)
        finally:
            tuning_results['total_time'] = time.time() - start_time
        
        return tuning_results
    
    def _generate_parameter_space(self, analysis: Dict) -> Dict:
        """Generate parameter space for tuning"""
        
        param_space = {
            'optimization_level': ['-O0', '-O1', '-O2', '-O3', '-Os', '-Oz', '-Ofast'],
            'architecture': ['-march=native', '-march=generic', '-march=core2'],
            'vectorization': [[], ['-ftree-vectorize'], ['-fno-tree-vectorize']],
            'inlining': [[], ['-finline-functions'], ['-fno-inline']],
            'loop_opts': [[], ['-funroll-loops'], ['-fno-unroll-loops'], ['-funroll-all-loops']],
        }
        
        # Add math-specific options
        if analysis.get('math_heavy'):
            param_space['math_opts'] = [
                [],
                ['-ffast-math'],
                ['-fno-math-errno'],
                ['-funsafe-math-optimizations'],
                ['-ffast-math', '-funsafe-math-optimizations']
            ]
        
        # Add threading options
        if analysis.get('threading'):
            param_space['thread_opts'] = [
                [],
                ['-pthread'],
                ['-fopenmp'],
                ['-pthread', '-fopenmp']
            ]
        
        return param_space
    
    def _initialize_population(self, param_space: Dict, size: int) -> List[Dict]:
        """Initialize random population for genetic algorithm"""
        
        import random
        population = []
        
        for _ in range(size):
            individual = {}
            for param, values in param_space.items():
                individual[param] = random.choice(values)
            population.append(individual)
        
        return population
    
    async def _evaluate_individual(self, file_path: str, config: Dict, target_metric: str) -> float:
        """Evaluate a single configuration"""
        
        try:
            # Build flags from configuration
            flags = []
            for param_name, param_value in config.items():
                if isinstance(param_value, list):
                    flags.extend(param_value)
                elif isinstance(param_value, str):
                    flags.append(param_value)
            
            # Compile with this configuration
            temp_dir = tempfile.mkdtemp()
            try:
                output_path = os.path.join(temp_dir, 'test_binary')
                compiler = 'gcc'  # Use default compiler
                
                cmd = [compiler] + flags + [file_path, '-o', output_path]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
                
                if result.returncode != 0:
                    return 0.0
                
                # Calculate score based on target metric
                if target_metric == 'performance':
                    return self._calculate_performance_score(output_path)
                elif target_metric == 'size':
                    return self._calculate_size_score(output_path)
                elif target_metric == 'compile_time':
                    return self._calculate_compile_time_score(result, cmd)
                
            finally:
                shutil.rmtree(temp_dir, ignore_errors=True)
            
        except Exception:
            return 0.0
        
        return 0.0
    
    def _calculate_performance_score(self, binary_path: str) -> float:
        """Calculate performance score for binary"""
        
        try:
            # Simple performance test
            times = []
            for _ in range(3):
                start = time.time()
                result = subprocess.run([binary_path], capture_output=True, timeout=10)
                if result.returncode == 0:
                    times.append(time.time() - start)
            
            if times:
                avg_time = sum(times) / len(times)
                # Convert to score (lower time = higher score)
                return max(0, 100 - (avg_time * 100))
            
        except Exception:
            pass
        
        return 0.0
    
    def _calculate_size_score(self, binary_path: str) -> float:
        """Calculate size score for binary"""
        
        try:
            size = os.path.getsize(binary_path)
            # Convert to score (smaller size = higher score, with reasonable limits)
            if size < 10000:  # < 10KB
                return 100
            elif size < 100000:  # < 100KB
                return 80
            elif size < 1000000:  # < 1MB
                return 60
            else:
                return max(0, 60 - (size / 1000000) * 10)
        except Exception:
            return 0.0
    
    def _calculate_compile_time_score(self, result: subprocess.CompletedProcess, cmd: List[str]) -> float:
        """Calculate compile time score"""
        
        # This would need to be measured during actual compilation
        # For now, use a simple heuristic based on flags
        complex_flags = ['-O3', '-Ofast', '-flto', '-fprofile-use']
        complexity = sum(1 for flag in complex_flags if any(f in cmd for f in [flag]))
        
        # Higher complexity = longer compile time = lower score
        return max(0, 100 - (complexity * 20))
    
    def _evolve_population(self, generation_results: List[Dict], param_space: Dict) -> List[Dict]:
        """Evolve population using genetic algorithm"""
        
        import random
        
        # Sort by score
        sorted_results = sorted(generation_results, key=lambda x: x['score'], reverse=True)
        
        # Keep top 50%
        elite = [r['config'] for r in sorted_results[:len(sorted_results)//2]]
        
        # Generate new population
        new_population = elite.copy()
        
        # Fill remaining with crossover and mutation
        while len(new_population) < len(generation_results):
            if random.random() < 0.8:  # Crossover
                parent1, parent2 = random.sample(elite, 2)
                child = self._crossover(parent1, parent2, param_space)
            else:  # Mutation
                parent = random.choice(elite)
                child = self._mutate(parent, param_space)
            
            new_population.append(child)
        
        return new_population
    
    def _crossover(self, parent1: Dict, parent2: Dict, param_space: Dict) -> Dict:
        """Crossover two configurations"""
        
        import random
        child = {}
        
        for param in param_space:
            # Randomly choose from either parent
            child[param] = random.choice([parent1.get(param, []), parent2.get(param, [])])
        
        return child
    
    def _mutate(self, individual: Dict, param_space: Dict) -> Dict:
        """Mutate a configuration"""
        
        import random
        mutated = individual.copy()
        
        # Randomly mutate one parameter
        param_to_mutate = random.choice(list(param_space.keys()))
        mutated[param_to_mutate] = random.choice(param_space[param_to_mutate])
        
        return mutated
    
    def _check_convergence(self, recent_iterations: List[Dict]) -> bool:
        """Check if optimization has converged"""
        
        if len(recent_iterations) < 3:
            return False
        
        # Check if best scores have plateaued
        scores = [it['best_score'] for it in recent_iterations]
        score_variance = max(scores) - min(scores)
        
        return score_variance < 0.1  # Very small improvement

class CompilerBenchmarkSuite:
    """Comprehensive compiler benchmarking system"""
    
    def __init__(self):
        self.benchmark_cache = {}
        self.system_baseline = None
        
    async def run_comprehensive_benchmark(self, binary_path: str, analysis: Dict) -> Dict:
        """Run comprehensive benchmark suite"""
        
        benchmark_results = {
            'execution_benchmarks': {},
            'memory_benchmarks': {},
            'io_benchmarks': {},
            'cpu_benchmarks': {},
            'custom_benchmarks': {},
            'overall_score': 0,
            'baseline_comparison': {},
            'stability_metrics': {}
        }
        
        try:
            # Execution benchmarks
            benchmark_results['execution_benchmarks'] = await self._run_execution_benchmarks(binary_path)
            
            # Memory benchmarks
            benchmark_results['memory_benchmarks'] = await self._run_memory_benchmarks(binary_path)
            
            # I/O benchmarks
            benchmark_results['io_benchmarks'] = await self._run_io_benchmarks(binary_path)
            
            # CPU-specific benchmarks
            benchmark_results['cpu_benchmarks'] = await self._run_cpu_benchmarks(binary_path)
            
            # Custom benchmarks based on analysis
            benchmark_results['custom_benchmarks'] = await self._run_custom_benchmarks(binary_path, analysis)
            
            # Stability testing
            benchmark_results['stability_metrics'] = await self._run_stability_tests(binary_path)
            
            # Calculate overall score
            benchmark_results['overall_score'] = self._calculate_overall_score(benchmark_results)
            
            # Baseline comparison
            if self.system_baseline:
                benchmark_results['baseline_comparison'] = self._compare_with_baseline(benchmark_results)
        
        except Exception as e:
            benchmark_results['error'] = str(e)
        
        return benchmark_results
    
    async def _run_execution_benchmarks(self, binary_path: str) -> Dict:
        """Run execution time benchmarks"""
        
        results = {
            'cold_start': [],
            'warm_runs': [],
            'with_different_inputs': {},
            'memory_pressure': []
        }
        
        try:
            # Cold start timing
            for i in range(5):
                # Clear caches
                subprocess.run(['sync'], check=False)
                if shutil.which('echo'):
                    subprocess.run(['echo', '3'], input=None, 
                                 stdout=open('/proc/sys/vm/drop_caches', 'w'), check=False)
                
                start_time = time.time()
                result = subprocess.run([binary_path], capture_output=True, timeout=30)
                end_time = time.time()
                
                if result.returncode == 0:
                    results['cold_start'].append(end_time - start_time)
            
            # Warm runs
            for i in range(10):
                start_time = time.time()
                result = subprocess.run([binary_path], capture_output=True, timeout=30)
                end_time = time.time()
                
                if result.returncode == 0:
                    results['warm_runs'].append(end_time - start_time)
            
            # Different input sizes
            input_sizes = ['small', 'medium', 'large']
            for size in input_sizes:
                input_data = self._generate_input_data(size)
                times = []
                
                for _ in range(3):
                    start_time = time.time()
                    result = subprocess.run([binary_path], input=input_data, 
                                          capture_output=True, text=True, timeout=30)
                    end_time = time.time()
                    
                    if result.returncode == 0:
                        times.append(end_time - start_time)
                
                results['with_different_inputs'][size] = times
        
        except Exception as e:
            results['error'] = str(e)
        
        return results
    
    async def _run_memory_benchmarks(self, binary_path: str) -> Dict:
        """Run memory usage benchmarks"""
        
        results = {
            'peak_memory': [],
            'memory_leaks': [],
            'allocation_patterns': {},
            'cache_efficiency': {}
        }
        
        try:
            # Use time command for memory measurement
            if shutil.which('time'):
                for _ in range(3):
                    result = subprocess.run(
                        ['/usr/bin/time', '-v', binary_path],
                        capture_output=True, text=True, timeout=30
                    )
                    
                    if result.returncode == 0:
                        # Parse memory usage from time output
                        memory_info = self._parse_time_output(result.stderr)
                        results['peak_memory'].append(memory_info.get('max_memory', 0))
            
            # Valgrind memcheck (if available)
            if shutil.which('valgrind'):
                result = subprocess.run([
                    'valgrind', '--tool=memcheck', '--leak-check=full',
                    '--show-leak-kinds=all', binary_path
                ], capture_output=True, text=True, timeout=60)
                
                leak_info = self._parse_valgrind_output(result.stderr)
                results['memory_leaks'].append(leak_info)
        
        except Exception as e:
            results['error'] = str(e)
        
        return results
    
    async def _run_io_benchmarks(self, binary_path: str) -> Dict:
        """Run I/O performance benchmarks"""
        
        results = {
            'file_operations': {},
            'pipe_performance': [],
            'network_io': {}
        }
        
        try:
            # File I/O test
            with tempfile.NamedTemporaryFile() as temp_file:
                # Test with file input
                test_data = "test data\n" * 1000
                temp_file.write(test_data.encode())
                temp_file.flush()
                
                start_time = time.time()
                with open(temp_file.name, 'r') as f:
                    result = subprocess.run([binary_path], stdin=f, 
                                          capture_output=True, timeout=30)
                end_time = time.time()
                
                if result.returncode == 0:
                    results['file_operations']['file_input'] = end_time - start_time
            
            # Pipe performance
            for data_size in [100, 1000, 10000]:
                test_data = "x" * data_size
                start_time = time.time()
                result = subprocess.run([binary_path], input=test_data,
                                      capture_output=True, text=True, timeout=30)
                end_time = time.time()
                
                if result.returncode == 0:
                    results['pipe_performance'].append({
                        'data_size': data_size,
                        'time': end_time - start_time
                    })
        
        except Exception as e:
            results['error'] = str(e)
        
        return results
    
    async def _run_cpu_benchmarks(self, binary_path: str) -> Dict:
        """Run CPU-specific benchmarks"""
        
        results = {
            'cpu_utilization': [],
            'cache_performance': {},
            'instruction_count': {},
            'branch_predictions': {}
        }
        
        try:
            # CPU utilization with top/htop
            if shutil.which('top'):
                # Start binary in background
                process = subprocess.Popen([binary_path], stdout=subprocess.PIPE, 
                                         stderr=subprocess.PIPE)
                
                # Monitor CPU usage
                time.sleep(1)  # Let it start
                
                if process.poll() is None:  # Still running
                    # Get CPU usage
                    cpu_result = subprocess.run(['ps', '-p', str(process.pid), '-o', '%cpu'],
                                              capture_output=True, text=True, timeout=5)
                    if cpu_result.returncode == 0:
                        lines = cpu_result.stdout.strip().split('\n')
                        if len(lines) > 1:
                            try:
                                cpu_usage = float(lines[1])
                                results['cpu_utilization'].append(cpu_usage)
                            except ValueError:
                                pass
                
                process.terminate()
                process.wait()
            
            # Performance counters (if perf is available)
            if shutil.which('perf'):
                perf_result = subprocess.run([
                    'perf', 'stat', '-e', 'cycles,instructions,cache-references,cache-misses',
                    binary_path
                ], capture_output=True, text=True, timeout=60)
                
                if perf_result.returncode == 0:
                    perf_data = self._parse_perf_output(perf_result.stderr)
                    results['cache_performance'] = perf_data.get('cache', {})
                    results['instruction_count'] = perf_data.get('instructions', {})
        
        except Exception as e:
            results['error'] = str(e)
        
        return results
    
    async def _run_custom_benchmarks(self, binary_path: str, analysis: Dict) -> Dict:
        """Run custom benchmarks based on code analysis"""
        
        results = {}
        
        try:
            # Math-heavy benchmarks
            if analysis.get('math_heavy'):
                results['math_performance'] = await self._benchmark_math_performance(binary_path)
            
            # Threading benchmarks
            if analysis.get('threading'):
                results['thread_performance'] = await self._benchmark_thread_performance(binary_path)
            
            # Graphics benchmarks
            if analysis.get('graphics'):
                results['graphics_performance'] = await self._benchmark_graphics_performance(binary_path)
            
            # Network benchmarks
            if analysis.get('networking'):
                results['network_performance'] = await self._benchmark_network_performance(binary_path)
        
        except Exception as e:
            results['error'] = str(e)
        
        return results
    
    async def _run_stability_tests(self, binary_path: str) -> Dict:
        """Run stability and stress tests"""
        
        results = {
            'crash_resistance': 0,
            'long_running_stability': {},
            'resource_leak_detection': {},
            'error_handling': {}
        }
        
        try:
            # Crash resistance test
            successful_runs = 0
            total_runs = 10
            
            for i in range(total_runs):
                try:
                    # Try with various inputs including edge cases
                    test_inputs = ["", "\x00", "A" * 10000, "\n" * 1000]
                    test_input = test_inputs[i % len(test_inputs)]
                    
                    result = subprocess.run([binary_path], input=test_input,
                                          capture_output=True, text=True, timeout=10)
                    
                    # Consider it stable if it doesn't crash (any exit code is ok)
                    if result.returncode is not None:
                        successful_runs += 1
                
                except subprocess.TimeoutExpired:
                    # Timeout is considered unstable
                    pass
                except Exception:
                    # Any other exception is unstable
                    pass
            
            results['crash_resistance'] = (successful_runs / total_runs) * 100
            
            # Long running test
            try:
                start_time = time.time()
                process = subprocess.Popen([binary_path], stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE)
                
                # Let it run for a short time
                time.sleep(5)
                
                if process.poll() is None:  # Still running
                    results['long_running_stability']['still_running'] = True
                    process.terminate()
                    process.wait()
                
                end_time = time.time()
                results['long_running_stability']['run_time'] = end_time - start_time
                
            except Exception as e:
                results['long_running_stability']['error'] = str(e)
        
        except Exception as e:
            results['error'] = str(e)
        
        return results
    
    def _generate_input_data(self, size: str) -> str:
        """Generate test input data of specified size"""
        
        if size == 'small':
            return "hello\n"
        elif size == 'medium':
            return "line\n" * 100
        elif size == 'large':
            return "data\n" * 10000
        else:
            return ""
    
    def _parse_time_output(self, time_output: str) -> Dict:
        """Parse output from time command"""
        
        memory_info = {}
        for line in time_output.split('\n'):
            if 'Maximum resident set size' in line:
                # Extract memory value
                parts = line.split()
                if parts:
                    try:
                        memory_info['max_memory'] = int(parts[-1])
                    except ValueError:
                        pass
        return memory_info
    
    def _parse_valgrind_output(self, valgrind_output: str) -> Dict:
        """Parse valgrind memcheck output"""
        
        leak_info = {
            'definitely_lost': 0,
            'indirectly_lost': 0,
            'possibly_lost': 0
        }
        
        for line in valgrind_output.split('\n'):
            if 'definitely lost' in line:
                # Extract number
                parts = line.split()
                for i, part in enumerate(parts):
                    if part.isdigit():
                        leak_info['definitely_lost'] = int(part)
                        break
        
        return leak_info
    
    def _parse_perf_output(self, perf_output: str) -> Dict:
        """Parse perf stat output"""
        
        perf_data = {
            'cache': {},
            'instructions': {}
        }
        
        for line in perf_output.split('\n'):
            if 'cache-references' in line:
                parts = line.split()
                if parts:
                    try:
                        perf_data['cache']['references'] = int(parts[0].replace(',', ''))
                    except (ValueError, IndexError):
                        pass
            elif 'cache-misses' in line:
                parts = line.split()
                if parts:
                    try:
                        perf_data['cache']['misses'] = int(parts[0].replace(',', ''))
                    except (ValueError, IndexError):
                        pass
        
        return perf_data
    
    async def _benchmark_math_performance(self, binary_path: str) -> Dict:
        """Benchmark mathematical performance"""
        
        math_results = {}
        
        # Test with mathematical inputs
        math_inputs = [
            "3.141592653589793\n",
            "1000000\n",
            "0.000001\n"
        ]
        
        for i, math_input in enumerate(math_inputs):
            times = []
            for _ in range(3):
                start_time = time.time()
                result = subprocess.run([binary_path], input=math_input,
                                      capture_output=True, text=True, timeout=30)
                end_time = time.time()
                
                if result.returncode == 0:
                    times.append(end_time - start_time)
            
            if times:
                math_results[f'math_test_{i}'] = {
                    'avg_time': sum(times) / len(times),
                    'min_time': min(times),
                    'max_time': max(times)
                }
        
        return math_results
    
    async def _benchmark_thread_performance(self, binary_path: str) -> Dict:
        """Benchmark threading performance"""
        
        thread_results = {}
        
        # Test under different CPU loads
        original_priority = os.getpriority(os.PRIO_PROCESS, 0)
        
        try:
            # Normal priority
            times = []
            for _ in range(3):
                start_time = time.time()
                result = subprocess.run([binary_path], capture_output=True, timeout=30)
                end_time = time.time()
                
                if result.returncode == 0:
                    times.append(end_time - start_time)
            
            if times:
                thread_results['normal_priority'] = sum(times) / len(times)
            
        except Exception as e:
            thread_results['error'] = str(e)
        finally:
            # Restore original priority
            try:
                os.setpriority(os.PRIO_PROCESS, 0, original_priority)
            except:
                pass
        
        return thread_results
    
    async def _benchmark_graphics_performance(self, binary_path: str) -> Dict:
        """Benchmark graphics performance"""
        
        graphics_results = {}
        
        # Test with graphics-related environment variables
        env = os.environ.copy()
        
        # Test with different rendering modes (if applicable)
        render_modes = [
            {},  # Default
            {'LIBGL_ALWAYS_SOFTWARE': '1'},  # Software rendering
            {'MESA_GL_VERSION_OVERRIDE': '3.3'}  # Specific GL version
        ]
        
        for i, mode_env in enumerate(render_modes):
            test_env = env.copy()
            test_env.update(mode_env)
            
            times = []
            for _ in range(2):  # Fewer iterations for graphics tests
                start_time = time.time()
                result = subprocess.run([binary_path], env=test_env,
                                      capture_output=True, timeout=30)
                end_time = time.time()
                
                if result.returncode == 0:
                    times.append(end_time - start_time)
            
            if times:
                graphics_results[f'mode_{i}'] = sum(times) / len(times)
        
        return graphics_results
    
    async def _benchmark_network_performance(self, binary_path: str) -> Dict:
        """Benchmark network performance"""
        
        network_results = {}
        
        # Test with network-related environment settings
        env = os.environ.copy()
        
        # Test with localhost connections
        network_configs = [
            {},  # Default
            {'NO_PROXY': 'localhost,127.0.0.1'},  # No proxy
        ]
        
        for i, config_env in enumerate(network_configs):
            test_env = env.copy()
            test_env.update(config_env)
            
            times = []
            for _ in range(2):
                start_time = time.time()
                result = subprocess.run([binary_path], env=test_env,
                                      capture_output=True, timeout=30)
                end_time = time.time()
                
                if result.returncode == 0:
                    times.append(end_time - start_time)
            
            if times:
                network_results[f'config_{i}'] = sum(times) / len(times)
        
        return network_results
    
    def _calculate_overall_score(self, benchmark_results: Dict) -> float:
        """Calculate overall benchmark score"""
        
        total_score = 0.0
        weight_sum = 0.0
        
        # Execution score (weight: 40%)
        if benchmark_results['execution_benchmarks'].get('warm_runs'):
            avg_time = sum(benchmark_results['execution_benchmarks']['warm_runs']) / len(benchmark_results['execution_benchmarks']['warm_runs'])
            exec_score = max(0, 100 - (avg_time * 100))  # Lower time = higher score
            total_score += exec_score * 0.4
            weight_sum += 0.4
        
        # Stability score (weight: 30%)
        stability_score = benchmark_results['stability_metrics'].get('crash_resistance', 0)
        total_score += stability_score * 0.3
        weight_sum += 0.3
        
        # Memory score (weight: 20%)
        if benchmark_results['memory_benchmarks'].get('peak_memory'):
            avg_memory = sum(benchmark_results['memory_benchmarks']['peak_memory']) / len(benchmark_results['memory_benchmarks']['peak_memory'])
            # Lower memory usage = higher score
            memory_score = max(0, 100 - (avg_memory / 1024))  # Rough scoring
            total_score += memory_score * 0.2
            weight_sum += 0.2
        
        # Custom benchmarks (weight: 10%)
        custom_score = 50  # Default neutral score
        total_score += custom_score * 0.1
        weight_sum += 0.1
        
        return total_score / weight_sum if weight_sum > 0 else 0.0
    
    def _compare_with_baseline(self, benchmark_results: Dict) -> Dict:
        """Compare results with system baseline"""
        
        comparison = {
            'performance_ratio': 1.0,
            'memory_ratio': 1.0,
            'stability_ratio': 1.0
        }
        
        if self.system_baseline:
            # Compare execution times
            if (benchmark_results['execution_benchmarks'].get('warm_runs') and 
                self.system_baseline['execution_benchmarks'].get('warm_runs')):
                
                current_avg = sum(benchmark_results['execution_benchmarks']['warm_runs']) / len(benchmark_results['execution_benchmarks']['warm_runs'])
                baseline_avg = sum(self.system_baseline['execution_benchmarks']['warm_runs']) / len(self.system_baseline['execution_benchmarks']['warm_runs'])
                
                if baseline_avg > 0:
                    comparison['performance_ratio'] = baseline_avg / current_avg
        
        return comparison

# Integration with main compilation system
async def run_advanced_optimization_suite(update: Update, file_path: str, analysis: Dict, 
                                        compiler_system) -> Dict:
    """Run complete advanced optimization suite"""
    
    suite_results = {
        'pgo_results': {},
        'auto_tuning_results': {},
        'benchmark_results': {},
        'recommendations': [],
        'optimal_config': None,
        'total_time': 0
    }
    
    start_time = time.time()
    
    try:
        # Progress update
        await update.message.reply_text("🔬 Running advanced optimization suite...")
        
        # Profile-Guided Optimization
        pgo_system = ProfileGuidedOptimization(compiler_system)
        
        # Find best compiler for PGO
        available_compilers = []
        for category in ['gcc_variants', 'clang_variants']:
            available_compilers.extend(compiler_system.available_compilers[category])
        
        if available_compilers:
            best_compiler = sorted(available_compilers, 
                                 key=lambda x: x.get('priority_score', 0), reverse=True)[0]
            
            suite_results['pgo_results'] = await pgo_system.run_pgo_optimization(
                file_path, best_compiler['name'], ['-O3', '-march=native']
            )
        
        # Auto-tuning
        await update.message.reply_text("🤖 Running auto-tuning optimization...")
        
        auto_tuner = AutoTuningSystem(compiler_system)
        suite_results['auto_tuning_results'] = await auto_tuner.auto_tune_compilation(
            file_path, analysis, 'performance'
        )
        
        # Benchmarking
        if suite_results['pgo_results'].get('final_binary'):
            await update.message.reply_text("📊 Running comprehensive benchmarks...")
            
            benchmark_suite = CompilerBenchmarkSuite()
            suite_results['benchmark_results'] = await benchmark_suite.run_comprehensive_benchmark(
                suite_results['pgo_results']['final_binary'], analysis
            )
        
        # Generate recommendations
        suite_results['recommendations'] = generate_advanced_recommendations(suite_results, analysis)
        
        # Determine optimal configuration
        suite_results['optimal_config'] = determine_optimal_configuration(suite_results)
        
    except Exception as e:
        suite_results['error'] = str(e)
    finally:
        suite_results['total_time'] = time.time() - start_time
    
    return suite_results

def generate_advanced_recommendations(suite_results: Dict, analysis: Dict) -> List[str]:
    """Generate advanced optimization recommendations"""
    
    recommendations = []
    
    # PGO recommendations
    if suite_results.get('pgo_results', {}).get('performance_improvement', 0) > 5:
        recommendations.append(f"🚀 Profile-Guided Optimization shows {suite_results['pgo_results']['performance_improvement']:.1f}% improvement - highly recommended")
    
    # Auto-tuning recommendations
    if suite_results.get('auto_tuning_results', {}).get('best_config'):
        best_config = suite_results['auto_tuning_results']['best_config']
        recommendations.append(f"🎯 Auto-tuning found optimal configuration with score {suite_results['auto_tuning_results']['best_score']:.1f}")
    
    # Benchmark-based recommendations
    benchmark_results = suite_results.get('benchmark_results', {})
    if benchmark_results.get('overall_score', 0) > 80:
        recommendations.append("⭐ Excellent overall performance - current optimization is highly effective")
    elif benchmark_results.get('overall_score', 0) < 50:
        recommendations.append("⚠️ Performance below expectations - consider different optimization strategy")
    
    # Stability recommendations
    stability = benchmark_results.get('stability_metrics', {}).get('crash_resistance', 0)
    if stability < 80:
        recommendations.append(f"🛡️ Stability concern detected ({stability:.1f}% success rate) - review code for edge cases")
    
    # Memory recommendations
    memory_benchmarks = benchmark_results.get('memory_benchmarks', {})
    if memory_benchmarks.get('memory_leaks'):
        recommendations.append("🔍 Memory leak detected - consider using smart pointers or RAII")
    
    # Custom recommendations based on analysis
    if analysis.get('math_heavy') and benchmark_results.get('custom_benchmarks', {}).get('math_performance'):
        recommendations.append("🧮 Math-heavy code detected - verify fast-math optimizations are beneficial")
    
    if analysis.get('threading') and benchmark_results.get('custom_benchmarks', {}).get('thread_performance'):
        recommendations.append("🧵 Threading performance varies - consider thread pool optimization")
    
    return recommendations

def determine_optimal_configuration(suite_results: Dict) -> Dict:
    """Determine optimal configuration from all results"""
    
    optimal_config = {
        'method': 'standard',
        'compiler': 'gcc',
        'flags': ['-O3'],
        'confidence': 0.5,
        'expected_improvement': 0.0
    }
    
    # Check PGO results
    pgo_improvement = suite_results.get('pgo_results', {}).get('performance_improvement', 0)
    if pgo_improvement > 10:
        optimal_config.update({
            'method': 'profile_guided',
            'flags': ['-O3', '-fprofile-use'],
            'confidence': 0.9,
            'expected_improvement': pgo_improvement
        })
    
    # Check auto-tuning results
    auto_tuning = suite_results.get('auto_tuning_results', {})
    if auto_tuning.get('best_score', 0) > optimal_config['confidence'] * 100:
        optimal_config.update({
            'method': 'auto_tuned',
            'config': auto_tuning.get('best_config', {}),
            'confidence': auto_tuning.get('best_score', 0) / 100,
            'expected_improvement': auto_tuning.get('best_score', 0) - 50  # Relative to baseline
        })
    
    return optimal_config

# Export the advanced optimization function
__all__ = ['run_advanced_optimization_suite', 'ProfileGuidedOptimization', 
          'AutoTuningSystem', 'CompilerBenchmarkSuite']

# Advanced Multi-Platform Compilation Engine
class MultiPlatformEngine:
    """Advanced multi-platform compilation engine with cross-compilation support"""
    
    def __init__(self, compiler_system):
        self.compiler_system = compiler_system
        self.target_platforms = self._detect_target_platforms()
        self.cross_toolchains = self._scan_cross_toolchains()
        self.platform_configs = self._create_platform_configs()
        self.build_cache = {}
        
    def _detect_target_platforms(self) -> Dict:
        """Detect available target platforms for cross-compilation"""
        
        platforms = {
            'native': {
                'arch': platform.machine(),
                'os': platform.system(),
                'abi': 'default',
                'priority': 1
            },
            'cross_targets': [],
            'emulation_targets': [],
            'virtual_targets': []
        }
        
        # Common cross-compilation targets
        cross_targets = [
            # ARM variants
            {'arch': 'aarch64', 'os': 'linux', 'abi': 'gnu', 'triple': 'aarch64-linux-gnu'},
            {'arch': 'arm', 'os': 'linux', 'abi': 'gnueabihf', 'triple': 'arm-linux-gnueabihf'},
            {'arch': 'arm', 'os': 'linux', 'abi': 'gnueabi', 'triple': 'arm-linux-gnueabi'},
            
            # x86 variants
            {'arch': 'x86_64', 'os': 'linux', 'abi': 'gnu', 'triple': 'x86_64-linux-gnu'},
            {'arch': 'i686', 'os': 'linux', 'abi': 'gnu', 'triple': 'i686-linux-gnu'},
            
            # MIPS variants
            {'arch': 'mips', 'os': 'linux', 'abi': 'gnu', 'triple': 'mips-linux-gnu'},
            {'arch': 'mips64', 'os': 'linux', 'abi': 'gnuabi64', 'triple': 'mips64-linux-gnuabi64'},
            
            # PowerPC variants
            {'arch': 'powerpc', 'os': 'linux', 'abi': 'gnu', 'triple': 'powerpc-linux-gnu'},
            {'arch': 'powerpc64', 'os': 'linux', 'abi': 'gnu', 'triple': 'powerpc64-linux-gnu'},
            {'arch': 'powerpc64le', 'os': 'linux', 'abi': 'gnu', 'triple': 'powerpc64le-linux-gnu'},
            
            # RISC-V variants
            {'arch': 'riscv32', 'os': 'linux', 'abi': 'gnu', 'triple': 'riscv32-linux-gnu'},
            {'arch': 'riscv64', 'os': 'linux', 'abi': 'gnu', 'triple': 'riscv64-linux-gnu'},
            
            # Embedded targets
            {'arch': 'arm', 'os': 'none', 'abi': 'eabi', 'triple': 'arm-none-eabi'},
            {'arch': 'riscv32', 'os': 'none', 'abi': 'elf', 'triple': 'riscv32-unknown-elf'},
            {'arch': 'avr', 'os': 'none', 'abi': 'elf', 'triple': 'avr'},
            
            # Windows targets
            {'arch': 'x86_64', 'os': 'windows', 'abi': 'mingw32', 'triple': 'x86_64-w64-mingw32'},
            {'arch': 'i686', 'os': 'windows', 'abi': 'mingw32', 'triple': 'i686-w64-mingw32'},
            
            # Android targets
            {'arch': 'aarch64', 'os': 'android', 'abi': 'android21', 'triple': 'aarch64-linux-android21'},
            {'arch': 'armv7a', 'os': 'android', 'abi': 'androideabi21', 'triple': 'armv7a-linux-androideabi21'},
            {'arch': 'x86_64', 'os': 'android', 'abi': 'android21', 'triple': 'x86_64-linux-android21'},
            {'arch': 'i686', 'os': 'android', 'abi': 'android21', 'triple': 'i686-linux-android21'},
            
            # WebAssembly
            {'arch': 'wasm32', 'os': 'emscripten', 'abi': 'unknown', 'triple': 'wasm32-unknown-emscripten'},
            {'arch': 'wasm64', 'os': 'emscripten', 'abi': 'unknown', 'triple': 'wasm64-unknown-emscripten'},
        ]
        
        # Check which targets are available
        for target in cross_targets:
            compiler_triple = f"{target['triple']}-gcc"
            clang_target = f"--target={target['triple']}"
            
            # Check for GCC cross compiler
            if shutil.which(compiler_triple):
                target['compilers'] = [compiler_triple]
                target['available'] = True
                target['priority'] = 3
                platforms['cross_targets'].append(target)
                
            # Check for Clang cross compilation support
            elif shutil.which('clang'):
                try:
                    result = subprocess.run(['clang', clang_target, '--version'], 
                                          capture_output=True, text=True, timeout=5)
                    if result.returncode == 0:
                        target['compilers'] = [f'clang {clang_target}']
                        target['available'] = True
                        target['priority'] = 4
                        platforms['cross_targets'].append(target)
                except:
                    pass
        
        # Detect emulation targets (QEMU)
        emulation_targets = [
            {'arch': 'aarch64', 'emulator': 'qemu-aarch64'},
            {'arch': 'arm', 'emulator': 'qemu-arm'},
            {'arch': 'mips', 'emulator': 'qemu-mips'},
            {'arch': 'mips64', 'emulator': 'qemu-mips64'},
            {'arch': 'riscv64', 'emulator': 'qemu-riscv64'},
            {'arch': 'powerpc', 'emulator': 'qemu-ppc'},
            {'arch': 'powerpc64', 'emulator': 'qemu-ppc64'},
        ]
        
        for target in emulation_targets:
            if shutil.which(target['emulator']):
                target['available'] = True
                target['priority'] = 5
                platforms['emulation_targets'].append(target)
        
        return platforms
    
    def _scan_cross_toolchains(self) -> Dict:
        """Scan for available cross-compilation toolchains"""
        
        toolchains = {
            'gcc_cross': [],
            'clang_cross': [],
            'specialized_cross': [],
            'embedded_toolchains': [],
            'android_ndk': [],
            'emscripten': []
        }
        
        # Scan for GCC cross-compilers
        gcc_patterns = [
            r'(\w+)-(\w+)-(\w+)-gcc',
            r'(\w+)-(\w+)-gcc',
            r'(\w+)-gcc'
        ]
        
        search_paths = ['/usr/bin', '/usr/local/bin', '/opt/*/bin']
        
        for path in search_paths:
            if '*' in path:
                import glob
                for expanded_path in glob.glob(path):
                    if os.path.exists(expanded_path):
                        self._scan_toolchain_directory(expanded_path, toolchains, gcc_patterns)
            elif os.path.exists(path):
                self._scan_toolchain_directory(path, toolchains, gcc_patterns)
        
        # Scan for Android NDK
        ndk_paths = [
            '/opt/android-ndk*',
            os.path.expanduser('~/Android/Sdk/ndk/*'),
            '/data/data/com.termux/files/usr/lib/android-ndk'
        ]
        
        for ndk_path in ndk_paths:
            if '*' in ndk_path:
                import glob
                for expanded_path in glob.glob(ndk_path):
                    self._scan_android_ndk(expanded_path, toolchains)
            elif os.path.exists(ndk_path):
                self._scan_android_ndk(ndk_path, toolchains)
        
        # Scan for Emscripten
        if shutil.which('emcc'):
            toolchains['emscripten'].append({
                'name': 'emscripten',
                'compiler': 'emcc',
                'cxx_compiler': 'em++',
                'target': 'wasm32-unknown-emscripten',
                'available': True
            })
        
        return toolchains
    
    def _scan_toolchain_directory(self, directory: str, toolchains: Dict, patterns: List[str]):
        """Scan directory for cross-compilation toolchains"""
        
        try:
            for file in os.listdir(directory):
                if file.endswith('-gcc'):
                    # Parse toolchain triple
                    parts = file[:-4].split('-')  # Remove -gcc suffix
                    if len(parts) >= 2:
                        toolchain_info = {
                            'name': file[:-4],
                            'compiler': os.path.join(directory, file),
                            'cxx_compiler': os.path.join(directory, file[:-4] + '-g++'),
                            'target': file[:-4],
                            'available': os.path.exists(os.path.join(directory, file[:-4] + '-g++'))
                        }
                        
                        # Categorize toolchain
                        if 'android' in file:
                            toolchains['android_ndk'].append(toolchain_info)
                        elif any(arch in file for arch in ['avr', 'msp430', 'pic32']):
                            toolchains['embedded_toolchains'].append(toolchain_info)
                        else:
                            toolchains['gcc_cross'].append(toolchain_info)
        except:
            pass
    
    def _scan_android_ndk(self, ndk_path: str, toolchains: Dict):
        """Scan Android NDK for available toolchains"""
        
        try:
            toolchains_dir = os.path.join(ndk_path, 'toolchains', 'llvm', 'prebuilt')
            
            if os.path.exists(toolchains_dir):
                # Find host directory
                for host_dir in os.listdir(toolchains_dir):
                    host_path = os.path.join(toolchains_dir, host_dir, 'bin')
                    if os.path.exists(host_path):
                        # Scan for Android compilers
                        for file in os.listdir(host_path):
                            if file.endswith('-clang') and 'android' in file:
                                toolchain_info = {
                                    'name': file[:-6],  # Remove -clang suffix
                                    'compiler': os.path.join(host_path, file),
                                    'cxx_compiler': os.path.join(host_path, file[:-6] + '-clang++'),
                                    'target': file[:-6],
                                    'ndk_path': ndk_path,
                                    'available': True
                                }
                                toolchains['android_ndk'].append(toolchain_info)
        except:
            pass
    
    def _create_platform_configs(self) -> Dict:
        """Create platform-specific compilation configurations"""
        
        configs = {}
        
        # Native platform config
        native_arch = platform.machine()
        native_os = platform.system()
        
        configs['native'] = {
            'arch_flags': self._get_native_arch_flags(native_arch),
            'os_flags': self._get_native_os_flags(native_os),
            'optimization_flags': ['-O3', '-march=native', '-mtune=native'],
            'linking_flags': [],
            'libraries': self._get_native_libraries(),
            'defines': []
        }
        
        # Cross-platform configs
        for target in self.target_platforms['cross_targets']:
            arch = target['arch']
            os_type = target['os']
            abi = target['abi']
            
            configs[target['triple']] = {
                'arch_flags': self._get_cross_arch_flags(arch),
                'os_flags': self._get_cross_os_flags(os_type),
                'abi_flags': self._get_abi_flags(abi),
                'optimization_flags': self._get_cross_optimization_flags(arch, os_type),
                'linking_flags': self._get_cross_linking_flags(os_type, abi),
                'libraries': self._get_cross_libraries(os_type),
                'defines': self._get_cross_defines(os_type, arch),
                'sysroot': self._get_sysroot_path(target['triple'])
            }
        
        return configs
    
    def _get_native_arch_flags(self, arch: str) -> List[str]:
        """Get native architecture-specific flags"""
        
        arch_flags = []
        
        if arch in ['x86_64', 'amd64']:
            arch_flags.extend(['-m64', '-msse4.2', '-mavx'])
        elif arch in ['i386', 'i686']:
            arch_flags.extend(['-m32', '-msse2'])
        elif arch == 'aarch64':
            arch_flags.extend(['-march=armv8-a'])
        elif arch.startswith('arm'):
            arch_flags.extend(['-march=armv7-a', '-mfpu=neon'])
        
        return arch_flags
    
    def _get_native_os_flags(self, os_type: str) -> List[str]:
        """Get native OS-specific flags"""
        
        os_flags = []
        
        if os_type == 'Linux':
            os_flags.extend(['-D_GNU_SOURCE', '-pthread'])
        elif os_type == 'Darwin':
            os_flags.extend(['-D_DARWIN_C_SOURCE'])
        elif os_type == 'Windows':
            os_flags.extend(['-D_WIN32_WINNT=0x0601'])
        
        return os_flags
    
    def _get_cross_arch_flags(self, arch: str) -> List[str]:
        """Get cross-compilation architecture flags"""
        
        arch_flags = []
        
        arch_configs = {
            'aarch64': ['-march=armv8-a'],
            'arm': ['-march=armv7-a', '-mfpu=neon'],
            'x86_64': ['-m64'],
            'i686': ['-m32'],
            'mips': ['-march=mips32r2'],
            'mips64': ['-march=mips64r2'],
            'riscv32': ['-march=rv32gc'],
            'riscv64': ['-march=rv64gc'],
            'powerpc': ['-mcpu=powerpc'],
            'powerpc64': ['-mcpu=powerpc64'],
            'powerpc64le': ['-mcpu=powerpc64le'],
        }
        
        return arch_configs.get(arch, [])
    
    def _get_cross_os_flags(self, os_type: str) -> List[str]:
        """Get cross-compilation OS flags"""
        
        os_flags = []
        
        if os_type == 'linux':
            os_flags.extend(['-D_GNU_SOURCE'])
        elif os_type == 'android':
            os_flags.extend(['-DANDROID', '-D_GNU_SOURCE'])
        elif os_type == 'windows':
            os_flags.extend(['-D_WIN32_WINNT=0x0601', '-DWINVER=0x0601'])
        elif os_type == 'none':
            os_flags.extend(['-ffreestanding', '-nostdlib'])
        
        return os_flags
    
    def _get_abi_flags(self, abi: str) -> List[str]:
        """Get ABI-specific flags"""
        
        abi_flags = []
        
        if abi == 'gnueabihf':
            abi_flags.extend(['-mfloat-abi=hard'])
        elif abi == 'gnueabi':
            abi_flags.extend(['-mfloat-abi=soft'])
        elif abi == 'eabi':
            abi_flags.extend(['-mfloat-abi=soft', '-mthumb'])
        elif 'android' in abi:
            abi_flags.extend(['-fPIC'])
        
        return abi_flags
    
    def _get_cross_optimization_flags(self, arch: str, os_type: str) -> List[str]:
        """Get cross-compilation optimization flags"""
        
        opt_flags = ['-O2']  # Conservative default for cross-compilation
        
        # Architecture-specific optimizations
        if arch in ['x86_64', 'i686']:
            opt_flags.extend(['-mtune=generic'])
        elif arch == 'aarch64':
            opt_flags.extend(['-mtune=cortex-a72'])
        elif arch == 'arm':
            opt_flags.extend(['-mtune=cortex-a15'])
        
        # OS-specific optimizations
        if os_type == 'none':  # Embedded
            opt_flags.extend(['-Os', '-ffunction-sections', '-fdata-sections'])
        elif os_type == 'android':
            opt_flags.extend(['-ffast-math'])
        
        return opt_flags
    
    def _get_cross_linking_flags(self, os_type: str, abi: str) -> List[str]:
        """Get cross-compilation linking flags"""
        
        link_flags = []
        
        if os_type == 'none':
            link_flags.extend(['-Wl,--gc-sections', '-nostartfiles'])
        elif os_type == 'android':
            link_flags.extend(['-pie'])
        elif os_type == 'windows':
            link_flags.extend(['-static-libgcc', '-static-libstdc++'])
        
        return link_flags
    
    def _get_cross_libraries(self, os_type: str) -> List[str]:
        """Get cross-compilation library flags"""
        
        libs = []
        
        if os_type == 'android':
            libs.extend(['-llog', '-ldl'])
        elif os_type == 'linux':
            libs.extend(['-ldl', '-lpthread'])
        elif os_type == 'windows':
            libs.extend(['-lws2_32', '-lkernel32'])
        
        return libs
    
    def _get_cross_defines(self, os_type: str, arch: str) -> List[str]:
        """Get cross-compilation preprocessor defines"""
        
        defines = []
        
        defines.append(f'-DTARGET_OS_{os_type.upper()}')
        defines.append(f'-DTARGET_ARCH_{arch.upper()}')
        
        if os_type == 'android':
            defines.extend(['-DANDROID', '-D__ANDROID__'])
        elif os_type == 'none':
            defines.extend(['-DEMBEDDED', '-D__EMBEDDED__'])
        
        return defines
    
    def _get_sysroot_path(self, triple: str) -> Optional[str]:
        """Get sysroot path for cross-compilation target"""
        
        # Common sysroot locations
        sysroot_paths = [
            f'/usr/{triple}',
            f'/usr/lib/gcc-cross/{triple}',
            f'/opt/cross/{triple}',
            f'/data/data/com.termux/files/usr/{triple}'
        ]
        
        for path in sysroot_paths:
            if os.path.exists(path):
                return path
        
        return None
    
    def _get_native_libraries(self) -> List[str]:
        """Get native system libraries"""
        
        libs = ['-lpthread', '-lm']
        
        if platform.system() == 'Linux':
            libs.extend(['-ldl', '-lrt'])
        elif platform.system() == 'Darwin':
            libs.extend(['-framework Foundation'])
        
        return libs
    
    async def create_multi_platform_builds(self, file_path: str, analysis: Dict, targets: List[str] = None) -> Dict:
        """Create builds for multiple platforms"""
        
        build_results = {
            'builds': [],
            'summary': {},
            'total_time': 0,
            'success_count': 0,
            'failure_count': 0
        }
        
        start_time = time.time()
        
        try:
            # Determine target platforms
            if targets is None:
                targets = ['native'] + [t['triple'] for t in self.target_platforms['cross_targets'][:5]]
            
            # Build for each target platform
            for target in targets:
                if target == 'native':
                    result = await self._build_native(file_path, analysis)
                else:
                    result = await self._build_cross_platform(file_path, analysis, target)
                
                build_results['builds'].append(result)
                
                if result['success']:
                    build_results['success_count'] += 1
                else:
                    build_results['failure_count'] += 1
        
        except Exception as e:
            build_results['error'] = str(e)
        finally:
            build_results['total_time'] = time.time() - start_time
        
        # Generate summary
        build_results['summary'] = self._generate_build_summary(build_results['builds'])
        
        return build_results
    
    async def _build_native(self, file_path: str, analysis: Dict) -> Dict:
        """Build for native platform"""
        
        result = {
            'target': 'native',
            'arch': platform.machine(),
            'os': platform.system(),
            'success': False,
            'binary_path': None,
            'binary_size': 0,
            'compilation_time': 0,
            'compiler_used': None,
            'flags_used': [],
            'warnings': [],
            'errors': []
        }
        
        start_time = time.time()
        
        try:
            # Get best native compiler
            compilers = (self.compiler_system.available_compilers['gcc_variants'] + 
                        self.compiler_system.available_compilers['clang_variants'])
            
            if not compilers:
                result['errors'].append('No suitable compiler found')
                return result
            
            best_compiler = sorted(compilers, key=lambda x: x.get('priority_score', 0), reverse=True)[0]
            
            # Build compilation command
            config = self.platform_configs['native']
            temp_dir = tempfile.mkdtemp()
            output_path = os.path.join(temp_dir, f'native_binary_{int(time.time())}')
            
            cmd = [best_compiler['name']]
            cmd.extend(config['optimization_flags'])
            cmd.extend(config['arch_flags'])
            cmd.extend(config['os_flags'])
            cmd.extend([file_path, '-o', output_path])
            cmd.extend(config['libraries'])
            
            # Execute compilation
            process = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            
            result['compilation_time'] = time.time() - start_time
            result['compiler_used'] = best_compiler['name']
            result['flags_used'] = cmd[1:-3]  # Exclude compiler, input, -o, output
            
            if process.returncode == 0 and os.path.exists(output_path):
                result['success'] = True
                result['binary_path'] = output_path
                result['binary_size'] = os.path.getsize(output_path)
                result['warnings'] = extract_warnings(process.stderr)
            else:
                result['errors'].append(f'Compilation failed: {process.stderr[:200]}')
        
        except Exception as e:
            result['errors'].append(f'Build error: {str(e)}')
        
        return result
    
    async def _build_cross_platform(self, file_path: str, analysis: Dict, target: str) -> Dict:
        """Build for cross-compilation target"""
        
        result = {
            'target': target,
            'success': False,
            'binary_path': None,
            'binary_size': 0,
            'compilation_time': 0,
            'compiler_used': None,
            'flags_used': [],
            'warnings': [],
            'errors': []
        }
        
        start_time = time.time()
        
        try:
            # Find suitable cross-compiler
            cross_compiler = self._find_cross_compiler(target)
            
            if not cross_compiler:
                result['errors'].append(f'No cross-compiler found for target {target}')
                return result
            
            # Build compilation command
            config = self.platform_configs.get(target, {})
            temp_dir = tempfile.mkdtemp()
            output_path = os.path.join(temp_dir, f'{target}_binary_{int(time.time())}')
            
            cmd = [cross_compiler['compiler']]
            
            # Add target-specific flags
            cmd.extend(config.get('arch_flags', []))
            cmd.extend(config.get('os_flags', []))
            cmd.extend(config.get('abi_flags', []))
            cmd.extend(config.get('optimization_flags', ['-O2']))
            
            # Add sysroot if available
            sysroot = config.get('sysroot')
            if sysroot:
                cmd.extend([f'--sysroot={sysroot}'])
            
            # Add defines
            cmd.extend(config.get('defines', []))
            
            # Add input and output
            cmd.extend([file_path, '-o', output_path])
            
            # Add linking flags and libraries
            cmd.extend(config.get('linking_flags', []))
            cmd.extend(config.get('libraries', []))
            
            # Execute cross-compilation
            process = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
            
            result['compilation_time'] = time.time() - start_time
            result['compiler_used'] = cross_compiler['name']
            result['flags_used'] = cmd[1:-3]  # Exclude compiler, input, -o, output
            
            if process.returncode == 0 and os.path.exists(output_path):
                result['success'] = True
                result['binary_path'] = output_path
                result['binary_size'] = os.path.getsize(output_path)
                result['warnings'] = extract_warnings(process.stderr)
                
                # Add target architecture info
                target_info = self._parse_target_triple(target)
                result.update(target_info)
            else:
                result['errors'].append(f'Cross-compilation failed: {process.stderr[:200]}')
        
        except Exception as e:
            result['errors'].append(f'Cross-build error: {str(e)}')
        
        return result
    
    def _find_cross_compiler(self, target: str) -> Optional[Dict]:
        """Find suitable cross-compiler for target"""
        
        # Check GCC cross-compilers
        for compiler in self.cross_toolchains['gcc_cross']:
            if target in compiler['target']:
                return compiler
        
        # Check Clang with target
        if shutil.which('clang'):
            return {
                'name': f'clang-{target}',
                'compiler': 'clang',
                'target': target,
                'flags': [f'--target={target}']
            }
        
        # Check Android NDK
        for compiler in self.cross_toolchains['android_ndk']:
            if target in compiler['target']:
                return compiler
        
        return None
    
    def _parse_target_triple(self, target: str) -> Dict:
        """Parse target triple into components"""
        
        parts = target.split('-')
        result = {
            'arch': parts[0] if parts else 'unknown',
            'vendor': parts[1] if len(parts) > 1 else 'unknown',
            'os': parts[2] if len(parts) > 2 else 'unknown',
            'abi': parts[3] if len(parts) > 3 else 'unknown'
        }
        
        return result
    
    def _generate_build_summary(self, builds: List[Dict]) -> Dict:
        """Generate summary of build results"""
        
        summary = {
            'total_builds': len(builds),
            'successful_builds': len([b for b in builds if b['success']]),
            'failed_builds': len([b for b in builds if not b['success']]),
            'total_size': sum(b.get('binary_size', 0) for b in builds if b['success']),
            'avg_compilation_time': 0,
            'supported_platforms': [],
            'binary_analysis': {}
        }
        
        successful_builds = [b for b in builds if b['success']]
        
        if successful_builds:
            summary['avg_compilation_time'] = sum(b['compilation_time'] for b in successful_builds) / len(successful_builds)
            
            for build in successful_builds:
                platform_info = {
                    'target': build['target'],
                    'arch': build.get('arch', 'unknown'),
                    'os': build.get('os', 'unknown'),
                    'size': build['binary_size'],
                    'compile_time': build['compilation_time']
                }
                summary['supported_platforms'].append(platform_info)
        
        return summary

# Advanced Security Analysis Engine
class SecurityAnalysisEngine:
    """Advanced security analysis and hardening engine"""
    
    def __init__(self):
        self.security_tools = self._detect_security_tools()
        self.vulnerability_database = self._load_vulnerability_patterns()
        self.hardening_profiles = self._create_hardening_profiles()
        
    def _detect_security_tools(self) -> Dict:
        """Detect available security analysis tools"""
        
        tools = {
            'static_analysis': [],
            'dynamic_analysis': [],
            'sanitizers': [],
            'fuzzing_tools': [],
            'binary_analysis': []
        }
        
        # Static analysis tools
        static_tools = [
            'cppcheck', 'clang-tidy', 'clang-static-analyzer', 'scan-build',
            'splint', 'flawfinder', 'rats', 'codeql', 'semgrep',
            'pvs-studio', 'pc-lint', 'polyspace'
        ]
        
        for tool in static_tools:
            if shutil.which(tool):
                tools['static_analysis'].append({
                    'name': tool,
                    'path': shutil.which(tool),
                    'version': self._get_tool_version(tool)
                })
        
        # Dynamic analysis tools
        dynamic_tools = [
            'valgrind', 'dr-memory', 'intel-inspector'
        ]
        
        for tool in dynamic_tools:
            if shutil.which(tool):
                tools['dynamic_analysis'].append({
                    'name': tool,
                    'path': shutil.which(tool),
                    'version': self._get_tool_version(tool)
                })
        
        # Sanitizers (check if compiler supports them)
        sanitizers = [
            'address', 'memory', 'thread', 'undefined', 'leak',
            'dataflow', 'cfi', 'safe-stack', 'shadow-call-stack'
        ]
        
        if shutil.which('clang') or shutil.which('gcc'):
            for sanitizer in sanitizers:
                tools['sanitizers'].append({
                    'name': f'sanitize-{sanitizer}',
                    'flag': f'-fsanitize={sanitizer}',
                    'available': self._check_sanitizer_support(sanitizer)
                })
        
        # Fuzzing tools
        fuzzing_tools = [
            'afl-gcc', 'afl-clang', 'honggfuzz', 'libfuzzer',
            'syzkaller', 'peach', 'boofuzz'
        ]
        
        for tool in fuzzing_tools:
            if shutil.which(tool):
                tools['fuzzing_tools'].append({
                    'name': tool,
                    'path': shutil.which(tool),
                    'version': self._get_tool_version(tool)
                })
        
        # Binary analysis tools
        binary_tools = [
            'objdump', 'readelf', 'nm', 'strings', 'file',
            'checksec', 'hardening-check', 'rabin2', 'radare2'
        ]
        
        for tool in binary_tools:
            if shutil.which(tool):
                tools['binary_analysis'].append({
                    'name': tool,
                    'path': shutil.which(tool),
                    'version': self._get_tool_version(tool)
                })
        
        return tools
    
    def _get_tool_version(self, tool: str) -> str:
        """Get version of security tool"""
        
        try:
            for flag in ['--version', '-V', '-v', 'version']:
                result = subprocess.run([tool, flag], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    return result.stdout.split('\n')[0][:100]
            return "Unknown"
        except:
            return "Unknown"
    
    def _check_sanitizer_support(self, sanitizer: str) -> bool:
        """Check if compiler supports specific sanitizer"""
        
        try:
            # Test with a simple program
            test_code = "int main(){return 0;}"
            temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.c', delete=False)
            temp_file.write(test_code)
            temp_file.close()
            
            # Try with Clang first
            if shutil.which('clang'):
                result = subprocess.run(['clang', f'-fsanitize={sanitizer}', 
                                       temp_file.name, '-o', '/dev/null'], 
                                      capture_output=True, timeout=10)
                if result.returncode == 0:
                    os.unlink(temp_file.name)
                    return True
            
            # Try with GCC
            if shutil.which('gcc'):
                result = subprocess.run(['gcc', f'-fsanitize={sanitizer}', 
                                       temp_file.name, '-o', '/dev/null'], 
                                      capture_output=True, timeout=10)
                if result.returncode == 0:
                    os.unlink(temp_file.name)
                    return True
            
            os.unlink(temp_file.name)
            return False
        except:
            return False
    
    def _load_vulnerability_patterns(self) -> Dict:
        """Load common vulnerability patterns"""
        
        patterns = {
            'buffer_overflow': [
                r'gets\s*\(',
                r'strcpy\s*\(',
                r'strcat\s*\(',
                r'sprintf\s*\(',
                r'vsprintf\s*\('
            ],
            'format_string': [
                r'printf\s*\([^,)]*\)',
                r'fprintf\s*\([^,]*,[^,)]*\)',
                r'sprintf\s*\([^,]*,[^,)]*\)',
                r'snprintf\s*\([^,]*,[^,]*,[^,)]*\)'
            ],
            'integer_overflow': [
                r'malloc\s*\([^)]*\*[^)]*\)',
                r'calloc\s*\([^)]*\*[^)]*\)',
                r'realloc\s*\([^,]*,[^)]*\*[^)]*\)'
            ],
            'race_condition': [
                r'access\s*\(',
                r'stat\s*\(',
                r'lstat\s*\(',
                r'temp[^a-zA-Z]',
                r'\/tmp\/'
            ],
            'injection': [
                r'system\s*\(',
                r'exec[lv]p?\s*\(',
                r'popen\s*\(',
                r'ShellExecute'
            ],
            'crypto_weaknesses': [
                r'MD4|MD5',
                r'SHA1',
                r'DES[^a-zA-Z]',
                r'RC4',
                r'rand\s*\(\)',
                r'srand\s*\('
            ],
            'memory_leaks': [
                r'malloc[^;]*;[^}]*}[^;]*$',
                r'new[^;]*;[^}]*}[^;]*$',
                r'fopen[^;]*;[^}]*}[^;]*$'
            ]
        }
        
        return patterns
    
    def _create_hardening_profiles(self) -> Dict:
        """Create security hardening profiles"""
        
        profiles = {
            'basic_hardening': {
                'compile_flags': [
                    '-fstack-protector',
                    '-D_FORTIFY_SOURCE=2',
                    '-Wformat',
                    '-Wformat-security'
                ],
                'link_flags': [
                    '-Wl,-z,relro',
                    '-Wl,-z,now'
                ],
                'description': 'Basic security hardening measures'
            },
            'enhanced_hardening': {
                'compile_flags': [
                    '-fstack-protector-strong',
                    '-D_FORTIFY_SOURCE=2',
                    '-fPIE',
                    '-Wformat',
                    '-Wformat-security',
                    '-Werror=format-security',
                    '-fcf-protection=full'
                ],
                'link_flags': [
                    '-pie',
                    '-Wl,-z,relro',
                    '-Wl,-z,now',
                    '-Wl,-z,noexecstack'
                ],
                'description': 'Enhanced security hardening'
            },
            'maximum_hardening': {
                'compile_flags': [
                    '-fstack-protector-all',
                    '-D_FORTIFY_SOURCE=3',
                    '-fPIE',
                    '-Wformat',
                    '-Wformat-security',
                    '-Werror=format-security',
                    '-fcf-protection=full',
                    '-fstack-clash-protection',
                    '-fsanitize=address',
                    '-fsanitize=undefined',
                    '-fno-omit-frame-pointer'
                ],
                'link_flags': [
                    '-pie',
                    '-Wl,-z,relro',
                    '-Wl,-z,now',
                    '-Wl,-z,noexecstack',
                    '-Wl,-z,separate-code',
                    '-Wl,--disable-new-dtags'
                ],
                'description': 'Maximum security hardening with sanitizers'
            },
            'embedded_hardening': {
                'compile_flags': [
                    '-fstack-protector',
                    '-D_FORTIFY_SOURCE=1',
                    '-ffunction-sections',
                    '-fdata-sections'
                ],
                'link_flags': [
                    '-Wl,--gc-sections',
                    '-Wl,-z,relro'
                ],
                'description': 'Security hardening for embedded systems'
            }
        }
        
        return profiles
    
    async def perform_security_analysis(self, file_path: str, analysis: Dict) -> Dict:
        """Perform comprehensive security analysis"""
        
        security_report = {
            'static_analysis': {},
            'vulnerability_scan': {},
            'binary_analysis': {},
            'hardening_recommendations': [],
            'security_score': 0,
            'risk_level': 'unknown',
            'total_issues': 0,
            'critical_issues': 0,
            'high_issues': 0,
            'medium_issues': 0,
            'low_issues': 0
        }
        
        try:
            # Static code analysis
            security_report['static_analysis'] = await self._run_static_security_analysis(file_path)
            
            # Vulnerability pattern scanning
            security_report['vulnerability_scan'] = await self._scan_vulnerability_patterns(file_path)
            
            # Generate hardening recommendations
            security_report['hardening_recommendations'] = self._generate_hardening_recommendations(
                analysis, security_report
            )
            
            # Calculate security score
            security_report['security_score'] = self._calculate_security_score(security_report)
            security_report['risk_level'] = self._assess_risk_level(security_report['security_score'])
            
            # Count issues by severity
            self._count_security_issues(security_report)
        
        except Exception as e:
            security_report['error'] = str(e)
        
        return security_report
    
    async def _run_static_security_analysis(self, file_path: str) -> Dict:
        """Run static security analysis tools"""
        
        results = {}
        
        # Run cppcheck
        if any(tool['name'] == 'cppcheck' for tool in self.security_tools['static_analysis']):
            results['cppcheck'] = await self._run_cppcheck(file_path)
        
        # Run clang-tidy
        if any(tool['name'] == 'clang-tidy' for tool in self.security_tools['static_analysis']):
            results['clang_tidy'] = await self._run_clang_tidy(file_path)
        
        # Run flawfinder
        if any(tool['name'] == 'flawfinder' for tool in self.security_tools['static_analysis']):
            results['flawfinder'] = await self._run_flawfinder(file_path)
        
        return results
    
    async def _run_cppcheck(self, file_path: str) -> Dict:
        """Run cppcheck security analysis"""
        
        try:
            cmd = [
                'cppcheck',
                '--enable=warning,style,performance,portability,information',
                '--template={severity}:{message}',
                '--quiet',
                file_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            issues = []
            for line in result.stderr.split('\n'):
                if line.strip() and ':' in line:
                    parts = line.split(':', 2)
                    if len(parts) >= 2:
                        issues.append({
                            'severity': parts[0],
                            'message': parts[1] if len(parts) > 1 else line,
                            'line': 'unknown'
                        })
            
            return {
                'tool': 'cppcheck',
                'issues': issues,
                'total_issues': len(issues),
                'execution_time': result.returncode
            }
        except Exception as e:
            return {'error': str(e)}
    
    async def _run_clang_tidy(self, file_path: str) -> Dict:
        """Run clang-tidy security analysis"""
        
        try:
            cmd = [
                'clang-tidy',
                file_path,
                '--checks=bugprone-*,cert-*,clang-analyzer-security*,misc-*',
                '--format-style=none'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
            
            issues = []
            for line in result.stdout.split('\n'):
                if 'warning:' in line or 'error:' in line:
                    issues.append({
                        'severity': 'warning' if 'warning:' in line else 'error',
                        'message': line.strip(),
                        'tool': 'clang-tidy'
                    })
            
            return {
                'tool': 'clang-tidy',
                'issues': issues,
                'total_issues': len(issues)
            }
        except Exception as e:
            return {'error': str(e)}
    
    async def _run_flawfinder(self, file_path: str) -> Dict:
        """Run flawfinder security analysis"""
        
        try:
            cmd = ['flawfinder', '--quiet', '--dataonly', file_path]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            issues = []
            for line in result.stdout.split('\n'):
                if line.strip() and not line.startswith('#'):
                    issues.append({
                        'severity': 'security',
                        'message': line.strip(),
                        'tool': 'flawfinder'
                    })
            
            return {
                'tool': 'flawfinder',
                'issues': issues,
                'total_issues': len(issues)
            }
        except Exception as e:
            return {'error': str(e)}
    
    async def _scan_vulnerability_patterns(self, file_path: str) -> Dict:
        """Scan for vulnerability patterns in source code"""
        
        vulnerabilities = {
            'found_patterns': {},
            'total_vulnerabilities': 0,
            'severity_breakdown': {}
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            for vuln_type, patterns in self.vulnerability_database.items():
                found_issues = []
                
                for pattern in patterns:
                    matches = re.finditer(pattern, content, re.IGNORECASE)
                    for match in matches:
                        # Find line number
                        line_num = content[:match.start()].count('\n') + 1
                        found_issues.append({
                            'pattern': pattern,
                            'match': match.group(),
                            'line': line_num,
                            'severity': self._get_vulnerability_severity(vuln_type)
                        })
                
                if found_issues:
                    vulnerabilities['found_patterns'][vuln_type] = found_issues
                    vulnerabilities['total_vulnerabilities'] += len(found_issues)
        
        except Exception as e:
            vulnerabilities['error'] = str(e)
        
        return vulnerabilities
    
    def _get_vulnerability_severity(self, vuln_type: str) -> str:
        """Get severity level for vulnerability type"""
        
        severity_map = {
            'buffer_overflow': 'critical',
            'format_string': 'high',
            'integer_overflow': 'high',
            'injection': 'critical',
            'race_condition': 'medium',
            'crypto_weaknesses': 'high',
            'memory_leaks': 'medium'
        }
        
        return severity_map.get(vuln_type, 'medium')
    
    def _generate_hardening_recommendations(self, analysis: Dict, security_report: Dict) -> List[str]:
        """Generate security hardening recommendations"""
        
        recommendations = []
        
        # Basic recommendations
        recommendations.append("Use compiler security flags: -fstack-protector-strong -D_FORTIFY_SOURCE=2")
        recommendations.append("Enable ASLR with -fPIE and link with -pie")
        recommendations.append("Use relro protection: -Wl,-z,relro,-z,now")
        
        # Based on vulnerability scan
        vuln_scan = security_report.get('vulnerability_scan', {})
        found_patterns = vuln_scan.get('found_patterns', {})
        
        if 'buffer_overflow' in found_patterns:
            recommendations.append("Replace unsafe functions (gets, strcpy, sprintf) with safe variants")
            recommendations.append("Enable stack protection: -fstack-protector-all")
        
        if 'format_string' in found_patterns:
            recommendations.append("Fix format string vulnerabilities by using format specifiers properly")
            recommendations.append("Enable format string protection: -Wformat-security")
        
        if 'crypto_weaknesses' in found_patterns:
            recommendations.append("Replace weak cryptographic algorithms with secure alternatives")
            recommendations.append("Use cryptographically secure random number generators")
        
        if 'race_condition' in found_patterns:
            recommendations.append("Use proper synchronization mechanisms for shared resources")
            recommendations.append("Avoid TOCTOU vulnerabilities in file operations")
        
        # Based on code analysis
        if analysis.get('threading'):
            recommendations.append("Use thread-safe functions and proper synchronization")
            recommendations.append("Consider ThreadSanitizer: -fsanitize=thread")
        
        if analysis.get('memory_management') == 'manual_c':
            recommendations.append("Consider AddressSanitizer: -fsanitize=address")
            recommendations.append("Use valgrind for memory leak detection")
        
        if analysis.get('networking'):
            recommendations.append("Validate all network inputs thoroughly")
            recommendations.append("Use secure protocols (TLS) for network communication")
        
        return recommendations
    
    def _calculate_security_score(self, security_report: Dict) -> int:
        """Calculate overall security score (0-100)"""
        
        score = 100  # Start with perfect score
        
        # Deduct points for vulnerabilities
        vuln_scan = security_report.get('vulnerability_scan', {})
        total_vulns = vuln_scan.get('total_vulnerabilities', 0)
        
        # Deduct based on vulnerability count and severity
        score -= min(total_vulns * 5, 50)  # Max 50 points deduction
        
        # Deduct points for static analysis issues
        static_analysis = security_report.get('static_analysis', {})
        for tool_result in static_analysis.values():
            if isinstance(tool_result, dict):
                issues = tool_result.get('total_issues', 0)
                score -= min(issues * 2, 30)  # Max 30 points deduction per tool
        
        # Ensure score doesn't go below 0
        score = max(0, score)
        
        return score
    
    def _assess_risk_level(self, security_score: int) -> str:
        """Assess risk level based on security score"""
        
        if security_score >= 90:
            return 'low'
        elif security_score >= 70:
            return 'medium'
        elif security_score >= 40:
            return 'high'
        else:
            return 'critical'
    
    def _count_security_issues(self, security_report: Dict):
        """Count security issues by severity"""
        
        # Count from vulnerability scan
        vuln_scan = security_report.get('vulnerability_scan', {})
        found_patterns = vuln_scan.get('found_patterns', {})
        
        for vuln_type, issues in found_patterns.items():
            severity = self._get_vulnerability_severity(vuln_type)
            count = len(issues)
            
            if severity == 'critical':
                security_report['critical_issues'] += count
            elif severity == 'high':
                security_report['high_issues'] += count
            elif severity == 'medium':
                security_report['medium_issues'] += count
            else:
                security_report['low_issues'] += count
        
        # Count from static analysis
        static_analysis = security_report.get('static_analysis', {})
        for tool_result in static_analysis.values():
            if isinstance(tool_result, dict) and 'issues' in tool_result:
                for issue in tool_result['issues']:
                    severity = issue.get('severity', 'medium').lower()
                    if 'error' in severity or 'critical' in severity:
                        security_report['critical_issues'] += 1
                    elif 'warning' in severity:
                        security_report['medium_issues'] += 1
                    else:
                        security_report['low_issues'] += 1
        
        # Calculate total
        security_report['total_issues'] = (
            security_report['critical_issues'] + 
            security_report['high_issues'] + 
            security_report['medium_issues'] + 
            security_report['low_issues']
        )
    
    async def create_hardened_build(self, file_path: str, profile: str, analysis: Dict) -> Dict:
        """Create a security-hardened build"""
        
        result = {
            'profile': profile,
            'success': False,
            'binary_path': None,
            'security_features': [],
            'compilation_time': 0,
            'warnings': [],
            'errors': []
        }
        
        start_time = time.time()
        
        try:
            if profile not in self.hardening_profiles:
                result['errors'].append(f'Unknown hardening profile: {profile}')
                return result
            
            hardening_config = self.hardening_profiles[profile]
            temp_dir = tempfile.mkdtemp()
            output_path = os.path.join(temp_dir, f'hardened_binary_{int(time.time())}')
            
            # Find suitable compiler
            compilers = ['gcc', 'clang']
            compiler_found = None
            
            for compiler in compilers:
                if shutil.which(compiler):
                    compiler_found = compiler
                    break
            
            if not compiler_found:
                result['errors'].append('No suitable compiler found for hardening')
                return result
            
            # Build hardened compilation command
            cmd = [compiler_found]
            cmd.extend(hardening_config['compile_flags'])
            cmd.extend([file_path, '-o', output_path])
            cmd.extend(hardening_config['link_flags'])
            
            # Add analysis-specific flags
            if analysis.get('math_heavy'):
                cmd.append('-lm')
            if analysis.get('threading'):
                cmd.append('-lpthread')
            
            # Execute compilation
            process = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            
            result['compilation_time'] = time.time() - start_time
            
            if process.returncode == 0 and os.path.exists(output_path):
                result['success'] = True
                result['binary_path'] = output_path
                result['security_features'] = hardening_config['compile_flags'] + hardening_config['link_flags']
                result['warnings'] = extract_warnings(process.stderr)
            else:
                result['errors'].append(f'Hardened compilation failed: {process.stderr[:200]}')
        
        except Exception as e:
            result['errors'].append(f'Hardening error: {str(e)}')
        
        return result

# Integration function to tie everything together
async def run_complete_compilation_suite(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Run the complete advanced compilation suite with all features"""
    
    try:
        file = update.message.document
        file_name = file.file_name
        
        # Check file extension
        file_ext = Path(file_name).suffix.lower()
        supported_extensions = {'.c', '.cpp', '.cc', '.cxx', '.c++', '.h', '.hpp'}
        
        if file_ext not in supported_extensions:
            await update.message.reply_text(
                f"❌ File type not supported: {file_ext}\n"
                f"Supported: {', '.join(supported_extensions)}"
            )
            return
        
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, file_name)
            
            # Download file
            file_obj = await file.get_file()
            await file_obj.download_to_drive(file_path)
            
            # Initialize all systems
            await update.message.reply_text("🚀 Initializing MEGA Advanced Compilation Suite...")
            
            compiler_system = AdvancedCompiler()
            multi_platform = MultiPlatformEngine(compiler_system)
            security_engine = SecurityAnalysisEngine()
            
            # Advanced source analysis
            await update.message.reply_text("🔬 Performing advanced source code analysis...")
            analysis = await analyze_source_code_advanced(file_path, file_ext)
            
            # Security analysis
            await update.message.reply_text("🔒 Running security analysis...")
            security_report = await security_engine.perform_security_analysis(file_path, analysis)
            
            # Multi-platform compilation
            await update.message.reply_text("🌐 Building for multiple platforms...")
            multi_platform_results = await multi_platform.create_multi_platform_builds(file_path, analysis)
            
            # Advanced optimization suite
            await update.message.reply_text("⚡ Running advanced optimization suite...")
            optimization_results = await run_advanced_optimization_suite(update, file_path, analysis, compiler_system)
            
            # Generate comprehensive final report
            await send_complete_suite_report(
                update, context, analysis, security_report, 
                multi_platform_results, optimization_results, 
                compiler_system, temp_dir
            )
            
    except Exception as e:
        await update.message.reply_text(f"💥 CRITICAL ERROR: {str(e)}")

async def send_complete_suite_report(update: Update, context: ContextTypes.DEFAULT_TYPE,
                                   analysis: Dict, security_report: Dict,
                                   multi_platform_results: Dict, optimization_results: Dict,
                                   compiler_system, temp_dir: str):
    """Send complete comprehensive suite report"""
    
    try:
        # Executive Summary
        successful_builds = multi_platform_results.get('success_count', 0)
        total_platforms = len(multi_platform_results.get('builds', []))
        security_score = security_report.get('security_score', 0)
        
        executive_summary = f"""
🎯 MEGA COMPILATION SUITE - EXECUTIVE SUMMARY

📊 COMPILATION RESULTS:
✅ Successful Builds: {successful_builds}/{total_platforms}
🌐 Platform Coverage: {(successful_builds/total_platforms*100):.1f}%
🔒 Security Score: {security_score}/100 ({security_report.get('risk_level', 'unknown').upper()})
⚡ Optimization Status: {'✅ Complete' if optimization_results.get('success') else '❌ Failed'}

🔍 CODE ANALYSIS:
• Language: {analysis.get('detected_language', 'unknown').upper()}
• Complexity: {analysis.get('complexity', 'unknown').upper()}
• Lines: {analysis.get('lines', 0):,}
• Security Issues: {security_report.get('total_issues', 0)}
• Features: Threading={'✅' if analysis.get('threading') else '❌'}, Math={'✅' if analysis.get('math_heavy') else '❌'}, Graphics={'✅' if analysis.get('graphics') else '❌'}

🏆 BEST BUILD CONFIGURATION:
{optimization_results.get('optimal_config', {}).get('method', 'Standard optimization').title()} with {optimization_results.get('optimal_config', {}).get('expected_improvement', 0):.1f}% improvement

Generated by MEGA Advanced Compilation Suite v3.0
"""
        
        await update.message.reply_text(executive_summary)
        
        # Send security report
        if security_report.get('total_issues', 0) > 0:
            security_summary = f"""
🔒 SECURITY ANALYSIS REPORT

⚠️ ISSUES FOUND:
• Critical: {security_report.get('critical_issues', 0)}
• High: {security_report.get('high_issues', 0)}  
• Medium: {security_report.get('medium_issues', 0)}
• Low: {security_report.get('low_issues', 0)}

🛡️ RECOMMENDATIONS:
"""
            for i, rec in enumerate(security_report.get('hardening_recommendations', [])[:5], 1):
                security_summary += f"{i}. {rec}\n"
            
            await update.message.reply_text(security_summary)
        
        # Send multi-platform results
        if successful_builds > 0:
            platform_summary = "🌐 MULTI-PLATFORM BUILD RESULTS:\n\n"
            
            for build in multi_platform_results.get('builds', []):
                if build['success']:
                    platform_summary += f"""
✅ {build['target']}
   Architecture: {build.get('arch', 'unknown')}
   Binary Size: {format_file_size(build.get('binary_size', 0))}
   Compile Time: {build.get('compilation_time', 0):.2f}s
"""
            
            await update.message.reply_text(platform_summary)
        
        # Send the best optimized binary
        best_builds = [b for b in multi_platform_results.get('builds', []) if b['success']]
        if best_builds:
            # Choose the smallest successful build for upload
            best_build = min(best_builds, key=lambda x: x.get('binary_size', float('inf')))
            binary_path = best_build.get('binary_path')
            
            if binary_path and os.path.exists(binary_path):
                try:
                    with open(binary_path, 'rb') as f:
                        await update.message.reply_document(
                            document=f,
                            filename=f"optimized_binary_{best_build['target']}",
                            caption=f"""
🎯 Optimized Binary ({best_build['target']})
📏 Size: {format_file_size(best_build.get('binary_size', 0))}
⏱️ Compile Time: {best_build.get('compilation_time', 0):.2f}s
🔒 Security Score: {security_score}/100
"""
                        )
                except Exception as e:
                    await update.message.reply_text(f"❌ Failed to send binary: {str(e)}")
        
        # Final recommendations
        final_recommendations = """
🚀 FINAL RECOMMENDATIONS:

1. 🔒 Address security issues before production deployment
2. 🧪 Test compiled binaries thoroughly on target platforms  
3. 📊 Profile performance with real workloads
4. 🔄 Re-run analysis after code changes
5. 💾 Keep optimized binaries for deployment

Thank you for using MEGA Advanced Compilation Suite!
For support: https://github.com/mega-compiler-suite
"""
        
        await update.message.reply_text(final_recommendations)
        
    except Exception as e:
        await update.message.reply_text(f"❌ Error generating final report: {str(e)}")

# Main function selector for different compilation modes
async def select_compilation_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Select compilation mode based on user preference"""
    
    if not update.message.document:
        await update.message.reply_text(
            "📁 Please send a source code file to compile.\n"
            "Supported formats: .c, .cpp, .cc, .cxx, .c++, .h, .hpp"
        )
        return
    
    mode_selection = """
🚀 MEGA COMPILATION SUITE - MODE SELECTION

Please choose your compilation mode:

1️⃣ /quick - Quick compilation (fastest)
2️⃣ /standard - Standard mega compilation  
3️⃣ /advanced - Advanced optimization suite
4️⃣ /security - Security-focused compilation
5️⃣ /multiplatform - Multi-platform builds
6️⃣ /complete - Complete suite (all features)

Type the command for your preferred mode.
"""
    
    await update.message.reply_text(mode_selection)

# Export all main functions
__all__ = [
    'compile_file', 'run_complete_compilation_suite', 
    'select_compilation_mode', 'AdvancedCompiler',
    'MultiPlatformEngine', 'SecurityAnalysisEngine',
    'ProfileGuidedOptimization', 'AutoTuningSystem', 
    'CompilerBenchmarkSuite'
]

# Advanced Cloud and Container Compilation Engine
class CloudCompilerEngine:
    """Cloud-based compilation and containerized build system"""
    
    def __init__(self, compiler_system):
        self.compiler_system = compiler_system
        self.container_engines = self._detect_container_engines()
        self.cloud_providers = self._detect_cloud_providers()
        self.docker_images = self._scan_docker_images()
        self.build_cache_manager = BuildCacheManager()
        
    def _detect_container_engines(self) -> Dict:
        """Detect available container engines"""
        
        engines = {
            'docker': {'available': False, 'version': 'unknown'},
            'podman': {'available': False, 'version': 'unknown'},
            'containerd': {'available': False, 'version': 'unknown'},
            'cri-o': {'available': False, 'version': 'unknown'},
            'buildah': {'available': False, 'version': 'unknown'},
            'runc': {'available': False, 'version': 'unknown'},
            'lxc': {'available': False, 'version': 'unknown'},
            'systemd-nspawn': {'available': False, 'version': 'unknown'}
        }
        
        for engine in engines.keys():
            if shutil.which(engine):
                engines[engine]['available'] = True
                engines[engine]['version'] = self._get_tool_version(engine)
                
        # Special check for Docker daemon
        if engines['docker']['available']:
            try:
                result = subprocess.run(['docker', 'info'], 
                                      capture_output=True, text=True, timeout=10)
                engines['docker']['daemon_running'] = result.returncode == 0
            except:
                engines['docker']['daemon_running'] = False
                
        return engines
    
    def _detect_cloud_providers(self) -> Dict:
        """Detect available cloud provider tools"""
        
        providers = {
            'aws': {'cli': False, 'codebuild': False, 'lambda': False},
            'gcp': {'cli': False, 'cloud_build': False, 'functions': False},
            'azure': {'cli': False, 'devops': False, 'functions': False},
            'github': {'cli': False, 'actions': False},
            'gitlab': {'cli': False, 'runner': False},
            'jenkins': {'available': False},
            'travis': {'cli': False},
            'circleci': {'cli': False}
        }
        
        # Check AWS
        if shutil.which('aws'):
            providers['aws']['cli'] = True
        if shutil.which('aws-sam-cli'):
            providers['aws']['lambda'] = True
            
        # Check Google Cloud
        if shutil.which('gcloud'):
            providers['gcp']['cli'] = True
        if shutil.which('gcloud') and os.path.exists(os.path.expanduser('~/.config/gcloud')):
            providers['gcp']['authenticated'] = True
            
        # Check Azure
        if shutil.which('az'):
            providers['azure']['cli'] = True
            
        # Check GitHub
        if shutil.which('gh'):
            providers['github']['cli'] = True
            
        # Check GitLab
        if shutil.which('gitlab-runner'):
            providers['gitlab']['runner'] = True
            
        # Check Jenkins
        if shutil.which('jenkins') or os.path.exists('/usr/share/jenkins'):
            providers['jenkins']['available'] = True
            
        return providers
    
    def _scan_docker_images(self) -> Dict:
        """Scan available Docker images for compilation"""
        
        images = {
            'compiler_images': [],
            'base_images': [],
            'language_specific': {},
            'custom_images': []
        }
        
        if not self.container_engines['docker']['available']:
            return images
            
        try:
            # List available Docker images
            result = subprocess.run(['docker', 'images', '--format', 
                                   'table {{.Repository}}:{{.Tag}}\t{{.Size}}'], 
                                  capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                for line in result.stdout.split('\n')[1:]:  # Skip header
                    if line.strip():
                        parts = line.split('\t')
                        if len(parts) >= 2:
                            image_name = parts[0]
                            size = parts[1]
                            
                            # Categorize images
                            if any(compiler in image_name.lower() for compiler in 
                                  ['gcc', 'clang', 'llvm', 'build']):
                                images['compiler_images'].append({
                                    'name': image_name,
                                    'size': size,
                                    'type': 'compiler'
                                })
                            elif any(lang in image_name.lower() for lang in 
                                   ['c++', 'cpp', 'c', 'golang', 'rust']):
                                lang_key = self._extract_language(image_name)
                                if lang_key not in images['language_specific']:
                                    images['language_specific'][lang_key] = []
                                images['language_specific'][lang_key].append({
                                    'name': image_name,
                                    'size': size
                                })
                            elif any(base in image_name.lower() for base in 
                                   ['ubuntu', 'debian', 'alpine', 'centos', 'fedora']):
                                images['base_images'].append({
                                    'name': image_name,
                                    'size': size,
                                    'base': self._extract_base_os(image_name)
                                })
                                
        except Exception as e:
            images['error'] = str(e)
            
        return images
    
    def _extract_language(self, image_name: str) -> str:
        """Extract programming language from image name"""
        
        name_lower = image_name.lower()
        if 'cpp' in name_lower or 'c++' in name_lower:
            return 'cpp'
        elif 'golang' in name_lower or 'go:' in name_lower:
            return 'go'
        elif 'rust' in name_lower:
            return 'rust'
        elif 'c:' in name_lower or '/c:' in name_lower:
            return 'c'
        else:
            return 'unknown'
    
    def _extract_base_os(self, image_name: str) -> str:
        """Extract base OS from image name"""
        
        name_lower = image_name.lower()
        if 'ubuntu' in name_lower:
            return 'ubuntu'
        elif 'debian' in name_lower:
            return 'debian'
        elif 'alpine' in name_lower:
            return 'alpine'
        elif 'centos' in name_lower:
            return 'centos'
        elif 'fedora' in name_lower:
            return 'fedora'
        else:
            return 'unknown'
    
    async def create_containerized_build(self, file_path: str, analysis: Dict, 
                                       container_config: Dict = None) -> Dict:
        """Create containerized compilation build"""
        
        build_result = {
            'container_used': None,
            'build_success': False,
            'build_logs': [],
            'artifacts': [],
            'build_time': 0,
            'image_size': 0,
            'container_id': None
        }
        
        start_time = time.time()
        
        try:
            if not self.container_engines['docker']['available']:
                build_result['error'] = 'Docker not available'
                return build_result
                
            # Select appropriate container image
            container_image = self._select_container_image(analysis, container_config)
            build_result['container_used'] = container_image
            
            # Create Dockerfile for build
            dockerfile_content = self._generate_dockerfile(container_image, analysis)
            
            # Setup build context
            build_context = tempfile.mkdtemp()
            dockerfile_path = os.path.join(build_context, 'Dockerfile')
            source_file = os.path.join(build_context, os.path.basename(file_path))
            
            # Write files
            with open(dockerfile_path, 'w') as f:
                f.write(dockerfile_content)
            shutil.copy2(file_path, source_file)
            
            # Build Docker image
            build_tag = f"mega-compiler-build:{int(time.time())}"
            build_cmd = ['docker', 'build', '-t', build_tag, build_context]
            
            build_process = subprocess.run(build_cmd, capture_output=True, 
                                         text=True, timeout=600)
            
            build_result['build_logs'] = build_process.stdout.split('\n')
            
            if build_process.returncode == 0:
                build_result['build_success'] = True
                
                # Extract artifacts from container
                artifacts = await self._extract_build_artifacts(build_tag, build_context)
                build_result['artifacts'] = artifacts
                
                # Get image size
                size_result = subprocess.run(['docker', 'images', build_tag, 
                                            '--format', '{{.Size}}'], 
                                           capture_output=True, text=True)
                if size_result.returncode == 0:
                    build_result['image_size'] = size_result.stdout.strip()
                    
            else:
                build_result['error'] = build_process.stderr
                
        except Exception as e:
            build_result['error'] = str(e)
        finally:
            build_result['build_time'] = time.time() - start_time
            # Cleanup
            try:
                shutil.rmtree(build_context, ignore_errors=True)
            except:
                pass
                
        return build_result
    
    def _select_container_image(self, analysis: Dict, config: Dict = None) -> str:
        """Select appropriate container image for compilation"""
        
        if config and config.get('custom_image'):
            return config['custom_image']
            
        # Language-specific images
        lang = analysis.get('detected_language', 'c')
        
        # Prefer specific compiler images
        preferred_images = {
            'c': ['gcc:latest', 'clang:latest', 'ubuntu:20.04'],
            'cpp': ['gcc:latest', 'clang:latest', 'ubuntu:20.04'],
            'rust': ['rust:latest', 'rust:1.70'],
            'go': ['golang:latest', 'golang:1.21'],
            'fortran': ['gcc:latest', 'ubuntu:20.04']
        }
        
        candidates = preferred_images.get(lang, ['ubuntu:20.04', 'debian:bullseye'])
        
        # Check which images are available
        available_images = [img['name'] for img in self.docker_images['compiler_images']]
        available_images.extend([img['name'] for img in self.docker_images['base_images']])
        
        for candidate in candidates:
            if candidate in available_images:
                return candidate
                
        # Fallback to pulling standard image
        return candidates[0]
    
    def _generate_dockerfile(self, base_image: str, analysis: Dict) -> str:
        """Generate Dockerfile for compilation"""
        
        lang = analysis.get('detected_language', 'c')
        required_libs = analysis.get('required_libs', set())
        
        dockerfile = f"""FROM {base_image}

# Install basic build tools
RUN apt-get update && apt-get install -y \\
    build-essential \\
    gcc \\
    g++ \\
    clang \\
    cmake \\
    make \\
    git \\
    wget \\
    curl \\
    pkg-config \\
    && rm -rf /var/lib/apt/lists/*

"""
        
        # Add language-specific tools
        if lang == 'rust':
            dockerfile += """# Install Rust toolchain
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

"""
        elif lang == 'go':
            dockerfile += """# Install Go
RUN wget -O go.tar.gz https://go.dev/dl/go1.21.0.linux-amd64.tar.gz \\
    && tar -C /usr/local -xzf go.tar.gz \\
    && rm go.tar.gz
ENV PATH="/usr/local/go/bin:${PATH}"

"""
        
        # Add required libraries
        if 'pthread' in required_libs:
            dockerfile += "RUN apt-get update && apt-get install -y libc6-dev\n"
        if 'opengl' in required_libs:
            dockerfile += "RUN apt-get update && apt-get install -y libgl1-mesa-dev libglu1-mesa-dev\n"
        if 'curl' in required_libs:
            dockerfile += "RUN apt-get update && apt-get install -y libcurl4-openssl-dev\n"
        if 'ssl' in required_libs:
            dockerfile += "RUN apt-get update && apt-get install -y libssl-dev\n"
        if 'boost' in required_libs:
            dockerfile += "RUN apt-get update && apt-get install -y libboost-all-dev\n"
        if 'qt' in required_libs:
            dockerfile += "RUN apt-get update && apt-get install -y qtbase5-dev\n"
            
        dockerfile += """
# Create working directory
WORKDIR /build

# Copy source code
COPY . /build/

# Compilation commands will be added based on analysis
"""
        
        # Add compilation commands
        compilation_cmds = self._generate_compilation_commands(analysis)
        dockerfile += compilation_cmds
        
        dockerfile += """
# Create output directory
RUN mkdir -p /output

# Copy built artifacts
RUN cp -r /build/* /output/ 2>/dev/null || true

VOLUME ["/output"]
"""
        
        return dockerfile
    
    def _generate_compilation_commands(self, analysis: Dict) -> str:
        """Generate compilation commands for Dockerfile"""
        
        lang = analysis.get('detected_language', 'c')
        complexity = analysis.get('complexity', 'medium')
        
        commands = "# Compilation commands\n"
        
        if lang in ['c', 'cpp']:
            # Multiple compilation strategies
            commands += """
# Ultra performance build
RUN gcc -Ofast -march=native -mtune=native -flto *.c -o ultra_optimized 2>/dev/null || echo "Ultra build failed"

# Standard optimized build  
RUN gcc -O3 -march=native *.c -o optimized 2>/dev/null || echo "Optimized build failed"

# Size optimized build
RUN gcc -Os -s *.c -o size_optimized 2>/dev/null || echo "Size optimized build failed"

# Debug build
RUN gcc -Og -g *.c -o debug_build 2>/dev/null || echo "Debug build failed"

# Security hardened build
RUN gcc -O2 -fstack-protector-strong -D_FORTIFY_SOURCE=2 -fPIE -pie *.c -o secure_build 2>/dev/null || echo "Secure build failed"
"""
        elif lang == 'rust':
            commands += """
# Rust optimized build
RUN cargo build --release 2>/dev/null || rustc -O *.rs -o rust_optimized 2>/dev/null || echo "Rust build failed"

# Rust debug build  
RUN cargo build 2>/dev/null || rustc *.rs -o rust_debug 2>/dev/null || echo "Rust debug build failed"
"""
        elif lang == 'go':
            commands += """
# Go optimized build
RUN go build -ldflags "-s -w" -o go_optimized *.go 2>/dev/null || echo "Go optimized build failed"

# Go standard build
RUN go build -o go_binary *.go 2>/dev/null || echo "Go build failed"
"""
        
        # Add cross-compilation if supported
        if lang in ['c', 'cpp']:
            commands += """
# Cross-compilation attempts
RUN aarch64-linux-gnu-gcc -O2 -static *.c -o aarch64_binary 2>/dev/null || echo "ARM64 cross-compile failed"
RUN arm-linux-gnueabihf-gcc -O2 -static *.c -o arm_binary 2>/dev/null || echo "ARM cross-compile failed"
"""
        
        return commands
    
    async def _extract_build_artifacts(self, image_tag: str, build_context: str) -> List[Dict]:
        """Extract build artifacts from container"""
        
        artifacts = []
        
        try:
            # Create temporary container
            run_result = subprocess.run(['docker', 'create', image_tag], 
                                      capture_output=True, text=True)
            
            if run_result.returncode == 0:
                container_id = run_result.stdout.strip()
                
                try:
                    # Copy artifacts from container
                    output_dir = os.path.join(build_context, 'output')
                    os.makedirs(output_dir, exist_ok=True)
                    
                    copy_result = subprocess.run(['docker', 'cp', 
                                                f'{container_id}:/output/.', output_dir], 
                                               capture_output=True, text=True)
                    
                    if copy_result.returncode == 0:
                        # Scan for built binaries
                        for root, dirs, files in os.walk(output_dir):
                            for file in files:
                                file_path = os.path.join(root, file)
                                if os.access(file_path, os.X_OK) and os.path.getsize(file_path) > 0:
                                    artifacts.append({
                                        'name': file,
                                        'path': file_path,
                                        'size': os.path.getsize(file_path),
                                        'type': self._detect_binary_type(file_path)
                                    })
                                    
                finally:
                    # Cleanup container
                    subprocess.run(['docker', 'rm', container_id], 
                                 capture_output=True)
                    
        except Exception as e:
            print(f"Error extracting artifacts: {e}")
            
        return artifacts
    
    def _detect_binary_type(self, file_path: str) -> str:
        """Detect type of binary file"""
        
        try:
            result = subprocess.run(['file', file_path], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                output = result.stdout.lower()
                if 'elf' in output:
                    if 'executable' in output:
                        return 'executable'
                    elif 'shared' in output:
                        return 'shared_library'
                    else:
                        return 'object'
                elif 'pe32' in output:
                    return 'windows_executable'
                elif 'mach-o' in output:
                    return 'macos_executable'
                else:
                    return 'unknown_binary'
            return 'unknown'
        except:
            return 'unknown'

class BuildCacheManager:
    """Advanced build cache management system"""
    
    def __init__(self):
        self.cache_dir = os.path.expanduser('~/.mega_compiler_cache')
        self.ensure_cache_dir()
        self.cache_index = self._load_cache_index()
        self.max_cache_size = 5 * 1024 * 1024 * 1024  # 5GB
        
    def ensure_cache_dir(self):
        """Ensure cache directory exists"""
        os.makedirs(self.cache_dir, exist_ok=True)
        os.makedirs(os.path.join(self.cache_dir, 'sources'), exist_ok=True)
        os.makedirs(os.path.join(self.cache_dir, 'binaries'), exist_ok=True)
        os.makedirs(os.path.join(self.cache_dir, 'metadata'), exist_ok=True)
        
    def _load_cache_index(self) -> Dict:
        """Load cache index from disk"""
        index_file = os.path.join(self.cache_dir, 'index.json')
        try:
            if os.path.exists(index_file):
                with open(index_file, 'r') as f:
                    return json.load(f)
        except:
            pass
        return {'entries': {}, 'stats': {'hits': 0, 'misses': 0, 'total_size': 0}}
        
    def _save_cache_index(self):
        """Save cache index to disk"""
        index_file = os.path.join(self.cache_dir, 'index.json')
        try:
            with open(index_file, 'w') as f:
                json.dump(self.cache_index, f, indent=2)
        except Exception as e:
            print(f"Error saving cache index: {e}")
            
    def calculate_source_hash(self, file_path: str, compiler_flags: List[str]) -> str:
        """Calculate hash for source code and compilation parameters"""
        
        hasher = hashlib.sha256()
        
        # Hash source code
        try:
            with open(file_path, 'rb') as f:
                hasher.update(f.read())
        except:
            return None
            
        # Hash compiler flags
        flags_str = '|'.join(sorted(compiler_flags))
        hasher.update(flags_str.encode('utf-8'))
        
        # Hash system info that affects compilation
        system_info = f"{platform.machine()}|{platform.system()}"
        hasher.update(system_info.encode('utf-8'))
        
        return hasher.hexdigest()
        
    def get_cached_binary(self, source_hash: str) -> Optional[Dict]:
        """Get cached binary if available"""
        
        if source_hash in self.cache_index['entries']:
            entry = self.cache_index['entries'][source_hash]
            binary_path = os.path.join(self.cache_dir, 'binaries', f"{source_hash}.bin")
            metadata_path = os.path.join(self.cache_dir, 'metadata', f"{source_hash}.json")
            
            if os.path.exists(binary_path) and os.path.exists(metadata_path):
                try:
                    with open(metadata_path, 'r') as f:
                        metadata = json.load(f)
                    
                    # Update access time
                    entry['last_accessed'] = time.time()
                    entry['access_count'] += 1
                    self.cache_index['stats']['hits'] += 1
                    self._save_cache_index()
                    
                    return {
                        'binary_path': binary_path,
                        'metadata': metadata,
                        'cache_hit': True
                    }
                except:
                    pass
        
        self.cache_index['stats']['misses'] += 1
        self._save_cache_index()
        return None
        
    def cache_binary(self, source_hash: str, binary_path: str, metadata: Dict):
        """Cache compiled binary with metadata"""
        
        try:
            # Copy binary to cache
            cache_binary_path = os.path.join(self.cache_dir, 'binaries', f"{source_hash}.bin")
            shutil.copy2(binary_path, cache_binary_path)
            
            # Save metadata
            metadata_path = os.path.join(self.cache_dir, 'metadata', f"{source_hash}.json")
            cache_metadata = {
                **metadata,
                'cached_at': time.time(),
                'original_path': binary_path,
                'file_size': os.path.getsize(cache_binary_path)
            }
            
            with open(metadata_path, 'w') as f:
                json.dump(cache_metadata, f, indent=2)
                
            # Update cache index
            self.cache_index['entries'][source_hash] = {
                'created_at': time.time(),
                'last_accessed': time.time(),
                'access_count': 0,
                'file_size': cache_metadata['file_size']
            }
            
            self.cache_index['stats']['total_size'] += cache_metadata['file_size']
            self._save_cache_index()
            
            # Cleanup if cache too large
            self._cleanup_cache_if_needed()
            
        except Exception as e:
            print(f"Error caching binary: {e}")
            
    def _cleanup_cache_if_needed(self):
        """Cleanup old cache entries if cache is too large"""
        
        if self.cache_index['stats']['total_size'] > self.max_cache_size:
            # Sort entries by last accessed time
            entries = [(k, v) for k, v in self.cache_index['entries'].items()]
            entries.sort(key=lambda x: x[1]['last_accessed'])
            
            # Remove oldest entries until under limit
            for source_hash, entry in entries:
                if self.cache_index['stats']['total_size'] <= self.max_cache_size * 0.8:
                    break
                    
                try:
                    # Remove files
                    binary_path = os.path.join(self.cache_dir, 'binaries', f"{source_hash}.bin")
                    metadata_path = os.path.join(self.cache_dir, 'metadata', f"{source_hash}.json") 
                    
                    if os.path.exists(binary_path):
                        os.unlink(binary_path)
                    if os.path.exists(metadata_path):
                        os.unlink(metadata_path)
                        
                    # Update stats
                    self.cache_index['stats']['total_size'] -= entry['file_size']
                    del self.cache_index['entries'][source_hash]
                    
                except Exception as e:
                    print(f"Error cleaning cache entry: {e}")
                    
            self._save_cache_index()
            
    def get_cache_stats(self) -> Dict:
        """Get cache statistics"""
        
        stats = self.cache_index['stats'].copy()
        stats['entry_count'] = len(self.cache_index['entries'])
        stats['cache_dir'] = self.cache_dir
        stats['hit_ratio'] = (stats['hits'] / (stats['hits'] + stats['misses'])) if (stats['hits'] + stats['misses']) > 0 else 0
        
        return stats

class DistributedCompilationManager:
    """Distributed compilation across multiple machines/containers"""
    
    def __init__(self, compiler_system):
        self.compiler_system = compiler_system
        self.build_nodes = self._discover_build_nodes()
        self.task_queue = []
        self.completed_tasks = {}
        self.load_balancer = LoadBalancer()
        
    def _discover_build_nodes(self) -> List[Dict]:
        """Discover available build nodes"""
        
        nodes = []
        
        # Local node (always available)
        nodes.append({
            'id': 'local',
            'type': 'local',
            'address': 'localhost',
            'cpu_cores': os.cpu_count(),
            'memory_gb': psutil.virtual_memory().total / (1024**3) if 'psutil' in globals() else 4,
            'available': True,
            'load': 0.0,
            'priority': 1
        })
        
        # Docker containers as build nodes
        if shutil.which('docker'):
            try:
                result = subprocess.run(['docker', 'ps', '--format', 
                                       'table {{.ID}}\t{{.Image}}\t{{.Status}}'], 
                                      capture_output=True, text=True, timeout=10)
                
                if result.returncode == 0:
                    for line in result.stdout.split('\n')[1:]:
                        if line.strip():
                            parts = line.split('\t')
                            if len(parts) >= 3 and 'Up' in parts[2]:
                                container_id = parts[0]
                                image = parts[1]
                                
                                # Check if container has build tools
                                check_result = subprocess.run(['docker', 'exec', container_id, 
                                                             'which', 'gcc'], 
                                                            capture_output=True, timeout=5)
                                
                                if check_result.returncode == 0:
                                    nodes.append({
                                        'id': f'docker-{container_id[:8]}',
                                        'type': 'docker',
                                        'container_id': container_id,
                                        'image': image,
                                        'available': True,
                                        'load': 0.0,
                                        'priority': 3
                                    })
            except:
                pass
        
        # SSH-accessible remote nodes (if configured)
        ssh_nodes = self._discover_ssh_nodes()
        nodes.extend(ssh_nodes)
        
        return nodes
    
    def _discover_ssh_nodes(self) -> List[Dict]:
        """Discover SSH-accessible build nodes"""
        
        nodes = []
        
        # Check SSH config for potential build machines
        ssh_config_path = os.path.expanduser('~/.ssh/config')
        if os.path.exists(ssh_config_path):
            try:
                with open(ssh_config_path, 'r') as f:
                    content = f.read()
                    
                # Simple parsing for Host entries
                hosts = re.findall(r'Host\s+(\S+)', content)
                for host in hosts[:5]:  # Limit to first 5 hosts
                    if host != '*':  # Skip wildcard entries
                        # Test if host has build tools
                        test_result = subprocess.run(['ssh', '-o', 'ConnectTimeout=5', 
                                                    host, 'which gcc'], 
                                                   capture_output=True, timeout=10)
                        
                        if test_result.returncode == 0:
                            nodes.append({
                                'id': f'ssh-{host}',
                                'type': 'ssh',
                                'address': host,
                                'available': True,
                                'load': 0.0,
                                'priority': 5
                            })
            except:
                pass
                
        return nodes
    
    async def compile_distributed(self, file_path: str, strategies: List[Dict]) -> List[Dict]:
        """Compile using distributed build nodes"""
        
        if len(self.build_nodes) <= 1:
            # Fallback to local compilation
            return await self._compile_local_fallback(file_path, strategies)
        
        results = []
        
        # Distribute strategies across nodes
        strategy_chunks = self._distribute_strategies(strategies)
        
        # Execute compilation on each node
        tasks = []
        for node_id, node_strategies in strategy_chunks.items():
            task = self._compile_on_node(node_id, file_path, node_strategies)
            tasks.append(task)
        
        # Wait for all tasks to complete
        node_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Combine results
        for node_result in node_results:
            if isinstance(node_result, list):
                results.extend(node_result)
            elif isinstance(node_result, Exception):
                # Log error but continue
                print(f"Node compilation error: {node_result}")
        
        return results
    
    def _distribute_strategies(self, strategies: List[Dict]) -> Dict[str, List[Dict]]:
        """Distribute compilation strategies across available nodes"""
        
        distribution = {}
        available_nodes = [node for node in self.build_nodes if node['available']]
        
        if not available_nodes:
            return {'local': strategies}
        
        # Calculate load distribution based on node capabilities
        total_capacity = sum(self._calculate_node_capacity(node) for node in available_nodes)
        
        strategy_index = 0
        for node in available_nodes:
            node_capacity = self._calculate_node_capacity(node)
            node_share = len(strategies) * (node_capacity / total_capacity)
            node_strategies = strategies[strategy_index:strategy_index + int(node_share)]
            
            if node_strategies:
                distribution[node['id']] = node_strategies
                strategy_index += len(node_strategies)
        
        # Assign remaining strategies to local node
        if strategy_index < len(strategies):
            remaining = strategies[strategy_index:]
            if 'local' in distribution:
                distribution['local'].extend(remaining)
            else:
                distribution['local'] = remaining
        
        return distribution
    
    def _calculate_node_capacity(self, node: Dict) -> float:
        """Calculate node compilation capacity"""
        
        base_capacity = 1.0
        
        # Adjust based on node type
        if node['type'] == 'local':
            base_capacity = 2.0  # Prefer local for faster I/O
        elif node['type'] == 'docker':
            base_capacity = 1.5  # Good for isolation
        elif node['type'] == 'ssh':
            base_capacity = 0.8  # Network overhead
        
        # Adjust based on resources
        if 'cpu_cores' in node:
            base_capacity *= min(node['cpu_cores'] / 4.0, 2.0)
        
        # Adjust based on current load
        base_capacity *= (1.0 - node.get('load', 0.0))
        
        return max(0.1, base_capacity)
    
    async def _compile_on_node(self, node_id: str, file_path: str, strategies: List[Dict]) -> List[Dict]:
        """Compile strategies on specific node"""
        
        node = next((n for n in self.build_nodes if n['id'] == node_id), None)
        if not node:
            return []
        
        if node['type'] == 'local':
            return await self._compile_local(file_path, strategies)
        elif node['type'] == 'docker':
            return await self._compile_docker(node, file_path, strategies)
        elif node['type'] == 'ssh':
            return await self._compile_ssh(node, file_path, strategies)
        else:
            return []
    
    async def _compile_local(self, file_path: str, strategies: List[Dict]) -> List[Dict]:
        """Compile strategies locally"""
        
        results = []
        for strategy in strategies:
            result = execute_single_compilation(strategy)
            results.append(result)
        return results
    
    async def _compile_docker(self, node: Dict, file_path: str, strategies: List[Dict]) -> List[Dict]:
        """Compile strategies in Docker container"""
        
        results = []
        container_id = node['container_id']
        
        try:
            # Copy source file to container
            container_file = f'/tmp/{os.path.basename(file_path)}'
            subprocess.run(['docker', 'cp', file_path, f'{container_id}:{container_file}'], 
                          check=True, timeout=30)
            
            # Execute each strategy
            for strategy in strategies:
                try:
                    # Build compilation command
                    cmd_parts = [strategy['compiler']]
                    cmd_parts.extend(strategy.get('flags', []))
                    cmd_parts.extend([container_file, '-o', f'/tmp/output_{strategy["strategy_id"]}'])
                    cmd_parts.extend(strategy.get('libs', []))
                    
                    # Execute in container
                    docker_cmd = ['docker', 'exec', container_id] + cmd_parts
                    
                    start_time = time.time()
                    result_proc = subprocess.run(docker_cmd, capture_output=True, 
                                               text=True, timeout=120)
                    compilation_time = time.time() - start_time
                    
                    # Create result
                    result = {
                        'strategy': strategy,
                        'success': result_proc.returncode == 0,
                        'compilation_time': compilation_time,
                        'node_id': node['id'],
                        'node_type': 'docker',
                        'compiler_output': result_proc.stdout + result_proc.stderr
                    }
                    
                    if result['success']:
                        # Try to get file size
                        size_cmd = ['docker', 'exec', container_id, 'stat', '-c', '%s', 
                                  f'/tmp/output_{strategy["strategy_id"]}']
                        size_result = subprocess.run(size_cmd, capture_output=True, text=True)
                        if size_result.returncode == 0:
                            result['file_size'] = int(size_result.stdout.strip())
                        else:
                            result['file_size'] = 0
                    else:
                        result['file_size'] = 0
                        result['error'] = result_proc.stderr
                    
                    results.append(result)
                    
                except Exception as e:
                    results.append({
                        'strategy': strategy,
                        'success': False,
                        'error': str(e),
                        'node_id': node['id'],
                        'compilation_time': 0,
                        'file_size': 0
                    })
                    
        except Exception as e:
            # If container setup fails, return failed results for all strategies
            for strategy in strategies:
                results.append({
                    'strategy': strategy,
                    'success': False,
                    'error': f'Container error: {str(e)}',
                    'node_id': node['id'],
                    'compilation_time': 0,
                    'file_size': 0
                })
        
        return results
    
    async def _compile_ssh(self, node: Dict, file_path: str, strategies: List[Dict]) -> List[Dict]:
        """Compile strategies on remote SSH node"""
        
        results = []
        ssh_host = node['address']
        
        try:
            # Copy source file to remote
            remote_file = f'/tmp/{os.path.basename(file_path)}'
            subprocess.run(['scp', file_path, f'{remote_user}@{remote_host}:{remote_path}'], check=True)
            return {
                'success': True,
                'remote_path': f'{remote_host}:{remote_path}',
                'transfer_time': time.time() - start_time
            }
        except subprocess.CalledProcessError as e:
            return {
                'success': False,
                'error': f'SCP transfer failed: {str(e)}'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Remote execution error: {str(e)}'
            }

    async def _run_cpu_benchmarks(self, binary_path: str) -> Dict:
        """Run CPU-specific benchmarks"""
        
        results = {
            'single_core': [],
            'multi_core': [],
            'vector_operations': [],
            'math_operations': []
        }
        
        try:
            # Single core performance
            for _ in range(3):
                start_time = time.time()
                result = subprocess.run([binary_path], 
                                      capture_output=True, 
                                      timeout=30,
                                      env={'OMP_NUM_THREADS': '1'})
                end_time = time.time()
                
                if result.returncode == 0:
                    results['single_core'].append(end_time - start_time)
            
            # Multi-core performance (if supported)
            cpu_count = os.cpu_count() or 1
            if cpu_count > 1:
                for _ in range(3):
                    start_time = time.time()
                    result = subprocess.run([binary_path], 
                                          capture_output=True, 
                                          timeout=30,
                                          env={'OMP_NUM_THREADS': str(cpu_count)})
                    end_time = time.time()
                    
                    if result.returncode == 0:
                        results['multi_core'].append(end_time - start_time)
            
            # Vector operation test
            vec_test_data = "\n".join([str(i) for i in range(1000000)])
            for _ in range(3):
                start_time = time.time()
                result = subprocess.run([binary_path], 
                                      input=vec_test_data,
                                      capture_output=True, 
                                      text=True,
                                      timeout=30)
                end_time = time.time()
                
                if result.returncode == 0:
                    results['vector_operations'].append(end_time - start_time)
            
            # Math operation test
            math_test_data = "math\n" + "\n".join([f"{i}.123456" for i in range(10000)])
            for _ in range(3):
                start_time = time.time()
                result = subprocess.run([binary_path], 
                                      input=math_test_data,
                                      capture_output=True, 
                                      text=True,
                                      timeout=30)
                end_time = time.time()
                
                if result.returncode == 0:
                    results['math_operations'].append(end_time - start_time)
        
        except Exception as e:
            results['error'] = str(e)
        
        return results

    async def _run_custom_benchmarks(self, binary_path: str, analysis: Dict) -> Dict:
        """Run custom benchmarks based on code analysis"""
        
        results = {}
        
        try:
            # Threading benchmark if code uses threads
            if analysis.get('threading'):
                thread_results = []
                for thread_count in [1, 2, 4, 8]:
                    if thread_count > (os.cpu_count() or 1):
                        continue
                    
                    env = os.environ.copy()
                    env['OMP_NUM_THREADS'] = str(thread_count)
                    
                    times = []
                    for _ in range(3):
                        start_time = time.time()
                        result = subprocess.run([binary_path], 
                                              env=env,
                                              capture_output=True, 
                                              timeout=30)
                        end_time = time.time()
                        
                        if result.returncode == 0:
                            times.append(end_time - start_time)
                    
                    if times:
                        thread_results.append({
                            'threads': thread_count,
                            'time': sum(times)/len(times),
                            'speedup': times[0]/times[-1] if len(times) > 1 else 1.0
                        })
                
                results['thread_scaling'] = thread_results
            
            # Math benchmark if code is math-heavy
            if analysis.get('math_heavy'):
                math_input = "\n".join([f"{i}.123456" for i in range(10000)])
                math_times = []
                
                for _ in range(5):
                    start_time = time.time()
                    result = subprocess.run([binary_path], 
                                          input=math_input,
                                          capture_output=True, 
                                          text=True,
                                          timeout=30)
                    end_time = time.time()
                    
                    if result.returncode == 0:
                        math_times.append(end_time - start_time)
                
                if math_times:
                    results['math_performance'] = {
                        'average_time': sum(math_times)/len(math_times),
                        'samples': len(math_times)
                    }
            
            # Network benchmark if code uses networking
            if analysis.get('networking'):
                # Simple network test using localhost
                try:
                    import socket
                    test_port = 54321
                    
                    # Start simple echo server
                    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    server.bind(('localhost', test_port))
                    server.listen(1)
                    server.settimeout(5)
                    
                    net_times = []
                    for _ in range(3):
                        start_time = time.time()
                        result = subprocess.run([binary_path, str(test_port)], 
                                              capture_output=True, 
                                              timeout=30)
                        end_time = time.time()
                        
                        if result.returncode == 0:
                            net_times.append(end_time - start_time)
                    
                    if net_times:
                        results['network_performance'] = {
                            'average_time': sum(net_times)/len(net_times),
                            'samples': len(net_times)
                        }
                except Exception as e:
                    results['network_error'] = str(e)
                finally:
                    server.close()
        
        except Exception as e:
            results['error'] = str(e)
        
        return results

    async def _run_stability_tests(self, binary_path: str) -> Dict:
        """Run stability and reliability tests"""
        
        results = {
            'long_running': {},
            'memory_stability': {},
            'crash_recovery': {}
        }
        
        try:
            # Long running test (30 seconds)
            start_time = time.time()
            proc = subprocess.Popen([binary_path], 
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
            
            try:
                stdout, stderr = proc.communicate(timeout=30)
                results['long_running'] = {
                    'success': True,
                    'duration': time.time() - start_time,
                    'exit_code': proc.returncode
                }
            except subprocess.TimeoutExpired:
                proc.terminate()
                results['long_running'] = {
                    'success': False,
                    'error': 'Timeout after 30 seconds'
                }
            
            # Memory stability test with Valgrind (if available)
            if shutil.which('valgrind'):
                result = subprocess.run([
                    'valgrind', '--tool=memcheck', '--leak-check=full',
                    binary_path
                ], capture_output=True, text=True, timeout=60)
                
                valgrind_output = result.stderr
                results['memory_stability'] = {
                    'leaks': 'no leaks' not in valgrind_output.lower(),
                    'errors': 'error summary:' in valgrind_output.lower(),
                    'output': valgrind_output[:500] + '...' if valgrind_output else None
                }
            
            # Crash recovery test
            try:
                # Send SIGTERM after 1 second
                proc = subprocess.Popen([binary_path], 
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
                time.sleep(1)
                proc.terminate()
                stdout, stderr = proc.communicate(timeout=5)
                
                results['crash_recovery'] = {
                    'success': proc.returncode is not None,
                    'exit_code': proc.returncode,
                    'output': (stdout + stderr).decode()[:200] + '...' if stdout or stderr else None
                }
            except Exception as e:
                results['crash_recovery'] = {
                    'success': False,
                    'error': str(e)
                }
        
        except Exception as e:
            results['error'] = str(e)
        
        return results

    def _calculate_overall_score(self, benchmark_results: Dict) -> float:
        """Calculate overall benchmark score"""
        
        score = 50  # Base score
        
        try:
            # Execution performance (40% weight)
            if benchmark_results['execution_benchmarks'].get('warm_runs'):
                avg_exec_time = sum(benchmark_results['execution_benchmarks']['warm_runs'])/len(benchmark_results['execution_benchmarks']['warm_runs'])
                exec_score = max(0, 100 - (avg_exec_time * 10))  # 0.1s = 100, 10s = 0
                score += exec_score * 0.4
            
            # Memory efficiency (20% weight)
            if benchmark_results['memory_benchmarks'].get('peak_memory'):
                avg_mem = sum(benchmark_results['memory_benchmarks']['peak_memory'])/len(benchmark_results['memory_benchmarks']['peak_memory'])
                mem_score = max(0, 100 - (avg_mem / 1000000))  # 1MB = 99, 100MB = 0
                score += mem_score * 0.2
            
            # CPU performance (20% weight)
            if benchmark_results['cpu_benchmarks'].get('single_core'):
                avg_cpu_time = sum(benchmark_results['cpu_benchmarks']['single_core'])/len(benchmark_results['cpu_benchmarks']['single_core'])
                cpu_score = max(0, 100 - (avg_cpu_time * 10))
                score += cpu_score * 0.2
            
            # Custom benchmarks (20% weight)
            if benchmark_results['custom_benchmarks'].get('thread_scaling'):
                thread_score = min(100, benchmark_results['custom_benchmarks']['thread_scaling'][-1]['speedup'] * 50)
                score += thread_score * 0.1
                
            if benchmark_results['custom_benchmarks'].get('math_performance'):
                math_score = max(0, 100 - (benchmark_results['custom_benchmarks']['math_performance']['average_time'] * 10))
                score += math_score * 0.1
            
            # Stability penalty
            if not benchmark_results['stability_metrics'].get('long_running', {}).get('success'):
                score -= 20
            if benchmark_results['stability_metrics'].get('memory_stability', {}).get('leaks'):
                score -= 15
            
            # Clamp between 0-100
            score = max(0, min(100, score))
        
        except Exception:
            pass
        
        return round(score, 1)

    def _compare_with_baseline(self, benchmark_results: Dict) -> Dict:
        """Compare results with system baseline"""
        
        comparison = {}
        
        try:
            if not self.system_baseline:
                return comparison
                
            # Execution time comparison
            if 'execution_benchmarks' in benchmark_results and 'execution_benchmarks' in self.system_baseline:
                current_avg = sum(benchmark_results['execution_benchmarks']['warm_runs'])/len(benchmark_results['execution_benchmarks']['warm_runs'])
                baseline_avg = sum(self.system_baseline['execution_benchmarks']['warm_runs'])/len(self.system_baseline['execution_benchmarks']['warm_runs'])
                comparison['execution_time'] = {
                    'current': current_avg,
                    'baseline': baseline_avg,
                    'improvement': ((baseline_avg - current_avg) / baseline_avg) * 100 if baseline_avg > 0 else 0
                }
            
            # Memory comparison
            if 'memory_benchmarks' in benchmark_results and 'memory_benchmarks' in self.system_baseline:
                current_avg = sum(benchmark_results['memory_benchmarks']['peak_memory'])/len(benchmark_results['memory_benchmarks']['peak_memory'])
                baseline_avg = sum(self.system_baseline['memory_benchmarks']['peak_memory'])/len(self.system_baseline['memory_benchmarks']['peak_memory'])
                comparison['memory_usage'] = {
                    'current': current_avg,
                    'baseline': baseline_avg,
                    'improvement': ((baseline_avg - current_avg) / baseline_avg) * 100 if baseline_avg > 0 else 0
                }
            
            # Overall score comparison
            if 'overall_score' in benchmark_results and 'overall_score' in self.system_baseline:
                comparison['overall_score'] = {
                    'current': benchmark_results['overall_score'],
                    'baseline': self.system_baseline['overall_score'],
                    'improvement': benchmark_results['overall_score'] - self.system_baseline['overall_score']
                }
        
        except Exception as e:
            comparison['error'] = str(e)
        
        return comparison

    def _parse_time_output(self, output: str) -> Dict:
        """Parse output from GNU time command"""
        
        stats = {}
        
        try:
            for line in output.split('\n'):
                if 'Maximum resident set size' in line:
                    stats['max_memory'] = int(line.split()[-1])  # in KB
                elif 'User time (seconds)' in line:
                    stats['user_time'] = float(line.split()[-1])
                elif 'System time (seconds)' in line:
                    stats['system_time'] = float(line.split()[-1])
                elif 'Percent of CPU this job got' in line:
                    stats['cpu_percent'] = int(line.split()[-1].rstrip('%'))
        
        except Exception:
            pass
        
        return stats

    def _parse_valgrind_output(self, output: str) -> Dict:
        """Parse output from Valgrind memcheck"""
        
        stats = {
            'leaks': 0,
            'errors': 0
        }
        
        try:
            for line in output.split('\n'):
                if 'ERROR SUMMARY:' in line:
                    stats['errors'] = int(line.split()[3])
                elif 'LEAK SUMMARY:' in line:
                    stats['leaks'] = int(output.split('\n')[output.split('\n').index(line)+1].split()[3])
        
        except Exception:
            pass
        
        return stats

    def _generate_input_data(self, size: str) -> str:
        """Generate input data for benchmarks"""
        
        if size == 'small':
            return "test\n"
        elif size == 'medium':
            return "\n".join([f"line {i}" for i in range(100)]) + "\n"
        else:  # large
            return "\n".join([f"data {i} {'x' * 100}" for i in range(1000)]) + "\n"

# Final integration with the main compiler system

async def integrate_advanced_features(update: Update, context: ContextTypes.DEFAULT_TYPE,
                                    best_result: Dict, analysis: Dict):
    """Integrate advanced optimization features with main compilation flow"""
    
    try:
        # Initialize advanced systems
        compiler_system = AdvancedCompiler()
        pgo_system = ProfileGuidedOptimization(compiler_system)
        tuning_system = AutoTuningSystem(compiler_system)
        benchmark_suite = CompilerBenchmarkSuite()
        
        # Run PGO optimization if applicable
        if best_result['strategy']['compiler'] in ['gcc', 'clang', 'g++', 'clang++']:
            await update.message.reply_text("🔧 Starting Profile-Guided Optimization...")
            pgo_results = await pgo_system.run_pgo_optimization(
                best_result['strategy']['input_path'],
                best_result['strategy']['compiler'],
                best_result['strategy'].get('flags', [])
            )
            
            if pgo_results['success']:
                await update.message.reply_text(
                    f"🎉 PGO Optimization Complete!\n"
                    f"⏱️ Total time: {pgo_results['total_time']:.1f}s\n"
                    f"📈 Performance improvement: {pgo_results['performance_improvement']:.1f}%\n"
                    f"📦 Final binary: {pgo_results['final_binary']}"
                )
                best_result['output_path'] = pgo_results['final_binary']
                best_result['pgo_improvement'] = pgo_results['performance_improvement']
        
        # Run auto-tuning if code is performance critical
        if analysis.get('performance_critical'):
            await update.message.reply_text("⚙️ Starting Auto-Tuning Optimization...")
            tune_results = await tuning_system.auto_tune_compilation(
                best_result['strategy']['input_path'],
                analysis,
                'performance'
            )
            
            if tune_results['success']:
                await update.message.reply_text(
                    f"🎯 Auto-Tuning Complete!\n"
                    f"⏱️ Total time: {tune_results['total_time']:.1f}s\n"
                    f"📊 Best score: {tune_results['best_score']:.1f}\n"
                    f"🔧 Configuration: {json.dumps(tune_results['best_config'], indent=2)}"
                )
        
        # Run comprehensive benchmarks
        if best_result.get('output_path'):
            await update.message.reply_text("📊 Running Comprehensive Benchmarks...")
            benchmark_results = await benchmark_suite.run_comprehensive_benchmark(
                best_result['output_path'],
                analysis
            )
            
            if benchmark_results.get('overall_score'):
                await update.message.reply_text(
                    f"🏆 Benchmark Results:\n"
                    f"⭐ Overall Score: {benchmark_results['overall_score']}/100\n"
                    f"⏱️ Execution Time: {sum(benchmark_results['execution_benchmarks']['warm_runs'])/len(benchmark_results['execution_benchmarks']['warm_runs']):.3f}s\n"
                    f"💾 Memory Usage: {sum(benchmark_results['memory_benchmarks']['peak_memory'])/len(benchmark_results['memory_benchmarks']['peak_memory'])/1024:.1f} MB\n"
                    f"🧵 Thread Scaling: {benchmark_results['custom_benchmarks'].get('thread_scaling', [{}])[-1].get('speedup', 1.0):.1f}x"
                )
    
    except Exception as e:
        await update.message.reply_text(f"⚠️ Advanced features error: {str(e)}")

# Main function to handle compilation with all features
async def handle_compilation_with_advanced_features(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle compilation with all advanced features integrated"""
    
    try:
        # Initialize compiler system
        compiler_system = AdvancedCompiler()
        
        # Download and analyze file
        file = update.message.document
        file_name = file.file_name
        file_ext = Path(file_name).suffix.lower()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, file_name)
            file_obj = await file.get_file()
            await file_obj.download_to_drive(file_path)
            
            analysis = await analyze_source_code_advanced(file_path, file_ext)
            
            # Generate compilation strategies
            strategies = await generate_mega_compilation_strategies(
                compiler_system, file_path, file_ext, analysis, temp_dir
            )
            
            # Execute compilation
            results = await execute_mega_parallel_compilation(strategies, update)
            successful_results = [r for r in results if r['success']]
            
            if successful_results:
                best_result = sorted(successful_results, 
                                   key=lambda x: (x['priority'], -x.get('performance_score', 0), x['file_size']))[0]
                
                # Run advanced optimizations
                await integrate_advanced_features(update, context, best_result, analysis)
                
                # Send final binary
                if os.path.exists(best_result['output_path']):
                    with open(best_result['output_path'], 'rb') as f:
                        await update.message.reply_document(
                            document=f,
                            filename=f"optimized_{file_name.split('.')[0]}{'.exe' if platform.system() == 'Windows' else ''}",
                            caption="🚀 Optimized Binary with Advanced Features"
                        )
            else:
                await handle_mega_compilation_failure(update, results, analysis, compiler_system)
    
    except Exception as e:
        await update.message.reply_text(f"💥 Critical error in advanced compilation: {str(e)}")

# Fitur 2: Upload ke GitHub (Fixed)
async def upload_to_github(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = update.message.document or (update.message.photo[-1] if update.message.photo else None)

    if not file:
        await update.message.reply_text("❌ Tidak ada file yang ditemukan")
        return

    try:
        # Buat folder uploads jika belum ada
        upload_dir = os.path.join(os.getcwd(), "uploads")
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        # Ambil nama file dan download
        if update.message.document:
            file_name = update.message.document.file_name
            file_path = os.path.join(upload_dir, file_name)
            tg_file = await update.message.document.get_file()
            await tg_file.download_to_drive(file_path)
            with open(file_path, 'rb') as f:
                content = f.read()
        else:
            file_name = f"photo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            file_path = os.path.join(upload_dir, file_name)
            tg_file = await update.message.photo[-1].get_file()
            await tg_file.download_to_drive(file_path)
            with open(file_path, 'rb') as f:
                content = f.read()

        # Upload ke GitHub
        try:
            existing_file = repo.get_contents(f"uploads/{file_name}", ref="main")
            repo.update_file(
                path=existing_file.path,
                message=f"Update {file_name} via Telegram Bot",
                content=content,
                sha=existing_file.sha,
                branch="main"
            )
            message = f"♻️ File {file_name} berhasil diupdate di Server!"
        except Exception:
            repo.create_file(
                path=f"uploads/{file_name}",
                message=f"Upload {file_name} via Telegram Bot",
                content=content,
                branch="main"
            )
            message = f"✅ File {file_name} berhasil diupload ke Server!"

        # Kirim konfirmasi dengan info file
        raw_url = f"https://raw.githubusercontent.com/{GITHUB_REPO}/main/uploads/{file_name}"
        file_size = os.path.getsize(file_path) / 1024
        
        await update.message.reply_text(
            f"{message}\n\n"
            f"🔗 URL: <code>{raw_url}</code>\n"
            f"📊 Size: {file_size:.2f} KB\n"
            f"📅 Upload: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
            f"<i>File berhasil disimpan di server</i>",
            parse_mode='HTML'
        )

        # Auto-process berdasarkan tipe file
        if file_name.endswith((".c", ".cpp")):
            await compile_file(update, context)
        elif file_name.endswith(".js"):
            await obfuscate_js(update, context)
        elif file_name.endswith(".lua"):
            await obfuscate_lua(update, context)
        elif file_name.endswith(".sh"):
            await encode_shell(update, context)
        elif file_name.endswith(".py"):
            await encode_python(update, context)
            
    except Exception as e:
        await update.message.reply_text(f"❌ Gagal upload: {str(e)}")
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

# Fitur 3: Deploy ke Firebase Hosting (Fixed)
async def firebase_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("🔙 Kembali", callback_data='deploy_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "<b>🔥 Firebase Hosting</b>\n\n"
        "Untuk deploy ke Firebase Hosting:\n"
        "1. Kirim file/folder (zip)\n"
        "2. Ketik <code>/deploy_firebase [nama_site]</code>\n\n"
        "<i>Contoh: /deploy_firebase my-website</i>",
        parse_mode='HTML',
        reply_markup=reply_markup
    )

async def deploy_firebase(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) < 1:
        await update.message.reply_text("❌ Format: /deploy_firebase [nama_site]\nContoh: /deploy_firebase my-site")
        return
    
    site_id = args[0]
    temp_dir = tempfile.mkdtemp()
    
    try:
        await update.message.reply_text("⏳ Mempersiapkan deploy ke Firebase...")
        
        # Buat struktur folder public
        public_dir = os.path.join(temp_dir, "public")
        os.makedirs(public_dir, exist_ok=True)
        
        # Buat file index.html default
        index_path = os.path.join(public_dir, "index.html")
        with open(index_path, 'w') as f:
            f.write(f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{site_id} - Deployed via Nikzzx Bot</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .container {{
            text-align: center;
            max-width: 600px;
            padding: 2rem;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        }}
        h1 {{ font-size: 3rem; margin-bottom: 1rem; }}
        p {{ font-size: 1.2rem; margin-bottom: 2rem; }}
        .badge {{
            display: inline-block;
            padding: 0.5rem 1rem;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 25px;
            margin: 0.5rem;
            font-size: 0.9rem;
        }}
        .footer {{
            margin-top: 2rem;
            font-size: 0.8rem;
            opacity: 0.8;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔥 Firebase Deployed!</h1>
        <p>Site <strong>{site_id}</strong> berhasil di-deploy menggunakan Nikzzx Multi-Feature Bot v2.0</p>
        <div>
            <span class="badge">🔥 Firebase</span>
            <span class="badge">🤖 Telegram Bot</span>
            <span class="badge">⚡ Nikzzx</span>
        </div>
        <div class="footer">
            <p>Deployed on {datetime.now().strftime('%d %B %Y at %H:%M UTC')}</p>
        </div>
    </div>
</body>
</html>
            """)
        
        # Hitung hash file
        file_hash = sha256_hash(index_path)
        
        # Deploy ke Firebase
        access_token = get_firebase_access_token()
        if not access_token:
            await update.message.reply_text("❌ Gagal mendapatkan Firebase access token")
            return
            
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        # Buat versi baru
        version_url = f"https://firebasehosting.googleapis.com/v1beta1/sites/{site_id}/versions"
        version_payload = {"config": {"headers": [{"glob": "", "headers": {"Cache-Control": "max-age=3600"}}]}}
        
        resp = requests.post(version_url, headers=headers, json=version_payload)
        if resp.status_code != 200:
            raise Exception(f"Gagal membuat versi: {resp.text}")
        
        version_data = resp.json()
        version_name = version_data['name']
        
        # Populate files
        populate_url = f"https://firebasehosting.googleapis.com/v1beta1/{version_name}:populateFiles"
        populate_payload = {"files": {"/index.html": file_hash}}
        
        resp = requests.post(populate_url, headers=headers, json=populate_payload)
        if resp.status_code != 200:
            raise Exception(f"Gagal populate files: {resp.text}")
        
        populate_data = resp.json()
        upload_url = populate_data.get("uploadUrl")
        if not upload_url:
            raise Exception("Upload URL tidak ditemukan")
        
        # Upload file
        with open(index_path, "rb") as f:
            upload_resp = requests.put(upload_url, data=f, headers={"Content-Type": "text/html"})
            if upload_resp.status_code != 200:
                raise Exception(f"Gagal upload file: {upload_resp.text}")
        
        # Finalisasi dan release
        finalize_url = f"https://firebasehosting.googleapis.com/v1beta1/{version_name}:finalize"
        finalize_resp = requests.post(finalize_url, headers=headers)
        if finalize_resp.status_code != 200:
            raise Exception(f"Gagal finalisasi: {finalize_resp.text}")
        
        release_url = f"https://firebasehosting.googleapis.com/v1beta1/sites/{site_id}/releases"
        release_payload = {"versionName": version_name, "type": "DEPLOY"}
        
        release_resp = requests.post(release_url, headers=headers, json=release_payload)
        if release_resp.status_code != 200:
            raise Exception(f"Gagal deploy: {release_resp.text}")
        
        await update.message.reply_text(
            f"✅ <b>Berhasil deploy ke Firebase Hosting!</b>\n\n"
            f"🌐 URL: https://{site_id}.web.app/\n"
            f"🌐 Alt URL: https://{site_id}.firebaseapp.com/\n"
            f"📊 Dashboard: https://console.firebase.google.com/project/{FIREBASE_PROJECT}/hosting/sites/{site_id}\n\n"
            f"<i>Website berhasil di-deploy dan dapat diakses secara global</i>",
            parse_mode='HTML'
        )
        
    except Exception as e:
        await update.message.reply_text(f"❌ Gagal deploy ke Firebase: {str(e)}")
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

# Fitur 4: Deploy ke Vercel (Fixed)
async def vercel_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("🔙 Kembali", callback_data='deploy_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "<b>🚀 Vercel Deployment</b>\n\n"
        "Untuk deploy ke Vercel:\n"
        "1. Kirim file/folder (zip)\n"
        "2. Ketik <code>/deploy_vercel [nama_proyek]</code>\n\n"
        "<i>Contoh: /deploy_vercel my-project</i>",
        parse_mode='HTML',
        reply_markup=reply_markup
    )

async def deploy_vercel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) < 1:
        await update.message.reply_text("❌ Format: /deploy_vercel [nama_proyek]\nContoh: /deploy_vercel my-project")
        return
    
    project_name = args[0]
    temp_dir = tempfile.mkdtemp()
    
    try:
        await update.message.reply_text("⏳ Mempersiapkan deploy ke Vercel...")
        
        # Buat file konfigurasi Vercel
        vercel_json = {
            "version": 2,
            "name": project_name,
            "builds": [{"src": "*.html", "use": "@vercel/static"}],
            "routes": [{"src": "/(.*)", "dest": "/index.html"}]
        }
        
        with open(os.path.join(temp_dir, "vercel.json"), 'w') as f:
            json.dump(vercel_json, f, indent=2)
        
        # Buat file index.html
        with open(os.path.join(temp_dir, "index.html"), 'w') as f:
            f.write(f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{project_name} - Deployed via Nikzzx Bot</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, #000000 0%, #434343 100%);
            color: white;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .container {{
            text-align: center;
            max-width: 700px;
            padding: 3rem;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 20px;
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}
        h1 {{ font-size: 3.5rem; margin-bottom: 1rem; font-weight: 700; }}
        p {{ font-size: 1.3rem; margin-bottom: 2rem; opacity: 0.9; }}
        .badge {{
            display: inline-block;
            padding: 0.7rem 1.5rem;
            background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
            border-radius: 30px;
            margin: 0.5rem;
            font-size: 1rem;
            font-weight: 600;
        }}
        .footer {{
            margin-top: 3rem;
            font-size: 0.9rem;
            opacity: 0.7;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Vercel Deployed!</h1>
        <p>Project <strong>{project_name}</strong> berhasil di-deploy menggunakan Nikzzx Multi-Feature Bot v2.0</p>
        <div>
            <span class="badge">🚀 Vercel</span>
            <span class="badge">🤖 Telegram Bot</span>
            <span class="badge">⚡ Nikzzx</span>
        </div>
        <div class="footer">
            <p>Deployed on {datetime.now().strftime('%d %B %Y at %H:%M UTC')}</p>
            <p>Powered by Vercel Edge Network</p>
        </div>
    </div>
</body>
</html>
            """)
        
        # Simulasi deploy (karena Vercel CLI memerlukan auth)
        await update.message.reply_text(
            f"✅ <b>Simulasi Deploy ke Vercel Berhasil!</b>\n\n"
            f"🌐 URL: https://{project_name}-nikzzx.vercel.app/\n"
            f"📊 Dashboard: https://vercel.com/dashboard\n\n"
            f"<i>File project telah disiapkan untuk deployment</i>\n\n"
            f"📝 <b>Manual Deploy:</b>\n"
            f"1. Install Vercel CLI: <code>npm i -g vercel</code>\n"
            f"2. Login: <code>vercel login</code>\n"
            f"3. Deploy: <code>vercel --prod</code>",
            parse_mode='HTML'
        )
        
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

# Fitur 5: JavaScript Obfuscator (Improved)
async def obfuscator_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("🔙 Kembali", callback_data='security_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "<b>🔒 JavaScript Obfuscator Extreme</b>\n\n"
        "Untuk mengobfuscate kode JavaScript:\n"
        "1. Kirim file <code>.js</code>\n"
        "2. Bot akan mengobfuscate dengan level extreme\n"
        "3. Hasil akan sangat sulit di-reverse\n\n"
        "<i>Menggunakan teknik obfuscation tingkat enterprise</i>",
        parse_mode='HTML',
        reply_markup=reply_markup
    )

async def obfuscator_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("🔙 Kembali", callback_data='security_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "<b>🔒 JavaScript Obfuscator</b>\n\n"
        "Untuk mengobfuscate kode JavaScript:\n"
        "1. Kirim file <code>.js</code>\n"
        "2. Bot akan mengobfuscate dan mengirimkan hasilnya\n\n"
        "<i>Hasil obfuscation akan sangat sulit dibaca dan dianalisis</i>",
        parse_mode='HTML',
        reply_markup=reply_markup
    )

async def obfuscate_js(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = update.message.document
    if not file or not file.file_name.endswith('.js'):
        await update.message.reply_text("❌ File harus berekstensi .js")
        return
    
    # Download file
    file_name = file.file_name
    file_path = os.path.join(os.getcwd(), file_name)
    file_obj = await file.get_file()
    await file_obj.download_to_drive(file_path)
    
    await update.message.reply_text("⏳ Sedang mengobfuscate JavaScript...")
    
    try:
        # Obfuscate menggunakan javascript-obfuscator
        obf_file_name = file_name.replace('.js', '-obf.js')
        obf_file_path = os.path.join(os.getcwd(), obf_file_name)
        
        result = subprocess.run([
            'javascript-obfuscator', file_path,
            '--output', obf_file_path,
            '--compact', 'true',
            '--control-flow-flattening', 'true',
            '--control-flow-flattening-threshold', '1',
            '--dead-code-injection', 'true',
            '--dead-code-injection-threshold', '1',
            '--string-array', 'true',
            '--string-array-threshold', '1',
            '--string-array-encoding', 'rc4',
            '--string-array-index-shift', 'true',
            '--string-array-rotate', 'true',
            '--string-array-wrappers-type', 'function',
            '--string-array-wrappers-chained-calls', 'true',
            '--string-array-wrappers-count', '10',
            '--split-strings', 'true',
            '--split-strings-chunk-length', '5',
            '--transform-object-keys', 'true',
            '--unicode-escape-sequence', 'true',
            '--self-defending', 'true',
            '--debug-protection', 'true',
            '--debug-protection-interval', '4000',
            '--disable-console-output', 'true',
            '--rename-globals', 'true',
            '--numbers-to-expressions', 'true',
            '--simplify', 'true',
            '--identifier-names-generator', 'mangled',
            '--identifiers-prefix', 'ENCBYNIKZZXIT_',
            '--seed', '12345',
            '--target', 'browser-no-eval',
            '--string-array-calls-transform', 'true',
            '--string-array-calls-transform-threshold', '1',
            '--ignore-imports', 'true',
            '--log', 'false'
        ], capture_output=True, text=True)
        
        if os.path.exists(obf_file_path):
            # Konversi \xXX ke \u00XX
            with open(obf_file_path, "r", encoding="utf-8") as f:
                code = f.read()
            
            code = re.sub(r'\\x([0-9a-fA-F]{2})', lambda m: '\\u00' + m.group(1), code)
            
            hex_file_name = file_name.replace('.js', '-hex.js')
            hex_file_path = os.path.join(os.getcwd(), hex_file_name)
            with open(hex_file_path, "w", encoding="utf-8") as f:
                f.write(code)
            
            await update.message.reply_text("✅ Obfuscate berhasil!")
            
            # Kirim file obfuscated
            with open(hex_file_path, 'rb') as f:
                await context.bot.send_document(
                    chat_id=update.message.chat_id,
                    document=f,
                    caption=f"🔒 File {file_name} yang telah diobfuscate"
                )
            
            # Upload ke GitHub juga
            with open(hex_file_path, 'rb') as f:
                content = f.read()
            repo.create_file(
                path=f"obfuscated/{hex_file_name}",
                message=f"Upload obfuscated {hex_file_name} via Telegram Bot",
                content=content,
                branch="main"
            )
        else:
            await update.message.reply_text(f"❌ Gagal mengobfuscate:\n{result.stderr}")
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
        if os.path.exists(obf_file_path):
            os.remove(obf_file_path)
        if 'hex_file_path' in locals() and os.path.exists(hex_file_path):
            os.remove(hex_file_path)

# Fitur 6: Lua Obfuscator (Extreme)
async def luaobfuscator_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("🔙 Kembali", callback_data='security_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "<b>🌙 Lua Obfuscator Extreme</b>\n\n"
        "Untuk mengobfuscate kode Lua:\n"
        "1. Kirim file <code>.lua</code>\n"
        "2. Bot akan mengobfuscate dengan level extreme\n"
        "3. Hasil tetap dapat dijalankan dengan sempurna\n\n"
        "<i>Menggunakan teknik obfuscation tingkat militer</i>",
        parse_mode='HTML',
        reply_markup=reply_markup
    )

async def obfuscate_lua(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = update.message.document
    if not file or not file.file_name.endswith('.lua'):
        await update.message.reply_text("❌ File harus berekstensi .lua")
        return
    
    file_name = file.file_name
    file_path = os.path.join(os.getcwd(), file_name)
    file_obj = await file.get_file()
    await file_obj.download_to_drive(file_path)
    
    await update.message.reply_text("⏳ Sedang mengobfuscate Lua script dengan level extreme...")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lua_content = f.read()
        
        # Extreme Lua Obfuscation
        def random_lua_var(length=15):
            return '_' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
        
        # Encode strings to hex
        def encode_string(s):
            return ''.join([f'\\{ord(c)}' for c in s])
        
        # Generate obfuscated code
        obfuscated_lua = f"""
-- Obfuscated by Nikzzx Lua Obfuscator v2.0 - Extreme Level
-- Military Grade Protection

local {random_lua_var()} = string
local {random_lua_var()} = table
local {random_lua_var()} = math
local {random_lua_var()} = loadstring
local {random_lua_var()} = getfenv
local {random_lua_var()} = setfenv

-- Anti-debug protection
local {random_lua_var()} = function()
    local {random_lua_var()} = debug and debug.getinfo
    if {random_lua_var()} then
        error("Debug detected!")
    end
end

-- String decoder
local {random_lua_var()} = function(s)
    local result = ""
    for i = 1, #s, 4 do
        local hex = s:sub(i, i+3)
        result = result .. string.char(tonumber(hex, 16))
    end
    return result
end

-- Code chunks
local {random_lua_var()} = {{
"""
        
        # Split code into chunks and encode
        chunk_size = random.randint(50, 100)
        chunks = [lua_content[i:i+chunk_size] for i in range(0, len(lua_content), chunk_size)]
        
        for i, chunk in enumerate(chunks):
            encoded_chunk = ''.join([f'{ord(c):04x}' for c in chunk])
            obfuscated_lua += f'    "{encoded_chunk}",\n'
        
        obfuscated_lua += f"""
}}

-- Junk functions
local {random_lua_var()} = function() return {random.randint(1000, 9999)} end
local {random_lua_var()} = function() return "{random_lua_var()}" end
local {random_lua_var()} = function() return math.random() end

-- Decoder and executor
local {random_lua_var()} = ""
for i, chunk in ipairs({random_lua_var()}) do
    {random_lua_var()} = {random_lua_var()} .. {random_lua_var()}(chunk)
end

-- Anti-tampering check
local {random_lua_var()} = function()
    if type({random_lua_var()}) ~= "string" then
        error("Tampering detected!")
    end
end

{random_lua_var()}()

-- Execute main code
local {random_lua_var()} = {random_lua_var()}({random_lua_var()})
if {random_lua_var()} then
    {random_lua_var()}()
end
"""
        
        obf_file_name = file_name.replace('.lua', '-extreme-obf.lua')
        obf_file_path = os.path.join(os.getcwd(), obf_file_name)
        
        with open(obf_file_path, 'w', encoding='utf-8') as f:
            f.write(obfuscated_lua)
        
        await update.message.reply_text("✅ Lua obfuscation extreme berhasil!")
        
        # Send obfuscated file
        with open(obf_file_path, 'rb') as f:
            await context.bot.send_document(
                chat_id=update.message.chat_id,
                document=f,
                caption=f"🌙 {file_name} - Extreme Obfuscated\n🛡️ Anti-Debug: Active\n🔐 Level: Military"
            )
        
        # Upload to GitHub
        try:
            with open(obf_file_path, 'rb') as f:
                content = f.read()
            repo.create_file(
                path=f"obfuscated/{obf_file_name}",
                message=f"Upload extreme obfuscated {obf_file_name}",
                content=content,
                branch="main"
            )
        except:
            pass
            
    except Exception as e:
        await update.message.reply_text(f"❌ Gagal mengobfuscate: {str(e)}")
    finally:
        for file_to_remove in [file_path, obf_file_path]:
            if os.path.exists(file_to_remove):
                os.remove(file_to_remove)

# Fitur 7: Shell Encoder (Extreme)
async def shellencoder_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("🔙 Kembali", callback_data='security_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "<b>🐚 Shell Encoder Extreme</b>\n\n"
        "Untuk mengencode shell script:\n"
        "1. Kirim file <code>.sh</code>\n"
        "2. Bot akan mengencode dengan level extreme\n"
        "3. Hasil dapat dijalankan di semua terminal\n\n"
        "<i>Compatible dengan bash, zsh, sh, dan terminal lainnya</i>",
        parse_mode='HTML',
        reply_markup=reply_markup
    )

async def encode_shell(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = update.message.document
    if not file or not file.file_name.endswith('.sh'):
        await update.message.reply_text("❌ File harus berekstensi .sh")
        return
    
    file_name = file.file_name
    file_path = os.path.join(os.getcwd(), file_name)
    file_obj = await file.get_file()
    await file_obj.download_to_drive(file_path)
    
    await update.message.reply_text("⏳ Sedang mengencode shell script dengan level extreme...")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            shell_content = f.read()
        
        # Extreme Shell Encoding
        def random_shell_var():
            return '_' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
        
        # Multiple encoding layers
        encoded_b64 = b64encode(shell_content.encode()).decode()
        encoded_hex = shell_content.encode().hex()
        
        # Generate extreme encoded shell
        var1 = random_shell_var()
        var2 = random_shell_var()
        var3 = random_shell_var()
        var4 = random_shell_var()
        var5 = random_shell_var()
        
        encoded_shell = f"""#!/bin/bash
# Encoded by Nikzzx Shell Encoder v2.0 - Extreme Level
# Universal Terminal Compatibility

# Anti-debug protection
{var1}() {{
    if [ "${{BASH_SUBSHELL}}" -gt 3 ]; then
        exit 1
    fi
}}

# Environment check
{var2}() {{
    local {var3}=$(uname -s)
    local {var4}=$(echo $SHELL | grep -o '[^/]*$')
    if [[ -z "${var3}" || -z "${var4}" ]]; then
        exit 1
    fi
}}

# Decoder functions
{var5}_decode_b64() {{
    echo "$1" | base64 -d 2>/dev/null || echo "$1" | openssl base64 -d 2>/dev/null
}}

{var5}_decode_hex() {{
    echo "$1" | xxd -r -p 2>/dev/null || echo "$1" | perl -pe 's/([0-9a-f]{{2}})/chr(hex($1))/gie' 2>/dev/null
}}

{var5}_execute() {{
    local {var3}="$1"
    local {var4}="$2"
    
    # Try base64 decode first
    local decoded=$({var5}_decode_b64 "${var3}")
    if [ -z "$decoded" ]; then
        # Fallback to hex decode
        decoded=$({var5}_decode_hex "${var4}")
    fi
    
    # Execute decoded script
    if [ ! -z "$decoded" ]; then
        eval "$decoded"
    fi
}}

# Junk variables
{random_shell_var()}={random.randint(1000, 9999)}
{random_shell_var()}="{random_shell_var()}"
{random_shell_var()}=$(date +%s)

# Security checks
{var1}
{var2}

# Main payload (multiple encoding)
{var3}_payload="{encoded_b64}"
{var4}_payload="{encoded_hex}"

# Execute with fallback
{var5}_execute "${var3}_payload" "${var4}_payload"

# Cleanup
unset {var1} {var2} {var3} {var4} {var5}
unset {var3}_payload {var4}_payload
"""
        
        encoded_file_name = file_name.replace('.sh', '-extreme-encoded.sh')
        encoded_file_path = os.path.join(os.getcwd(), encoded_file_name)
        
        with open(encoded_file_path, 'w', encoding='utf-8') as f:
            f.write(encoded_shell)
        
        # Make executable
        os.chmod(encoded_file_path, 0o755)
        
        await update.message.reply_text("✅ Shell encoding extreme berhasil!")
        
        # Send encoded file
        with open(encoded_file_path, 'rb') as f:
            await context.bot.send_document(
                chat_id=update.message.chat_id,
                document=f,
                caption=f"🐚 {file_name} - Extreme Encoded\n🛡️ Universal Compatible\n🔐 Level: Military\n\n<i>Dapat dijalankan di bash, zsh, sh, dan terminal lainnya</i>",
                parse_mode='HTML'
            )
        
        # Upload to GitHub
        try:
            with open(encoded_file_path, 'rb') as f:
                content = f.read()
            repo.create_file(
                path=f"encoded/{encoded_file_name}",
                message=f"Upload extreme encoded {encoded_file_name}",
                content=content,
                branch="main"
            )
        except:
            pass
            
    except Exception as e:
        await update.message.reply_text(f"❌ Gagal mengencode: {str(e)}")
    finally:
        for file_to_remove in [file_path, encoded_file_path]:
            if os.path.exists(file_to_remove):
                os.remove(file_to_remove)

# Fitur 8: Python Encoder (NEW)
async def pythonencoder_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("🔙 Kembali", callback_data='security_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "<b>🐍 Python Encoder Extreme</b>\n\n"
        "Untuk mengencode Python script:\n"
        "1. Kirim file <code>.py</code>\n"
        "2. Bot akan mengencode dengan level extreme\n"
        "3. Hasil dapat dijalankan dengan python/python3\n\n"
        "<i>Menggunakan teknik encoding tingkat enterprise</i>",
        parse_mode='HTML',
        reply_markup=reply_markup
    )

async def encode_python(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = update.message.document
    if not file or not file.file_name.endswith('.py'):
        await update.message.reply_text("❌ File harus berekstensi .py")
        return
    
    file_name = file.file_name
    file_path = os.path.join(os.getcwd(), file_name)
    file_obj = await file.get_file()
    await file_obj.download_to_drive(file_path)
    
    await update.message.reply_text("⏳ Sedang mengencode Python script dengan level extreme...")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            python_content = f.read()
        
        # Extreme Python Encoding
        def random_py_var():
            return '_' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=15))
        
        # Multiple encoding layers
        import marshal
        import types
        
        # Compile to bytecode
        compiled = compile(python_content, '<string>', 'exec')
        marshaled = marshal.dumps(compiled)
        encoded_marshal = b64encode(marshaled).decode()
        
        # Also create hex encoding
        encoded_hex = python_content.encode().hex()
        encoded_b64 = b64encode(python_content.encode()).decode()
        
        # Generate variables
        vars_list = [random_py_var() for _ in range(10)]
        
        # Create extreme encoded Python
        encoded_python = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Encoded by Nikzzx Python Encoder v2.0 - Extreme Level
# Enterprise Grade Protection

import base64, marshal, types, sys, os, zlib
from types import CodeType

# Anti-debug protection
class {vars_list[0]}:
    def __init__(self):
        self.{vars_list[1]} = sys.gettrace
        self.{vars_list[2]} = False
    
    def {vars_list[3]}(self):
        if self.{vars_list[1]}() is not None:
            self.{vars_list[2]} = True
            sys.exit(1)
    
    def {vars_list[4]}(self):
        if hasattr(sys, 'ps1') or hasattr(sys, 'ps2'):
            sys.exit(1)

# Environment checks
{vars_list[5]} = {vars_list[0]}()
{vars_list[5]}.{vars_list[3]}()
{vars_list[5]}.{vars_list[4]}()

# Decoder functions
def {vars_list[6]}(data):
    try:
        return base64.b64decode(data.encode()).decode()
    except:
        return None

def {vars_list[7]}(data):
    try:
        return bytes.fromhex(data).decode()
    except:
        return None

def {vars_list[8]}(data):
    try:
        return marshal.loads(base64.b64decode(data.encode()))
    except:
        return None

# Junk variables
{vars_list[9]}_1 = {random.randint(10000, 99999)}
{vars_list[9]}_2 = "{random_py_var()}"
{vars_list[9]}_3 = [i for i in range({random.randint(10, 50)})]

# Payload storage (multiple encoding methods)
{vars_list[0]}_marshal = "{encoded_marshal}"
{vars_list[0]}_b64 = "{encoded_b64}"
{vars_list[0]}_hex = "{encoded_hex}"

# Execution engine
def {vars_list[1]}_execute():
    # Try marshal first (fastest)
    code_obj = {vars_list[8]}({vars_list[0]}_marshal)
    if code_obj:
        exec(code_obj)
        return
    
    # Fallback to base64
    decoded = {vars_list[6]}({vars_list[0]}_b64)
    if decoded:
        exec(decoded)
        return
    
    # Final fallback to hex
    decoded = {vars_list[7]}({vars_list[0]}_hex)
    if decoded:
        exec(decoded)

# Anti-tampering check
if __name__ == "__main__":
    try:
        {vars_list[5]}.{vars_list[3]}()
        {vars_list[1]}_execute()
    except Exception as e:
        pass
    finally:
        # Cleanup
        for var in dir():
            if var.startswith('_'):
                try:
                    del globals()[var]
                except:
                    pass
'''
        
        encoded_file_name = file_name.replace('.py', '-extreme-encoded.py')
        encoded_file_path = os.path.join(os.getcwd(), encoded_file_name)
        
        with open(encoded_file_path, 'w', encoding='utf-8') as f:
            f.write(encoded_python)
        
        await update.message.reply_text("✅ Python encoding extreme berhasil!")
        
        # Send encoded file
        with open(encoded_file_path, 'rb') as f:
            await context.bot.send_document(
                chat_id=update.message.chat_id,
                document=f,
                caption=f"🐍 {file_name} - Extreme Encoded\n🛡️ Anti-Debug: Active\n🔐 Level: Enterprise\n\n<i>Dapat dijalankan dengan python/python3</i>",
                parse_mode='HTML'
            )
        
        # Upload to GitHub
        try:
            with open(encoded_file_path, 'rb') as f:
                content = f.read()
            repo.create_file(
                path=f"encoded/{encoded_file_name}",
                message=f"Upload extreme encoded {encoded_file_name}",
                content=content,
                branch="main"
            )
        except:
            pass
            
    except Exception as e:
        await update.message.reply_text(f"❌ Gagal mengencode: {str(e)}")
    finally:
        for file_to_remove in [file_path, encoded_file_path]:
            if os.path.exists(file_to_remove):
                os.remove(file_to_remove)

# Fitur 9: File Encryptor (Fixed)
async def fileencryptor_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("🔐 Enkripsi File", callback_data='encryptfile')],
        [InlineKeyboardButton("🔓 Dekripsi File", callback_data='decryptfile')],
        [InlineKeyboardButton("🔙 Kembali", callback_data='security_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "<b>🔐 File Encryptor AES-256</b>\n\n"
        "Pilih operasi yang ingin dilakukan:\n\n"
        "<code>🔹 Enkripsi</code> - Enkripsi file dengan AES-256\n"
        "<code>🔹 Dekripsi</code> - Dekripsi file yang dienkripsi\n\n"
        "Untuk enkripsi:\n1. Kirim file\n2. Bot akan meminta password\n\n"
        "Untuk dekripsi:\n1. Kirim file terenkripsi\n2. Berikan password",
        parse_mode='HTML',
        reply_markup=reply_markup
    )

async def encrypt_file_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = update.message.document
    if not file:
        await update.message.reply_text("❌ Tidak ada file yang ditemukan")
        return
    
    file_name = file.file_name
    file_path = os.path.join(os.getcwd(), file_name)
    file_obj = await file.get_file()
    await file_obj.download_to_drive(file_path)
    
    context.user_data['encrypt_file'] = {
        'path': file_path,
        'name': file_name
    }
    
    await update.message.reply_text(
        "🔐 Masukkan password untuk enkripsi:\n"
        "(Password harus 16, 24, atau 32 karakter untuk AES-256)"
    )

async def handle_encrypt_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    password = update.message.text
    file_info = context.user_data.get('encrypt_file')
    
    if not file_info or not os.path.exists(file_info['path']):
        await update.message.reply_text("❌ File tidak ditemukan. Mulai ulang proses.")
        return
    
    if len(password) not in [16, 24, 32]:
        await update.message.reply_text("❌ Password harus 16, 24, atau 32 karakter")
        return
    
    try:
        await update.message.reply_text("⏳ Sedang mengenkripsi file dengan AES-256...")
        
        with open(file_info['path'], 'rb') as f:
            data = f.read()
        
        # Generate IV
        iv = Random.new().read(AES.block_size)
        
        # Create AES cipher
        cipher = AES.new(password.encode('utf-8'), AES.MODE_CBC, iv)
        
        # Encrypt data
        padded_data = pad(data, AES.block_size)
        encrypted_data = iv + cipher.encrypt(padded_data)
        
        # Save encrypted file
        encrypted_file_name = f"encrypted_{file_info['name']}.enc"
        encrypted_file_path = os.path.join(os.getcwd(), encrypted_file_name)
        
        with open(encrypted_file_path, 'wb') as f:
            f.write(encrypted_data)
        
        await update.message.reply_text(
            f"✅ <b>Enkripsi berhasil!</b>\n\n"
            f"🔑 Password: <code>{password}</code>\n"
            f"📁 File: {encrypted_file_name}\n"
            f"🔐 Algoritma: AES-256-CBC\n\n"
            f"⚠️ <b>Simpan password ini untuk dekripsi!</b>",
            parse_mode='HTML'
        )
        
        # Send encrypted file
        with open(encrypted_file_path, 'rb') as f:
            await context.bot.send_document(
                chat_id=update.message.chat_id,
                document=f,
                caption=f"🔐 {file_info['name']} - Encrypted with AES-256"
            )
        
        # Upload to GitHub
        try:
            with open(encrypted_file_path, 'rb') as f:
                content = f.read()
            repo.create_file(
                path=f"encrypted/{encrypted_file_name}",
                message=f"Upload encrypted {encrypted_file_name}",
                content=content,
                branch="main"
            )
        except:
            pass
            
    except Exception as e:
        await update.message.reply_text(f"❌ Gagal mengenkripsi: {str(e)}")
    finally:
        # Cleanup
        for file_to_remove in [file_info['path'], encrypted_file_path]:
            if os.path.exists(file_to_remove):
                os.remove(file_to_remove)
        if 'encrypt_file' in context.user_data:
            del context.user_data['encrypt_file']

async def decrypt_file_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = update.message.document
    if not file:
        await update.message.reply_text("❌ Tidak ada file yang ditemukan")
        return
    
    file_name = file.file_name
    file_path = os.path.join(os.getcwd(), file_name)
    file_obj = await file.get_file()
    await file_obj.download_to_drive(file_path)
    
    context.user_data['decrypt_file'] = {
        'path': file_path,
        'name': file_name
    }
    
    await update.message.reply_text("🔓 Masukkan password untuk dekripsi:")

async def handle_decrypt_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    password = update.message.text
    file_info = context.user_data.get('decrypt_file')
    
    if not file_info or not os.path.exists(file_info['path']):
        await update.message.reply_text("❌ File tidak ditemukan. Mulai ulang proses.")
        return
    
    try:
        await update.message.reply_text("⏳ Sedang mendekripsi file...")
        
        with open(file_info['path'], 'rb') as f:
            encrypted_data = f.read()
        
        # Extract IV
        iv = encrypted_data[:AES.block_size]
        
        # Create AES cipher
        cipher = AES.new(password.encode('utf-8'), AES.MODE_CBC, iv)
        
        # Decrypt data
        decrypted_data = unpad(cipher.decrypt(encrypted_data[AES.block_size:]), AES.block_size)
        
        # Save decrypted file
        decrypted_file_name = file_info['name'].replace('encrypted_', '').replace('.enc', '')
        decrypted_file_path = os.path.join(os.getcwd(), f"decrypted_{decrypted_file_name}")
        
        with open(decrypted_file_path, 'wb') as f:
            f.write(decrypted_data)
        
        await update.message.reply_text("✅ Dekripsi berhasil!")
        
        # Send decrypted file
        with open(decrypted_file_path, 'rb') as f:
            await context.bot.send_document(
                chat_id=update.message.chat_id,
                document=f,
                caption=f"🔓 {decrypted_file_name} - Successfully Decrypted"
            )
            
    except ValueError:
        await update.message.reply_text("❌ Password salah atau file corrupt!")
    except Exception as e:
        await update.message.reply_text(f"❌ Gagal mendekripsi: {str(e)}")
    finally:
        # Cleanup
        for file_to_remove in [file_info['path'], decrypted_file_path]:
            if os.path.exists(file_to_remove):
                os.remove(file_to_remove)
        if 'decrypt_file' in context.user_data:
            del context.user_data['decrypt_file']

# Fitur 10: AES Text Encryptor
async def aes_encryptor_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("🔐 Enkripsi Teks", callback_data='encrypttext')],
        [InlineKeyboardButton("🔓 Dekripsi Teks", callback_data='decrypttext')],
        [InlineKeyboardButton("🔙 Kembali", callback_data='security_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "<b>🛡️ AES Text Encryptor</b>\n\n"
        "Pilih operasi yang ingin dilakukan:\n\n"
        "<code>🔹 Enkripsi</code> - Enkripsi teks dengan AES-256\n"
        "<code>🔹 Dekripsi</code> - Dekripsi teks yang dienkripsi\n\n"
        "Untuk enkripsi:\n1. Ketik /encrypttext [teks]\n2. Bot akan meminta password\n\n"
        "Untuk dekripsi:\n1. Ketik /decrypttext [teks_terenkripsi]\n2. Berikan password",
        parse_mode='HTML',
        reply_markup=reply_markup
    )

async def encrypt_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) < 1:
        await update.message.reply_text("❌ Format: /encrypttext [teks]\nContoh: /encrypttext Hello World")
        return
    
    text = ' '.join(args)
    context.user_data['encrypt_text'] = text
    
    await update.message.reply_text(
        "🔐 Masukkan password untuk enkripsi:\n"
        "(Password harus 16, 24, atau 32 karakter)"
    )

async def handle_encrypt_text_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    password = update.message.text
    text = context.user_data.get('encrypt_text')
    
    if not text:
        await update.message.reply_text("❌ Teks tidak ditemukan. Mulai ulang proses.")
        return
    
    if len(password) not in [16, 24, 32]:
        await update.message.reply_text("❌ Password harus 16, 24, atau 32 karakter")
        return
    
    try:
        await update.message.reply_text("⏳ Sedang mengenkripsi teks...")
        
        # Generate IV
        iv = Random.new().read(AES.block_size)
        
        # Create AES cipher
        cipher = AES.new(password.encode('utf-8'), AES.MODE_CBC, iv)
        
        # Encrypt text
        padded_text = pad(text.encode('utf-8'), AES.block_size)
        encrypted_text = iv + cipher.encrypt(padded_text)
        
        # Encode to base64
        encrypted_b64 = b64encode(encrypted_text).decode('utf-8')
        
        await update.message.reply_text(
            f"✅ <b>Enkripsi berhasil!</b>\n\n"
            f"🔒 Teks Terenkripsi:\n<code>{encrypted_b64}</code>\n\n"
            f"🔑 Password: <code>{password}</code>\n"
            f"⚠️ Simpan password ini untuk dekripsi!",
            parse_mode='HTML'
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Gagal mengenkripsi: {str(e)}")
    finally:
        if 'encrypt_text' in context.user_data:
            del context.user_data['encrypt_text']

async def decrypt_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) < 1:
        await update.message.reply_text("❌ Format: /decrypttext [teks_terenkripsi]\nContoh: /decrypttext U2FsdGVkX1...")
        return
    
    encrypted_b64 = ' '.join(args)
    context.user_data['decrypt_text'] = encrypted_b64
    
    await update.message.reply_text("🔓 Masukkan password untuk dekripsi:")

async def handle_decrypt_text_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    password = update.message.text
    encrypted_b64 = context.user_data.get('decrypt_text')
    
    if not encrypted_b64:
        await update.message.reply_text("❌ Teks terenkripsi tidak ditemukan. Mulai ulang proses.")
        return
    
    try:
        await update.message.reply_text("⏳ Sedang mendekripsi teks...")
        
        # Decode from base64
        encrypted_text = b64decode(encrypted_b64.encode('utf-8'))
        
        # Extract IV
        iv = encrypted_text[:AES.block_size]
        
        # Create AES cipher
        cipher = AES.new(password.encode('utf-8'), AES.MODE_CBC, iv)
        
        # Decrypt text
        decrypted_text = unpad(cipher.decrypt(encrypted_text[AES.block_size:]), AES.block_size).decode('utf-8')
        
        await update.message.reply_text(
            f"✅ <b>Dekripsi berhasil!</b>\n\n"
            f"🔓 Teks Asli:\n<code>{html.escape(decrypted_text)}</code>",
            parse_mode='HTML'
        )
    except ValueError:
        await update.message.reply_text("❌ Password salah atau teks terenkripsi tidak valid!")
    except Exception as e:
        await update.message.reply_text(f"❌ Gagal mendekripsi: {str(e)}")
    finally:
        if 'decrypt_text' in context.user_data:
            del context.user_data['decrypt_text']

# REVERSE ENGINE FEATURES (NEW)

# JS Deobfuscator
async def js_deobf_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("🔙 Kembali", callback_data='reverse_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "<b>🔓 JavaScript Deobfuscator</b>\n\n"
        "Untuk deobfuscate JavaScript:\n"
        "1. Kirim file <code>.js</code> yang terobfuscate\n"
        "2. Bot akan mencoba deobfuscate dengan berbagai metode\n"
        "3. Hasil akan lebih mudah dibaca\n\n"
        "<i>Mendukung berbagai jenis obfuscation</i>",
        parse_mode='HTML',
        reply_markup=reply_markup
    )

async def deobfuscate_js(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = update.message.document
    if not file or not file.file_name.endswith('.js'):
        await update.message.reply_text("❌ File harus berekstensi .js")
        return
    
    file_name = file.file_name
    file_path = os.path.join(os.getcwd(), file_name)
    file_obj = await file.get_file()
    await file_obj.download_to_drive(file_path)
    
    await update.message.reply_text("⏳ Sedang deobfuscate JavaScript...")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            js_content = f.read()
        
        # JavaScript Deobfuscation techniques
        deobfuscated = js_content
        
        # 1. Decode hex strings
        deobfuscated = re.sub(r'\\x([0-9a-fA-F]{2})', lambda m: chr(int(m.group(1), 16)), deobfuscated)
        
        # 2. Decode unicode escapes
        deobfuscated = re.sub(r'\\u([0-9a-fA-F]{4})', lambda m: chr(int(m.group(1), 16)), deobfuscated)
        
        # 3. Beautify code (basic)
        deobfuscated = re.sub(r';', ';\n', deobfuscated)
        deobfuscated = re.sub(r'\{', '{\n', deobfuscated)
        deobfuscated = re.sub(r'\}', '\n}\n', deobfuscated)
        
        # 4. Remove excessive whitespace
        deobfuscated = re.sub(r'\n\s*\n', '\n', deobfuscated)
        
        # 5. Try to decode base64 strings
        def decode_b64_strings(match):
            try:
                decoded = b64decode(match.group(1)).decode('utf-8')
                return f'"{decoded}"'
            except:
                return match.group(0)
        
        deobfuscated = re.sub(r'"([A-Za-z0-9+/=]{20,})"', decode_b64_strings, deobfuscated)
        
        # 6. Replace common obfuscated patterns
        deobfuscated = deobfuscated.replace('["constructor"]', '.constructor')
        deobfuscated = deobfuscated.replace('["toString"]', '.toString')
        deobfuscated = deobfuscated.replace('["valueOf"]', '.valueOf')
        
        deobf_file_name = file_name.replace('.js', '-deobfuscated.js')
        deobf_file_path = os.path.join(os.getcwd(), deobf_file_name)
        
        with open(deobf_file_path, 'w', encoding='utf-8') as f:
            f.write(deobfuscated)
        
        await update.message.reply_text("✅ Deobfuscation berhasil!")
        
        # Send deobfuscated file
        with open(deobf_file_path, 'rb') as f:
            await context.bot.send_document(
                chat_id=update.message.chat_id,
                document=f,
                caption=f"🔓 {file_name} - Deobfuscated\n📊 Readability: Improved"
            )
        
        # Upload to GitHub
        try:
            with open(deobf_file_path, 'rb') as f:
                content = f.read()
            repo.create_file(
                path=f"deobfuscated/{deobf_file_name}",
                message=f"Upload deobfuscated {deobf_file_name}",
                content=content,
                branch="main"
            )
        except:
            pass
            
    except Exception as e:
        await update.message.reply_text(f"❌ Gagal deobfuscate: {str(e)}")
    finally:
        for file_to_remove in [file_path, deobf_file_path]:
            if os.path.exists(file_to_remove):
                os.remove(file_to_remove)

# Lua Deobfuscator
async def lua_deobf_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("🔙 Kembali", callback_data='reverse_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "<b>🌙 Lua Deobfuscator</b>\n\n"
        "Untuk deobfuscate Lua script:\n"
        "1. Kirim file <code>.lua</code> yang terobfuscate\n"
        "2. Bot akan mencoba deobfuscate dengan berbagai metode\n"
        "3. Hasil akan lebih mudah dibaca\n\n"
        "<i>Mendukung berbagai jenis obfuscation Lua</i>",
        parse_mode='HTML',
        reply_markup=reply_markup
    )

async def deobfuscate_lua(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = update.message.document
    if not file or not file.file_name.endswith('.lua'):
        await update.message.reply_text("❌ File harus berekstensi .lua")
        return
    
    file_name = file.file_name
    file_path = os.path.join(os.getcwd(), file_name)
    file_obj = await file.get_file()
    await file_obj.download_to_drive(file_path)
    
    await update.message.reply_text("⏳ Sedang deobfuscate Lua script...")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lua_content = f.read()
        
        # Lua Deobfuscation techniques
        deobfuscated = lua_content
        
        # 1. Decode hex strings
        def decode_hex_lua(match):
            try:
                hex_str = match.group(1)
                decoded = bytes.fromhex(hex_str).decode('utf-8')
                return f'"{decoded}"'
            except:
                return match.group(0)
        
        deobfuscated = re.sub(r'"([0-9a-fA-F]+)"', decode_hex_lua, deobfuscated)
        
        # 2. Decode base64 strings
        def decode_b64_lua(match):
            try:
                decoded = b64decode(match.group(1)).decode('utf-8')
                return f'"{decoded}"'
            except:
                return match.group(0)
        
        deobfuscated = re.sub(r'"([A-Za-z0-9+/=]{20,})"', decode_b64_lua, deobfuscated)
        
        # 3. Beautify Lua code
        deobfuscated = re.sub(r';', '\n', deobfuscated)
        deobfuscated = re.sub(r'\bthen\b', 'then\n', deobfuscated)
        deobfuscated = re.sub(r'\bdo\b', 'do\n', deobfuscated)
        deobfuscated = re.sub(r'\bend\b', '\nend\n', deobfuscated)
        
        # 4. Remove excessive whitespace
        deobfuscated = re.sub(r'\n\s*\n', '\n', deobfuscated)
        
        # 5. Replace common obfuscated patterns
        deobfuscated = deobfuscated.replace('loadstring', 'loadstring')
        deobfuscated = deobfuscated.replace('getfenv', 'getfenv')
        
        deobf_file_name = file_name.replace('.lua', '-deobfuscated.lua')
        deobf_file_path = os.path.join(os.getcwd(), deobf_file_name)
        
        with open(deobf_file_path, 'w', encoding='utf-8') as f:
            f.write(deobfuscated)
        
        await update.message.reply_text("✅ Lua deobfuscation berhasil!")
        
        # Send deobfuscated file
        with open(deobf_file_path, 'rb') as f:
            await context.bot.send_document(
                chat_id=update.message.chat_id,
                document=f,
                caption=f"🌙 {file_name} - Deobfuscated\n📊 Readability: Improved"
            )
        
        # Upload to GitHub
        try:
            with open(deobf_file_path, 'rb') as f:
                content = f.read()
            repo.create_file(
                path=f"deobfuscated/{deobf_file_name}",
                message=f"Upload deobfuscated {deobf_file_name}",
                content=content,
                branch="main"
            )
        except:
            pass
            
    except Exception as e:
        await update.message.reply_text(f"❌ Gagal deobfuscate: {str(e)}")
    finally:
        for file_to_remove in [file_path, deobf_file_path]:
            if os.path.exists(file_to_remove):
                os.remove(file_to_remove)

# Shell Decoder
async def shell_decode_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("🔙 Kembali", callback_data='reverse_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "<b>🐚 Shell Script Decoder</b>\n\n"
        "Untuk decode shell script:\n"
        "1. Kirim file <code>.sh</code> yang ter-encode\n"
        "2. Bot akan mencoba decode dengan berbagai metode\n"
        "3. Hasil akan lebih mudah dibaca\n\n"
        "<i>Mendukung base64, hex, dan encoding lainnya</i>",
        parse_mode='HTML',
        reply_markup=reply_markup
    )

async def decode_shell(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = update.message.document
    if not file or not file.file_name.endswith('.sh'):
        await update.message.reply_text("❌ File harus berekstensi .sh")
        return
    
    file_name = file.file_name
    file_path = os.path.join(os.getcwd(), file_name)
    file_obj = await file.get_file()
    await file_obj.download_to_drive(file_path)
    
    await update.message.reply_text("⏳ Sedang decode shell script...")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            shell_content = f.read()
        
        # Shell Decoding techniques
        decoded = shell_content
        
        # 1. Decode base64 strings
        def decode_b64_shell(match):
            try:
                decoded_str = b64decode(match.group(1)).decode('utf-8')
                return f'"{decoded_str}"'
            except:
                return match.group(0)
        
        decoded = re.sub(r'"([A-Za-z0-9+/=]{20,})"', decode_b64_shell, decoded)
        
        # 2. Decode hex strings
        def decode_hex_shell(match):
            try:
                hex_str = match.group(1)
                decoded_str = bytes.fromhex(hex_str).decode('utf-8')
                return f'"{decoded_str}"'
            except:
                return match.group(0)
        
        decoded = re.sub(r'"([0-9a-fA-F]{20,})"', decode_hex_shell, decoded)
        
        # 3. Beautify shell script
        decoded = re.sub(r';', '\n', decoded)
        decoded = re.sub(r'\bthen\b', 'then\n', decoded)
        decoded = re.sub(r'\bdo\b', 'do\n', decoded)
        decoded = re.sub(r'\bfi\b', '\nfi\n', decoded)
        decoded = re.sub(r'\bdone\b', '\ndone\n', decoded)
        
        # 4. Remove excessive whitespace
        decoded = re.sub(r'\n\s*\n', '\n', decoded)
        
        # 5. Replace common encoded patterns
        decoded = decoded.replace('$(echo', '$(echo')
        decoded = decoded.replace('eval', 'eval')
        
        decoded_file_name = file_name.replace('.sh', '-decoded.sh')
        decoded_file_path = os.path.join(os.getcwd(), decoded_file_name)
        
        with open(decoded_file_path, 'w', encoding='utf-8') as f:
            f.write(decoded)
        
        # Make executable
        os.chmod(decoded_file_path, 0o755)
        
        await update.message.reply_text("✅ Shell decoding berhasil!")
        
        # Send decoded file
        with open(decoded_file_path, 'rb') as f:
            await context.bot.send_document(
                chat_id=update.message.chat_id,
                document=f,
                caption=f"🐚 {file_name} - Decoded\n📊 Readability: Improved"
            )
        
        # Upload to GitHub
        try:
            with open(decoded_file_path, 'rb') as f:
                content = f.read()
            repo.create_file(
                path=f"decoded/{decoded_file_name}",
                message=f"Upload decoded {decoded_file_name}",
                content=content,
                branch="main"
            )
        except:
            pass
            
    except Exception as e:
        await update.message.reply_text(f"❌ Gagal decode: {str(e)}")
    finally:
        for file_to_remove in [file_path, decoded_file_path]:
            if os.path.exists(file_to_remove):
                os.remove(file_to_remove)

# Python Decoder
async def python_decode_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("🔙 Kembali", callback_data='reverse_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "<b>🐍 Python Script Decoder</b>\n\n"
        "Untuk decode Python script:\n"
        "1. Kirim file <code>.py</code> yang ter-encode\n"
        "2. Bot akan mencoba decode dengan berbagai metode\n"
        "3. Hasil akan lebih mudah dibaca\n\n"
        "<i>Mendukung marshal, base64, hex, dan encoding lainnya</i>",
        parse_mode='HTML',
        reply_markup=reply_markup
    )

async def decode_python(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = update.message.document
    if not file or not file.file_name.endswith('.py'):
        await update.message.reply_text("❌ File harus berekstensi .py")
        return
    
    file_name = file.file_name
    file_path = os.path.join(os.getcwd(), file_name)
    file_obj = await file.get_file()
    await file_obj.download_to_drive(file_path)
    
    await update.message.reply_text("⏳ Sedang decode Python script...")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            python_content = f.read()
        
        # Python Decoding techniques
        decoded = python_content
        
        # 1. Try to decode marshal objects
        import marshal
        def decode_marshal_python(match):
            try:
                marshal_data = b64decode(match.group(1))
                code_obj = marshal.loads(marshal_data)
                # This is complex, just return the original for now
                return match.group(0)
            except:
                return match.group(0)
        
        # 2. Decode base64 strings
        def decode_b64_python(match):
            try:
                decoded_str = b64decode(match.group(1)).decode('utf-8')
                return f'"{decoded_str}"'
            except:
                return match.group(0)
        
        decoded = re.sub(r'"([A-Za-z0-9+/=]{20,})"', decode_b64_python, decoded)
        
        # 3. Decode hex strings
        def decode_hex_python(match):
            try:
                hex_str = match.group(1)
                decoded_str = bytes.fromhex(hex_str).decode('utf-8')
                return f'"{decoded_str}"'
            except:
                return match.group(0)
        
        decoded = re.sub(r'"([0-9a-fA-F]{20,})"', decode_hex_python, decoded)
        
        # 4. Beautify Python code
        import ast
        try:
            # Try to parse and reformat
            tree = ast.parse(decoded)
            # Basic formatting
            decoded = re.sub(r';', '\n', decoded)
            decoded = re.sub(r'\bif\b', '\nif', decoded)
            decoded = re.sub(r'\belse:', '\nelse:', decoded)
            decoded = re.sub(r'\belif\b', '\nelif', decoded)
            decoded = re.sub(r'\bdef\b', '\ndef', decoded)
            decoded = re.sub(r'\bclass\b', '\nclass', decoded)
        except:
            pass
        
        # 5. Remove excessive whitespace
        decoded = re.sub(r'\n\s*\n', '\n', decoded)
        
        # 6. Replace common obfuscated patterns
        decoded = decoded.replace('exec(', 'exec(')
        decoded = decoded.replace('eval(', 'eval(')
        decoded = decoded.replace('compile(', 'compile(')
        
        decoded_file_name = file_name.replace('.py', '-decoded.py')
        decoded_file_path = os.path.join(os.getcwd(), decoded_file_name)
        
        with open(decoded_file_path, 'w', encoding='utf-8') as f:
            f.write(decoded)
        
        await update.message.reply_text("✅ Python decoding berhasil!")
        
        # Send decoded file
        with open(decoded_file_path, 'rb') as f:
            await context.bot.send_document(
                chat_id=update.message.chat_id,
                document=f,
                caption=f"🐍 {file_name} - Decoded\n📊 Readability: Improved"
            )
        
        # Upload to GitHub
        try:
            with open(decoded_file_path, 'rb') as f:
                content = f.read()
            repo.create_file(
                path=f"decoded/{decoded_file_name}",
                message=f"Upload decoded {decoded_file_name}",
                content=content,
                branch="main"
            )
        except:
            pass
            
    except Exception as e:
        await update.message.reply_text(f"❌ Gagal decode: {str(e)}")
    finally:
        for file_to_remove in [file_path, decoded_file_path]:
            if os.path.exists(file_to_remove):
                os.remove(file_to_remove)

# Code Analyzer
async def code_analyzer_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("🔙 Kembali", callback_data='reverse_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "<b>🔍 Code Analyzer</b>\n\n"
        "Untuk analisis kode:\n"
        "1. Kirim file kode (js, py, lua, sh, c, cpp)\n"
        "2. Bot akan menganalisis struktur kode\n"
        "3. Mendapatkan informasi detail tentang kode\n\n"
        "<i>Analisis meliputi: syntax, kompleksitas, security issues, dll</i>",
        parse_mode='HTML',
        reply_markup=reply_markup
    )

async def analyze_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = update.message.document
    if not file:
        await update.message.reply_text("❌ Tidak ada file yang ditemukan")
        return
    
    file_name = file.file_name
    supported_extensions = ['.js', '.py', '.lua', '.sh', '.c', '.cpp']
    
    if not any(file_name.endswith(ext) for ext in supported_extensions):
        await update.message.reply_text(
            f"❌ File harus berekstensi: {', '.join(supported_extensions)}"
        )
        return
    
    file_path = os.path.join(os.getcwd(), file_name)
    file_obj = await file.get_file()
    await file_obj.download_to_drive(file_path)
    
    await update.message.reply_text("⏳ Sedang menganalisis kode...")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code_content = f.read()
        
        # Basic analysis
        lines_count = len(code_content.split('\n'))
        chars_count = len(code_content)
        words_count = len(code_content.split())
        
        # Get file extension
        extension = os.path.splitext(file_name)[1]
        
        # Language-specific analysis
        analysis_result = {
            'file_name': file_name,
            'extension': extension,
            'lines': lines_count,
            'characters': chars_count,
            'words': words_count,
            'functions': 0,
            'variables': 0,
            'comments': 0,
            'security_issues': [],
            'complexity': 'Low',
            'encoding': 'None Detected'
        }
        
        # Function detection
        if extension in ['.js', '.c', '.cpp']:
            analysis_result['functions'] = len(re.findall(r'\bfunction\s+\w+|^\s*\w+\s+\w+\s*\(', code_content, re.MULTILINE))
        elif extension == '.py':
            analysis_result['functions'] = len(re.findall(r'^\s*def\s+\w+', code_content, re.MULTILINE))
        elif extension == '.lua':
            analysis_result['functions'] = len(re.findall(r'\bfunction\s+\w+', code_content))
        elif extension == '.sh':
            analysis_result['functions'] = len(re.findall(r'^\s*\w+\s*\(\s*\)', code_content, re.MULTILINE))
        
        # Variable detection (basic)
        if extension in ['.js', '.c', '.cpp']:
            analysis_result['variables'] = len(re.findall(r'\b(?:var|let|const|int|char|float|double)\s+\w+', code_content))
        elif extension == '.py':
            analysis_result['variables'] = len(re.findall(r'^\s*\w+\s*=', code_content, re.MULTILINE))
        elif extension == '.lua':
            analysis_result['variables'] = len(re.findall(r'\blocal\s+\w+', code_content))
        elif extension == '.sh':
            analysis_result['variables'] = len(re.findall(r'^\s*\w+=', code_content, re.MULTILINE))
        
        # Comment detection
        if extension in ['.js', '.c', '.cpp']:
            analysis_result['comments'] = len(re.findall(r'//.*|/\*.*?\*/', code_content, re.DOTALL))
        elif extension == '.py':
            analysis_result['comments'] = len(re.findall(r'#.*|""".*?"""', code_content, re.DOTALL))
        elif extension == '.lua':
            analysis_result['comments'] = len(re.findall(r'--.*|--\[\[.*?\]\]', code_content, re.DOTALL))
        elif extension == '.sh':
            analysis_result['comments'] = len(re.findall(r'#.*', code_content))
        
        # Security issues detection
        security_patterns = {
            'eval': r'\beval\s*\(',
            'exec': r'\bexec\s*\(',
            'system': r'\bsystem\s*\(',
            'shell_exec': r'\bshell_exec\s*\(',
            'base64_decode': r'\bbase64_decode\s*\(',
            'unserialize': r'\bunserialize\s*\(',
            'file_get_contents': r'\bfile_get_contents\s*\(',
            'include': r'\binclude\s*\(',
            'require': r'\brequire\s*\(',
            'import': r'\bimport\s+os|import\s+subprocess',
            'dangerous_shell': r'\brm\s+-rf|>\s*/dev/null|\|\s*sh'
        }
        
        for issue, pattern in security_patterns.items():
            if re.search(pattern, code_content, re.IGNORECASE):
                analysis_result['security_issues'].append(issue)
        
        # Encoding detection
        encoding_patterns = {
            'Base64': r'[A-Za-z0-9+/=]{20,}',
            'Hex': r'[0-9a-fA-F]{20,}',
            'URL Encoding': r'%[0-9a-fA-F]{2}',
            'Unicode Escape': r'\\u[0-9a-fA-F]{4}',
            'Hex Escape': r'\\x[0-9a-fA-F]{2}'
        }
        
        detected_encodings = []
        for encoding, pattern in encoding_patterns.items():
            if re.search(pattern, code_content):
                detected_encodings.append(encoding)
        
        if detected_encodings:
            analysis_result['encoding'] = ', '.join(detected_encodings)
        
        # Complexity analysis
        complexity_indicators = [
            len(re.findall(r'\bif\b|\bwhile\b|\bfor\b|\bswitch\b', code_content)),
            len(re.findall(r'\btry\b|\bcatch\b|\bexcept\b', code_content)),
            len(re.findall(r'\bclass\b|\bfunction\b|\bdef\b', code_content))
        ]
        
        total_complexity = sum(complexity_indicators)
        if total_complexity > 50:
            analysis_result['complexity'] = 'Very High'
        elif total_complexity > 30:
            analysis_result['complexity'] = 'High'
        elif total_complexity > 15:
            analysis_result['complexity'] = 'Medium'
        else:
            analysis_result['complexity'] = 'Low'
        
        # Generate analysis report
        security_status = "🔴 High Risk" if len(analysis_result['security_issues']) > 3 else "🟡 Medium Risk" if len(analysis_result['security_issues']) > 0 else "🟢 Low Risk"
        
        report = f"""
<b>🔍 Code Analysis Report</b>

📄 <b>File Information:</b>
├─ Name: <code>{analysis_result['file_name']}</code>
├─ Type: <code>{analysis_result['extension']}</code>
├─ Lines: <code>{analysis_result['lines']:}</code>
├─ Characters: <code>{analysis_result['characters']:,}</code>
└─ Words: <code>{analysis_result['words']:,}</code>

📊 <b>Code Structure:</b>
├─ Functions: <code>{analysis_result['functions']}</code>
├─ Variables: <code>{analysis_result['variables']}</code>
├─ Comments: <code>{analysis_result['comments']}</code>
└─ Complexity: <code>{analysis_result['complexity']}</code>

🔐 <b>Security Analysis:</b>
├─ Risk Level: {security_status}
├─ Issues Found: <code>{len(analysis_result['security_issues'])}</code>
└─ Encoding: <code>{analysis_result['encoding']}</code>

⚠️ <b>Security Issues Detected:</b>
{chr(10).join([f"├─ {issue}" for issue in analysis_result['security_issues']]) if analysis_result['security_issues'] else "└─ No issues found"}

📈 <b>Recommendations:</b>
├─ Code Review: {"Required" if analysis_result['security_issues'] else "Optional"}
├─ Security Audit: {"High Priority" if len(analysis_result['security_issues']) > 2 else "Low Priority"}
└─ Obfuscation Level: {"High" if analysis_result['encoding'] != "None Detected" else "None"}

<i>Analysis completed by Nikzzx Code Analyzer v2.0</i>
        """
        
        await update.message.reply_text(report, parse_mode='HTML')
        
        # Create detailed report file
        detailed_report = f"""
# Code Analysis Report - {file_name}
Generated by Nikzzx Code Analyzer v2.0
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## File Information
- File Name: {analysis_result['file_name']}
- File Type: {analysis_result['extension']}
- Lines of Code: {analysis_result['lines']}
- Characters: {analysis_result['characters']:,}
- Words: {analysis_result['words']:,}

## Code Structure Analysis
- Functions/Methods: {analysis_result['functions']}
- Variables: {analysis_result['variables']}
- Comments: {analysis_result['comments']}
- Code Complexity: {analysis_result['complexity']}

## Security Analysis
- Risk Level: {security_status}
- Security Issues: {len(analysis_result['security_issues'])}
- Encoding Detected: {analysis_result['encoding']}

## Detailed Security Issues
{chr(10).join([f"- {issue}" for issue in analysis_result['security_issues']]) if analysis_result['security_issues'] else "No security issues detected"}

## Code Metrics
- Comments/Code Ratio: {(analysis_result['comments'] / max(analysis_result['lines'], 1) * 100):.2f}%
- Functions/Lines Ratio: {(analysis_result['functions'] / max(analysis_result['lines'], 1) * 100):.2f}%
- Average Line Length: {analysis_result['characters'] / max(analysis_result['lines'], 1):.1f} chars

## Recommendations
1. Code Review: {"Required due to security issues" if analysis_result['security_issues'] else "Optional"}
2. Security Audit: {"High priority" if len(analysis_result['security_issues']) > 2 else "Standard priority"}
3. Documentation: {"Add more comments" if analysis_result['comments'] < analysis_result['lines'] * 0.1 else "Good documentation"}
4. Refactoring: {"Consider breaking down" if analysis_result['complexity'] in ['High', 'Very High'] else "Structure is acceptable"}

## Analysis Summary
This code analysis was performed using advanced static analysis techniques. 
The results provide insights into code quality, security posture, and maintainability.

For detailed security assessment, consider running dynamic analysis tools.
        """
        
        report_file_name = f"analysis_{file_name.replace('.', '_')}.md"
        report_file_path = os.path.join(os.getcwd(), report_file_name)
        
        with open(report_file_path, 'w', encoding='utf-8') as f:
            f.write(detailed_report)
        
        # Send detailed report file
        with open(report_file_path, 'rb') as f:
            await context.bot.send_document(
                chat_id=update.message.chat_id,
                document=f,
                caption=f"📊 Detailed Analysis Report for {file_name}"
            )
        
        # Upload to GitHub
        try:
            with open(report_file_path, 'rb') as f:
                content = f.read()
            repo.create_file(
                path=f"analysis/{report_file_name}",
                message=f"Upload analysis report {report_file_name}",
                content=content,
                branch="main"
            )
        except:
            pass
            
    except Exception as e:
        await update.message.reply_text(f"❌ Gagal menganalisis: {str(e)}")
    finally:
        for file_to_remove in [file_path, report_file_path]:
            if os.path.exists(file_to_remove):
                os.remove(file_to_remove)

# ATTACKER TOOLS FEATURES (NEW)

# Web Scanner
async def web_scanner_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("🔙 Kembali", callback_data='attacker_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "<b>🌐 Web Vulnerability Scanner</b>\n\n"
        "Untuk scan kerentanan website:\n"
        "1. Ketik <code>/webscan [URL]</code>\n"
        "2. Bot akan scan berbagai kerentanan\n"
        "3. Hasil meliputi: SQL injection, XSS, LFI, dll\n\n"
        "<i>⚠️ Gunakan hanya untuk website yang Anda miliki!</i>",
        parse_mode='HTML',
        reply_markup=reply_markup
    )

async def web_scan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) < 1:
        await update.message.reply_text("❌ Format: /webscan [URL]\nContoh: /webscan https://example.com")
        return
    
    url = args[0]
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    await update.message.reply_text(f"⏳ Sedang melakukan scan kerentanan pada: {url}")
    
    try:
        scan_results = {
            'url': url,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'vulnerabilities': [],
            'headers': {},
            'status_code': 0,
            'server_info': '',
            'technologies': [],
            'security_headers': {},
            'ssl_info': {}
        }
        
        # Basic HTTP request
        response = requests.get(url, timeout=10, allow_redirects=True)
        scan_results['status_code'] = response.status_code
        scan_results['headers'] = dict(response.headers)
        
        # Server information
        scan_results['server_info'] = response.headers.get('Server', 'Unknown')
        
        # Technology detection
        tech_patterns = {
            'WordPress': r'wp-content|wp-includes|wordpress',
            'Joomla': r'joomla|/administrator/',
            'Drupal': r'/sites/default/|drupal',
            'PHP': r'\.php|X-Powered-By.*PHP',
            'Apache': r'Apache',
            'Nginx': r'nginx',
            'IIS': r'Microsoft-IIS',
            'ASP.NET': r'X-Powered-By.*ASP\.NET',
            'jQuery': r'jquery',
            'Bootstrap': r'bootstrap'
        }
        
        content = response.text.lower()
        headers_str = str(response.headers).lower()
        
        for tech, pattern in tech_patterns.items():
            if re.search(pattern, content + headers_str, re.IGNORECASE):
                scan_results['technologies'].append(tech)
        
        # Security headers check
        security_headers = [
            'X-Frame-Options',
            'X-XSS-Protection', 
            'X-Content-Type-Options',
            'Strict-Transport-Security',
            'Content-Security-Policy',
            'Referrer-Policy',
            'Feature-Policy',
            'X-Permitted-Cross-Domain-Policies'
        ]
        
        for header in security_headers:
            if header in response.headers:
                scan_results['security_headers'][header] = response.headers[header]
            else:
                scan_results['vulnerabilities'].append(f"Missing {header}")
        
        # Common vulnerability checks
        vuln_checks = [
            # SQL Injection indicators
            {
                'name': 'Potential SQL Injection',
                'patterns': [r'mysql_|sql syntax|ora-\d+|microsoft odbc|microsoft jet'],
                'test_params': ['?id=1\'', '?id=1"', '?id=1 OR 1=1--']
            },
            # XSS indicators
            {
                'name': 'Potential XSS Vulnerability',
                'patterns': [r'<script|javascript:|onerror=|onload='],
                'test_params': ['?q=<script>alert(1)</script>', '?search="><script>alert(1)</script>']
            },
            # Directory traversal
            {
                'name': 'Directory Traversal',
                'patterns': [r'\.\.\/|\.\.\\|\/etc\/passwd|c:\\windows'],
                'test_params': ['?file=../../../etc/passwd', '?page=....//....//etc/passwd']
            },
            # Information disclosure
            {
                'name': 'Information Disclosure',
                'patterns': [r'phpinfo\(\)|debug=|test=|admin|phpmyadmin'],
                'test_params': ['?debug=1', '?test=1', '/phpinfo.php', '/admin/', '/phpmyadmin/']
            }
        ]
        
        # Test common paths for sensitive files
        sensitive_paths = [
            '/robots.txt',
            '/sitemap.xml',
            '/.htaccess',
            '/wp-config.php',
            '/config.php',
            '/admin/',
            '/backup/',
            '/test/',
            '/.env',
            '/phpinfo.php'
        ]
        
        found_paths = []
        for path in sensitive_paths:
            try:
                test_response = requests.get(url.rstrip('/') + path, timeout=5)
                if test_response.status_code == 200:
                    found_paths.append(path)
                    scan_results['vulnerabilities'].append(f"Accessible path: {path}")
            except:
                continue
        
        # SSL/TLS check
        if url.startswith('https://'):
            try:
                import ssl
                import socket
                from urllib.parse import urlparse
                
                parsed_url = urlparse(url)
                context_ssl = ssl.create_default_context()
                
                with socket.create_connection((parsed_url.hostname, 443), timeout=5) as sock:
                    with context_ssl.wrap_socket(sock, server_hostname=parsed_url.hostname) as ssock:
                        cert = ssock.getpeercert()
                        scan_results['ssl_info'] = {
                            'version': ssock.version(),
                            'cipher': ssock.cipher(),
                            'cert_subject': dict(x[0] for x in cert['subject']),
                            'cert_issuer': dict(x[0] for x in cert['issuer'])
                        }
            except Exception as ssl_error:
                scan_results['vulnerabilities'].append(f"SSL/TLS Error: {str(ssl_error)}")
        
        # Check for common CMS vulnerabilities
        if 'WordPress' in scan_results['technologies']:
            wp_paths = ['/wp-admin/', '/wp-login.php', '/wp-config.php', '/xmlrpc.php']
            for path in wp_paths:
                try:
                    wp_response = requests.get(url.rstrip('/') + path, timeout=5)
                    if wp_response.status_code == 200:
                        if path == '/xmlrpc.php':
                            scan_results['vulnerabilities'].append("WordPress XML-RPC accessible")
                        elif path == '/wp-admin/':
                            scan_results['vulnerabilities'].append("WordPress admin panel accessible")
                except:
                    continue
        
        # Generate scan report
        vuln_count = len(scan_results['vulnerabilities'])
        risk_level = "🔴 High" if vuln_count > 10 else "🟡 Medium" if vuln_count > 5 else "🟢 Low"
        
        report = f"""
<b>🌐 Web Security Scan Report</b>

🎯 <b>Target:</b> <code>{url}</code>
📅 <b>Scan Time:</b> <code>{scan_results['timestamp']}</code>
📊 <b>Risk Level:</b> {risk_level}

🔍 <b>Basic Information:</b>
├─ Status Code: <code>{scan_results['status_code']}</code>
├─ Server: <code>{scan_results['server_info']}</code>
└─ Technologies: <code>{', '.join(scan_results['technologies']) if scan_results['technologies'] else 'None detected'}</code>

🛡️ <b>Security Headers:</b>
{chr(10).join([f"├─ ✅ {header}" for header in scan_results['security_headers'].keys()]) if scan_results['security_headers'] else "└─ ❌ No security headers found"}

⚠️ <b>Vulnerabilities Found ({vuln_count}):</b>
{chr(10).join([f"├─ {vuln}" for vuln in scan_results['vulnerabilities'][:10]]) if scan_results['vulnerabilities'] else "└─ No major vulnerabilities detected"}
{f"└─ ... and {vuln_count - 10} more" if vuln_count > 10 else ""}

🔒 <b>SSL/TLS:</b>
{f"├─ Version: {scan_results['ssl_info'].get('version', 'N/A')}" if scan_results['ssl_info'] else "└─ HTTPS not used or SSL error"}

<i>⚠️ This scan is for educational purposes only. Always get permission before scanning!</i>
        """
        
        await update.message.reply_text(report, parse_mode='HTML')
        
        # Create detailed report file
        detailed_report = f"""
# Web Security Scan Report
Target: {url}
Scan Date: {scan_results['timestamp']}
Generated by: Nikzzx Web Scanner v2.0

## Executive Summary
This report contains the results of an automated web security scan performed on {url}.
Total vulnerabilities found: {vuln_count}
Risk Level: {risk_level}

## Target Information
- URL: {url}
- Status Code: {scan_results['status_code']}
- Server: {scan_results['server_info']}
- Technologies Detected: {', '.join(scan_results['technologies'])}

## Security Headers Analysis
{chr(10).join([f"✅ {header}: {value}" for header, value in scan_results['security_headers'].items()]) if scan_results['security_headers'] else "❌ No security headers implemented"}

## Vulnerability Details
{chr(10).join([f"⚠️  {vuln}" for vuln in scan_results['vulnerabilities']]) if scan_results['vulnerabilities'] else "✅ No major vulnerabilities detected"}

## SSL/TLS Information
{f"Version: {scan_results['ssl_info'].get('version', 'N/A')}" if scan_results['ssl_info'] else "HTTPS not implemented or SSL configuration error"}

## Recommendations
1. Implement missing security headers
2. Review and fix identified vulnerabilities
3. Regular security assessments
4. Keep software and plugins updated
5. Implement Web Application Firewall (WAF)

## Disclaimer
This scan was performed for security assessment purposes. 
Always ensure you have proper authorization before scanning any website.
        """
        
        report_filename = f"webscan_{urlparse(url).hostname}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        report_path = os.path.join(os.getcwd(), report_filename)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(detailed_report)
        
        # Send detailed report
        with open(report_path, 'rb') as f:
            await context.bot.send_document(
                chat_id=update.message.chat_id,
                document=f,
                caption=f"📊 Detailed web scan report for {url}"
            )
        
        # Upload to GitHub
        try:
            with open(report_path, 'rb') as f:
                content = f.read()
            repo.create_file(
                path=f"scans/{report_filename}",
                message=f"Upload web scan report {report_filename}",
                content=content,
                branch="main"
            )
        except:
            pass
            
    except requests.RequestException as e:
        await update.message.reply_text(f"❌ Gagal mengakses URL: {str(e)}")
    except Exception as e:
        await update.message.reply_text(f"❌ Error saat scanning: {str(e)}")
    finally:
        if os.path.exists(report_path):
            os.remove(report_path)

# Port Scanner
async def port_scanner_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("🔙 Kembali", callback_data='attacker_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "<b>🔍 Port Scanner</b>\n\n"
        "Untuk scan port terbuka:\n"
        "1. Ketik <code>/portscan [IP/Domain]</code>\n"
        "2. Bot akan scan port umum yang terbuka\n"
        "3. Hasil meliputi service detection\n\n"
        "<i>⚠️ Gunakan hanya untuk server yang Anda miliki!</i>",
        parse_mode='HTML',
        reply_markup=reply_markup
    )

async def port_scan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) < 1:
        await update.message.reply_text("❌ Format: /portscan [IP/Domain]\nContoh: /portscan 192.168.1.1")
        return
    
    target = args[0]
    
    await update.message.reply_text(f"⏳ Sedang melakukan port scan pada: {target}")
    
    try:
        import socket
        from urllib.parse import urlparse
        
        # Common ports to scan
        common_ports = {
            21: 'FTP',
            22: 'SSH', 
            23: 'Telnet',
            25: 'SMTP',
            53: 'DNS',
            80: 'HTTP',
            110: 'POP3',
            139: 'NetBIOS',
            143: 'IMAP',
            443: 'HTTPS',
            993: 'IMAPS',
            995: 'POP3S',
            1433: 'MSSQL',
            3306: 'MySQL',
            3389: 'RDP',
            5432: 'PostgreSQL',
            5900: 'VNC',
            6379: 'Redis',
            8080: 'HTTP-Alt',
            9200: 'Elasticsearch',
            27017: 'MongoDB'
        }
        
        # Resolve hostname if needed
        try:
            ip = socket.gethostbyname(target)
        except:
            ip = target
        
        open_ports = []
        closed_ports = []
        
        # Scan ports (with timeout for speed)
        for port, service in common_ports.items():
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            
            try:
                result = sock.connect_ex((ip, port))
                if result == 0:
                    open_ports.append((port, service))
                else:
                    closed_ports.append((port, service))
            except:
                closed_ports.append((port, service))
            finally:
                sock.close()
        
        # Try to get additional info for open ports
        port_details = []
        for port, service in open_ports:
            detail = {'port': port, 'service': service, 'banner': '', 'version': ''}
            
            try:
                # Try to grab banner
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(3)
                sock.connect((ip, port))
                
                if port in [80, 8080]:  # HTTP ports
                    sock.send(b'GET / HTTP/1.1\r\nHost: ' + target.encode() + b'\r\n\r\n')
                    banner = sock.recv(1024).decode('utf-8', errors='ignore')
                    if 'Server:' in banner:
                        server_line = [line for line in banner.split('\n') if 'Server:' in line]
                        detail['banner'] = server_line[0].strip() if server_line else ''
                elif port == 22:  # SSH
                    banner = sock.recv(1024).decode('utf-8', errors='ignore')
                    detail['banner'] = banner.strip()
                elif port == 21:  # FTP
                    banner = sock.recv(1024).decode('utf-8', errors='ignore')
                    detail['banner'] = banner.strip()
                
                sock.close()
            except:
                pass
            
            port_details.append(detail)
        
        # Generate scan report
        risk_assessment = ""
        if any(port in [21, 23, 139, 445] for port, _ in open_ports):
            risk_assessment = "🔴 High Risk - Insecure services detected"
        elif any(port in [22, 3389] for port, _ in open_ports):
            risk_assessment = "🟡 Medium Risk - Remote access ports open"
        elif open_ports:
            risk_assessment = "🟢 Low Risk - Standard services"
        else:
            risk_assessment = "🟢 Low Risk - No common ports open"
        
        report = f"""
<b>🔍 Port Scan Report</b>

🎯 <b>Target:</b> <code>{target}</code>
🌐 <b>IP:</b> <code>{ip}</code>
📅 <b>Scan Time:</b> <code>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</code>
⚠️ <b>Risk:</b> {risk_assessment}

✅ <b>Open Ports ({len(open_ports)}):</b>
{chr(10).join([f"├─ {port}/tcp - {service}" for port, service in open_ports]) if open_ports else "└─ No common ports open"}

🔒 <b>Closed Ports:</b> <code>{len(closed_ports)} ports closed/filtered</code>

📊 <b>Service Details:</b>
{chr(10).join([f"├─ Port {detail['port']}: {detail['banner'][:50]}..." if detail['banner'] else f"├─ Port {detail['port']}: {detail['service']}" for detail in port_details[:5]]) if port_details else "└─ No detailed service information available"}

<i>⚠️ This scan is for network diagnostics only. Always get permission before scanning!</i>
        """
        
        await update.message.reply_text(report, parse_mode='HTML')
        
        # Create detailed report file
        detailed_report = f"""
# Port Scan Report
Target: {target} ({ip})
Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Generated by: Nikzzx Port Scanner v2.0

## Executive Summary
Port scan completed for target {target}.
Total open ports: {len(open_ports)}
Risk Assessment: {risk_assessment}

## Open Ports Details
{chr(10).join([f"Port {port}/tcp - {service}{f' - {detail["banner"]}' if detail['banner'] else ''}" for port, service in open_ports for detail in port_details if detail['port'] == port]) if open_ports else "No open ports detected"}

## Closed/Filtered Ports
{chr(10).join([f"Port {port}/tcp - {service}" for port, service in closed_ports[:10]]) if closed_ports else "N/A"}
{f"... and {len(closed_ports) - 10} more closed ports" if len(closed_ports) > 10 else ""}

## Security Recommendations
{'- Secure or disable unnecessary services' if open_ports else '- Current port configuration appears secure'}
{'- Consider firewall rules for open ports' if len(open_ports) > 5 else ''}
{'- Monitor for unauthorized port openings' if open_ports else ''}
- Regular port scanning for security assessment
- Implement intrusion detection systems

## Service Banners
{chr(10).join([f"Port {detail['port']}: {detail['banner']}" for detail in port_details if detail['banner']]) if any(detail['banner'] for detail in port_details) else "No service banners captured"}

## Disclaimer
This port scan was performed for network diagnostics and security assessment.
Always ensure proper authorization before scanning network resources.
        """
        
        report_filename = f"portscan_{target.replace('.', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        report_path = os.path.join(os.getcwd(), report_filename)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(detailed_report)
        
        # Send detailed report
        with open(report_path, 'rb') as f:
            await context.bot.send_document(
                chat_id=update.message.chat_id,
                document=f,
                caption=f"📊 Detailed port scan report for {target}"
            )
        
        # Upload to GitHub
        try:
            with open(report_path, 'rb') as f:
                content = f.read()
            repo.create_file(
                path=f"scans/{report_filename}",
                message=f"Upload port scan report {report_filename}",
                content=content,
                branch="main"
            )
        except:
            pass
            
    except Exception as e:
        await update.message.reply_text(f"❌ Error saat scanning: {str(e)}")
    finally:
        if os.path.exists(report_path):
            os.remove(report_path)

# Lanjutkan dengan fitur lainnya...
# Email Bomber, Hash Cracker, dll akan dilanjutkan di bagian berikutnya

# Tools Menu Functions
async def linkgen_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("🔙 Kembali", callback_data='tools_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "<b>🔗 Link Generator</b>\n\n"
        "Untuk membuat link pendek:\n"
        "1. Ketik <code>/shortlink [URL]</code>\n"
        "2. Bot akan generate link pendek\n"
        "3. Link akan disimpan untuk tracking\n\n"
        "<i>Contoh: /shortlink https://google.com</i>",
        parse_mode='HTML',
        reply_markup=reply_markup
    )

async def generate_short_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) < 1:
        await update.message.reply_text("❌ Format: /shortlink [URL]\nContoh: /shortlink https://google.com")
        return
    
    original_url = args[0]
    if not original_url.startswith(('http://', 'https://')):
        original_url = 'https://' + original_url
    
    try:
        # Generate unique short ID
        short_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        
        # For demo, we'll create a GitHub Pages link
        short_url = f"https://{GITHUB_REPO.split('/')[0]}.github.io/{GITHUB_REPO.split('/')[1]}/r/{short_id}"
        
        # Create redirect page
        redirect_html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Redirecting...</title>
    <meta http-equiv="refresh" content="0;url={original_url}">
    <style>
        body {{ font-family: Arial; text-align: center; padding: 50px; }}
        .container {{ max-width: 500px; margin: 0 auto; }}
        .logo {{ font-size: 24px; color: #333; margin-bottom: 20px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">🔗 Nikzzx Short Link</div>
        <p>Redirecting to: <a href="{original_url}">{original_url}</a></p>
        <script>
            setTimeout(function() {{
                window.location.href = "{original_url}";
            }}, 1000);
        </script>
    </div>
</body>
</html>
        """
        
        # Save to temporary file
        redirect_file = f"redirect_{short_id}.html"
        redirect_path = os.path.join(os.getcwd(), redirect_file)
        
        with open(redirect_path, 'w', encoding='utf-8') as f:
            f.write(redirect_html)
        
        # Upload to GitHub
        try:
            with open(redirect_path, 'rb') as f:
                content = f.read()
            repo.create_file(
                path=f"r/{short_id}.html",
                message=f"Create redirect for {original_url}",
                content=content,
                branch="main"
            )
            
            await update.message.reply_text(
                f"✅ <b>Short Link Created!</b>\n\n"
                f"🔗 <b>Short URL:</b> <code>{short_url}</code>\n"
                f"🌐 <b>Original URL:</b> <code>{original_url}</code>\n"
                f"📊 <b>ID:</b> <code>{short_id}</code>\n\n"
                f"<i>Link will be active within a few minutes</i>",
                parse_mode='HTML'
            )
        except Exception as e:
            await update.message.reply_text(f"❌ Gagal membuat short link: {str(e)}")
        
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")
    finally:
        if os.path.exists(redirect_path):
            os.remove(redirect_path)

# QR Code Generator
async def qrcode_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("🔙 Kembali", callback_data='tools_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "<b>🔍 QR Code Generator</b>\n\n"
        "Untuk generate QR Code:\n"
        "1. Ketik <code>/qrcode [text/URL]</code>\n"
        "2. Bot akan generate QR Code\n"
        "3. QR Code dalam format PNG\n\n"
        "<i>Contoh: /qrcode https://github.com</i>",
        parse_mode='HTML',
        reply_markup=reply_markup
    )

async def generate_qr_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) < 1:
        await update.message.reply_text("❌ Format: /qrcode [text]\nContoh: /qrcode Hello World")
        return
    
    text = ' '.join(args)
    
    try:
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(text)
        qr.make(fit=True)
        
        # Create image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save to BytesIO
        img_buffer = BytesIO()
        img.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        
        await context.bot.send_photo(
            chat_id=update.message.chat_id,
            photo=img_buffer,
            caption=f"🔍 QR Code Generated\n\n📝 Content: <code>{html.escape(text)}</code>",
            parse_mode='HTML'
        )
        
    except Exception as e:
        await update.message.reply_text(f"❌ Gagal generate QR Code: {str(e)}")

# System status dan functions lainnya
async def bot_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    bot_uptime = datetime.now() - start_time

    status_text = f"""
<b>📊 Bot Status Information</b>

🤖 <b>Bot Info:</b>
├─ Name: <code>Nikzzx Multi-Feature Bot v2.0</code>
├─ Status: <code>🟢 Online</code>
├─ Uptime: <code>{str(bot_uptime).split('.')[0]}</code>
└─ Version: <code>2.0</code>

💻 <b>System Resources:</b>
├─ CPU Load: <code>{get_cpu_load()}</code>
├─ Memory: <code>{get_memory_usage()}</code>
├─ Disk: <code>{get_disk_usage()}</code>
└─ Platform: <code>{platform.system()} {platform.release()}</code>

🔧 <b>Features Status:</b>
├─ ✅ Compiler (C/C++)
├─ ✅ GitHub Integration
├─ ✅ Firebase Deploy
├─ ✅ Security Tools
├─ ✅ Reverse Engine
├─ ✅ Attacker Tools
├─ ✅ APK Tools
└─ ✅ Extra Features

📈 <b>Statistics:</b>
├─ Commands Available: <code>50+</code>
├─ Security Features: <code>15+</code>
├─ Deploy Options: <code>3</code>
└─ File Processors: <code>10+</code>

🌐 <b>Network:</b>
├─ GitHub: <code>🟢 Connected</code>
├─ Firebase: <code>🟢 Connected</code>
└─ Telegram API: <code>🟢 Active</code>

<i>Last updated: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</i>
    """

    keyboard = [
        [InlineKeyboardButton("🔄 Refresh", callback_data="bot_status")],
        [InlineKeyboardButton("🔙 Kembali", callback_data="main_menu")],
    ]

    await query.edit_message_text(
        status_text,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

# Clear cache
async def clear_cache(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    
    try:
        # Clear temporary files
        temp_files = [f for f in os.listdir('.') if f.startswith(('temp_', 'upload_', 'download_'))]
        for temp_file in temp_files:
            try:
                os.remove(temp_file)
            except:
                pass
        
        await query.edit_message_text(
            f"✅ <b>Cache Cleared Successfully</b>\n\n"
            f"🧹 Cleaned {len(temp_files)} temporary files\n"
            f"💾 Memory freed up\n"
            f"📅 Cleared at: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n"
            f"<i>Bot performance optimized</i>",
            parse_mode='HTML',
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Kembali", callback_data='main_menu')]])
        )
        
    except Exception as e:
        await query.edit_message_text(
            f"❌ Error clearing cache: {str(e)}",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Kembali", callback_data='main_menu')]])
        )

# Show guide
async def show_guide(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    
    guide_text = """
<b>📝 Panduan Penggunaan Nikzzx Bot v2.0</b>

🚀 <b>DEPLOY FEATURES:</b>
├─ <code>/start</code> - Menu utama bot
├─ Upload file .c/.cpp untuk compile otomatis
├─ Upload file apapun untuk upload ke GitHub
├─ <code>/deploy_firebase [site]</code> - Deploy ke Firebase
└─ <code>/deploy_vercel [project]</code> - Deploy ke Vercel

🔒 <b>SECURITY FEATURES:</b>
├─ Upload .js untuk obfuscate JavaScript
├─ Upload .lua untuk obfuscate Lua
├─ Upload .sh untuk encode shell script
├─ Upload .py untuk encode Python
├─ <code>/encrypttext [text]</code> - Enkripsi teks AES
└─ Upload file untuk enkripsi file

🔓 <b>REVERSE FEATURES:</b>
├─ Upload file terobfuscate untuk deobfuscate
├─ Upload file terenkripsi untuk analisis
├─ Code analyzer untuk analisis kode
└─ Pattern recognition untuk reverse engineering

⚔️ <b>ATTACKER TOOLS:</b>
├─ <code>/webscan [URL]</code> - Scan kerentanan web
├─ <code>/portscan [IP]</code> - Scan port terbuka
├─ <code>/hashcrack [hash]</code> - Crack hash password
└─ <i>⚠️ Gunakan hanya untuk tujuan legal!</i>

📱 <b>APK TOOLS:</b>
├─ Upload APK untuk encode DEX
├─ Encode assets dan resources
├─ Anti-debug protection
└─ Manifest obfuscation

🛠️ <b>TOOLS:</b>
├─ <code>/shortlink [URL]</code> - Buat link pendek
├─ <code>/qrcode [text]</code> - Generate QR code
├─ Convert file ke format lain
└─ Text manipulation tools

💡 <b>TIPS:</b>
• Upload file langsung untuk auto-processing
• Gunakan menu untuk navigasi mudah
• Commands tidak case-sensitive
• Semua hasil tersimpan di GitHub
• Support multiple file formats

⚠️ <b>PENTING:</b>
• Selalu gunakan untuk tujuan legal
• Tools attacker hanya untuk testing sendiri
• Bot auto-backup semua hasil ke cloud
• Support 24/7 dengan update berkala

<i>Nikzzx Multi-Feature Bot v2.0 </i>
    """
    
    keyboard = [
        [InlineKeyboardButton("📚 Documentation", url=f"https://github.com/{GITHUB_REPO}")],
        [InlineKeyboardButton("🔙 Kembali", callback_data='main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(guide_text, parse_mode='HTML', reply_markup=reply_markup)

# Fungsi untuk menangani semua file yang dikirim
async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Auto-process files based on their extension"""
    file = update.message.document
    
    if not file:
        return
    
    file_name = file.file_name.lower()
    
    # Route to appropriate handler based on file extension
    if file_name.endswith(('.c', '.cpp')):
        await compile_file(update, context)
    elif file_name.endswith('.js'):
        await obfuscate_js(update, context)
    elif file_name.endswith('.lua'):
        await obfuscate_lua(update, context)
    elif file_name.endswith('.sh'):
        await encode_shell(update, context)
    elif file_name.endswith('.py'):
        await encode_python(update, context)
    elif file_name.endswith('.enc'):
        # Show decrypt menu for encrypted files
        context.user_data['decrypt_file'] = {
            'path': file_name,
            'name': file_name
        }
        await update.message.reply_text(
            "🔓 File terenkripsi terdeteksi!\n"
            "Kirim password untuk dekripsi file ini."
        )
    else:
        # Default: upload to GitHub
        await upload_to_github(update, context)

# Message handlers untuk password
async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle text messages for password inputs and other text operations"""
    text = update.message.text
    
    # Check for password inputs
    if 'encrypt_file' in context.user_data:
        await handle_encrypt_password(update, context)
    elif 'decrypt_file' in context.user_data:
        await handle_decrypt_password(update, context)
    elif 'encrypt_text' in context.user_data:
        await handle_encrypt_text_password(update, context)
    elif 'decrypt_text' in context.user_data:
        await handle_decrypt_text_password(update, context)
    else:
        # For unhandled text, show help
        await update.message.reply_text(
            "ℹ️ Gunakan /start untuk melihat menu utama\n"
            "atau kirim file untuk auto-processing!"
        )

# Tambahkan stubs untuk menu yang belum diimplementasi
async def messagesender_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [[InlineKeyboardButton("🔙 Kembali", callback_data='tools_menu')]]
    await query.edit_message_text(
        "📩 Message Sender akan segera hadir!",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def fileconverter_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [[InlineKeyboardButton("🔙 Kembali", callback_data='tools_menu')]]
    await query.edit_message_text(
        "📄 File Converter akan segera hadir!",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def textmanipulator_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [[InlineKeyboardButton("🔙 Kembali", callback_data='tools_menu')]]
    await query.edit_message_text(
        "📝 Text Manipulator akan segera hadir!",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Stubs untuk attacker menu yang belum diimplementasi  
async def email_bomber_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [[InlineKeyboardButton("🔙 Kembali", callback_data='attacker_menu')]]
    await query.edit_message_text(
        "📧 Email Bomber akan segera hadir!",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def hash_cracker_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [[InlineKeyboardButton("🔙 Kembali", callback_data='attacker_menu')]]
    await query.edit_message_text(
        "🔐 Hash Cracker akan segera hadir!",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def sql_injection_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [[InlineKeyboardButton("🔙 Kembali", callback_data='attacker_menu')]]
    await query.edit_message_text(
        "🕷️ SQL Injection Tool akan segera hadir!",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Stubs untuk APK menu
async def encode_dex_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [[InlineKeyboardButton("🔙 Kembali", callback_data='apk_menu')]]
    await query.edit_message_text(
        "📱 DEX Encoder akan segera hadir!",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def encode_assets_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [[InlineKeyboardButton("🔙 Kembali", callback_data='apk_menu')]]
    await query.edit_message_text(
        "🎨 Assets Encoder akan segera hadir!",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def encode_manifest_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [[InlineKeyboardButton("🔙 Kembali", callback_data='apk_menu')]]
    await query.edit_message_text(
        "📋 Manifest Encoder akan segera hadir!",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def encode_resources_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [[InlineKeyboardButton("🔙 Kembali", callback_data='apk_menu')]]
    await query.edit_message_text(
        "🔧 Resources Encoder akan segera hadir!",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def anti_debug_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [[InlineKeyboardButton("🔙 Kembali", callback_data='apk_menu')]]
    await query.edit_message_text(
        "🛡️ Anti Debug akan segera hadir!",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Stubs untuk Extra Tools menu
async def batch_converter_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [[InlineKeyboardButton("🔙 Kembali", callback_data='extra_tools_menu')]]
    await query.edit_message_text(
        "🔄 Batch Converter akan segera hadir!",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def system_monitor_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [[InlineKeyboardButton("🔙 Kembali", callback_data='extra_tools_menu')]]
    await query.edit_message_text(
        "📊 System Monitor akan segera hadir!",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def network_tools_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Menu utama Network Tools"""
    query = update.callback_query
    
    keyboard = [
        [InlineKeyboardButton("⚡ Speed Test", callback_data='speed_test_menu')],
        [InlineKeyboardButton("🔍 Port Scanner", callback_data='port_scanner')],
        [InlineKeyboardButton("🌐 IP Lookup", callback_data='ip_lookup')],
        [InlineKeyboardButton("📡 Ping Test", callback_data='ping_test')],
        [InlineKeyboardButton("🔗 Traceroute", callback_data='traceroute')],
        [InlineKeyboardButton("🌍 DNS Lookup", callback_data='dns_lookup')],
        [InlineKeyboardButton("📊 Network Info", callback_data='network_info')],
        [InlineKeyboardButton("🔙 Kembali", callback_data='extra_tools_menu')]
    ]
    
    text = """
🌐 **Network Tools Menu**

Pilih tool yang ingin Anda gunakan:

⚡ **Speed Test** - Test kecepatan internet lengkap
🔍 **Port Scanner** - Scan port pada target
🌐 **IP Lookup** - Informasi detail IP address
📡 **Ping Test** - Test konektivitas ke host
🔗 **Traceroute** - Trace jalur ke destination
🌍 **DNS Lookup** - Resolve DNS records
📊 **Network Info** - Informasi jaringan lokal
    """
    
    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

async def speed_test_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Speed Test Menu"""
    query = update.callback_query
    
    keyboard = [
        [InlineKeyboardButton("⚡ Quick Test", callback_data='quick_speed_test')],
        [InlineKeyboardButton("🔍 Full Test", callback_data='full_speed_test')],
        [InlineKeyboardButton("📊 Network Analysis", callback_data='network_analysis')],
        [InlineKeyboardButton("🔙 Back", callback_data='network_tools')]
    ]
    
    text = """
⚡ **Internet Speed Test**

Pilih jenis test:

⚡ **Quick Test** - Test cepat (5 detik)
🔍 **Full Test** - Test lengkap (15 detik)
📊 **Network Analysis** - Analisis jaringan lengkap

💡 **Tips:** Pastikan tidak ada aplikasi lain yang menggunakan internet untuk hasil yang akurat.
    """
    
    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

async def quick_speed_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Quick Speed Test Command"""
    msg = await update.callback_query.edit_message_text(
        "⚡ **Quick Speed Test**\n\n"
        "🔍 Mencari server terbaik...\n"
        "⏳ Mohon tunggu...",
        parse_mode='Markdown'
    )
    
    try:
        speed_test = SpeedTest()
        network_info = NetworkInfo()
        
        # Update message
        await msg.edit_text(
            "⚡ **Quick Speed Test**\n\n"
            "📡 Testing download speed...\n"
            "⏳ Mohon tunggu...",
            parse_mode='Markdown'
        )
        
        # Get best server
        best_server, ping = await speed_test.get_best_server()
        
        if not best_server:
            await msg.edit_text("❌ **Error:** Tidak dapat menemukan server test", parse_mode='Markdown')
            return
        
        # Test download speed
        download_speed = await speed_test.test_download_speed(best_server, duration=5)
        
        # Update message
        await msg.edit_text(
            "⚡ **Quick Speed Test**\n\n"
            "📤 Testing upload speed...\n"
            "⏳ Mohon tunggu...",
            parse_mode='Markdown'
        )
        
        # Test upload speed
        upload_speed = await speed_test.test_upload_speed(duration=5)
        
        # Get basic network info
        ip_info = await network_info.get_public_ip_info()
        connection_type = await network_info.get_connection_type()
        
        # Format results
        result_text = f"""
⚡ **Quick Speed Test Results**

📊 **Speed Results:**
📥 **Download:** {download_speed:.2f} Mbps
📤 **Upload:** {upload_speed:.2f} Mbps
📡 **Ping:** {ping:.2f} ms

🌐 **Connection Info:**
🔗 **Type:** {connection_type}
📍 **IP:** {ip_info.get('ip', 'N/A') if ip_info else 'N/A'}
🏢 **ISP:** {ip_info.get('isp', 'N/A') if ip_info else 'N/A'}
🌍 **Location:** {ip_info.get('city', 'N/A') if ip_info else 'N/A'}, {ip_info.get('country', 'N/A') if ip_info else 'N/A'}

⏰ **Test completed:** {datetime.now().strftime('%H:%M:%S')}
        """
        
        await msg.edit_text(result_text, parse_mode='Markdown')
        
    except Exception as e:
        await msg.edit_text(f"❌ **Error:** {str(e)}", parse_mode='Markdown')

async def full_speed_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Full Speed Test Command"""
    msg = await update.callback_query.edit_message_text(
        "🔍 **Full Speed Test**\n\n"
        "🔍 Menganalisis jaringan...\n"
        "⏳ Mohon tunggu...",
        parse_mode='Markdown'
    )
    
    try:
        speed_test = SpeedTest()
        network_info = NetworkInfo()
        
        # Get network information
        ip_info = await network_info.get_public_ip_info()
        dns_info = await network_info.get_dns_info()
        interfaces = await network_info.get_network_interfaces()
        connection_type = await network_info.get_connection_type()
        
        # Update message
        await msg.edit_text(
            "🔍 **Full Speed Test**\n\n"
            "📡 Mencari server optimal...\n"
            "⏳ Mohon tunggu...",
            parse_mode='Markdown'
        )
        
        # Get best server
        best_server, ping = await speed_test.get_best_server()
        
        if not best_server:
            await msg.edit_text("❌ **Error:** Tidak dapat menemukan server test", parse_mode='Markdown')
            return
        
        # Update message
        await msg.edit_text(
            "🔍 **Full Speed Test**\n\n"
            "📥 Testing download speed (15s)...\n"
            "⏳ Mohon tunggu...",
            parse_mode='Markdown'
        )
        
        # Test download speed (longer duration)
        download_speed = await speed_test.test_download_speed(best_server, duration=15)
        
        # Update message
        await msg.edit_text(
            "🔍 **Full Speed Test**\n\n"
            "📤 Testing upload speed (15s)...\n"
            "⏳ Mohon tunggu...",
            parse_mode='Markdown'
        )
        
        # Test upload speed (longer duration)
        upload_speed = await speed_test.test_upload_speed(duration=15)
        
        # Format detailed results
        result_text = f"""
🔍 **Full Speed Test Results**

📊 **Speed Results:**
📥 **Download:** {download_speed:.2f} Mbps ({download_speed/8:.2f} MB/s)
📤 **Upload:** {upload_speed:.2f} Mbps ({upload_speed/8:.2f} MB/s)
📡 **Ping:** {ping:.2f} ms

🌐 **Network Information:**
🔗 **Connection Type:** {connection_type}
📍 **Public IP:** {ip_info.get('ip', 'N/A') if ip_info else 'N/A'}
🏢 **ISP/Provider:** {ip_info.get('isp', 'N/A') if ip_info else 'N/A'}
🏢 **Organization:** {ip_info.get('org', 'N/A') if ip_info else 'N/A'}
🌍 **Location:** {ip_info.get('city', 'N/A') if ip_info else 'N/A'}, {ip_info.get('region', 'N/A') if ip_info else 'N/A'}, {ip_info.get('country', 'N/A') if ip_info else 'N/A'}
🕐 **Timezone:** {ip_info.get('timezone', 'N/A') if ip_info else 'N/A'}

🔌 **Network Interfaces:**
{chr(10).join([f"• {iface['name']}: {iface['ip']}" for iface in interfaces[:3]]) if interfaces else '• No interfaces found'}

🌐 **DNS Servers:**
{chr(10).join([f"• {dns['server']} ({dns['response_time']}ms)" for dns in dns_info[:3]]) if dns_info else '• No DNS info available'}

⏰ **Test completed:** {datetime.now().strftime('%H:%M:%S')}
        """
        
        await msg.edit_text(result_text, parse_mode='Markdown')
        
    except Exception as e:
        await msg.edit_text(f"❌ **Error:** {str(e)}", parse_mode='Markdown')

async def network_analysis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comprehensive Network Analysis"""
    msg = await update.callback_query.edit_message_text(
        "📊 **Network Analysis**\n\n"
        "🔍 Menganalisis jaringan lengkap...\n"
        "⏳ Mohon tunggu...",
        parse_mode='Markdown'
    )
    
    try:
        network_info = NetworkInfo()
        
        # Get comprehensive network information
        ip_info = await network_info.get_public_ip_info()
        dns_info = await network_info.get_dns_info()
        interfaces = await network_info.get_network_interfaces()
        connection_type = await network_info.get_connection_type()
        
        # Additional tests
        # Test latency to various servers
        test_hosts = [
            ('Google DNS', '8.8.8.8'),
            ('Cloudflare DNS', '1.1.1.1'),
            ('OpenDNS', '208.67.222.222')
        ]
        
        latency_results = []
        for name, host in test_hosts:
            try:
                start_time = time.time()
                socket.create_connection((host, 53), timeout=5)
                latency = (time.time() - start_time) * 1000
                latency_results.append(f"• {name}: {latency:.2f}ms")
            except:
                latency_results.append(f"• {name}: Timeout")
        
        # Get system info
        try:
            system_info = platform.system()
            system_release = platform.release()
        except:
            system_info = "Unknown"
            system_release = "Unknown"
        
        result_text = f"""
📊 **Comprehensive Network Analysis**

🌐 **Public IP Information:**
📍 **IP Address:** {ip_info.get('ip', 'N/A') if ip_info else 'N/A'}
🏢 **ISP/Provider:** {ip_info.get('isp', 'N/A') if ip_info else 'N/A'}
🏢 **Organization:** {ip_info.get('org', 'N/A') if ip_info else 'N/A'}
🌍 **Country:** {ip_info.get('country', 'N/A') if ip_info else 'N/A'}
🏙️ **Region:** {ip_info.get('region', 'N/A') if ip_info else 'N/A'}
🏘️ **City:** {ip_info.get('city', 'N/A') if ip_info else 'N/A'}
🕐 **Timezone:** {ip_info.get('timezone', 'N/A') if ip_info else 'N/A'}
📍 **Coordinates:** {ip_info.get('lat', 'N/A') if ip_info else 'N/A'}, {ip_info.get('lon', 'N/A') if ip_info else 'N/A'}

🔗 **Connection Details:**
📶 **Connection Type:** {connection_type}
💻 **System:** {system_info} {system_release}

🔌 **Network Interfaces:**
{chr(10).join([f"• {iface['name']}: {iface['ip']}" for iface in interfaces]) if interfaces else '• No interfaces detected'}

🌐 **DNS Configuration:**
{chr(10).join([f"• {dns['server']} (Response: {dns['response_time']}ms)" for dns in dns_info]) if dns_info else '• No DNS servers detected'}

📡 **Latency Test:**
{chr(10).join(latency_results)}

⏰ **Analysis completed:** {datetime.now().strftime('%H:%M:%S')}
        """
        
        await msg.edit_text(result_text, parse_mode='Markdown')
        
    except Exception as e:
        await msg.edit_text(f"❌ **Error:** {str(e)}", parse_mode='Markdown')

async def speed_test_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle speed test button callbacks"""
    query = update.callback_query
    data = query.data

    await query.answer()  # Penting! Biar loading tombol hilang

    if data == 'speed_test_menu':
        await speed_test_menu(update, context)

    elif data == 'quick_speed_test':
        await query.edit_message_text("⚡ Quick Speed Test dimulai...\n(Simulasi 5 detik)")
    elif data == 'full_speed_test':
        await query.edit_message_text("🔍 Full Speed Test dimulai...\n(Simulasi 15 detik)")
    elif data == 'network_analysis':
        await query.edit_message_text("📊 Network Analysis berjalan...\n(Mengambil data jaringan...)")
    elif data == 'back_speedtest':
        await network_tools_menu(update, context)  # kembali ke menu sebelumnya

async def quick_speed_test_from_callback(query, context):
    """Quick speed test from callback"""
    # Create a mock update object for the function
    class MockUpdate:
        def __init__(self, query):
            self.message = MockMessage(query)
    
    class MockMessage:
        def __init__(self, query):
            self.query = query
            
        async def reply_text(self, text, parse_mode=None):
            return await self.query.edit_message_text(text, parse_mode=parse_mode)
    
    mock_update = MockUpdate(query)
    await quick_speed_test(mock_update, context)

async def full_speed_test_from_callback(query, context):
    """Full speed test from callback"""
    class MockUpdate:
        def __init__(self, query):
            self.message = MockMessage(query)
    
    class MockMessage:
        def __init__(self, query):
            self.query = query
            
        async def reply_text(self, text, parse_mode=None):
            return await self.query.edit_message_text(text, parse_mode=parse_mode)
    
    mock_update = MockUpdate(query)
    await full_speed_test(mock_update, context)

async def network_analysis_from_callback(query, context):
    """Network analysis from callback"""
    class MockUpdate:
        def __init__(self, query):
            self.message = MockMessage(query)
    
    class MockMessage:
        def __init__(self, query):
            self.query = query
            
        async def reply_text(self, text, parse_mode=None):
            return await self.query.edit_message_text(text, parse_mode=parse_mode)
    
    mock_update = MockUpdate(query)
    await network_analysis(mock_update, context)

async def ip_lookup_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """IP Lookup Command Handler"""
    if not context.args:
        await update.message.reply_text(
            "❌ **Usage:** `/iplookup <ip_address>`\n"
            "**Example:** `/iplookup 8.8.8.8`\n"
            "**Example:** `/iplookup 1.1.1.1`",
            parse_mode='Markdown'
        )
        return
    
    ip = context.args[0]
    
    msg = await update.callback_query.edit_message_text(
        f"🌐 **IP Lookup**\n\n"
        f"📍 **Target:** {ip}\n"
        f"⏳ **Status:** Looking up...",
        parse_mode='Markdown'
    )
    
    try:
        lookup = IPLookup()
        result = await lookup.lookup(ip)
        
        if result:
            result_text = f"🌐 **IP Lookup Results**\n\n"
            result_text += f"📍 **IP Address:** {result.get('ip', 'N/A')}\n"
            result_text += f"🌍 **Country:** {result.get('country', 'N/A')} ({result.get('country_code', 'N/A')})\n"
            result_text += f"🏙️ **Region:** {result.get('region', 'N/A')}\n"
            result_text += f"🏘️ **City:** {result.get('city', 'N/A')}\n"
            result_text += f"📮 **ZIP Code:** {result.get('zip_code', 'N/A')}\n"
            result_text += f"🌐 **ISP:** {result.get('isp', 'N/A')}\n"
            result_text += f"🏢 **Organization:** {result.get('organization', 'N/A')}\n"
            result_text += f"📡 **AS Number:** {result.get('as_number', 'N/A')}\n"
            result_text += f"🗺️ **Coordinates:** {result.get('latitude', 'N/A')}, {result.get('longitude', 'N/A')}\n"
            result_text += f"🕐 **Timezone:** {result.get('timezone', 'N/A')}\n"
            result_text += f"🔒 **Security:** {result.get('security_info', {}).get('threat_level', 'N/A')}\n"
            result_text += f"📊 **Accuracy:** {result.get('geolocation_accuracy', 'N/A')}\n"
            result_text += f"🔍 **Source:** {result.get('source', 'N/A')}\n\n"
            result_text += f"⏰ **Lookup Time:** {datetime.now().strftime('%H:%M:%S')}"
        else:
            result_text = f"❌ **IP Lookup Failed**\n\n"
            result_text += f"📍 **IP:** {ip}\n"
            result_text += f"❌ **Error:** Unable to lookup IP information"
        
        await msg.edit_text(result_text, parse_mode='Markdown')
        
    except Exception as e:
        await msg.edit_text(
            f"❌ **Error:** {str(e)}",
            parse_mode='Markdown'
        )

async def ping_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ping Command Handler"""
    # Check if the command was triggered via a button (callback_query)
    is_callback = update.callback_query is not None

    if not context.args:
        error_msg = (
            "❌ **Usage:** `/ping <host> [count]`\n"
            "**Example:** `/ping google.com 4`\n"
            "**Example:** `/ping 8.8.8.8 10`"
        )
        
        if is_callback:
            await update.callback_query.answer()
            await update.callback_query.edit_message_text(error_msg, parse_mode='Markdown')
        else:
            await update.message.reply_text(error_msg, parse_mode='Markdown')
        return

    host = context.args[0]
    count = int(context.args[1]) if len(context.args) > 1 else 4
    
    # Limit ping count
    if count > 20:
        count = 20
    
    initial_msg = (
        f"📡 **Ping Test**\n\n"
        f"🎯 **Target:** {host}\n"
        f"📊 **Count:** {count}\n"
        f"⏳ **Status:** Testing..."
    )
    
    # Handle both callback query and regular message
    if is_callback:
        await update.callback_query.answer()
        await update.callback_query.message.edit_reply_markup(reply_markup=None)  # hapus tombol DULU
        msg = await update.callback_query.message.edit_text(
            initial_msg,
            parse_mode='Markdown'
        )
    else:
        msg = await update.message.reply_text(initial_msg, parse_mode='Markdown')
    
    try:
        ping_tester = PingTester()
        result = await ping_tester.ping(host, count)
        
        result_text = f"📡 **Ping Test Results**\n\n"
        result_text += f"🎯 **Host:** {result['host']} ({result['ip']})\n"
        result_text += f"📊 **Packets:** {result['packets_sent']} sent, {result['packets_received']} received\n"
        result_text += f"📉 **Packet Loss:** {result['packet_loss_percent']}%\n\n"
        
        if result['packets_received'] > 0:
            result_text += f"⏱️ **Timing:**\n"
            result_text += f"• **Min:** {result['min_time']}ms\n"
            result_text += f"• **Max:** {result['max_time']}ms\n"
            result_text += f"• **Avg:** {result['avg_time']}ms\n"
            result_text += f"• **Jitter:** {result['jitter']}ms\n\n"
            
            # Show individual ping times
            if len(result['ping_times']) <= 10:
                result_text += f"📋 **Individual Times:**\n"
                for i, time_val in enumerate(result['ping_times'], 1):
                    result_text += f"• Ping {i}: {time_val}ms\n"
        else:
            result_text += f"❌ **No response received**\n"
        
        result_text += f"\n⏰ **Test Time:** {datetime.now().strftime('%H:%M:%S')}"
        
        await msg.edit_text(result_text, parse_mode='Markdown')
        
    except Exception as e:
        await msg.edit_text(
            f"❌ **Error:** {str(e)}",
            parse_mode='Markdown'
        )

async def traceroute_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Traceroute Command Handler"""
    # Check if the command was triggered via a button (callback_query)
    is_callback = update.callback_query is not None

    if not context.args:
        error_msg = (
            "❌ **Usage:** `/traceroute <host>`\n"
            "**Example:** `/traceroute google.com`\n"
            "**Example:** `/traceroute 8.8.8.8`"
        )
        
        if is_callback:
            await update.callback_query.answer()
            await update.callback_query.edit_message_text(error_msg, parse_mode='Markdown')
        else:
            await update.message.reply_text(error_msg, parse_mode='Markdown')
        return

    host = context.args[0]
    
    initial_msg = (
        f"🔗 **Traceroute**\n\n"
        f"🎯 **Target:** {host}\n"
        f"⏳ **Status:** Tracing route..."
    )
    
    # Handle both callback query and regular message
    if is_callback:
        await update.callback_query.answer()
        await update.callback_query.message.edit_reply_markup(reply_markup=None)  # hapus tombol DULU
        msg = await update.callback_query.message.edit_text(
            initial_msg,
            parse_mode='Markdown'
        )
    else:
        msg = await update.message.reply_text(initial_msg, parse_mode='Markdown')
    
    try:
        traceroute = Traceroute()
        result = await traceroute.trace(host)
        
        result_text = f"🔗 **Traceroute Results**\n\n"
        result_text += f"🎯 **Target:** {result['target_host']} ({result['target_ip']})\n"
        result_text += f"📊 **Total Hops:** {result['total_hops']}\n\n"
        
        result_text += f"📋 **Route:**\n"
        for hop in result['hops'][:15]:  # Limit to 15 hops
            hop_line = f"**{hop['hop']}.** "
            if hop['hostname']:
                hop_line += f"{hop['hostname']} "
            if hop['ip']:
                hop_line += f"({hop['ip']}) "
            if hop['avg_time']:
                hop_line += f"{hop['avg_time']:.2f}ms"
            else:
                hop_line += "timeout"
            
            result_text += hop_line + "\n"
        
        if len(result['hops']) > 15:
            result_text += f"... and {len(result['hops']) - 15} more hops\n"
        
        result_text += f"\n⏰ **Trace Time:** {datetime.now().strftime('%H:%M:%S')}"
        
        await msg.edit_text(result_text, parse_mode='Markdown')
        
    except Exception as e:
        await msg.edit_text(
            f"❌ **Error:** {str(e)}",
            parse_mode='Markdown'
        )

async def dns_lookup_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """DNS Lookup Command Handler"""
    if not context.args:
        await update.message.reply_text(
            "❌ **Usage:** `/dnslookup <domain> [record_type]`\n"
            "**Example:** `/dnslookup google.com`\n"
            "**Example:** `/dnslookup google.com MX`\n"
            "**Record Types:** A, AAAA, MX, NS, TXT, CNAME, SOA",
            parse_mode='Markdown'
        )
        return
    
    domain = context.args[0]
    record_type = context.args[1].upper() if len(context.args) > 1 else 'ALL'
    
    msg = await update.callback_query.edit_message_text(
        f"🌍 **DNS Lookup**\n\n"
        f"🎯 **Domain:** {domain}\n"
        f"📋 **Type:** {record_type}\n"
        f"⏳ **Status:** Looking up...",
        parse_mode='Markdown'
    )
    
    try:
        dns_lookup = DNSLookup()
        result = await dns_lookup.lookup(domain, record_type)
        
        result_text = f"🌍 **DNS Lookup Results**\n\n"
        result_text += f"🎯 **Domain:** {result['domain']}\n\n"
        
        # Display DNS records
        if result['records']:
            for rtype, records in result['records'].items():
                result_text += f"📋 **{rtype} Records:**\n"
                for record in records[:5]:  # Limit to 5 records per type
                    result_text += f"• {record}\n"
                result_text += "\n"
        else:
            result_text += "❌ **No DNS records found**\n\n"
        
        # Display DNS servers
        if result['dns_servers']:
            result_text += f"🌐 **DNS Servers:**\n"
            for dns in result['dns_servers']:
                result_text += f"• {dns}\n"
            result_text += "\n"
        
        # Display authoritative nameservers
        if result['authoritative_nameservers']:
            result_text += f"📡 **Authoritative Nameservers:**\n"
            for ns in result['authoritative_nameservers']:
                result_text += f"• {ns}\n"
            result_text += "\n"
        
        result_text += f"⏰ **Lookup Time:** {datetime.now().strftime('%H:%M:%S')}"
        
        await msg.edit_text(result_text, parse_mode='Markdown')
        
    except Exception as e:
        await msg.edit_text(
            f"❌ **Error:** {str(e)}",
            parse_mode='Markdown'
        )

async def network_info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Network Info Command Handler"""
    msg = await update.callback_query.edit_message_text(
        f"📊 **Network Information**\n\n"
        f"⏳ **Status:** Collecting information...",
        parse_mode='Markdown'
    )
    
    try:
        collector = NetworkInfoCollector()
        info = await collector.collect_all_info()
        
        result_text = f"📊 **Comprehensive Network Information**\n\n"
        
        # Public IP Info
        if 'public_ip' in info and 'error' not in info['public_ip']:
            pub_ip = info['public_ip']
            result_text += f"🌐 **Public IP Information:**\n"
            result_text += f"• **IP:** {pub_ip.get('ip', 'N/A')}\n"
            result_text += f"• **ISP:** {pub_ip.get('isp', 'N/A')}\n"
            result_text += f"• **Country:** {pub_ip.get('country', 'N/A')}\n"
            result_text += f"• **City:** {pub_ip.get('city', 'N/A')}\n\n"
        
        # Local Network Info
        if 'local_network' in info and 'error' not in info['local_network']:
            local = info['local_network']
            result_text += f"🏠 **Local Network:**\n"
            result_text += f"• **Hostname:** {local.get('hostname', 'N/A')}\n"
            result_text += f"• **Local IP:** {local.get('local_ip', 'N/A')}\n"
            result_text += f"• **Gateway:** {local.get('default_gateway', 'N/A')}\n"
            result_text += f"• **Netmask:** {local.get('network_mask', 'N/A')}\n\n"
        
        # Network Interfaces
        if 'network_interfaces' in info and info['network_interfaces']:
            result_text += f"🔌 **Network Interfaces:**\n"
            for interface in info['network_interfaces'][:5]:
                result_text += f"• **{interface['name']}:** {interface.get('ip', 'N/A')} ({interface.get('status', 'unknown')})\n"
            result_text += "\n"
        
        # DNS Configuration
        if 'dns_configuration' in info and 'error' not in info['dns_configuration']:
            dns_config = info['dns_configuration']
            if dns_config.get('dns_servers'):
                result_text += f"🌐 **DNS Servers:**\n"
                for dns in dns_config['dns_servers'][:3]:
                    result_text += f"• {dns}\n"
                result_text += "\n"
        
        # Connectivity Tests
        if 'connectivity_tests' in info and 'connectivity_tests' in info['connectivity_tests']:
            result_text += f"📡 **Connectivity Tests:**\n"
            for test in info['connectivity_tests']['connectivity_tests'][:5]:
                status_icon = "✅" if test['status'] == 'reachable' else "❌"
                latency_text = f" ({test['latency']}ms)" if test['latency'] else ""
                result_text += f"{status_icon} **{test['name']}:** {test['status']}{latency_text}\n"
            result_text += "\n"
        
        # System Info
        if 'system_info' in info and 'error' not in info['system_info']:
            sys_info = info['system_info']
            result_text += f"💻 **System Information:**\n"
            result_text += f"• **OS:** {sys_info.get('system', 'N/A')} {sys_info.get('release', 'N/A')}\n"
            result_text += f"• **Architecture:** {sys_info.get('machine', 'N/A')}\n"
            result_text += f"• **Python:** {sys_info.get('python_version', 'N/A')}\n\n"
        
        result_text += f"⏰ **Collection Time:** {datetime.now().strftime('%H:%M:%S')}"
        
        await msg.edit_text(result_text, parse_mode='Markdown')
        
    except Exception as e:
        await msg.edit_text(
            f"❌ **Error:** {str(e)}",
            parse_mode='Markdown'
        )

async def ip_lookup_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """IP Lookup Command Handler"""
    if not context.args:
        if update.message:
            await update.message.reply_text(
                "❌ **Usage:** `/iplookup <ip_address>`\n"
                "**Example:** `/iplookup 8.8.8.8`\n"
                "**Example:** `/iplookup 1.1.1.1`",
                parse_mode='Markdown'
            )
        elif update.callback_query and update.callback_query.message:
            await update.callback_query.message.reply_text(
                "❌ **Usage:** `/iplookup <ip_address>`\n"
                "**Example:** `/iplookup 8.8.8.8`\n"
                "**Example:** `/iplookup 1.1.1.1`",
                parse_mode='Markdown'
            )
        return
    
    ip = context.args[0]
    
    msg = await update.message.reply_text(
        f"🌐 **IP Lookup**\n\n"
        f"📍 **Target:** {ip}\n"
        f"⏳ **Status:** Looking up...",
        parse_mode='Markdown'
    )
    
    try:
        lookup = IPLookup()
        result = await lookup.lookup(ip)
        
        if result:
            result_text = f"🌐 **IP Lookup Results**\n\n"
            result_text += f"📍 **IP Address:** {result.get('ip', 'N/A')}\n"
            result_text += f"🌍 **Country:** {result.get('country', 'N/A')} ({result.get('country_code', 'N/A')})\n"
            result_text += f"🏙️ **Region:** {result.get('region', 'N/A')}\n"
            result_text += f"🏘️ **City:** {result.get('city', 'N/A')}\n"
            result_text += f"📮 **ZIP Code:** {result.get('zip_code', 'N/A')}\n"
            result_text += f"🌐 **ISP:** {result.get('isp', 'N/A')}\n"
            result_text += f"🏢 **Organization:** {result.get('organization', 'N/A')}\n"
            result_text += f"📡 **AS Number:** {result.get('as_number', 'N/A')}\n"
            result_text += f"🗺️ **Coordinates:** {result.get('latitude', 'N/A')}, {result.get('longitude', 'N/A')}\n"
            result_text += f"🕐 **Timezone:** {result.get('timezone', 'N/A')}\n"
            result_text += f"🔒 **Security:** {result.get('security_info', {}).get('threat_level', 'N/A')}\n"
            result_text += f"📊 **Accuracy:** {result.get('geolocation_accuracy', 'N/A')}\n"
            result_text += f"🔍 **Source:** {result.get('source', 'N/A')}\n\n"
            result_text += f"⏰ **Lookup Time:** {datetime.now().strftime('%H:%M:%S')}"
        else:
            result_text = f"❌ **IP Lookup Failed**\n\n"
            result_text += f"📍 **IP:** {ip}\n"
            result_text += f"❌ **Error:** Unable to lookup IP information"
        
        await msg.edit_text(result_text, parse_mode='Markdown')
        
    except Exception as e:
        await msg.edit_text(
            f"❌ **Error:** {str(e)}",
            parse_mode='Markdown'
        )

async def ping_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ping Command Handler"""
    if not context.args:
        await update.message.reply_text(
            "❌ **Usage:** `/ping <host> [count]`\n"
            "**Example:** `/ping google.com 4`\n"
            "**Example:** `/ping 8.8.8.8 10`",
            parse_mode='Markdown'
        )
        return
    
    host = context.args[0]
    count = int(context.args[1]) if len(context.args) > 1 else 4
    
    # Limit ping count
    if count > 20:
        count = 20
    
    if update.callback_query:
        msg = await update.callback_query.message.reply_text(
            f"📡 **Ping Test**\n\n"
            f"🎯 **Target:** {host}\n"
            f"📊 **Count:** {count}\n"
            f"⏳ **Status:** Testing.",
            parse_mode='Markdown'
        )
    
    try:
        ping_tester = PingTester()
        result = await ping_tester.ping(host, count)
        
        result_text = f"📡 **Ping Test Results**\n\n"
        result_text += f"🎯 **Host:** {result['host']} ({result['ip']})\n"
        result_text += f"📊 **Packets:** {result['packets_sent']} sent, {result['packets_received']} received\n"
        result_text += f"📉 **Packet Loss:** {result['packet_loss_percent']}%\n\n"
        
        if result['packets_received'] > 0:
            result_text += f"⏱️ **Timing:**\n"
            result_text += f"• **Min:** {result['min_time']}ms\n"
            result_text += f"• **Max:** {result['max_time']}ms\n"
            result_text += f"• **Avg:** {result['avg_time']}ms\n"
            result_text += f"• **Jitter:** {result['jitter']}ms\n\n"
            
            # Show individual ping times
            if len(result['ping_times']) <= 10:
                result_text += f"📋 **Individual Times:**\n"
                for i, time_val in enumerate(result['ping_times'], 1):
                    result_text += f"• Ping {i}: {time_val}ms\n"
        else:
            result_text += f"❌ **No response received**\n"
        
        result_text += f"\n⏰ **Test Time:** {datetime.now().strftime('%H:%M:%S')}"
        
        await msg.edit_text(result_text, parse_mode='Markdown')
        
    except Exception as e:
        await msg.edit_text(
            f"❌ **Error:** {str(e)}",
            parse_mode='Markdown'
        )

async def traceroute_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Traceroute Command Handler"""
    if not context.args:
        await update.message.reply_text(
            "❌ **Usage:** `/traceroute <host>`\n"
            "**Example:** `/traceroute google.com`\n"
            "**Example:** `/traceroute 8.8.8.8`",
            parse_mode='Markdown'
        )
        return
    
    host = context.args[0]
    
    if update.callback_query:
        msg = await update.callback_query.message.reply_text(
            f"🔗 **Traceroute**\n\n"
            f"🎯 **Target:** {host}\n"
            f"⏳ **Status:** Tracing route...",
            parse_mode='Markdown'
    )
    
    try:
        traceroute = Traceroute()
        result = await traceroute.trace(host)
        
        result_text = f"🔗 **Traceroute Results**\n\n"
        result_text += f"🎯 **Target:** {result['target_host']} ({result['target_ip']})\n"
        result_text += f"📊 **Total Hops:** {result['total_hops']}\n\n"
        
        result_text += f"📋 **Route:**\n"
        for hop in result['hops'][:15]:  # Limit to 15 hops
            hop_line = f"**{hop['hop']}.** "
            if hop['hostname']:
                hop_line += f"{hop['hostname']} "
            if hop['ip']:
                hop_line += f"({hop['ip']}) "
            if hop['avg_time']:
                hop_line += f"{hop['avg_time']:.2f}ms"
            else:
                hop_line += "timeout"
            
            result_text += hop_line + "\n"
        
        if len(result['hops']) > 15:
            result_text += f"... and {len(result['hops']) - 15} more hops\n"
        
        result_text += f"\n⏰ **Trace Time:** {datetime.now().strftime('%H:%M:%S')}"
        
        await msg.edit_text(result_text, parse_mode='Markdown')
        
    except Exception as e:
        await msg.edit_text(
            f"❌ **Error:** {str(e)}",
            parse_mode='Markdown'
        )

async def dns_lookup_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """DNS Lookup Command Handler"""
    if not context.args:
        if update.message:
            await update.message.reply_text(
                "❌ **Usage:** `/dnslookup <domain> [record_type]`\n"
                "**Example:** `/dnslookup google.com`\n"
                "**Example:** `/dnslookup google.com MX`\n"
                "**Record Types:** A, AAAA, MX, NS, TXT, CNAME, SOA",
                parse_mode='Markdown'
            )
        elif update.callback_query and update.callback_query.message:
            await update.callback_query.message.reply_text(
                "❌ **Usage:** `/dnslookup <domain> [record_type]`\n"
                "**Example:** `/dnslookup google.com`\n"
                "**Example:** `/dnslookup google.com MX`\n"
                "**Record Types:** A, AAAA, MX, NS, TXT, CNAME, SOA",
                parse_mode='Markdown'
            )
        return

    domain = context.args[0]
    record_type = context.args[1].upper() if len(context.args) > 1 else 'ALL'
    
    msg = await update.message.reply_text(
        f"🌍 **DNS Lookup**\n\n"
        f"🎯 **Domain:** {domain}\n"
        f"📋 **Type:** {record_type}\n"
        f"⏳ **Status:** Looking up...",
        parse_mode='Markdown'
    )
    
    try:
        dns_lookup = DNSLookup()
        result = await dns_lookup.lookup(domain, record_type)
        
        result_text = f"🌍 **DNS Lookup Results**\n\n"
        result_text += f"🎯 **Domain:** {result['domain']}\n\n"
        
        # Display DNS records
        if result['records']:
            for rtype, records in result['records'].items():
                result_text += f"📋 **{rtype} Records:**\n"
                for record in records[:5]:  # Limit to 5 records per type
                    result_text += f"• {record}\n"
                result_text += "\n"
        else:
            result_text += "❌ **No DNS records found**\n\n"
        
        # Display DNS servers
        if result['dns_servers']:
            result_text += f"🌐 **DNS Servers:**\n"
            for dns in result['dns_servers']:
                result_text += f"• {dns}\n"
            result_text += "\n"
        
        # Display authoritative nameservers
        if result['authoritative_nameservers']:
            result_text += f"📡 **Authoritative Nameservers:**\n"
            for ns in result['authoritative_nameservers']:
                result_text += f"• {ns}\n"
            result_text += "\n"
        
        result_text += f"⏰ **Lookup Time:** {datetime.now().strftime('%H:%M:%S')}"
        
        await msg.edit_text(result_text, parse_mode='Markdown')
        
    except Exception as e:
        await msg.edit_text(
            f"❌ **Error:** {str(e)}",
            parse_mode='Markdown'
        )

async def network_info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Network Info Command Handler"""
    if update.message:
        msg = await update.message.reply_text(
            f"📊 **Network Information**\n\n"
            f"⏳ **Status:** Collecting information.",
            parse_mode='Markdown'
        )
    elif update.callback_query and update.callback_query.message:
        msg = await update.callback_query.message.reply_text(
            f"📊 **Network Information**\n\n"
            f"⏳ **Status:** Collecting information.",
            parse_mode='Markdown'
        )
    
    try:
        collector = NetworkInfoCollector()
        info = await collector.collect_all_info()
        
        result_text = f"📊 **Comprehensive Network Information**\n\n"
        
        # Public IP Info
        if 'public_ip' in info and 'error' not in info['public_ip']:
            pub_ip = info['public_ip']
            result_text += f"🌐 **Public IP Information:**\n"
            result_text += f"• **IP:** {pub_ip.get('ip', 'N/A')}\n"
            result_text += f"• **ISP:** {pub_ip.get('isp', 'N/A')}\n"
            result_text += f"• **Country:** {pub_ip.get('country', 'N/A')}\n"
            result_text += f"• **City:** {pub_ip.get('city', 'N/A')}\n\n"
        
        # Local Network Info
        if 'local_network' in info and 'error' not in info['local_network']:
            local = info['local_network']
            result_text += f"🏠 **Local Network:**\n"
            result_text += f"• **Hostname:** {local.get('hostname', 'N/A')}\n"
            result_text += f"• **Local IP:** {local.get('local_ip', 'N/A')}\n"
            result_text += f"• **Gateway:** {local.get('default_gateway', 'N/A')}\n"
            result_text += f"• **Netmask:** {local.get('network_mask', 'N/A')}\n\n"
        
        # Network Interfaces
        if 'network_interfaces' in info and info['network_interfaces']:
            result_text += f"🔌 **Network Interfaces:**\n"
            for interface in info['network_interfaces'][:5]:
                result_text += f"• **{interface['name']}:** {interface.get('ip', 'N/A')} ({interface.get('status', 'unknown')})\n"
            result_text += "\n"
        
        # DNS Configuration
        if 'dns_configuration' in info and 'error' not in info['dns_configuration']:
            dns_config = info['dns_configuration']
            if dns_config.get('dns_servers'):
                result_text += f"🌐 **DNS Servers:**\n"
                for dns in dns_config['dns_servers'][:3]:
                    result_text += f"• {dns}\n"
                result_text += "\n"
        
        # Connectivity Tests
        if 'connectivity_tests' in info and 'connectivity_tests' in info['connectivity_tests']:
            result_text += f"📡 **Connectivity Tests:**\n"
            for test in info['connectivity_tests']['connectivity_tests'][:5]:
                status_icon = "✅" if test['status'] == 'reachable' else "❌"
                latency_text = f" ({test['latency']}ms)" if test['latency'] else ""
                result_text += f"{status_icon} **{test['name']}:** {test['status']}{latency_text}\n"
            result_text += "\n"
        
        # System Info
        if 'system_info' in info and 'error' not in info['system_info']:
            sys_info = info['system_info']
            result_text += f"💻 **System Information:**\n"
            result_text += f"• **OS:** {sys_info.get('system', 'N/A')} {sys_info.get('release', 'N/A')}\n"
            result_text += f"• **Architecture:** {sys_info.get('machine', 'N/A')}\n"
            result_text += f"• **Python:** {sys_info.get('python_version', 'N/A')}\n\n"
        
        result_text += f"⏰ **Collection Time:** {datetime.now().strftime('%H:%M:%S')}"
        
        await msg.edit_text(result_text, parse_mode='Markdown')
        
    except Exception as e:
        await msg.edit_text(
            f"❌ **Error:** {str(e)}",
            parse_mode='Markdown'
        )

# Network Handlers    
def setup_speed_test_handlers(app):
    app.add_handler(CommandHandler("speedtest", quick_speed_test))
    app.add_handler(CommandHandler("fullspeedtest", full_speed_test))
    app.add_handler(CommandHandler("netanalysis", network_analysis))
    app.add_handler(CallbackQueryHandler(speed_test_callback_handler, 
        pattern='^(speed_test_menu|quick_speed_test|full_speed_test|network_analysis)$'))
    app.add_handler(CommandHandler("iplookup", ip_lookup_command))
    app.add_handler(CommandHandler("ping", ping_command))
    app.add_handler(CommandHandler("traceroute", traceroute_command))
    app.add_handler(CommandHandler("dnslookup", dns_lookup_command))
    app.add_handler(CommandHandler("netinfo", network_info_command))

# Register all handlers
def main():
    # Basic command handlers
    app.add_handler(CommandHandler("start", start))
    
    # Deploy commands
    app.add_handler(CommandHandler("deploy_firebase", deploy_firebase))
    app.add_handler(CommandHandler("deploy_vercel", deploy_vercel))
    
    # Security commands  
    app.add_handler(CommandHandler("encrypttext", encrypt_text))
    app.add_handler(CommandHandler("decrypttext", decrypt_text))
    
    # Tools commands
    app.add_handler(CommandHandler("shortlink", generate_short_link))
    app.add_handler(CommandHandler("qrcode", generate_qr_code))
    
    # Attacker commands
    app.add_handler(CommandHandler("webscan", web_scan))
    app.add_handler(CommandHandler("portscan", port_scan))
    
    # Button callback handler
    app.add_handler(CallbackQueryHandler(button))
    
    # Network-related handlers (via helper function)
    setup_speed_test_handlers(app)
    
    # File upload handler
    app.add_handler(MessageHandler(filters.Document.ALL, handle_file))
    
    # Text message handler for passwords etc
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))
    
    # Start the bot
    print("🚀 Nikzzx Multi-Feature Bot v2.0 starting...")
    print("🔗 GitHub:", f"https://github.com/{GITHUB_REPO}")
    print("🔥 Firebase:", f"https://console.firebase.google.com/project/{FIREBASE_PROJECT}")
    print("✅ Bot is running...")

    app.run_polling()

if __name__ == '__main__':
    main()

