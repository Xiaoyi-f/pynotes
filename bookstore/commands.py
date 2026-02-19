import click
from flask.cli import with_appcontext
from db.dbhelper import create_tables, load_data


# flask 命令 -> 下划线(_)可以转位中划线(-)
@click.command("create-tables")
@with_appcontext
def create_tables_command():
    """初始化数据库表"""
    create_tables()
    click.echo("表创建完成")


@click.command("load-data")
@with_appcontext
def load_data_command():
    """加载初始数据"""
    load_data()
    click.echo("数据加载完成")


def init_app(app):
    app.cli.add_command(create_tables_command)
    app.cli.add_command(load_data_command)
