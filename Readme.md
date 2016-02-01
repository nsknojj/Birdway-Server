# Birdway-Server基本介绍
### Birdway-Server支持两种模式，local模式和global模式。其中local模式用于小规模的私人项目共同编辑，global模式则可用于在线多人共同编辑。目前我们实现了local模式基本完整的服务器逻辑，可以投入使用。global模式支持文件夹结构，多文件编辑，文件权限管理，用户的维护等等，我们目前实现了这些功能的接口，经过了少量的测试，但是还不能投入使用。
----------------
# Local模式
## birdway.py
* ### 使用方式
birdway.py usage:  
-h, --help: print this help message.  
-f, --file: name of the file which you want to share with others  
-p, --password: set a password for your file, can be omitted  
For example: birdway.py -f log/a.txt -p 111  
hint: 输入指令后，若开启服务器成功，会显示主机IP以及端口号，口令。并且服务器会显示每一次文件的更改。
* ### 主体结构
main： 整个服务器进程。监听到客户端请求时建立一个连接，进入tcp_link；同时不断运行着两个子线程save_thread和syn_thread。  
tcp_link:  维护单个连接请求，使用自行定制的CETP协议与客户端交互。  
save_thread: 以一定的频率将所有未保存的文件定时保存的线程。  
syn_thread: 以一定的频率从服务器推送文件内容进行同步的线程。（目前只采用了最基本的全文件同步）

## Files.py
* ### 主体结构
save_file: 保存文件至硬盘  
add_editor: 为当前文件添加一个正在编辑的人（以维护每个文件当前编辑的人的列表，支持global模式的多文件）
del_editor: 为当前文件删除一个正在编辑的人  
change: 将对文件的modify作用于内存中的文件。内存中文件的保存形式：每一行为一个string，组合成list。此函数主要分两部操作，按协议中的修改，先删除，后增加。  
edit_file: 若文件没有在内存中，将其载入至内存中，并获取文件的字符串形式（用于与客户端交互）。  
其余未说明的函数是对这些函数的简单调用，或者被这些函数调用用以实现简单功能。
-------
# Global模式
## Users.py
* ### 基本介绍及所用技术
用于维护用户列表，包括登陆名、密码的维护，插入用户，获取用户信息，获取用户列表。使用了嵌入式数据库sqlite。
* ### 主体结构
insert_user: 按用户名、密码的hash值添加新用户。检查是否已有该用户，返回注册失败或成功。  
get_user: 将特定用户按照id或者用户名获取其条目，可用于查询密码（或以后的其他信息）。  
all_users： 获取全部用户的列表。可用于权限管理调度，对全体用户开放权限或关闭权限；也可用于查看用户数量等信息。

## Auth.py
* ### 基本介绍及所用技术
用于维护用户对于文件的权限，包括维护编辑权限、管理权限（更改权限的权限），获取可编辑文档列表，同样采用sqlite。
* ### 主体结构
have_edit_auth: 查询用户是否具有该文件的编辑权限。  
have_manage_auth: 查询用户是否具有该文件的管理权限。    
get_edit_list： 获取可编辑的文章列表。  
change: 更改权限。首先会检查用户是否有管理权限，无则给出失败的反馈。更改时有多种模式：使用户有这个文件的编辑权限，使用户有这个文件的管理权限（包含编辑），使所有人能编辑这个文件，使文件私有化，所有人都不能编辑这个文件。
