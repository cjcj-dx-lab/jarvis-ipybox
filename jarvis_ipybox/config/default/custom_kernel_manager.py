#!/usr/bin/env python3
import os
import json
from jupyter_client.kernelspec import KernelSpecManager
from jupyter_server.services.kernels.kernelmanager import MappingKernelManager

class CustomMappingKernelManager(MappingKernelManager):
    """
    각 커널이 독립된 디렉토리를 사용하도록 설정하는 커스텀 커널 매니저
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # root_dir 속성 직접 설정
        self.root_dir = os.environ.get('HOME', '/home/appuser')
    
    def _kernel_spec_manager_default(self):
        return KernelSpecManager()
    
    def start_kernel(self, kernel_id=None, path=None, **kwargs):
        """
        커널 시작 시 독립된 디렉토리를 설정합니다.
        """
        kernel_id = kernel_id or self.new_kernel_id()
        
        # 커널별 독립 디렉토리 설정
        kernel_dir = self._get_kernel_dir(kernel_id)
        os.environ['JUPYTER_DATA_DIR'] = kernel_dir
        
        # 환경 변수 설정
        env = kwargs.pop('env', {})
        env['KERNEL_ID'] = kernel_id
        env['KERNEL_DIR'] = kernel_dir
        
        # PYTHONPATH에 /app 디렉토리 추가
        python_path = env.get('PYTHONPATH', '')
        if python_path:
            env['PYTHONPATH'] = f"/app:{python_path}"
        else:
            env['PYTHONPATH'] = "/app"
        
        kwargs['env'] = env
        
        # 작업 디렉토리를 커널 디렉토리로 설정
        if path is None:
            path = kernel_dir
            
        # cwd 직접 설정하여 cwd_for_path 호출 방지
        kwargs['cwd'] = kernel_dir
        
        return super().start_kernel(kernel_id=kernel_id, path=path, **kwargs)
    
    def cwd_for_path(self, path, env=None):
        """
        cwd_for_path 메서드 오버라이드하여 root_dir 참조 오류 방지
        """
        if path is None:
            return self._get_kernel_dir(env.get('KERNEL_ID', '')) if env else os.getcwd()
        
        return os.path.abspath(path)
    
    def _get_kernel_dir(self, kernel_id):
        """
        커널 ID에 해당하는 디렉토리 경로를 반환합니다.
        """
        home = os.environ.get('HOME', '/home/appuser')
        kernel_root = os.environ.get('KERNEL_ROOT_DIR', f'{home}/data')
        
        # 커널 루트 디렉토리가 없으면 생성
        if not os.path.exists(kernel_root):
            os.makedirs(kernel_root, exist_ok=True)
        
        # 커널 ID를 기반으로 디렉토리 생성
        kernel_dir = os.path.join(kernel_root, kernel_id)
        if not os.path.exists(kernel_dir):
            os.makedirs(kernel_dir, exist_ok=True)

        # 커널 ID별 인풋, 아웃풋 디렉토리 생성
        kernel_input_dir = os.path.join(kernel_root, kernel_id, "input")
        if not os.path.exists(kernel_input_dir):
            os.makedirs(kernel_input_dir, exist_ok=True)
        
        kernel_output_dir = os.path.join(kernel_root, kernel_id, "output")
        if not os.path.exists(kernel_output_dir):
            os.makedirs(kernel_output_dir, exist_ok=True)
            
        return kernel_dir

if __name__ == "__main__":
    # 테스트 코드 또는 필요한 초기화 코드
    manager = CustomMappingKernelManager()
    print("커스텀 커널 매니저가 초기화되었습니다.") 