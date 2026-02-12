import shutil

shutil.copyfile("source", "target")
shutil.copytree("source", "target")
shutil.move("old", "new")
shutil.rmtree("dir_name")
usage = shutil.disk_usage(".")
usage.total
usage.free
usage.used
print(shutil.get_archive_formats())
print(shutil.get_unpack_formats())
shutil.make_archive("source", "type_can", "target")
shutil.unpack_archive("source", "target")
shutil.which("可执行文件")
