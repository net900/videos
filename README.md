# cpdaily-form 今日校园每日疫情填报自动提交

广东工程职业技术学院今日校园每日疫情填报新平台自动提交脚本

# 使用

1、有的账号无法使用是因为没有修改第一次的默认密码，先在学校网站中修改密码以及绑定邮箱即可
2、修改`form.py`文件中的账号密码、学校官网地址以及你需要定位的地区、地址、经纬度
3、填表的问题，有时候辅导员开启记录上次信息 就可以根据上次的信息去自动填写，但有的（比如我们学校）就会关闭这个功能，就是每次都要重新填写，程序中120-124行屏蔽了这段代码，有需要的可以按实际情况开启

# 一些关于使用过程中的问题
1、Cpextension只有问卷提交才会使用到，app每次更新都会换一次 Des加密 这里用的还是8.2.14的加密 暂未失效，仍可使用
2、关于Cpextension(`Cpdaily-Extension`)若提交时返回版本过低可以抓包获取一段新的放进去使用 一个Cpextension其他账号也通用
3、有能力的也可以将今日校园最新版脱壳(360加固)并反编译或者xp框架使用Hook的方法

# 关于作者
第一次使用`python`写程序，之前都是用`php`去写的 可能写的不怎么样，希望前辈们多指正

q:1340176819

