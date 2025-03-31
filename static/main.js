// 获取DOM元素
const createProcessBtn = document.getElementById('createProcessBtn');
const createProcessForm = document.getElementById('createProcessForm');
const cancelCreateBtn = document.getElementById('cancelCreate');
const processListDiv = document.getElementById('processList');

// 状态颜色映射
function getStatusColor(status) {
    const colors = {
        '运行中': 'success',
        '停止': 'danger',
        '等待中': 'warning'
    };
    return colors[status] || 'secondary';
}

// 优先级颜色映射
function getPriorityColor(priority) {
    const colors = {
        '高': 'danger',
        '中': 'warning',
        '低': 'info'
    };
    return colors[priority] || 'secondary';
}

// 显示创建进程表单
createProcessBtn.addEventListener('click', () => {
    createProcessForm.classList.remove('d-none');
    processListDiv.classList.add('d-none');
});

// 取消创建进程
cancelCreateBtn.addEventListener('click', () => {
    createProcessForm.classList.add('d-none');
    processListDiv.classList.remove('d-none');
    createProcessForm.querySelector('form').reset();
});

// 处理表单提交
const form = createProcessForm.querySelector('form');
const originalSubmitHandler = async (e) => {
    e.preventDefault();
    
    const formData = {
        name: document.getElementById('name').value,
        description: document.getElementById('description').value,
        status: document.getElementById('status').value,
        priority: document.getElementById('priority').value
    };

    try {
        const response = await fetch('/create-processes/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        if (response.ok) {
            alert('进程创建成功！');
            createProcessForm.classList.add('d-none');
            processListDiv.classList.remove('d-none');
            form.reset();
            loadProcessList();
        } else {
            throw new Error('创建失败');
        }
    } catch (error) {
        alert('创建进程失败：' + error.message);
    }
};

form.addEventListener('submit', originalSubmitHandler);

// 修改编辑进程函数
async function editProcess(processId) {
    try {
        // 获取当前进程数据
        const response = await fetch('/home');
        const processes = await response.json();
        const process = processes.find(p => p.id === processId);
        
        if (!process) {
            throw new Error('未找到进程');
        }

        // 显示编辑表单
        createProcessForm.classList.remove('d-none');
        processListDiv.classList.add('d-none');
        
        // 修改表单标题和按钮文本
        createProcessForm.querySelector('h3').textContent = '编辑进程';
        createProcessForm.querySelector('button[type="submit"]').textContent = '保存';
        
        // 填充表单数据
        document.getElementById('name').value = process.name;
        document.getElementById('description').value = process.description || '';
        document.getElementById('status').value = process.status;
        document.getElementById('priority').value = process.priority;
        
        // 修改表单提交事件
        // 移除所有现有的提交事件处理程序
        form.removeEventListener('submit', originalSubmitHandler);
        form.onsubmit = null;
        
        // 添加新的提交事件处理程序
        const editSubmitHandler = async (e) => {
            e.preventDefault();
            
            const formData = {
                name: document.getElementById('name').value,
                description: document.getElementById('description').value,
                status: document.getElementById('status').value,
                priority: document.getElementById('priority').value
            };

            try {
                const response = await fetch(`/update-process/${processId}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(formData)
                });

                if (response.ok) {
                    alert('进程更新成功！');
                    createProcessForm.classList.add('d-none');
                    processListDiv.classList.remove('d-none');
                    form.reset();
                    loadProcessList();
                    
                    // 清理编辑模式的事件处理程序
                    form.removeEventListener('submit', editSubmitHandler);
                    form.addEventListener('submit', originalSubmitHandler);
                } else {
                    const error = await response.json();
                    throw new Error(error.detail || '更新失败');
                }
            } catch (error) {
                alert('更新进程失败：' + error.message);
            }
        };

        form.addEventListener('submit', editSubmitHandler);
        
        // 修改取消按钮事件
        const originalCancelHandler = cancelCreateBtn.onclick;
        cancelCreateBtn.onclick = () => {
            createProcessForm.classList.add('d-none');
            processListDiv.classList.remove('d-none');
            form.reset();
            // 恢复表单标题和按钮文本
            createProcessForm.querySelector('h3').textContent = '创建新进程';
            createProcessForm.querySelector('button[type="submit"]').textContent = '创建';
            // 清理编辑模式的事件处理程序
            form.removeEventListener('submit', editSubmitHandler);
            form.addEventListener('submit', originalSubmitHandler);
            // 恢复原始取消按钮事件
            cancelCreateBtn.onclick = originalCancelHandler;
        };
        
    } catch (error) {
        alert('加载进程信息失败：' + error.message);
    }
}


// 页面加载完成后立即获取进程列表
document.addEventListener('DOMContentLoaded', () => {
    loadProcessList();
    // 重置表单状态
    form.reset();
    createProcessForm.querySelector('h3').textContent = '创建新进程';
    createProcessForm.querySelector('button[type="submit"]').textContent = '创建';
    form.removeEventListener('submit', form.onsubmit);
    form.addEventListener('submit', originalSubmitHandler);
});

// 加载进程列表函数
async function loadProcessList() {
    try {
        const response = await fetch('/home');
        if (!response.ok) {
            throw new Error('获取进程列表失败');
        }
        const processes = await response.json();
        
        const tableBody = document.getElementById('processTableBody');
        tableBody.innerHTML = '';
        
        if (processes.length === 0) {
            tableBody.innerHTML = '<tr><td colspan="7" class="text-center">暂无进程</td></tr>';
            return;
        }
        
        processes.forEach(process => {
            const row = document.createElement('tr');
            const description = process.description || '-';
            const descriptionHtml = description !== '-' ? marked.parse(description) : '-';
            
            row.innerHTML = `
                <td>${process.id}</td>
                <td>${process.name}</td>
                <td>
                    <div class="description-cell">
                        <div class="description-content markdown-content">
                            ${descriptionHtml}
                        </div>
                        <div class="toggle-description" style="display: none;">
                            <span class="toggle-text">展开</span>
                        </div>
                    </div>
                </td>
                <td><span class="badge bg-${getStatusColor(process.status)}">${process.status}</span></td>
                <td><span class="badge bg-${getPriorityColor(process.priority)}">${process.priority}</span></td>
                <td>${new Date(process.created_at).toLocaleString()}</td>
                <td>
                    <button class="btn btn-sm btn-info btn-operation" onclick="viewLogs(${process.id})">日志</button>
                    <button class="btn btn-sm btn-warning btn-operation" onclick="editProcess(${process.id})">编辑</button>
                    <button class="btn btn-sm btn-danger btn-operation" onclick="deleteProcess(${process.id})">删除</button>
                </td>
            `;
            
            // 添加展开/折叠功能
            const descriptionCell = row.querySelector('.description-cell');
            const descriptionContent = row.querySelector('.description-content');
            const toggleBtn = row.querySelector('.toggle-description');
            
            // 等待内容渲染完成后再检查是否需要展开按钮
            setTimeout(() => {
                if (descriptionContent && descriptionContent.scrollHeight > descriptionContent.clientHeight) {
                    toggleBtn.style.display = 'block';
                    
                    toggleBtn.addEventListener('click', () => {
                        descriptionCell.classList.toggle('expanded');
                        const toggleText = toggleBtn.querySelector('.toggle-text');
                        toggleText.textContent = descriptionCell.classList.contains('expanded') ? '收起' : '展开';
                    });
                }
            }, 0);
            
            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error('加载进程列表失败:', error);
        const tableBody = document.getElementById('processTableBody');
        tableBody.innerHTML = '<tr><td colspan="7" class="text-center text-danger">加载失败，请刷新页面重试</td></tr>';
    }
}

// 添加删除进程函数
async function deleteProcess(processId) {
    if (!confirm('确定要删除这个进程吗？此操作不可撤销。')) {
        return;
    }

    try {
        const response = await fetch(`/delete-process/${processId}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            // 删除成功后刷新列表
            loadProcessList();
            // 显示成功消息
            alert('进程删除成功！');
        } else {
            const error = await response.json();
            throw new Error(error.detail || '删除失败');
        }
    } catch (error) {
        alert('删除进程失败：' + error.message);
    }
}