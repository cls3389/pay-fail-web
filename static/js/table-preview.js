// 表格预览和图片复制功能
let previewData = {};
let processStats = {};

$(document).ready(function() {
    // 文件选择变化
    $('#fileInput').on('change', function() {
        const file = this.files[0];
        if (file) {
            showFileInfo(file);
        } else {
            hideFileInfo();
        }
    });

    // 设置拖拽上传
    setupDragAndDrop();
});

// 显示文件信息并自动上传
function showFileInfo(file) {
    if (!validateFile(file)) {
        hideFileInfo();
        return;
    }

    // 显示文件信息
    $('#fileName').text(file.name);
    $('#fileSize').text(formatFileSize(file.size));
    $('#fileType').text(file.name.split('.').pop().toUpperCase());
    
    $('#fileInfoContainer').fadeIn();
    $('#autoUploadTip').fadeIn();
    
    // 自动上传，无需确认
    setTimeout(() => {
        uploadAndPreview();
    }, 800); // 延迟800ms让用户看到文件信息
}

// 隐藏文件信息
function hideFileInfo() {
    $('#fileInfoContainer').fadeOut();
    $('#autoUploadTip').fadeOut();
}

// 格式化文件大小
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// 上传并预览文件
function uploadAndPreview() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    
    if (!file) {
        showAlert('请选择一个文件', 'warning');
        return;
    }

    if (!validateFile(file)) {
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    // 显示进度条
    showProgress();
    updateProgress(10, '正在上传文件...');

    // 禁用上传按钮
    const uploadBtn = $('#uploadBtn');
    const originalText = uploadBtn.html();
    uploadBtn.prop('disabled', true);
    uploadBtn.html('<i class="fas fa-spinner fa-spin me-2"></i>处理中...');

    // Ajax上传
    $.ajax({
        url: '/upload',
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        xhr: function() {
            const xhr = new window.XMLHttpRequest();
            xhr.upload.addEventListener('progress', function(evt) {
                if (evt.lengthComputable) {
                    const percentComplete = Math.round((evt.loaded / evt.total) * 50);
                    updateProgress(percentComplete, '上传中...');
                }
            });
            return xhr;
        },
        success: function(response) {
            updateProgress(80, '正在生成结果...');
            setTimeout(() => {
                hideProgress();
                if (response.success) {
                    showResult(response);
                } else {
                    showAlert(response.message || '处理失败', 'danger');
                }
            }, 1000);
        },
        error: function(xhr, status, error) {
            hideProgress();
            let errorMessage = '上传失败';
            
            if (xhr.responseJSON && xhr.responseJSON.message) {
                errorMessage = xhr.responseJSON.message;
            } else if (xhr.status === 413) {
                errorMessage = '文件太大，请选择较小的文件';
            } else if (xhr.status === 0) {
                errorMessage = '网络连接失败，请检查网络';
            }
            
            showAlert(errorMessage, 'danger');
        },
        complete: function() {
            // 恢复上传按钮
            uploadBtn.prop('disabled', false);
            uploadBtn.html(originalText);
        }
    });
}

// 显示处理结果
function showResult(response) {
    processStats = response.stats;
    
    // 隐藏上传区域，显示结果区域
    $('#introCard').hide();
    $('#resultContainer').show();
    
    // 显示Excel下载按钮
    if (response.download_url) {
        const downloadBtn = $('#downloadExcelBtn');
        downloadBtn.show();
        downloadBtn.off('click').on('click', function() {
            window.open(response.download_url, '_blank');
        });
    }
    
    // 显示统计信息
    showStatsInfo();
    
    // 滚动到结果区域
    $('html, body').animate({
        scrollTop: $('#resultContainer').offset().top - 100
    }, 1000);
}

// 显示统计信息
function showStatsInfo() {
    const statsHtml = `
        <div class="row g-3">
            <div class="col-md-3">
                <div class="text-center">
                    <div class="h4 text-primary mb-1">${processStats['原始数据行数'] || 0}</div>
                    <small class="text-muted">原始数据行数</small>
                </div>
            </div>
            <div class="col-md-3">
                <div class="text-center">
                    <div class="h4 text-info mb-1">${processStats['透视表行数'] || 0}</div>
                    <small class="text-muted">处理后行数</small>
                </div>
            </div>
            <div class="col-md-3">
                <div class="text-center">
                    <div class="h4 text-success mb-1">${processStats['直营中心数量'] || 0}</div>
                    <small class="text-muted">直营中心数</small>
                </div>
            </div>
            <div class="col-md-3">
                <div class="text-center">
                    <div class="h4 text-warning mb-1">¥${formatNumber(processStats['总金额'] || 0)}</div>
                    <small class="text-muted">总金额</small>
                </div>
            </div>
        </div>
    `;
    $('#statsInfo').html(statsHtml);
}

// 生成Excel风格表格
function generateTables() {
    const container = $('#tablesContainer');
    container.empty();
    
    const template = $('#excelTableTemplate').html();
    
    // 按直营中心顺序生成Excel风格表格
    Object.keys(previewData).forEach(centerKey => {
        const centerData = previewData[centerKey];
        const excelTable = centerData.excel_table;
        
        if (!excelTable) {
            console.error('Missing excel_table data for', centerKey);
            return;
        }
        
        // 生成表头
        const headers = excelTable.headers.map(col => `<th>${col}</th>`).join('');
        
        // 生成数据行with合并和样式
        const rows = generateExcelRows(excelTable);
        
        // 替换模板变量
        let tableHtml = template
            .replace(/{centerTitle}/g, excelTable.center_title)
            .replace(/{centerKey}/g, centerKey)
            .replace(/{headers}/g, headers)
            .replace(/{rows}/g, rows)
            .replace(/{rowCount}/g, centerData.row_count || centerData.raw_data.length)
            .replace(/{totalAmount}/g, formatNumber(centerData.total_amount || 0));
        
        container.append(tableHtml);
    });
    
    // 应用单元格合并
    applyExcelMerging();
    
    console.log('Excel风格表格生成完成');
}

// 生成Excel风格的数据行
function generateExcelRows(excelTable) {
    let rowsHtml = '';
    
    excelTable.rows.forEach((row, rowIndex) => {
        let rowHtml = '<tr>';
        
        row.forEach((cell, colIndex) => {
            let cellClass = '';
            let cellStyle = '';
            
            // 金额列样式
            if (cell.is_amount) {
                cellClass += ' amount-cell';
                if (cell.is_highlight) {
                    cellClass += ' highlight-cell';
                }
            }
            
            // 构建单元格
            rowHtml += `<td class="${cellClass}" data-row="${rowIndex}" data-col="${colIndex}">${cell.value}</td>`;
        });
        
        rowHtml += '</tr>';
        rowsHtml += rowHtml;
    });
    
    return rowsHtml;
}

// 应用Excel风格的单元格合并
function applyExcelMerging() {
    Object.keys(previewData).forEach(centerKey => {
        const excelTable = previewData[centerKey].excel_table;
        const tableElement = document.querySelector(`#excel-table-${centerKey} .excel-table tbody`);
        
        if (!excelTable || !excelTable.merge_info || !tableElement) {
            console.warn('Missing merge data for', centerKey);
            return;
        }
        
        // 获取列索引映射
        const headers = excelTable.headers;
        const columnMapping = {};
        headers.forEach((header, index) => {
            columnMapping[header] = index;
        });
        
        // 处理每一列的合并
        Object.keys(excelTable.merge_info).forEach(colName => {
            const colIndex = columnMapping[colName];
            const mergeGroups = excelTable.merge_info[colName];
            
            if (colIndex === undefined) {
                console.warn('Column not found:', colName);
                return;
            }
            
            mergeGroups.forEach(group => {
                if (group.start !== group.end) {
                    // 需要合并的单元格组
                    const startCell = tableElement.querySelector(`tr:nth-child(${group.start + 1}) td:nth-child(${colIndex + 1})`);
                    
                    if (startCell) {
                        // 设置rowspan
                        const rowspan = group.end - group.start + 1;
                        startCell.rowSpan = rowspan;
                        startCell.classList.add('merged-cell');
                        
                        // 隐藏其他需要合并的单元格
                        for (let i = group.start + 1; i <= group.end; i++) {
                            const cellToHide = tableElement.querySelector(`tr:nth-child(${i + 1}) td:nth-child(${colIndex + 1})`);
                            if (cellToHide) {
                                cellToHide.style.display = 'none';
                            }
                        }
                        
                        console.log(`合并 ${colName} 列: 行 ${group.start + 1} 到 ${group.end + 1}, rowspan=${rowspan}`);
                    }
                }
            });
        });
    });
}

// 复制Excel风格表格为图片
async function copyTableAsImage(centerKey) {
    try {
        const tableWrapper = document.getElementById(`excel-table-${centerKey}`);
        
        if (!tableWrapper) {
            showAlert('未找到表格元素', 'danger');
            return;
        }
        
        // 显示loading状态
        const container = tableWrapper.closest('.excel-table-container');
        const btn = container.querySelector('button[onclick*="copyTableAsImage"]');
        const originalHtml = btn.innerHTML;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>生成中...';
        btn.disabled = true;
        
        // 使用html2canvas生成高质量Excel风格图片
        const canvas = await html2canvas(tableWrapper, {
            backgroundColor: '#ffffff',
            scale: 3, // 提高分辨率，确保清晰度
            useCORS: true,
            logging: false,
            width: tableWrapper.offsetWidth,
            height: tableWrapper.offsetHeight,
            allowTaint: false,
            foreignObjectRendering: false,
            imageTimeout: 5000,
            // 确保字体正确渲染
            onclone: function(clonedDoc) {
                // 确保克隆文档中的样式正确
                const clonedElement = clonedDoc.getElementById(`excel-table-${centerKey}`);
                if (clonedElement) {
                    clonedElement.style.fontFamily = '微软雅黑, Microsoft YaHei, sans-serif';
                }
            }
        });
        
        // 将canvas转换为blob
        canvas.toBlob(async (blob) => {
            try {
                // 使用Clipboard API复制图片
                await navigator.clipboard.write([
                    new ClipboardItem({ 'image/png': blob })
                ]);
                
                // 显示成功提示
                showCopySuccessToast();
                console.log(`Excel表格图片复制成功: ${previewData[centerKey].name}`);
                
            } catch (err) {
                console.error('复制到剪贴板失败:', err);
                // 回退方案：下载图片
                downloadImageFromCanvas(canvas, `${previewData[centerKey].name}_Excel数据表.png`);
                showAlert('图片已下载到本地，请手动发送', 'info');
            } finally {
                // 恢复按钮状态
                btn.innerHTML = originalHtml;
                btn.disabled = false;
            }
        }, 'image/png', 1.0); // 最高质量
        
    } catch (error) {
        console.error('生成Excel风格图片失败:', error);
        showAlert('生成图片失败: ' + error.message, 'danger');
        
        // 恢复按钮状态
        const container = document.querySelector(`[data-center="${centerKey}"]`);
        const btn = container.querySelector('button[onclick*="copyTableAsImage"]');
        if (btn) {
            btn.innerHTML = '<i class="fas fa-image me-1"></i>复制图片';
            btn.disabled = false;
        }
    }
}

// 下载Excel风格表格图片
async function downloadTableAsImage(centerKey) {
    try {
        const tableWrapper = document.getElementById(`excel-table-${centerKey}`);
        
        const canvas = await html2canvas(tableWrapper, {
            backgroundColor: '#ffffff',
            scale: 3,
            useCORS: true,
            onclone: function(clonedDoc) {
                const clonedElement = clonedDoc.getElementById(`excel-table-${centerKey}`);
                if (clonedElement) {
                    clonedElement.style.fontFamily = '微软雅黑, Microsoft YaHei, sans-serif';
                }
            }
        });
        
        downloadImageFromCanvas(canvas, `${previewData[centerKey].name}_Excel数据表.png`);
        
    } catch (error) {
        console.error('下载Excel风格图片失败:', error);
        showAlert('下载图片失败: ' + error.message, 'danger');
    }
}

// 从canvas下载图片
function downloadImageFromCanvas(canvas, filename) {
    const link = document.createElement('a');
    link.download = filename;
    link.href = canvas.toDataURL('image/png');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// 复制所有表格
async function copyAllTables() {
    const btn = event.target;
    const originalHtml = btn.innerHTML;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>生成中...';
    btn.disabled = true;
    
    try {
        for (const centerKey of Object.keys(previewData)) {
            await copyTableAsImage(centerKey);
            await new Promise(resolve => setTimeout(resolve, 1000)); // 延迟1秒
        }
        showAlert('所有表格已复制完成', 'success');
    } catch (error) {
        showAlert('复制过程中出现错误', 'danger');
    } finally {
        btn.innerHTML = originalHtml;
        btn.disabled = false;
    }
}

// 显示复制成功提示
function showCopySuccessToast() {
    const toast = new bootstrap.Toast(document.getElementById('copySuccessToast'));
    toast.show();
}

// 重新显示上传表单
function showUploadForm() {
    $('#resultContainer').hide();
    $('#introCard').show();
    $('#fileInput').val('');
    $('#downloadExcelBtn').hide();
    hideFileInfo();
    
    // 滚动到顶部
    $('html, body').animate({scrollTop: 0}, 500);
}

// 文件验证
function validateFile(file) {
    const allowedTypes = ['.xlsx', '.xls'];
    const maxSize = 16 * 1024 * 1024; // 16MB
    
    const fileName = file.name.toLowerCase();
    const isValidType = allowedTypes.some(type => fileName.endsWith(type));
    
    if (!isValidType) {
        showAlert('不支持的文件格式，请选择 .xlsx 或 .xls 文件', 'danger');
        return false;
    }
    
    if (file.size > maxSize) {
        showAlert('文件太大，请选择小于16MB的文件', 'danger');
        return false;
    }
    
    return true;
}

// 显示进度条
function showProgress() {
    $('#progressContainer').slideDown();
    updateProgress(0, '准备处理...');
}

// 更新进度条
function updateProgress(percent, text) {
    $('#progressBar').css('width', percent + '%');
    $('#progressText').text(text);
}

// 隐藏进度条
function hideProgress() {
    $('#progressContainer').slideUp();
}

// 显示警告提示
function showAlert(message, type = 'info') {
    const iconMap = {
        'info': 'fa-info-circle',
        'success': 'fa-check-circle',
        'warning': 'fa-exclamation-triangle',
        'danger': 'fa-times-circle'
    };
    
    const alertHtml = `
        <div class="alert alert-${type} alert-dismissible fade show">
            <i class="fas ${iconMap[type] || 'fa-info-circle'} me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    $('.container').prepend(alertHtml);
    
    // 3秒后自动关闭
    setTimeout(() => {
        $('.alert').alert('close');
    }, 3000);
}

// 设置拖拽上传
function setupDragAndDrop() {
    const fileInput = $('#fileInput')[0];
    const uploadArea = fileInput.closest('.card-body');
    
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        uploadArea.addEventListener(eventName, preventDefaults, false);
        document.body.addEventListener(eventName, preventDefaults, false);
    });
    
    ['dragenter', 'dragover'].forEach(eventName => {
        uploadArea.addEventListener(eventName, highlight, false);
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
        uploadArea.addEventListener(eventName, unhighlight, false);
    });
    
    uploadArea.addEventListener('drop', handleDrop, false);
    
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    function highlight(e) {
        uploadArea.classList.add('drag-over');
    }
    
    function unhighlight(e) {
        uploadArea.classList.remove('drag-over');
    }
    
    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        
        if (files.length > 0) {
            fileInput.files = files;
            showFileInfo(files[0]);
        }
    }
}

// 简化的布局处理（如需要可以在这里添加）

// 格式化数字
function formatNumber(num) {
    return new Intl.NumberFormat('zh-CN', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    }).format(num);
}
