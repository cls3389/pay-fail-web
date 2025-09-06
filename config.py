import os
from pathlib import Path

class Config:
    """应用配置类"""
    # Flask配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'excel-processor-2025'
    
    # 文件上传配置
    UPLOAD_FOLDER = 'uploads'
    OUTPUT_FOLDER = 'output'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB限制
    
    # Excel处理配置
    ALLOWED_EXTENSIONS = {'.xlsx', '.xls'}
    REQUIRED_COLUMNS = ['应还款金额', '所属直营中心', '所属团队', '所属业务经理', '客户姓名']
    OPTIONAL_COLUMNS = ['客户UID', '贷后BP']
    
    # 排序配置
    SORT_CONFIG = {
        '团队排序': True,
        '业务经理排序': True,  
        '金额排序': True,
        '贷后BP团队置底': True
    }
    
    # 条件格式配置
    FORMAT_CONFIG = {
        '金额阈值': 10000,
        '浅红填充色': 'FFB6C1',
        '深红色文本': '8B0000'
    }
    
    @staticmethod
    def init_app():
        """初始化应用目录"""
        Path(Config.UPLOAD_FOLDER).mkdir(exist_ok=True)
        Path(Config.OUTPUT_FOLDER).mkdir(exist_ok=True)
        Path('logs').mkdir(exist_ok=True)
