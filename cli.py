import click
from models import Session, Process, Log
from datetime import datetime
from contextlib import contextmanager

class ProcessManager:
    @contextmanager
    def session_scope(self):
        session = Session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def create_process(self, name, status, priority, details=None):
        with self.session_scope() as session:
            process = Process(
                name=name,
                status=status,
                priority=priority,
                details=details
            )
            session.add(process)
            # 移除这里的 commit，让上下文管理器处理
            return process.id

    def update_process(self, id, **kwargs):
        with self.session_scope() as session:
            process = session.query(Process).filter(Process.id == id).first()
            if not process:
                return False
            
            for key, value in kwargs.items():
                setattr(process, key, value)
            
            log = Log(
                process_id=id,
                log_entry=f"进程更新: {', '.join(f'{k}={v}' for k, v in kwargs.items())}"
            )
            session.add(log)
            # 移除这里的 commit，让上下文管理器处理
            return True

    def get_processes(self, status=None, priority=None):
        with self.session_scope() as session:
            query = session.query(Process)
            if status:
                query = query.filter(Process.status == status)
            if priority:
                query = query.filter(Process.priority == priority)
        
        # 使用 joinedload 立即加载所有相关数据
        processes = query.options(joinedload(Process.logs)).all()
        
        # 将查询结果转换为字典列表
        result = [
            {
                "id": process.id,
                "name": process.name,
                "status": process.status,
                "priority": process.priority,
                "details": process.details,
                "created_at": process.created_at,
                "logs": [log.log_entry for log in process.logs] if hasattr(process, 'logs') else []
            }
            for process in processes
        ]
        return result

    def delete_process(self, id):
        with self.session_scope() as session:
            process = session.query(Process).filter(Process.id == id).first()
            if not process:
                return False
            session.delete(process)
            return True

    def get_process(self, id):
        with self.session_scope() as session:
            process = session.query(Process).filter(Process.id == id).first()
            if process:
                session.refresh(process)
            return process

    def get_process_logs(self, process_id):
        with self.session_scope() as session:
            logs = session.query(Log).filter(Log.process_id == process_id).all()
            for log in logs:
                session.refresh(log)
            return logs

def print_process_details(process):
    click.echo("-" * 50)
    click.echo(f"进程ID: {process.id}")
    click.echo(f"名称: {process.name}")
    click.echo(f"状态: {process.status}")
    click.echo(f"优先级: {process.priority}")
    click.echo(f"详细信息: {process.details or '无'}")
    click.echo(f"创建时间: {process.created_at}")
    click.echo("-" * 50)

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
    try:
        pm = ProcessManager()
        process_id = pm.create_process(name, status, priority, details)
        click.echo(f'进程创建成功，ID: {process_id}')
    except Exception as e:
        click.echo(f'创建进程失败: {str(e)}', err=True)

@cli.command()
@click.option('--status', type=click.Choice(['running', 'paused', 'blocked']), help='按状态筛选')
@click.option('--priority', type=click.Choice(['high', 'medium', 'low']), help='按优先级筛选')
def list(status, priority):
    """列出所有进程"""
    try:
        pm = ProcessManager()
        processes = pm.get_processes(status, priority)
        if not processes:
            click.echo("没有找到符合条件的进程")
            return
        
        for process in processes:
            print_process_details(process)
    except Exception as e:
        click.echo(f'获取进程列表失败: {str(e)}', err=True)

@cli.command()
@click.argument('id', type=int)
def show(id):
    """查看进程详细信息"""
    try:
        pm = ProcessManager()
        process = pm.get_process(id)
        if process:
            print_process_details(process)
        else:
            click.echo(f'进程 {id} 不存在')
    except Exception as e:
        click.echo(f'获取进程信息失败: {str(e)}', err=True)

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
    
    if not updates:
        click.echo('没有提供要更新的信息')
        return

    try:
        pm = ProcessManager()
        if pm.update_process(id, **updates):
            click.echo(f'进程 {id} 更新成功')
        else:
            click.echo(f'进程 {id} 不存在')
    except Exception as e:
        click.echo(f'更新进程失败: {str(e)}', err=True)

@cli.command()
@click.argument('id', type=int)
@click.confirmation_option(prompt='确定要删除这个进程吗？')
def delete(id):
    """删除进程"""
    try:
        pm = ProcessManager()
        if pm.delete_process(id):
            click.echo(f'进程 {id} 已删除')
        else:
            click.echo(f'进程 {id} 不存在')
    except Exception as e:
        click.echo(f'删除进程失败: {str(e)}', err=True)

@cli.command()
@click.argument('process_id', type=int)
def logs(process_id):
    """查看进程日志"""
    try:
        pm = ProcessManager()
        logs = pm.get_process_logs(process_id)
        if not logs:
            click.echo(f'进程 {process_id} 没有日志记录')
            return
        
        click.echo(f"进程 {process_id} 的日志记录：")
        click.echo("-" * 50)
        for log in logs:
            click.echo(f"时间: {log.created_at}")
            click.echo(f"内容: {log.log_entry}")
            click.echo("-" * 50)
    except Exception as e:
        click.echo(f'获取日志失败: {str(e)}', err=True)

if __name__ == '__main__':
    cli()