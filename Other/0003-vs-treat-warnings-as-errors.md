
在vs编译的时候，不知道为什么，方法的提前return，会编译报错。因为之前从没有遇到这种error，很奇怪，网上查了很多资料都没有找到原因，原来是因为我vs项目配置的错误。记录一下。

Each project in Visual Studio has a "treat warnings as errors" option. Go through each of your projects and change that setting:

1. Right-click on your project, select "Properties".
2. Click "Build".
3. Switch "Treat warnings as errors" from "All" to "Specific warnings" or "None".
The location of this switch varies, depending on the type of project (class library vs. web application, for example).
