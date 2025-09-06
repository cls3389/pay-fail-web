#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的应用测试文件
用于GitHub Actions CI/CD流程
"""

import pytest
import json
from excel_web import create_app


@pytest.fixture
def app():
    """创建测试应用实例"""
    app = create_app()
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    """创建测试客户端"""
    return app.test_client()


def test_health_check(client):
    """测试健康检查端点"""
    response = client.get('/health')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['status'] == 'healthy'
    assert 'timestamp' in data
    assert data['service'] == 'excel-processor-web'


def test_index_page(client):
    """测试主页"""
    response = client.get('/')
    assert response.status_code == 200


def test_stats_endpoint(client):
    """测试统计信息端点"""
    response = client.get('/api/stats')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'supported_formats' in data
    assert 'max_file_size_mb' in data
    assert 'required_columns' in data


def test_upload_no_file(client):
    """测试没有文件的上传请求"""
    response = client.post('/upload')
    assert response.status_code == 400
    
    data = json.loads(response.data)
    assert data['success'] is False
    assert '没有选择文件' in data['message']


def test_download_nonexistent_file(client):
    """测试下载不存在的文件"""
    response = client.get('/download/nonexistent.xlsx')
    assert response.status_code == 404


if __name__ == '__main__':
    pytest.main([__file__])
