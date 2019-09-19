# WebAPI & WCF 服务介绍和应用
## WebAPI
### WebAPI 的概念
> API：Application Interface
>
> WebAPI： Web Application Interface 
> 
> 可以使用 HTTP 协议访问的 Web 应用程序接口。

### WebAPI 与 MVC 控制器的区别
WebAPI 是一种概念。而 .NET 是一个平台。
ASP .NET Web API 是一个用于构建基于 HTTP 的服务的框架。其工作方式与 ASP .NET MVC Web 应用程序的工作方式大致相同，不同的是，Web API 是将数据作为响应返回，而不是 HTML 视图
### WebAPI 的作用
### WebAPI 的优缺点

### WebAPI Controller
Web API Controller 与 ASP .NET MVC Controller 类似。用来处理传入的 HTTP 请求并将响应结果发送给调用方。

Web API Controller 命名必须以 Controller 结尾。并且必须继承自 System.Web.Http.ApiController。

WebAPI 的 Action 命名建议使用 HTTP 请求方式作为前缀，提高可读性。如 GetUserInfo、PostUserInfo 等

### HTTP 协议规范 GET/POST/PUT/DELETE 请求的区别

HTTP 协议规范   规范   规范  -- 只是一种规范，并非强制

GET ：用于从服务器端获取数据。类似于 Select，不应该对服务器端的数据产生任何影响
POST：用于向服务器端增加数据，类似于 Insert，会对服务器端产生影响
PUT： 用于向服务器端更新数据，类似于 Update，会对带我去端产生影响
DELETE：用于向服务器端删除数据，类似于 Delete， 会对服务器端产生影响
OPTION：用于向服务器端发送探测请求，获取服务器是否允许执行某种类型请求。

### WebAPI 的配置

AppStart 文件夹下， 默认生成的 WebApiConfig.cs 文件中。

HttpConfiguration 主要有以下属性：

DependencyResolver 获取/设置依赖项注入的依赖项解析程序
Filters 获取/设置filters
Formatters 获取/设置 media-type 格式化
IncludeErrorDetailPolicy  获取/设置一个指示错误消息中是否应包含错误详细信息的值
MessageHandlers  获取/设置 message handlers
ParameterBindingRules 获取有关如何绑定参数的规则集合
Routers 获取为 WebAPI 配置的路由集合
Services 获取 WebAPI 服务


### WebAPI 的应用
### WebAPI 的跨域问题
### WebAPI 与 WebService 的区别
    Web Service：
    1、它是基于SOAP协议的，数据格式是XML
    2、只支持HTTP协议
    3、它不是开源的，但可以被任意一个了解XML的人使用
    4、它只能部署在IIS上
    Web API：
    1、这是一个简单的构建HTTP服务的新框架
    2、在.net平台上Web API 是一个开源的、理想的、构建REST-ful 服务的技术
    3、不像WCF REST Service.它可以使用HTTP的全部特点（比如URIs、request/response头，缓存，版本控制，多种内容格式）
    4、它也支持MVC的特征，像路由、控制器、action、filter、模型绑定、控制反转（IOC）或依赖注入（DI），单元测试。
    5、它可以部署在应用程序和IIS上
    6、这是一个轻量级的框架，并且对限制带宽的设备，比如智能手机等支持的很好
    7、Response可以被Web API的MediaTypeFormatter转换成Json、XML 或者任何你想转换的格式。 
### WebAPI 的安全性与 token 身份验证

### 使用 Visual Studio 创建 WebAPI 项目
1. 新建 .NET Web 项目
    ![img01](./img/01.png)

2. 选择 WebAPI 
    ![img02](./img/02.png)

3. 添加一般处理程序(.ashx)文件
     ![img03](./img/03.png)

4. 指定返回类型，构造返回信息
    ![img04](./img/04.png)

5. 访问 WebAPI 接口，获取数据
    ![img04](./img/05.png)

## WCF
### WCF 的概念

> WCF (Windows Communication Foundation：Windows 通讯开发平台) 是微软开发的一系列支持数据通信的应用程序框架。

>
>整合了原有的windows通讯的 .net Remoting，WebService，Socket的机制，并融合有HTTP和FTP的相关技术。
>
>是Windows平台上开发分布式应用最佳的实践方式。

>WCF 集合了.NET Framework几乎所有的通信方法，通信双方的沟通方式，由合约来订定；通信双方所遵循的通信方法，由协议绑定来订定；通信期间的安全性，由双方约定的安全性层次来订定。

### WCF 的契约
WCF 的基本概念是以契约(Contract) 来定义双方沟通的协议，合约必须要以接口的方式来体现，而实际的服务代码必须要由这些合约接口派生并实现。

合约分成了四种：

1. 数据契约(DataContract)，订定双方沟通时的数据格式。
2. 服务契约(ServiceContract)，订定服务的定义。
3. 操作契约(OperationContract)，订定服务提供的方法。
4. 消息契约(MessageContract)，订定在通信期间改写消息内容的规范


协议绑定


WCF 支持了 HTTP TCP 等多种协议，HTTP 又分为基本 HTTP 支持和 WS-HTTP 支持，TCP 也支持 NetTCPBinding，NETPerTCPBinding 等。

所以，双方必须配置统一的通信协议和编码规则


### WCF 的作用
### WCF 的优缺点

1. 统一性
    WCF是对于ASMX，.Net Remoting，Enterprise Service，WSE，MSMQ等技术的整合。由于WCF完全是由托管代码编写，因此开发WCF的应用程序与开发其它的.Net应用程序没有太大的区别，我们仍然可以像创建面向对象的应用程序那样，利用WCF来创建面向服务的应用程序

2. 互操作性

    由于WCF最基本的通信机制是SOAP（Simple Object Access Protocol 简易对象访问协议），这就保证了系统之间的互操作性，即使是运行不同的上下文中。
    可以跨进程、跨机器甚至于跨平台的通信，只要支持标准的Web Service

3. 安全与可信赖

4. 兼容性
    WCF充分的考虑到了与旧有系统的兼容性。安装WCF并不会影响原有的技术如ASMX和.Net Remoting。即使对于WCF和ASMX而言，虽然两者都使用了SOAP，但基于WCF开发的应用程序，仍然可以直接与ASMX进行交互


### WCF 与 WebService 的区别
### 使用 Visual Studio 创建 WCF 服务端
### 使用 Visual Studio 创建客户端调用 WCF 服务









Web Service
　　1、它是基于SOAP协议的，数据格式是XML
　　2、只支持HTTP协议
　　3、它不是开源的，但可以被任意一个了解XML的人使用
　　4、它只能部署在IIS上
 
　　WCF
　　1、这个也是基于SOAP的，数据格式是XML
　　2、这个是Web Service（ASMX）的进化版，可以支持各种各样的协议，像TCP，HTTP，HTTPS，Named Pipes, MSMQ.
　　3、WCF的主要问题是，它配置起来特别的繁琐
　　4、它不是开源的，但可以被任意一个了解XML的人使用
　　5、它可以部署应用程序中或者IIS上或者Windows服务中
 
　　WCF Rest
　　1、想使用WCF Rest service，你必须在WCF中使用webHttpBindings
　　2、它分别用[WebGet]和[WebInvoke]属性，实现了HTTP的GET和POST动词
　　3、要想使用其他的HTTP动词，你需要在IIS中做一些配置，使.svc文件可以接受这些动词的请求
　　4、使用WebGet通过参数传输数据，也需要配置。而且必须指定UriTemplate
　　5、它支持XML、JSON以及ATOM这些数据格式
 
　　Web API
　　1、这是一个简单的构建HTTP服务的新框架
　　2、在.net平台上Web API 是一个开源的、理想的、构建REST-ful 服务的技术
　　3、不像WCF REST Service.它可以使用HTTP的全部特点（比如URIs、request/response头，缓存，版本控制，多种内容格式）
　　4、它也支持MVC的特征，像路由、控制器、action、filter、模型绑定、控制反转（IOC）或依赖注入（DI），单元测试。这些可以使程序更简单、更健壮
　　5、它可以部署在应用程序和IIS上
　　6、这是一个轻量级的框架，并且对限制带宽的设备，比如智能手机等支持的很好
　　7、Response可以被Web API的MediaTypeFormatter转换成Json、XML 或者任何你想转换的格式。
　　
　　WCF和WEB API我该选择哪个？
　　1、当你想创建一个支持消息、消息队列、双工通信的服务时，你应该选择WCF
　　2、当你想创建一个服务，可以用更快速的传输通道时，像TCP、Named Pipes或者甚至是UDP（在WCF4.5中）,在其他传输通道不可用的时候也可以支持HTTP。
　　3、当你想创建一个基于HTTP的面向资源的服务并且可以使用HTTP的全部特征时（比如URIs、request/response头，缓存，版本控制，多种内容格式），你应该选择Web API
　　4、当你想让你的服务用于浏览器、手机、iPhone和平板电脑时，你应该选择Web API