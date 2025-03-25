import click
from models import Session, Process, Log
from datetime import datetime

class ProcessManager:
    def __init__(self):
        self.session = Session()

    def close(self):
        self.session.close()

    def create_process(self, name, status, priority, details=None):
        process = Process(
            name=name,
            status=status,
            priority=priority,
            details=details
        )
        self.session.add(process)
        self.session.commit()
        return process.id

    def update_process(self, id, **kwargs):
        process = self.session.query(Process).filter(Process.id == id).first()
        if process:
            for key, value in kwargs.items():
                setattr(process, key, value)
            # 添加日志
            log = Log(
                process_id=id,
                log_entry=f"Process updated: {', '.join(f'{k}={v}' for k, v in kwargs.items())}"
            )
            self.session.add(log)
            self.session.commit()
            return True
        return False

    def get_processes(self, status=None, priority=None):
        query = self.session.query(Process)
        if status:
            query = query.filter(Process.status == status)
        if priority:
            query = query.filter(Process.priority == priority)
        return query.all()

    def get_process_logs(self, process_id):
        return self.session.query(Log).filter(Log.process_id == process_id).all()

@click.group()
def cli():
    """进程管理系统 CLI"""
    pass

@cli.command()
@click.option('--name', prompt='进程名称', help='进程名称')
@click.option('--status', type=click.Choice(['running', 'paused', 'blocked']), prompt='状态', help='进程状态')
@click.option('--priority', type=click.Choice(['high', 'medium', 'low']), prompt='优先级', help='进程优先级')
@click.option('--details', prompt='详细信息', help='进程详细信息', default='')
def create(name, status, priority, details):
    """创建新进程"""
    pm = ProcessManager()
    process_id = pm.create_process(name, status, priority, details)
    click.echo(f'进程创建成功，ID: {process_id}')
    pm.close()

@cli.command()
@click.option('--status', type=click.Choice(['running', 'paused', 'blocked']), help='按状态筛选')
@click.option('--priority', type=click.Choice(['high', 'medium', 'low']), help='按优先级筛选')
def list(status, priority):
    """列出所有进程"""
    pm = ProcessManager()
    processes = pm.get_processes(status, priority)
    for process in processes:
        click.echo(f'ID: {process.id}, 名称: {process.name}, 状态: {process.status}, 优先级: {process.priority}')
    pm.close()

@cli.command()
@click.argument('id', type=int)
@click.option('--status', type=click.Choice(['running', 'paused', 'blocked']), help='新状态')
@click.option('--priority', type=click.Choice(['high', 'medium', 'low']), help='新优先级')
@click.option('--details', help='新详细信息')
def update(id, status, priority, details):
    """更新进程信息"""
    updates = {}
    if status:
        updates['status'] = status
    if priority:
        updates['priority'] = priority
    if details:
        updates['details'] = details
    
    if updates:
        pm = ProcessManager()
        success = pm.update_process(id, **updates)
        if success:
            click.echo(f'进程 {id} 更新成功')
        else:
            click.echo(f'进程 {id} 不存在')
        pm.close()
    else:
        click.echo('没有提供要更新的信息')

@cli.command()
@click.argument('process_id', type=int)
def logs(process_id):
    """查看进程日志"""
    pm = ProcessManager()
    logs = pm.get_process_logs(process_id)
    for log in logs:
        click.echo(f'时间: {log.created_at}, 内容: {log.log_entry}')
    pm.close()

if __name__ == '__main__':
    cli()