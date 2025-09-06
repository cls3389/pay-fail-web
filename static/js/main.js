// 简洁版主JavaScript文件
$(document).ready(function() {
    // 初始化事件
    initializeEvents();
    
    // 设置拖拽上传
    setupDragAndDrop();
});

function initializeEvents() {
    // 文件选择按钮点击
    $('#selectFileBtn').on('click', function() {
        $('#fileInput').click();
    });
    
    // 文件选择变化
    $('#fileInput').on('change', function() {
        const file = this.files[0];
        if (file) {
            processFile(file);
        }
    });
    
    // 下载按钮点击
    $(document).on('click', '#downloadBtn', function() {
        if (window.downloadUrl) {
            window.location.href = window.downloadUrl;
        }
    });
    
    // 重置按钮点击
    $(document).on('click', '#resetBtn, #retryBtn', function() {
        resetToUpload();
    });
}

// 处理文件函数（简洁版）
function processFile(file) {
    if (!validateFile(file)) {
        return;
    }
    
    // 显示处理状态
    showProcessing();
    
    const formData = new FormData();
    formData.append('file', file);
    
    // Ajax上传和处理
    $.ajax({
        url: '/upload',
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        timeout: 60000, // 60秒超时
        xhr: function() {
            const xhr = new window.XMLHttpRequest();
            // 上传进度
            xhr.upload.addEventListener('progress', function(evt) {
                if (evt.lengthComputable) {
                    const percentComplete = Math.round((evt.loaded / evt.total) * 100);
                    updateProgress(Math.min(percentComplete, 90));
                }
            });
            return xhr;
        },
        success: function(response) {
            console.log('收到响应:', response);
            updateProgress(100);
            setTimeout(() => {
                showResult(response);
            }, 500);
        },
        error: function(xhr, status, error) {
            console.log('Ajax错误:', status, error, xhr.responseText);
            let errorMessage = '处理失败，请重试';
            
            if (xhr.responseJSON && xhr.responseJSON.message) {
                errorMessage = xhr.responseJSON.message;
            } else if (xhr.status === 413) {
                errorMessage = '文件太大，请选择较小的文件';
            } else if (xhr.status === 0) {
                errorMessage = '网络连接失败，请检查网络';
            } else if (status === 'timeout') {
                errorMessage = '处理超时，请稍后重试';
            }
            
            showError(errorMessage);
        }
    });
}

// 文件验证
function validateFile(file) {
    const allowedTypes = ['.xlsx', '.xls'];
    const maxSize = 16 * 1024 * 1024; // 16MB
    
    // 检查文件类型
    const fileName = file.name.toLowerCase();
    const isValidType = allowedTypes.some(type => fileName.endsWith(type));
    
    if (!isValidType) {
        showAlert('不支持的文件格式，请选择 .xlsx 或 .xls 文件', 'danger');
        return false;
    }
    
    // 检查文件大小
    if (file.size > maxSize) {
        showAlert('文件太大，请选择小于16MB的文件', 'danger');
        return false;
    }
    
    return true;
}

// 显示处理状态
function showProcessing() {
    $('#uploadSection').hide();
    $('#processSection').show();
    updateProgress(10);
}

// 更新进度条
function updateProgress(percent) {
    $('#progressFill').css('width', percent + '%');
}

// 显示结果（简洁版）
function showResult(result) {
    console.log('显示结果:', result);
    $('#processSection').hide();
    
    if (result.success) {
        // 保存下载链接
        window.downloadUrl = result.download_url;
        
        $('#resultSection').show();
    } else {
        showError(result.message || '处理失败，请重试');
    }
}

// 显示错误
function showError(message) {
    $('#processSection').hide();
    $('#errorMessage').text(message);
    $('#errorSection').show();
}

// 重置到上传状态
function resetToUpload() {
    $('#processSection').hide();
    $('#resultSection').hide();
    $('#errorSection').hide();
    $('#uploadSection').show();
    
    // 清空文件选择
    $('#fileInput').val('');
    window.downloadUrl = null;
}

// 设置拖拽上传（简洁版）
function setupDragAndDrop() {
    const dropZone = $('#dropZone')[0];
    
    if (!dropZone) {
        console.log('dropZone元素不存在，跳过拖拽设置');
        return;
    }
    
    console.log('设置拖拽上传功能');
    
    // 防止默认拖拽行为
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
        document.body.addEventListener(eventName, preventDefaults, false);
    });
    
    // 拖拽高亮效果
    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, highlight, false);
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, unhighlight, false);
    });
    
    // 处理文件拖拽
    dropZone.addEventListener('drop', handleDrop, false);
    
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    function highlight(e) {
        dropZone.classList.add('drag-over');
    }
    
    function unhighlight(e) {
        dropZone.classList.remove('drag-over');
    }
    
    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        
        if (files.length > 0) {
            const fileInput = $('#fileInput')[0];
            if (fileInput) {
                fileInput.files = files;
                processFile(files[0]);
            }
        }
    }
}

// 页面加载完成后的初始化
$(window).on('load', function() {
    // 添加加载完成的样式类
    $('body').addClass('loaded');
});
