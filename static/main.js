// ================ DOM 元素获取 ================
const createProcessBtn = document.getElementById('createProcessBtn');
const createProcessForm = document.getElementById('createProcessForm');
const cancelCreateBtn = document.getElementById('cancelCreate');
const processListDiv = document.getElementById('processList');
const form = createProcessForm.querySelector('form');
const allProcessesBtn = document.getElementById('allProcessesBtn');
const runningProcessesBtn = document.getElementById('runningProcessesBtn');
const stoppedProcessesBtn = document.getElementById('stoppedProcessesBtn');
const waitingProcessesBtn = document.getElementById('waitingProcessesBtn');

// ================ 工具函数 ================
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

// 设置导航链接激活状态
function setActiveNavLink(clickedLink) {
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });
    clickedLink.classList.add('active');
}

// 更新进程列表标题
function updateProcessListTitle(status) {
    const title = document.querySelector('#processList h3');
    switch (status) {
        case 'all':
            title.textContent = '所有进程';
            break;
        case '运行中':
            title.textContent = '运行中的进程';
            break;
        case '停止':
            title.textContent = '已停止的进程';
            break;
        case '等待中':
            title.textContent = '等待中的进程';
            break;
    }
}

function getCurrentActiveStatus() {
    if (allProcessesBtn.classList.contains('active')) return 'all';
    if (runningProcessesBtn.classList.contains('active')) return '运行中';
    if (stoppedProcessesBtn.classList.contains('active')) return '停止';
    if (waitingProcessesBtn.classList.contains('active')) return '等待中';
    return '运行中'; // 默认状态
}

// 显示错误消息
function showErrorMessage() {
    const tableBody = document.getElementById('processTableBody');
    tableBody.innerHTML = '<tr><td colspan="7" class="text-center text-danger">加载失败，请刷新页面重试</td></tr>';
}

// ================ 进程列表相关函数 ================
// 加载进程列表
async function loadProcessList() {
    try {
        const response = await fetch('/home');
        if (!response.ok) {
            throw new Error('获取进程列表失败');
        }
        const processes = await response.json();
        updateProcessList(processes);
    } catch (error) {
        console.error('加载进程列表失败:', error);
        showErrorMessage();
    }
}

// 加载所有进程
async function loadAllProcesses() {
    try {
        const response = await fetch('/all-processes');
        if (!response.ok) {
            throw new Error('获取进程列表失败');
        }
        const processes = await response.json();
        updateProcessList(processes);
    } catch (error) {
        console.error('加载进程列表失败:', error);
        showErrorMessage();
    }
}

// 根据状态加载进程
async function loadProcessesByStatus(status) {
    try {
        const response = await fetch(`/processes-by-status/${status}`);
        if (!response.ok) {
            throw new Error('获取进程列表失败');
        }
        const processes = await response.json();
        updateProcessList(processes);
    } catch (error) {
        console.error('加载进程列表失败:', error);
        showErrorMessage();
    }
}

// 更新进程列表显示
function updateProcessList(processes) {
    const tableBody = document.getElementById('processTableBody');
    tableBody.innerHTML = '';

    if (processes.length === 0) {
        tableBody.innerHTML = '<tr><td colspan="7" class="text-center">暂无进程</td></tr>';
        return;
    }

    processes.forEach(process => {
        const row = createProcessRow(process);
        tableBody.appendChild(row);
    });
}

// 创建进程行
function createProcessRow(process) {
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

    addExpandFeature(row);
    return row;
}

// 添加展开/折叠功能
function addExpandFeature(row) {
    const descriptionCell = row.querySelector('.description-cell');
    const descriptionContent = row.querySelector('.description-content');
    const toggleBtn = row.querySelector('.toggle-description');

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
}

// ================ 进程操作相关函数 ================
// 删除进程
async function deleteProcess(processId) {
    if (!confirm('确定要删除这个进程吗？此操作不可撤销。')) {
        return;
    }

    try {
        console.log('开始删除进程:', processId);
        const response = await fetch(`/delete-process/${processId}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        console.log('删除请求响应状态:', response.status);

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || '删除失败');
        }

        // 删除成功后的处理
        console.log('尝试获取当前激活状态');
        const currentStatus = getCurrentActiveStatus();
        console.log('当前激活状态:', currentStatus);

        if (currentStatus === 'all') {
            console.log('正在刷新所有进程列表');
            loadAllProcesses();
        } else {
            console.log('正在刷新特定状态进程列表:', currentStatus);
            loadProcessesByStatus(currentStatus);
        }
        alert('进程删除成功！');

    } catch (error) {
        console.error('删除进程出错，详细信息:', error);
        alert('删除进程失败：' + error.message);
    }
}

// ================ 事件监听器 ================
// 创建进程按钮点击事件
createProcessBtn.addEventListener('click', () => {
    createProcessForm.classList.remove('d-none');
    processListDiv.classList.add('d-none');
});

// 取消创建按钮点击事件
cancelCreateBtn.addEventListener('click', () => {
    createProcessForm.classList.add('d-none');
    processListDiv.classList.remove('d-none');
    createProcessForm.querySelector('form').reset();
});

// 表单提交事件
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

            // 根据当前激活状态刷新列表
            const currentStatus = getCurrentActiveStatus();
            if (currentStatus === 'all') {
                loadAllProcesses();
            } else {
                loadProcessesByStatus(currentStatus);
            }
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
        const response = await fetch(`/get-process/${processId}`);  // 修改为直接获取指定进程
        if (!response.ok) {
            throw new Error('获取进程信息失败');
        }
        const process = await response.json();

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
        // 添加一个获取当前激活状态的函数
        // 获取当前激活状态
        function getCurrentActiveStatus() {
            if (allProcessesBtn.classList.contains('active')) return 'all';
            if (runningProcessesBtn.classList.contains('active')) return '运行中';
            if (stoppedProcessesBtn.classList.contains('active')) return '停止';
            if (waitingProcessesBtn.classList.contains('active')) return '等待中';
            return '运行中'; // 默认状态
        }

        // 修改编辑提交处理程序中的刷新逻辑
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

                    // 根据当前激活状态刷新列表
                    const currentStatus = getCurrentActiveStatus();
                    if (currentStatus === 'all') {
                        loadAllProcesses();
                    } else {
                        loadProcessesByStatus(currentStatus);
                    }

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
    // 设置"运行中进程"为默认选中状态
    setActiveNavLink(runningProcessesBtn);
    loadProcessList();  // 这个函数默认加载运行中的进程

    // 重置表单状态
    form.reset();
    createProcessForm.querySelector('h3').textContent = '创建新进程';
    createProcessForm.querySelector('button[type="submit"]').textContent = '创建';
    form.removeEventListener('submit', form.onsubmit);
    form.addEventListener('submit', originalSubmitHandler);

    // 导航按钮点击事件
    allProcessesBtn.addEventListener('click', (e) => {
        e.preventDefault();
        setActiveNavLink(allProcessesBtn);
        updateProcessListTitle('all');
        loadAllProcesses();
    });

    runningProcessesBtn.addEventListener('click', (e) => {
        e.preventDefault();
        setActiveNavLink(runningProcessesBtn);
        updateProcessListTitle('运行中');
        loadProcessesByStatus('运行中');
    });

    stoppedProcessesBtn.addEventListener('click', (e) => {
        e.preventDefault();
        setActiveNavLink(stoppedProcessesBtn);
        updateProcessListTitle('停止');
        loadProcessesByStatus('停止');
    });

    waitingProcessesBtn.addEventListener('click', (e) => {
        e.preventDefault();
        setActiveNavLink(waitingProcessesBtn);
        updateProcessListTitle('等待中');
        loadProcessesByStatus('等待中');
    });
});


// ================ 日志相关函数 ================
// 查看日志
// 全局变量声明
let mdEditor = null;

async function viewLogs(processId) {
    try {
        // 获取日志数据
        const response = await fetch(`/get-logs-of-process/${processId}`);
        if (!response.ok) {
            throw new Error('获取日志失败');
        }
        const logs = await response.json();

        // 按创建时间降序排序（新的在前）
        logs.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));

        // 更新日志列表
        const logsContainer = document.getElementById('logsContainer');
        logsContainer.innerHTML = '';

        if (logs.length === 0) {
            logsContainer.innerHTML = '<div class="text-center text-muted">暂无日志</div>';
        } else {
            // 在 viewLogs 函数中修改 logs.forEach 部分
            logs.forEach(log => {
                const logEntry = document.createElement('div');
                logEntry.className = 'log-entry';
                logEntry.innerHTML = `
                    <div class="log-time">${new Date(log.created_at).toLocaleString()}</div>
                    <div class="log-content markdown-content" ondblclick="editLogContent(${log.id}, this, ${processId})" data-raw-content="${log.log_entry.replace(/"/g, '&quot;')}">${marked.parse(log.log_entry)}</div>
                    <i class="fas fa-trash delete-log-btn" onclick="deleteLog(${log.id}, ${processId})"></i>
                `;
                logsContainer.appendChild(logEntry);
            });

            // 添加编辑日志内容的函数
            window.editLogContent = async function (logId, element, processId) {
                // 获取原始内容，移除 HTML 标签
                const currentContent = element.getAttribute('data-raw-content') ||
                    element.textContent.replace(/<[^>]*>/g, '').trim();

                // 保存原始 HTML，用于取消时恢复
                const originalHtml = element.innerHTML;

                // 创建编辑器实例
                const editArea = document.createElement('div');
                editArea.style.minHeight = '100px';  // 确保编辑区域有足够高度

                // 先将编辑区域添加到元素中
                element.innerHTML = '';
                element.appendChild(editArea);

                // 初始化 CodeMirror
                const editor = CodeMirror(editArea, {
                    value: currentContent,
                    mode: 'markdown',
                    theme: 'nord',
                    lineWrapping: true,
                    lineNumbers: true,
                    viewportMargin: Infinity  // 允许编辑器自动增长高度
                });

                // 添加保存和取消按钮
                const buttonContainer = document.createElement('div');
                buttonContainer.className = 'edit-buttons mt-2';
                buttonContainer.innerHTML = `
                    <button class="btn btn-sm btn-primary me-2">保存</button>
                    <button class="btn btn-sm btn-secondary">取消</button>
                `;
                element.appendChild(buttonContainer);

                // 保存按钮事件
                buttonContainer.querySelector('.btn-primary').onclick = async () => {
                    const newContent = editor.getValue().trim();
                    if (!newContent) {
                        alert('日志内容不能为空');
                        return;
                    }

                    try {
                        const response = await fetch(`/update-log/${logId}`, {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({ log_entry: newContent })
                        });

                        if (!response.ok) {
                            throw new Error('更新失败');
                        }

                        // 更新成功后刷新日志列表
                        viewLogs(processId);

                    } catch (error) {
                        alert('更新日志失败：' + error.message);
                    }
                };

                // 修改取消按钮事件
                buttonContainer.querySelector('.btn-secondary').onclick = () => {
                    element.innerHTML = originalHtml;  // 使用保存的原始 HTML 恢复
                };

                // 自动刷新编辑器布局
                setTimeout(() => {
                    editor.refresh();
                    editor.focus();
                }, 10);
            };
        }

        // 获取模态框元素
        const logModalElement = document.getElementById('logModal');

        // 初始化 CodeMirror 编辑器
        // 在 viewLogs 函数中修改初始化 CodeMirror 编辑器的部分
        if (!mdEditor) {
            mdEditor = CodeMirror.fromTextArea(document.getElementById('newLogContent'), {
                mode: 'markdown',
                theme: 'nord',
                lineWrapping: true,
                lineNumbers: true,
                placeholder: '在此输入新日志内容（支持 Markdown 格式）',
                viewportMargin: Infinity,
                extraKeys: {
                    'Enter': 'newlineAndIndentContinueMarkdownList',
                    'Tab': 'indentMore',
                    'Shift-Tab': 'indentLess'
                }
            });

            // 添加一个延时来刷新编辑器
            setTimeout(() => {
                mdEditor.refresh();
            }, 100);
        } else {
            mdEditor.setValue(''); // 清空编辑器内容
            mdEditor.refresh(); // 刷新编辑器布局
        }

        // 设置添加日志按钮的处理函数
        const addLogBtn = document.getElementById('addLogBtn');
        addLogBtn.onclick = () => {
            const content = mdEditor.getValue().trim();
            if (!content) {
                alert('日志内容不能为空');
                return;
            }
            addLog(processId, content);
        };

        // 监听模态框隐藏事件
        const modalInstance = new bootstrap.Modal(logModalElement);
        logModalElement.addEventListener('hidden.bs.modal', function () {
            document.body.classList.remove('modal-open');
            const backdrop = document.querySelector('.modal-backdrop');
            if (backdrop) {
                backdrop.remove();
            }
            // 清空编辑器
            mdEditor.setValue('');
        });

        // 显示模态框
        modalInstance.show();

    } catch (error) {
        console.error('加载日志失败:', error);
        alert('加载日志失败：' + error.message);
    }
}

// 修改添加日志函数
async function addLog(processId, logContent) {
    try {
        const response = await fetch(`/create-log-of-process/${processId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ log_entry: logContent })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || '添加日志失败');
        }

        // 清空输入框
        document.getElementById('newLogContent').value = '';

        // 刷新日志列表
        viewLogs(processId);

        alert('日志添加成功！');

    } catch (error) {
        console.error('添加日志失败:', error);
        alert('添加日志失败：' + error.message);
    }
}

// 添加到日志相关函数部分
async function deleteLog(logId, processId) {
    if (!confirm('确定要删除这条日志吗？此操作不可撤销。')) {
        return;
    }

    try {
        const response = await fetch(`/delete-log/${logId}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || '删除失败');
        }

        // 删除成功后刷新日志列表
        viewLogs(processId);
        alert('日志删除成功！');

    } catch (error) {
        console.error('删除日志失败:', error);
        alert('删除日志失败：' + error.message);
    }
}